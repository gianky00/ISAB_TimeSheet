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
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from src.core.paths import BASE_DIR, CONFIG_DIR, CONFIG_FILE
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

_config_cache: dict[str, Any] | None = None
_config_lock = threading.RLock()


def _reset_configuration_for_testing() -> None:
    """Resetta la cache della configurazione (solo per unit test)."""
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


def save_config(config: dict[str, Any]) -> bool:
    """Salva la configurazione su file, criptando le credenziali prima del write."""
    global _config_cache  # noqa: PLW0603
    try:
        config_to_save = copy.deepcopy(config)

        # Cripta credenziali per il salvataggio
        encrypt_all_credentials(config_to_save)

        # Scrittura atomica
        if _atomic_write_json(CONFIG_FILE, config_to_save):
            with _config_lock:
                # Forza l'invalidazione della cache per garantire che load_config() rilegga da disco
                _config_cache = None
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


def _atomic_write_json(path: Path, data: dict[str, Any]) -> bool:
    """Scrive un file JSON in modo atomico usando un file temporaneo."""
    temp_path = path.with_suffix(".tmp")
    try:
        ensure_config_dir()
        with temp_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            # Flush e sync per essere sicuri che i dati siano su disco prima di chiudere
            f.flush()
            os.fsync(f.fileno())

        if path.exists():
            os.replace(temp_path, path)
        else:
            temp_path.rename(path)
    except Exception as e:
        print(f"Atomic write failed for {path}: {e}")
        if temp_path.exists():
            with suppress(OSError):
                temp_path.unlink()
        return False
    else:
        return True


def get_config_value(key: str, default: Any = None) -> Any:
    """Recupera un singolo valore dalla configurazione."""
    return load_config().get(key, default)


def set_config_value(key: str, value: Any) -> bool:
    """Imposta e salva un singolo valore nella configurazione."""
    config = load_config()
    config[key] = value
    return save_config(config)


def set_config_values(updates: dict[str, Any]) -> bool:
    """Imposta e salva più valori contemporaneamente nella configurazione."""
    config = load_config()
    config.update(updates)
    return save_config(config)


def get_download_path() -> str:
    """
    Restituisce il percorso della cartella download configurata o quella predefinita di sistema.
    Esegue una validazione di esistenza per evitare percorsi hardcoded da altri PC (es. Coemi).
    """
    # Supporta sia la vecchia chiave che quella corretta per retrocompatibilità
    path = get_config_value("download_path") or get_config_value("browser_download_path")

    # Se il path non esiste o non è impostato, usa Downloads dell'utente corrente
    if not path or not Path(str(path)).exists():
        path = str(Path.home() / "Downloads")

    return str(path)


def reset_to_defaults() -> bool:
    """Ripristina la configurazione ai valori predefiniti di fabbrica."""
    return save_config(copy.deepcopy(DEFAULT_CONFIG))


# --- ACCOUNT MANAGEMENT HELPERS ---


def add_account(bot_type: str, account_data: dict[str, Any]) -> bool:
    """Aggiunge un nuovo account alla configurazione."""
    config = load_config()
    username = account_data.get("username", "")
    password = account_data.get("password", "")
    is_default = account_data.get("is_default", False)
    account_type = account_data.get("type", "") if bot_type != "isab" else ""

    add_account_logic(config, username, password, is_default, account_type)
    return save_config(config)


def remove_account(bot_type: str, username: str) -> bool:
    """Rimuove un account dalla configurazione."""
    config = load_config()
    remove_account_logic(config, username)
    return save_config(config)


def set_default_account(bot_type: str, username: str) -> bool:
    """Imposta l'account di default per un tipo di bot."""
    config = load_config()
    if set_default_account_logic(config, username):
        return save_config(config)
    return False


def switch_default_account(bot_type: str) -> bool:
    """Ruota l'account di default per un tipo di bot (Round Robin)."""
    config = load_config()
    success, _ = switch_default_account_logic(config, bot_type)
    if success:
        return save_config(config)
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


def import_config_from_file(file_path: Path) -> tuple[bool, str]:
    """Importa una configurazione da un file esterno (backup)."""
    try:
        new_data = json.loads(file_path.read_text(encoding="utf-8"))

        # Backup attuale
        if CONFIG_FILE.exists():
            backup_file = CONFIG_DIR / f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            CONFIG_FILE.rename(backup_file)

        # Salva nuova (passando per save_config per criptare)
        if save_config(new_data):
            return (
                True,
                f"Configurazione importata con successo.\nBackup precedente salvato in: {backup_file.name}",
            )
    except json.JSONDecodeError:
        return False, "Il file non è un JSON valido."
    except Exception as e:
        return False, f"Errore critico importazione: {e}"
    else:
        return False, "Errore durante il salvataggio della nuova configurazione."
