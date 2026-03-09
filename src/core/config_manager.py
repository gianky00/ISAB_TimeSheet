"""
Bot TS - Configuration Manager
Gestione della configurazione dell'applicazione.
Refactored V9.0: Modularized architecture.
"""

import copy
import json
import os
import threading
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from platformdirs import user_data_dir

from src.core.constants import FileNames
from src.core.version import __version__

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

# Path del file di configurazione
APP_NAME = "SyncroJob"
CONFIG_DIR = Path(user_data_dir(APP_NAME, appauthor=False))
CONFIG_FILE = CONFIG_DIR / FileNames.CONFIG
BASE_DIR = Path(__file__).resolve().parent.parent.parent

_config_cache: dict[str, Any] | None = None
_config_lock = threading.RLock()


def _reset_configuration_for_testing() -> None:
    """Resetta la cache della configurazione (solo per unit test)."""
    global _config_cache
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
    global _config_cache
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

        if env_val is not None:
            if isinstance(default_val, bool):
                config[key] = env_val.lower() in ("true", "1", "yes")
            elif isinstance(default_val, int):
                with suppress(ValueError):
                    config[key] = int(env_val)
            else:
                config[key] = env_val

    return config


def save_config(config: dict[str, Any]) -> None:
    """Salva la configurazione in modo atomico."""
    global _config_cache
    with _config_lock:
        ensure_config_dir()
        config_to_save = copy.deepcopy(config)

        # Cripta credenziali prima del salvataggio
        encrypt_all_credentials(config_to_save)

        try:
            _atomic_write_json(config_to_save, CONFIG_FILE)
            _config_cache = copy.deepcopy(config)
        except Exception as e:
            print(f"Errore critico durante il salvataggio: {e}")


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


# Public API helpers
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


def add_account(username: str, password: str, is_default: bool = False, account_type: str = "") -> None:
    """Aggiunge o aggiorna un account."""
    config = load_config()
    config = add_account_logic(config, username, password, is_default, account_type)
    save_config(config)


def remove_account(username: str) -> None:
    """Rimuove un account e le credenziali associate."""
    config = load_config()
    config = remove_account_logic(config, username)
    save_config(config)


def set_default_account(username: str) -> None:
    """Imposta un account come default."""
    config = load_config()
    if set_default_account_logic(config, username):
        save_config(config)


def switch_default_account(service_type: str = "isab") -> tuple[bool, str | None]:
    """Switcha l'account di default in modo circolare."""
    config = load_config()
    success, new_user = switch_default_account_logic(config, service_type)
    if success:
        save_config(config)
    return success, new_user


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
    """Esporta la configurazione corrente in un file JSON."""
    try:
        config = load_config()
        export_data = copy.deepcopy(config)
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
    """Ripristina la configurazione predefinita."""
    global _config_cache
    with _config_lock:
        _config_cache = copy.deepcopy(DEFAULT_CONFIG)
        save_config(_config_cache)


def import_configuration(import_path: str | Path) -> tuple[bool, str]:
    """Importa la configurazione da un file JSON."""
    try:
        path = Path(import_path)
        if not path.exists():
            return False, "File di importazione non trovato."

        new_config = json.loads(path.read_text(encoding="utf-8"))
        critical_keys = ["accounts", "browser_timeout", "fornitori"]
        if not any(k in new_config for k in critical_keys):
            return False, "Il file selezionato non sembra una configurazione valida di SyncroJob."

        new_config.pop("_meta", None)
        backup_file = CONFIG_DIR / f"config_backup_pre_import_{int(datetime.now(UTC).timestamp())}.json"
        current_config = load_config()
        backup_file.write_text(json.dumps(current_config, indent=2), encoding="utf-8")

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
