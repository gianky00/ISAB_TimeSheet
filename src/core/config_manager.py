"""
Bot TS - Configuration Manager
Gestione della configurazione dell'applicazione.
"""

import copy
import json
import os
import shutil
import sys
import threading
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from platformdirs import user_data_dir

from src.core.constants import FileNames, URLs
from src.core.secrets_manager import SecretsManager
from src.core.version import __version__

# Path del file di configurazione
# STANDARD DEFINITIVO: %LOCALAPPDATA%\SyncroJob
APP_NAME = "SyncroJob"

# Use platformdirs to get standard Local AppData path
CONFIG_DIR = Path(user_data_dir(APP_NAME, appauthor=False))
CONFIG_FILE = CONFIG_DIR / FileNames.CONFIG
# Root del progetto (assumendo src/core/config_manager.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
_config_cache: dict[str, Any] | None = None
_config_lock = threading.RLock()  # Lock per accesso thread-safe


def get_version() -> str:
    """Restituisce la versione corrente dell'applicazione."""
    return __version__


# Configurazione di default
DEFAULT_CONFIG: dict[str, Any] = {
    "accounts": [],
    "safework_accounts": [],
    "contracts": [],
    "default_contract": "",
    "browser_headless": False,
    "browser_timeout": 30,
    "download_path": "",
    "fornitori": [],
    "last_ts_data": [],
    "last_ts_date": f"01.01.{datetime.now(UTC).year}",
    "last_ts_fornitore": "",
    "last_carico_ts_data": [],
    "last_oda_data": [],
    "contabilita_file_path": "",
    "enable_auto_update_contabilita": True,
    "certificati_campione_path": "",
    "master_preventivi_path": "",
    "base_network_path_preventivi": r"\\192.168.11.251\Database_Tecnico_SMI\Contabilita' strumentale",
    "preventivi_tcl": [
        "MESSINA I.",
        "AGUSTA D.",
        "CALDARELLA F.",
        "PREZZAVENTO M.",
        "BOSCO F.",
        "RUGGIERI F.",
        "BARBAGALLO G.",
    ],
    "preventivi_stati": [
        "ATTIVITA' DA COMPLETARE",
        "IN ATTESA TCL",
        "RICHIESTA ODC MIDOLO",
        "CONTABILIZZATA",
    ],
    "reparti": ["STRUMENTALE", "ELETTRICO", "CANTIERE", "ANALISI"],
    "cantieri": [],
    "employee_mappings": {},
    "ai_provider": "gemini",
    "ai_model": "gemini-1.5-pro",
    "ollama_url": URLs.OLLAMA_DEFAULT,
    "quick_actions": ["nav_scarico_ts", "nav_lyra", "cmd_sync", "cmd_open_folder"],
    "statistics": {},
}


def ensure_config_dir() -> None:
    """Assicura che la directory di configurazione esista."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _deep_update_paths(data: Any, old_path: str, new_path: str) -> Any:
    """Sostituisce ricorsivamente i puntamenti ai vecchi percorsi nelle stringhe."""
    if isinstance(data, str):
        # Gestione sia backslash che forward slash
        updated = data.replace(old_path.replace("/", "\\"), new_path.replace("/", "\\"))
        updated = updated.replace(old_path.replace("\\", "/"), new_path.replace("\\", "/"))
        return updated
    if isinstance(data, dict):
        return {k: _deep_update_paths(v, old_path, new_path) for k, v in data.items()}
    if isinstance(data, list):
        return [_deep_update_paths(i, old_path, new_path) for i in data]
    return data


def _check_and_migrate_local_config() -> bool:
    r"""
    Cerca file config.json fuori dalla cartella standard (AppData\Local).
    Se trovato (es. in root progetto o AppData\Roaming), lo migra in Local.
    """
    # Trigger migration if file doesn't exist OR if it's a fresh (empty) installation
    # This check is now handled in load_config() to allow re-checking if accounts are missing

    # 1. Determine app root (where the .exe or main.py is)
    app_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else BASE_DIR

    # 2. Potential legacy directory locations (not just the files)
    legacy_app_names = ["BotTS", "Bot TS", "SyncroJob"]
    potential_dirs = [
        app_dir,  # Portable mode
        Path(user_data_dir(APP_NAME, appauthor=False, roaming=True)),  # Legacy Roaming
    ]

    # Add variant folders in Local AppData
    local_appdata = Path(os.environ.get("LOCALAPPDATA", ""))
    if local_appdata:
        for old_name in legacy_app_names:
            if old_name != APP_NAME:
                potential_dirs.extend(
                    (local_appdata / old_name, local_appdata / "GiancarloAllegretti" / old_name)
                )

    roaming_appdata = Path(os.environ.get("APPDATA", ""))
    if roaming_appdata:
        potential_dirs.extend(roaming_appdata / old_name for old_name in legacy_app_names)

    migrated = False
    for legacy_dir in potential_dirs:
        legacy_config_file = legacy_dir / FileNames.CONFIG
        # Avoid migrating from self
        if legacy_config_file.exists() and legacy_dir.resolve() != CONFIG_DIR.resolve():
            try:
                ensure_config_dir()

                # Carica vecchia configurazione
                with legacy_config_file.open("r", encoding="utf-8") as f:
                    old_config = json.load(f)

                # AGGIORNAMENTO PUNTAMENTI (Nessuna eccezione)
                # Sostituisce il vecchio path del folder con quello nuovo in tutte le stringhe
                old_path_str = str(legacy_dir)
                new_path_str = str(CONFIG_DIR)
                migrated_config = _deep_update_paths(old_config, old_path_str, new_path_str)

                # MERGE: Inserisce solo dove mancano (o se config attuale è vuota)
                current_config = _load_base_config()
                for key, value in migrated_config.items():
                    if key not in current_config or not current_config[key]:
                        current_config[key] = value

                # Salva configurazione migrata
                _atomic_write_json(current_config, CONFIG_FILE)
                print(f"[MIGRATION] Config merged and paths updated from {legacy_dir}")

                # Migrazione Cartella Data (Database) se presente
                legacy_data = legacy_dir / "data"
                target_data = CONFIG_DIR / "data"
                if legacy_data.exists():
                    try:
                        # Copy tree with merge capabilities
                        shutil.copytree(legacy_data, target_data, dirs_exist_ok=True)
                        print(f"[MIGRATION] Data folder merged from {legacy_dir}")
                    except Exception as de:
                        print(f"[MIGRATION] Warning: Partial data migration for {legacy_dir}: {de}")

                migrated = True
                # Una volta migrata una valida, ci fermiamo per evitare sovrascritture da versioni ancora più vecchie
                break
            except Exception as e:
                print(f"[MIGRATION] Error during migration from {legacy_dir}: {e}")

    return migrated


def load_config() -> dict[str, Any]:
    """
    Carica la configurazione dal file, la decripta e la mette in cache.
    """
    global _config_cache
    with _config_lock:
        if _config_cache is not None:
            return copy.deepcopy(_config_cache)

        # 0. Check for legacy configuration to migrate
        # Trigger migration if file doesn't exist OR if it's a fresh (empty) installation
        config = _load_base_config()
        if (
            not CONFIG_FILE.exists() or (not config.get("accounts") and not config.get("safework_accounts"))
        ) and _check_and_migrate_local_config():
            # Re-load if migration happened
            config = _load_base_config()

        ensure_config_dir()

        # Decripta password per tutti i tipi di account
        _decrypt_all_credentials(config)

        # Migrazione Legacy
        if _migrate_legacy_config(config):
            save_config(config)

        _config_cache = copy.deepcopy(config)
        return config


def _load_base_config() -> dict[str, Any]:
    """Carica il file JSON base o restituisce i default, con override da Env Vars."""
    config = copy.deepcopy(DEFAULT_CONFIG)
    if CONFIG_FILE.exists():
        with suppress(OSError, json.JSONDecodeError):
            config.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))

    # 12-Factor App: Override with Environment Variables
    # Format: SYNCROJOB_KEY (es. SYNCROJOB_BROWSER_HEADLESS=true)
    prefix = "SYNCROJOB_"
    for key, default_val in DEFAULT_CONFIG.items():
        env_key = f"{prefix}{key.upper()}"
        env_val = os.environ.get(env_key)

        if env_val is not None:
            # Type casting basic per bool/int
            if isinstance(default_val, bool):
                config[key] = env_val.lower() in ("true", "1", "yes")
            elif isinstance(default_val, int):
                with suppress(ValueError):
                    config[key] = int(env_val)
            else:
                config[key] = env_val

    return config


def _decrypt_all_credentials(config: dict[str, Any]) -> None:
    """Decripta le credenziali per Isab e SafeWork."""
    _decrypt_account_list(config.get("accounts", []), "isab_portal")
    _decrypt_account_list(config.get("safework_accounts", []), "safework_portal")


def _decrypt_account_list(accounts: list[dict[str, Any]], service_name: str) -> None:
    """Decripta una lista di account usando keyring o fallback locale."""
    if not accounts:
        return

    from src.utils.security import password_manager

    for acc in accounts:
        username = acc.get("username")
        if not username:
            continue

        # Priorità 1: Keyring
        pw_keyring = SecretsManager.get_credential(service_name, username)
        if pw_keyring:
            acc["password"] = pw_keyring
            continue

        # Priorità 2: Fallback criptato nel file
        pw_file = acc.get("password")
        if pw_file:
            with suppress(Exception):
                acc["password"] = password_manager.decrypt(pw_file)


def _migrate_legacy_config(config: dict[str, Any]) -> bool:
    """Migra le vecchie chiavi 'isab_username' nel nuovo formato accounts."""
    if "isab_username" not in config or not config.get("isab_username"):
        return False

    old_user = config["isab_username"]
    if not any(a.get("username") == old_user for a in config.get("accounts", [])):
        if "accounts" not in config:
            config["accounts"] = []
        config["accounts"].append(
            {
                "username": old_user,
                "password": config.get("isab_password", ""),
                "default": True,
            }
        )

    del config["isab_username"]
    config.pop("isab_password", None)
    return True


def _reset_configuration_for_testing() -> None:
    """
    Resetta la cache di configurazione per i test.
    DA USARE SOLO NEI TEST!
    """
    global _config_cache
    with _config_lock:
        _config_cache = None


def save_config(config: dict[str, Any]) -> None:
    """
    Salva la configurazione in modo atomico.
    """
    global _config_cache
    with _config_lock:
        ensure_config_dir()
        config_to_save = copy.deepcopy(config)

        # Cripta/Sposta in keyring le password prima del salvataggio su disco
        _encrypt_all_credentials(config_to_save)

        try:
            _atomic_write_json(config_to_save, CONFIG_FILE)
            # Cache aggiornata con dati in chiaro (originali)
            _config_cache = copy.deepcopy(config)
        except Exception as e:
            print(f"Errore critico durante il salvataggio: {e}")


def _encrypt_all_credentials(config: dict[str, Any]) -> None:
    """Gestisce la protezione delle credenziali prima del salvataggio."""
    _encrypt_account_list(config.get("accounts", []), "isab_portal")
    _encrypt_account_list(config.get("safework_accounts", []), "safework_portal")


def _encrypt_account_list(accounts: list[dict[str, Any]], service_name: str) -> None:
    """Sposta in keyring o cripta localmente le password di una lista di account."""
    if not accounts:
        return

    from src.utils.security import password_manager

    for acc in accounts:
        # Recupera la password originale prima di qualsiasi modifica
        password = acc.get("password")
        username = acc.get("username")

        if not username or not password:
            continue

        with suppress(Exception):
            if SecretsManager.is_available():
                SecretsManager.store_credential(service_name, username, password)
                # Rimuovi la password in chiaro dal dizionario che verrà salvato
                acc.pop("password", None)
                continue

        # Fallback: Cripta nel file
        acc["password"] = password_manager.encrypt(password)


def _atomic_write_json(data: dict[str, Any], target_path: Path) -> None:
    """Scrittura atomica del file JSON."""
    temp_file = target_path.with_suffix(".tmp")
    try:
        with temp_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        temp_file.replace(target_path)
    finally:
        with suppress(Exception):
            if temp_file.exists():
                temp_file.unlink()


def get_config_value(key: str, default: Any = None) -> Any:
    """Ottiene un valore dalla configurazione."""
    return load_config().get(key, default)


def set_config_value(key: str, value: Any) -> None:
    """Imposta un valore nella configurazione."""
    config = load_config()
    config[key] = value
    save_config(config)


def get_accounts() -> list[dict[str, Any]]:
    """Restituisce la lista degli account configurati."""
    return get_config_value("accounts", [])  # type: ignore[no-any-return]


def add_account(username: str, password: str, is_default: bool = False) -> None:
    """Aggiunge o aggiorna un account."""
    config = load_config()
    accounts = config.get("accounts", [])

    if not accounts:
        is_default = True

    accounts = [a for a in accounts if a.get("username") != username]

    if is_default:
        for acc in accounts:
            acc["default"] = False

    accounts.append({"username": username, "password": password, "default": is_default})

    config["accounts"] = accounts
    save_config(config)


def remove_account(username: str) -> None:
    """Rimuove un account e le credenziali associate."""
    config = load_config()
    accounts = config.get("accounts", [])
    config["accounts"] = [a for a in accounts if a.get("username") != username]

    try:
        if SecretsManager.is_available():
            SecretsManager.delete_credential("isab_portal", username)
    except Exception as e:
        print(f"Impossibile rimuovere credenziali dal keyring: {e}")

    if config["accounts"] and not any(a.get("default") for a in config["accounts"]):
        config["accounts"][0]["default"] = True

    save_config(config)


def set_default_account(username: str) -> None:
    """Imposta un account come default."""
    config = load_config()
    accounts = config.get("accounts", [])
    found = False
    for acc in accounts:
        acc["default"] = acc.get("username") == username
        if acc["default"]:
            found = True

    if found:
        config["accounts"] = accounts
        save_config(config)


def switch_default_account(service_type: str = "isab") -> tuple[bool, str | None]:
    """
    Switcha l'account di default in modo circolare.
    service_type: 'isab' o 'safework'
    Ritorna (successo, nuovo_username)
    """
    config = load_config()
    key = "accounts" if service_type == "isab" else "safework_accounts"
    accounts = config.get(key, [])

    if len(accounts) < 2:
        return False, None

    # Trova l'indice del default attuale
    current_idx = -1
    for i, acc in enumerate(accounts):
        if acc.get("default"):
            current_idx = i
            break

    # Se non c'è default, prendi il primo
    if current_idx == -1:
        current_idx = 0

    # Prossimo indice circolare
    next_idx = (current_idx + 1) % len(accounts)

    # Reset tutti i default
    for i, acc in enumerate(accounts):
        acc["default"] = i == next_idx

    config[key] = accounts
    save_config(config)
    return True, accounts[next_idx].get("username")


def get_default_account() -> dict[str, str] | None:
    """Restituisce l'account di default."""
    accounts = get_accounts()
    if not accounts:
        return None

    return next((acc for acc in accounts if acc.get("default")), accounts[0])


def get_data_path() -> str:
    """Restituisce il percorso base per i dati."""
    data_dir = CONFIG_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return str(data_dir)


def get_logs_path() -> str:
    """Restituisce il percorso per i file di log."""
    logs_dir = CONFIG_DIR / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return str(logs_dir)


def get_download_path() -> str:
    """Restituisce il path di download configurato."""
    path_str: str = get_config_value("download_path", "")
    if path_str:
        path = Path(path_str)
        if path.is_dir():
            return str(path)

    default_download = Path.home() / "Downloads"
    if default_download.exists():
        return str(default_download)
    return str(Path.home())


def export_configuration(export_path: str) -> tuple[bool, str]:
    """
    Esporta la configurazione corrente in un file JSON.
    Decripta le credenziali per l'export (Opzionale: aggiungere flag per escludere o criptare).
    Per ora esportiamo le credenziali in chiaro nel backup (l'utente deve proteggere il file).
    """
    try:
        config = load_config()
        # Per l'export, vogliamo che le password siano incluse (se l'utente vuole ripristinare altrove)
        # load_config le ha già decriptate in cache.

        export_data = copy.deepcopy(config)

        # Aggiungiamo metadati
        export_data["_meta"] = {
            "exported_at": str(datetime.now(UTC)),
            "app_version": __version__,
            "type": "syncrojob_config_backup",
        }

        Path(export_path).write_text(json.dumps(export_data, indent=4, ensure_ascii=False), encoding="utf-8")

        return True, "Esportazione completata con successo."
    except Exception as e:
        return False, f"Errore durante l'esportazione: {e}"


def reset_to_defaults() -> None:
    """Ripristina la configurazione predefinita cancellando la cache e salvando i default."""
    global _config_cache
    with _config_lock:
        _config_cache = copy.deepcopy(DEFAULT_CONFIG)
        save_config(_config_cache)


def import_configuration(import_path: str | Path) -> tuple[bool, str]:
    """
    Importa la configurazione da un file JSON, sovrascrivendo quella attuale.
    Effettua un backup automatico della configurazione attuale prima di sovrascrivere.
    """
    try:
        # 1. Validazione File
        path = Path(import_path)
        if not path.exists():
            return False, "File di importazione non trovato."

        new_config = json.loads(path.read_text(encoding="utf-8"))

        # Validazione base: controlliamo se sembra una config valida
        # Es. controlliamo chiavi critiche
        critical_keys = ["accounts", "browser_timeout", "fornitori"]
        if not any(k in new_config for k in critical_keys):
            return (
                False,
                "Il file selezionato non sembra una configurazione valida di SyncroJob.",
            )

        # Rimuovi metadati se presenti
        new_config.pop("_meta", None)

        # 2. Backup Configurazione Corrente
        backup_file = CONFIG_DIR / f"config_backup_pre_import_{int(datetime.now(UTC).timestamp())}.json"

        current_config = load_config()
        backup_file.write_text(json.dumps(current_config, indent=2), encoding="utf-8")

        # 3. Sovrascrittura
        # Uniamo i default con la nuova config per garantire che nuove chiavi aggiunte in versioni recenti non manchino
        merged_config = copy.deepcopy(DEFAULT_CONFIG)
        merged_config.update(new_config)

        save_config(merged_config)

        return (
            True,
            f"Configurazione importata con successo.\nBackup precedente salvato in: {backup_file.name}",
        )

    except json.JSONDecodeError:
        return False, "Il file non è un JSON valido."
    except Exception as e:
        return False, f"Errore critico importazione: {e}"
