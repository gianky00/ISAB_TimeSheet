"""
Bot TS - Configuration Manager
Gestione della configurazione dell'applicazione.
"""
import os
import json
import copy
from pathlib import Path
from typing import Any, Dict, Optional, List
from src.core.secrets_manager import SecretsManager
from platformdirs import user_data_dir

# Path del file di configurazione
CONFIG_DIR = Path(user_data_dir("BotTS", "GiancarloAllegretti"))
CONFIG_FILE = CONFIG_DIR / "config.json"

# Configurazione di default
DEFAULT_CONFIG: Dict[str, Any] = {
    "accounts": [],  # Lista di dict: {"username": "", "default": False} (password in keyring)
    "contracts": [],  # Lista numeri contratto
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
    Carica la configurazione dal file.
    Recupera le password dal keyring.
    
    Returns:
        Dict con la configurazione
    """
    ensure_config_dir()
    
    config = DEFAULT_CONFIG.copy()

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)

            # Merge con default
            for key, value in loaded_config.items():
                config[key] = value

            # Recupera password dal keyring
            if "accounts" in config:
                for acc in config["accounts"]:
                    username = acc.get("username")
                    if username:
                        password = SecretsManager.get_credential('isab_portal', username)
                        if password:
                            acc["password"] = password
                        else:
                            # Fallback: controlla se c'è una password legacy nel config (encrypted)
                            # Se sì, la decifriamo e la migriamo al prossimo save
                            from src.utils.security import password_manager
                            legacy_pwd = acc.get("password")
                            if legacy_pwd:
                                acc["password"] = password_manager.decrypt(legacy_pwd)

            # --- MIGRAZIONE ---
            migrated = False

            # Migrazione Account legacy
            if "isab_username" in config and config["isab_username"] and not config["accounts"]:
                config["accounts"].append({
                    "username": config["isab_username"],
                    "password": config.get("isab_password", ""),
                    "default": True
                })
                if "isab_username" in config: del config["isab_username"]
                if "isab_password" in config: del config["isab_password"]
                migrated = True

            if migrated:
                save_config(config)
            
            return config
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()
    else:
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]):
    """
    Salva la configurazione su file.
    Salva le password nel keyring e NON nel file JSON.
    
    Args:
        config: Dict con la configurazione da salvare
    """
    ensure_config_dir()
    
    config_to_save = copy.deepcopy(config)

    # Gestione Account: salva password in keyring e rimuovi da config_to_save
    if "accounts" in config_to_save:
        from src.utils.security import password_manager
        for acc in config_to_save["accounts"]:
            username = acc.get("username")
            password = acc.get("password")

            if username and password:
                # Tenta di salvare in keyring
                stored_in_keyring = SecretsManager.store_credential('isab_portal', username, password)

                # Se keyring fallisce, salva password criptata nel file come fallback
                if not stored_in_keyring:
                    acc["password"] = password_manager.encrypt(password)
                else:
                    # Se keyring ha successo, rimuovi password dal file
                    if "password" in acc:
                        del acc["password"]

    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_to_save, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Errore salvataggio configurazione: {e}")


def get_config_value(key: str, default: Any = None) -> Any:
    """Ottiene un valore dalla configurazione."""
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: Any):
    """Imposta un valore nella configurazione."""
    config = load_config()
    config[key] = value
    save_config(config)


# --- Gestione Account ---

def get_accounts() -> List[Dict[str, Any]]:
    """Restituisce la lista degli account configurati."""
    return get_config_value("accounts", [])

def add_account(username: str, password: str, is_default: bool = False):
    """Aggiunge o aggiorna un account."""
    accounts = get_accounts()

    if not accounts:
        is_default = True

    # Rimuovi se esiste già
    accounts = [a for a in accounts if a["username"] != username]

    if is_default:
        for acc in accounts:
            acc["default"] = False

    accounts.append({
        "username": username,
        "password": password, # Verrà salvato nel keyring da save_config
        "default": is_default
    })

    set_config_value("accounts", accounts)

def remove_account(username: str):
    """Rimuove un account e le credenziali dal keyring."""
    accounts = get_accounts()
    accounts = [a for a in accounts if a["username"] != username]

    # Rimuovi da keyring
    SecretsManager.delete_credential('isab_portal', username)

    if accounts and not any(a.get("default") for a in accounts):
        accounts[0]["default"] = True

    set_config_value("accounts", accounts)

def set_default_account(username: str):
    """Imposta un account come default."""
    accounts = get_accounts()
    found = False
    for acc in accounts:
        if acc["username"] == username:
            acc["default"] = True
            found = True
        else:
            acc["default"] = False

    if found:
        set_config_value("accounts", accounts)

def get_default_account() -> Optional[Dict[str, str]]:
    """Restituisce l'account di default."""
    accounts = get_accounts()
    if not accounts:
        return None

    for acc in accounts:
        if acc.get("default"):
            return acc

    return accounts[0]


# --- Altri Helper ---

def get_data_path() -> str:
    """Restituisce il percorso base per i dati."""
    # Priorità: Cartella Dati Utente
    data_dir = CONFIG_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return str(data_dir)


def get_download_path() -> str:
    """Restituisce il path di download configurato."""
    path = get_config_value("download_path", "")
    
    if path and os.path.isdir(path):
        return path
    
    default_download = Path.home() / "Downloads"
    if default_download.exists():
        return str(default_download)
    
    return str(Path.home())


def get_fornitori() -> list:
    """Restituisce la lista dei fornitori configurati."""
    return get_config_value("fornitori", [])
