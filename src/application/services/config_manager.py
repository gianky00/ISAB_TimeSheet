"""Bot TS - Configuration Manager.

Gestione della configurazione dell'applicazione.
Refactored V9.0: Modularized architecture.
"""

import copy
import json
import os
import threading
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from src.application.services.paths import BASE_DIR, CONFIG_DIR, CONFIG_FILE

__all__ = [
    "BASE_DIR",
    "CONFIG_DIR",
    "CONFIG_FILE",
    "add_account",
    "ensure_config_dir",
    "get_config_value",
    "get_default_account",
    "get_download_path",
    "import_config_from_file",
    "invalidate_config_cache",
    "load_config",
    "remove_account",
    "reset_to_defaults",
    "save_config",
    "set_config_value",
    "set_config_values",
    "set_default_account",
    "switch_default_account",
]
import time

from src.application.services.version import __version__

# Modular imports
from .config.account_manager import (
    add_account_logic,
    remove_account_logic,
    set_default_account_logic,
    switch_default_account_logic,
)
from .config.defaults import DEFAULT_CONFIG
from .config.migration import (
    check_and_migrate_local_config,
    migrate_legacy_keys,
)
from .config.security import decrypt_all_credentials, encrypt_all_credentials

# ... (rest of imports remains same, just adding time and uuid if needed)
_config_cache: dict[str, Any] | None = None
_config_lock = threading.RLock()
_file_io_lock = threading.Lock()


def _reset_configuration_for_testing() -> None:
    """Resetta la cache della configurazione (solo per unitàtest)."""
    global _config_cache  # noqa: PLW0603
    with _config_lock:
        _config_cache = None


def get_version() -> str:
    """Restituisce la versione corrente dell'applicazione."""
    return __version__


def ensure_config_dir() -> None:
    """Assicura che la directory di configurazione esista."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    """Carica la configurazione dal file, la decripta e la mette in cache."""
    global _config_cache  # noqa: PLW0603
    with _config_lock:
        if _config_cache is not None:
            return copy.deepcopy(_config_cache)

        # 0. Check for legacy configuration to migrate
        config = _load_base_config()
        if (
            not CONFIG_FILE.exists() or (not config.get("accounts") and not config.get("safework_accounts"))
        ) and check_and_migrate_local_config(BASE_DIR, _load_base_config, _atomic_write_json):
            config = _load_base_config()

        ensure_config_dir()

        # Decripta credenziali
        decrypt_all_credentials(config)

        # Migrazione Legacy interna
        if migrate_legacy_keys(config):
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
    prefix = "SYNCROJOB_"
    for key, default_val in DEFAULT_CONFIG.items():
        env_key = f"{prefix}{key.upper()}"
        env_val = os.environ.get(env_key)
        if env_val:
            if isinstance(default_val, bool):
                config[key] = env_val.lower() in ("true", "1", "yes")
            elif isinstance(default_val, int):
                with suppress(ValueError):
                    config[key] = int(env_val)
            else:
                config[key] = env_val
    return config


def save_config(config: dict[str, Any], async_save: bool = True) -> bool:
    """Salva la configurazione su file.

    Se async_save è True (default), l'operazione di I/O (inclusa la cifratura)
    viene delegata a un thread di background per non bloccare il Main Thread della GUI.
    """
    global _config_cache  # noqa: PLW0603

    def _execute_save(cfg_to_save: dict[str, Any]) -> None:
        try:
            # Cripta credenziali per il salvataggio
            encrypt_all_credentials(cfg_to_save)

            # Scrittura atomica
            _atomic_write_json(CONFIG_FILE, cfg_to_save)
        except Exception as e:
            print(f"Async save failed: {e}")

    try:
        config_to_save = copy.deepcopy(config)

        if async_save:
            # Sincronizziamo la cache immediatamente in memoria
            with _config_lock:
                _config_cache = copy.deepcopy(config)

            # Lanciamo il thread per l'I/O su disco
            threading.Thread(target=_execute_save, args=(config_to_save,), daemon=True).start()
            return True
        # Salvataggio sincrono (es. in fase di chiusura app o test)
        encrypt_all_credentials(config_to_save)
        if _atomic_write_json(CONFIG_FILE, config_to_save):
            with _config_lock:
                _config_cache = copy.deepcopy(config)
            return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False
    return False


def invalidate_config_cache() -> None:
    """Invalida forzatamente la cache della configurazione in memoria."""
    global _config_cache  # noqa: PLW0603
    with _config_lock:
        _config_cache = None


def _is_file_in_use_error(e: Exception) -> bool:
    win_err_file_in_use = 32
    return isinstance(e, PermissionError) or (
        isinstance(e, OSError) and getattr(e, "winerror", 0) == win_err_file_in_use
    )


def _write_temp_and_replace(temp_path: Path, path: Path, data: dict[str, Any]) -> None:
    ensure_config_dir()
    with temp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())

    with _file_io_lock:
        if path.exists():
            os.replace(temp_path, path)
        else:
            temp_path.rename(path)


def _atomic_write_json(path: Path, data: dict[str, Any]) -> bool:
    """Scrive un file JSON in modo atomico usando un file temporaneo con retry e lock."""
    temp_path = path.parent / f"{path.name}.{threading.get_ident()}.tmp"
    max_retries = 5
    retry_delay = 0.1

    for attempt in range(max_retries):
        try:
            _write_temp_and_replace(temp_path, path, data)
        except (PermissionError, OSError) as e:
            if _is_file_in_use_error(e) and attempt < max_retries - 1:
                print(
                    f"[{threading.get_ident()}] File occupato, retry {attempt + 1}/{max_retries} per {path.name}"
                )
                time.sleep(retry_delay * (attempt + 1))
            else:
                print(
                    f"[{threading.get_ident()}] Impossibile scrivere {path.name} dopo {attempt + 1} tentativi: {e}"
                )
                break
        else:
            return True
        finally:
            if temp_path.exists():
                with suppress(OSError):
                    temp_path.unlink()
    return False


def get_config_value(key: str, default: Any = None) -> Any:
    """Recupera un singolo valore dalla configurazione."""
    return load_config().get(key, default)


def set_config_value(key: str, value: Any, async_save: bool = True) -> bool:
    """Imposta e salva un singolo valore nella configurazione."""
    config = load_config()
    config[key] = value
    return save_config(config, async_save=async_save)


def set_config_values(updates: dict[str, Any], async_save: bool = True) -> bool:
    """Imposta e salva più valori contemporaneamente nella configurazione."""
    config = load_config()
    config.update(updates)
    return save_config(config, async_save=async_save)


def get_download_path() -> str:
    """Restituisce il percorso della cartella download configurata o quella predefinita di sistema.

    Esegue una validazione di esistenza per evitare percorsi hardcoded non validi.
    """
    # Supporta sia la vecchia chiave che quella corretta per retrocompatibilità
    path = get_config_value("download_path") or get_config_value("browser_download_path")

    # Se il path non esiste o non è impostato, usa Downloads dell'utente corrente
    if not path or not Path(str(path)).exists():
        path = str(Path.home() / "Downloads")

    return str(path)


def reset_to_defaults(async_save: bool = True) -> bool:
    """Ripristina la configurazione ai valori predefiniti di fabbrica."""
    return save_config(copy.deepcopy(DEFAULT_CONFIG), async_save=async_save)


# --- ACCOUNT MANAGEMENT HELPERS ---


def add_account(bot_type: str, account_data: dict[str, Any], async_save: bool = True) -> bool:
    """Aggiunge un nuovo account alla configurazione."""
    config = load_config()
    username = account_data.get("username", "")
    password = account_data.get("password", "")
    is_default = account_data.get("is_default", False)

    # Se bot_type è safework, forza la chiave corretta anche se manca 'type' nei dati
    account_type = account_data.get("type", "")
    if bot_type == "safework" and not account_type:
        account_type = "safework"

    add_account_logic(config, username, password, is_default, account_type)
    return save_config(config, async_save=async_save)


def remove_account(bot_type: str, username: str, async_save: bool = True) -> bool:
    """Rimuove un account dalla configurazione."""
    config = load_config()
    remove_account_logic(config, username)
    return save_config(config, async_save=async_save)


def set_default_account(bot_type: str, username: str, async_save: bool = True) -> bool:
    """Imposta l'account di default per un tipo di bot."""
    config = load_config()
    if set_default_account_logic(config, username, bot_type):
        return save_config(config, async_save=async_save)
    return False


def switch_default_account(bot_type: str, async_save: bool = True) -> bool:
    """Ruota l'account di default per un tipo di bot (Round Robin)."""
    config = load_config()
    success, _ = switch_default_account_logic(config, bot_type)
    if success:
        return save_config(config, async_save=async_save)
    return False


def get_default_account(bot_type: str) -> dict[str, Any] | None:
    """Restituisce i dati dell'account di default per un tipo di bot."""
    config = load_config()
    acc_key = "accounts" if bot_type == "isab" else "safework_accounts"
    accounts = config.get(acc_key, [])
    if not accounts:
        return None

    # Se c'è solo un account, è quello di default
    if len(accounts) == 1:
        return cast("dict[str, Any]", accounts[0])

    # Altrimenti cerchiamo il flag default (o is_default per legacy)
    for acc in accounts:
        if acc.get("default") or acc.get("is_default"):
            return cast("dict[str, Any]", acc)

    # Se nessun account ha il flag, restituiamo il primo
    return cast("dict[str, Any]", accounts[0])


def import_config_from_file(file_path: Path, async_save: bool = True) -> tuple[bool, str]:
    """Importa una configurazione da un file esterno (backup)."""
    try:
        new_data = json.loads(file_path.read_text(encoding="utf-8"))

        # Backup attuale
        backup_msg = ""
        if CONFIG_FILE.exists():
            backup_file = CONFIG_DIR / f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            CONFIG_FILE.rename(backup_file)
            backup_msg = f"\nBackup precedente salvato in: {backup_file.name}"

        # Salva nuova (passando per save_config per criptare)
        if save_config(new_data, async_save=async_save):
            return (
                True,
                f"Configurazione importata con successo.{backup_msg}",
            )
    except json.JSONDecodeError:
        return False, "Il file non è un JSON valido."
    except Exception as e:
        return False, f"Errore critico importazione: {e}"
    else:
        return False, "Errore durante il salvataggio della nuova configurazione."
