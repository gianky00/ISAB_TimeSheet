"""
Bot TS - Configuration Manager
Gestione della configurazione dell'applicazione.
"""

import copy
import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from platformdirs import user_data_dir

from src.core.secrets_manager import SecretsManager

# Path del file di configurazione
# STANDARD DEFINITIVO: %LOCALAPPDATA%\SyncroJob
APP_NAME = "SyncroJob"

CONFIG_DIR = Path(user_data_dir(APP_NAME, appauthor=False))
CONFIG_FILE = CONFIG_DIR / "config.json"
# Root del progetto (assumendo src/core/config_manager.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
_config_cache: Optional[Dict[str, Any]] = None
_config_lock = threading.RLock()  # Lock per accesso thread-safe

# Configurazione di default
DEFAULT_CONFIG: Dict[str, Any] = {
    "accounts": [],
    "safework_accounts": [],
    "contracts": [],
    "default_contract": "",
    "browser_headless": False,
    "browser_timeout": 30,
    "download_path": "",
    "fornitori": [],
    "last_ts_data": [],
    "last_ts_date": "01.01.2025",
    "last_ts_fornitore": "",
    "last_carico_ts_data": [],
    "last_oda_data": [],
    "contabilita_file_path": "",
    "enable_auto_update_contabilita": True,
    "certificati_campione_path": "",
    "reparti": ["STRUMENTALE", "ELETTRICO", "CANTIERE", "ANALISI"],
    "cantieri": [],
    "employee_mappings": {},
    "ai_model": "gemini-1.5-pro",
    "quick_actions": ["nav_scarico_ts", "nav_lyra", "cmd_sync", "cmd_open_folder"],
    "statistics": {},
}


def ensure_config_dir():
    """Assicura che la directory di configurazione esista."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """
    Carica la configurazione dal file, la decripta e la mette in cache.
    """
    global _config_cache
    with _config_lock:
        if _config_cache is not None:
            return copy.deepcopy(_config_cache)

        ensure_config_dir()
        config = _load_base_config()

        # Decripta password per tutti i tipi di account
        _decrypt_all_credentials(config)

        # Migrazione Legacy
        if _migrate_legacy_config(config):
            save_config(config)

        _config_cache = copy.deepcopy(config)
        return config


def _load_base_config() -> Dict[str, Any]:
    """Carica il file JSON base o restituisce i default."""
    config = copy.deepcopy(DEFAULT_CONFIG)
    if not CONFIG_FILE.exists():
        return config

    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            loaded_config = json.load(f)
        config.update(loaded_config)
    except (json.JSONDecodeError, IOError):
        pass
    return config


def _decrypt_all_credentials(config: Dict[str, Any]):
    """Decripta le credenziali per Isab e SafeWork."""
    _decrypt_account_list(config.get("accounts", []), "isab_portal")
    _decrypt_account_list(config.get("safework_accounts", []), "safework_portal")


def _decrypt_account_list(accounts: List[Dict[str, Any]], service_name: str):
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


def _migrate_legacy_config(config: Dict[str, Any]) -> bool:
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


def _reset_configuration_for_testing():
    """
    Resetta la cache di configurazione per i test.
    DA USARE SOLO NEI TEST!
    """
    global _config_cache
    with _config_lock:
        _config_cache = None


def save_config(config: Dict[str, Any]):
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


def _encrypt_all_credentials(config: Dict[str, Any]):
    """Gestisce la protezione delle credenziali prima del salvataggio."""
    _encrypt_account_list(config.get("accounts", []), "isab_portal")
    _encrypt_account_list(config.get("safework_accounts", []), "safework_portal")


def _encrypt_account_list(accounts: List[Dict[str, Any]], service_name: str):
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

        try:
            if SecretsManager.is_available():
                SecretsManager.store_credential(service_name, username, password)
                # Rimuovi la password in chiaro dal dizionario che verrà salvato
                acc.pop("password", None)
                continue
        except Exception:
            pass

        # Fallback: Cripta nel file
        acc["password"] = password_manager.encrypt(password)


def _atomic_write_json(data: Dict[str, Any], target_path: Path):
    """Scrittura atomica del file JSON."""
    temp_file = target_path.with_suffix(".tmp")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_file, target_path)
    finally:
        if temp_file.exists():
            try:
                os.remove(temp_file)
            except Exception:
                pass


def get_config_value(key: str, default: Any = None) -> Any:
    """Ottiene un valore dalla configurazione."""
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: Any):
    """Imposta un valore nella configurazione."""
    config = load_config()
    config[key] = value
    save_config(config)


def get_accounts() -> List[Dict[str, Any]]:
    """Restituisce la lista degli account configurati."""
    return get_config_value("accounts", [])


def add_account(username: str, password: str, is_default: bool = False):
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


def remove_account(username: str):
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


def set_default_account(username: str):
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


def switch_default_account(service_type: str = "isab") -> tuple[bool, Optional[str]]:
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


def get_default_account() -> Optional[Dict[str, str]]:
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


def get_download_path() -> str:
    """Restituisce il path di download configurato."""
    path = get_config_value("download_path", "")
    if path and os.path.isdir(path):
        return path

    default_download = Path.home() / "Downloads"
    return str(default_download) if default_download.exists() else str(Path.home())


def get_fornitori() -> list:
    """Restituisce la lista dei fornitori configurati."""
    return get_config_value("fornitori", [])
