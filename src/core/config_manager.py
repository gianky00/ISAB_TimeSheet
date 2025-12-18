"""
Bot TS - Configuration Manager
Gestione della configurazione dell'applicazione.
"""
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional, List


# Path del file di configurazione
CONFIG_DIR = Path.home() / ".bot_ts"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Configurazione di default
DEFAULT_CONFIG: Dict[str, Any] = {
    "accounts": [],  # Lista di dict: {"username": "", "password": "", "default": False}
    "default_contract_number": "",  # Numero contratto di default
    "browser_headless": False,
    "browser_timeout": 30,
    "download_path": "",
    "fornitori": [],  # Lista dei fornitori configurati
    "last_ts_data": [],
    "last_ts_date": "01.01.2025",
    "last_ts_fornitore": "",
    "last_carico_ts_data": [],
    "last_oda_data": []
}


def ensure_config_dir():
    """Assicura che la directory di configurazione esista."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """
    Carica la configurazione dal file.
    Gestisce la migrazione automatica dalle vecchie chiavi.
    
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
                
            # --- MIGRAZIONE ---
            # Se esistono vecchie credenziali e la lista accounts è vuota, migrale
            if "isab_username" in config and config["isab_username"] and not config["accounts"]:
                config["accounts"].append({
                    "username": config["isab_username"],
                    "password": config.get("isab_password", ""),
                    "default": True
                })
                # Rimuovi le vecchie chiavi (opzionale, ma pulisce il file al prossimo salvataggio)
                if "isab_username" in config: del config["isab_username"]
                if "isab_password" in config: del config["isab_password"]

                # Salva subito la migrazione
                save_config(config)
            
            return config
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()
    else:
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]):
    """
    Salva la configurazione su file.
    
    Args:
        config: Dict con la configurazione da salvare
    """
    ensure_config_dir()
    
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Errore salvataggio configurazione: {e}")


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Ottiene un valore dalla configurazione.
    
    Args:
        key: Chiave del valore
        default: Valore di default se la chiave non esiste
        
    Returns:
        Il valore della chiave o il default
    """
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: Any):
    """
    Imposta un valore nella configurazione.
    
    Args:
        key: Chiave del valore
        value: Valore da salvare
    """
    config = load_config()
    config[key] = value
    save_config(config)


# --- Gestione Account ---

def get_accounts() -> List[Dict[str, Any]]:
    """Restituisce la lista degli account configurati."""
    return get_config_value("accounts", [])

def add_account(username: str, password: str, is_default: bool = False):
    """
    Aggiunge o aggiorna un account.

    Args:
        username: Username
        password: Password
        is_default: Se True, lo imposta come default (e rimuove default dagli altri)
    """
    accounts = get_accounts()

    # Se è il primo account, è default per forza
    if not accounts:
        is_default = True

    # Rimuovi se esiste già (update)
    accounts = [a for a in accounts if a["username"] != username]

    # Se questo diventa default, togli il flag agli altri
    if is_default:
        for acc in accounts:
            acc["default"] = False

    accounts.append({
        "username": username,
        "password": password,
        "default": is_default
    })

    set_config_value("accounts", accounts)

def remove_account(username: str):
    """Rimuove un account."""
    accounts = get_accounts()
    accounts = [a for a in accounts if a["username"] != username]

    # Se ho rimosso il default e ne rimangono altri, rendi il primo default
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
    """Restituisce l'account di default o il primo disponibile o None."""
    accounts = get_accounts()
    if not accounts:
        return None

    for acc in accounts:
        if acc.get("default"):
            return acc

    # Fallback al primo
    return accounts[0]


# --- Altri Helper ---

def get_data_path() -> str:
    """
    Restituisce il percorso base per i dati (es. Licenza).
    Cerca prima in CONFIG_DIR (AppData), poi nel root del progetto.
    """
    # 1. Cerca in CONFIG_DIR (AppData)
    if (CONFIG_DIR / "Licenza").exists():
        return str(CONFIG_DIR)

    # 2. Cerca nel root del progetto
    project_root = Path(__file__).resolve().parent.parent.parent
    if (project_root / "Licenza").exists():
        return str(project_root)

    # 3. Default: CONFIG_DIR
    return str(CONFIG_DIR)


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
