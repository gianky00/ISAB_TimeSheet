"""
Bot TS - Configuration Manager
Gestione della configurazione dell'applicazione.
"""
import os
import json
import copy
import traceback
from pathlib import Path
from typing import Any, Dict, Optional, List
from src.core.secrets_manager import SecretsManager
from platformdirs import user_data_dir

# Path del file di configurazione
CONFIG_DIR = Path(user_data_dir("BotTS", "GiancarloAllegretti"))
CONFIG_FILE = CONFIG_DIR / "config.json"
_config_cache: Optional[Dict[str, Any]] = None

# Configurazione di default
DEFAULT_CONFIG: Dict[str, Any] = {
    "accounts": [],
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
    "certificati_campione_path": r"C:\Users\Coemi\Desktop\CERTIFICATI CAMPIONE\Registro calibrazioni\STRUMENTI CAMPIONE ISAB SUD AGGIORNATO.xlsm"
}

def ensure_config_dir():
    """Assicura che la directory di configurazione esista."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config() -> Dict[str, Any]:
    """
    Carica la configurazione dal file, la decripta e la mette in cache.
    Se la cache è piena, restituisce la cache.
    """
    global _config_cache
    if _config_cache is not None:
        return copy.deepcopy(_config_cache)

    ensure_config_dir()
    config = DEFAULT_CONFIG.copy()

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
            config.update(loaded_config)
        except (json.JSONDecodeError, IOError):
            pass # Usa i default

    # Decripta e recupera password
    if "accounts" in config:
        from src.utils.security import password_manager
        for acc in config["accounts"]:
            username = acc.get("username")
            if not username:
                continue

            # Priorità 1: Keyring
            password_from_keyring = SecretsManager.get_credential('isab_portal', username)
            if password_from_keyring:
                acc["password"] = password_from_keyring
                continue

            # Priorità 2: File di configurazione (fallback)
            password_from_file = acc.get("password")
            if password_from_file:
                acc["password"] = password_manager.decrypt(password_from_file)

    # Migrazione Legacy
    if "isab_username" in config and config.get("isab_username"):
        if not any(a.get("username") == config["isab_username"] for a in config["accounts"]):
            config["accounts"].append({
                "username": config["isab_username"],
                "password": config.get("isab_password", ""),
                "default": True
            })
        del config["isab_username"]
        if "isab_password" in config:
            del config["isab_password"]
        save_config(config) # Salva subito la configurazione migrata

    _config_cache = copy.deepcopy(config)
    return config

def save_config(config: Dict[str, Any]):
    """
    Salva la configurazione. Tenta di usare keyring, altrimenti cripta nel file.
    Aggiorna la cache con la versione decriptata.
    """
    global _config_cache
    ensure_config_dir()
    
    # Lavora su una copia per non modificare l'input
    config_to_process = copy.deepcopy(config)

    # Logica di salvataggio password
    if "accounts" in config_to_process:
        from src.utils.security import password_manager
        for acc in config_to_process["accounts"]:
            username = acc.get("username")
            password = acc.get("password")

            if not (username and password):
                continue

            # Tenta di salvare nel keyring
            try:
                if SecretsManager.is_available():
                    SecretsManager.store_credential('isab_portal', username, password)
                    # Se ha successo, rimuovi la password dal file
                    acc.pop("password", None)
                    continue
            except Exception as e:
                print(f"Keyring non disponibile, uso fallback: {e}")

            # Fallback: cripta la password nel file
            acc["password"] = password_manager.encrypt(password)

    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_to_process, f, indent=2, ensure_ascii=False)

        # Invalida e aggiorna la cache con i dati decriptati originali
        _config_cache = copy.deepcopy(config)
    except IOError as e:
        print(f"Errore salvataggio configurazione: {e}")
        # Se il salvataggio fallisce, la cache non viene aggiornata per sicurezza
    except Exception:
        print(f"Errore critico durante il salvataggio:\n{traceback.format_exc()}")


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

    accounts.append({
        "username": username,
        "password": password,
        "default": is_default
    })

    config["accounts"] = accounts
    save_config(config)

def remove_account(username: str):
    """Rimuove un account e le credenziali associate."""
    config = load_config()
    accounts = config.get("accounts", [])
    config["accounts"] = [a for a in accounts if a.get("username") != username]

    try:
        if SecretsManager.is_available():
            SecretsManager.delete_credential('isab_portal', username)
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
        acc["default"] = (acc.get("username") == username)
        if acc["default"]:
            found = True

    if found:
        config["accounts"] = accounts
        save_config(config)

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
