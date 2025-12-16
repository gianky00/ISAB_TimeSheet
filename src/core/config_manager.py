"""
Bot TS - Configuration Manager
Gestione della configurazione dell'applicazione.
"""
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional


# Path del file di configurazione
CONFIG_DIR = Path.home() / ".bot_ts"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Configurazione di default
DEFAULT_CONFIG: Dict[str, Any] = {
    "isab_username": "",
    "isab_password": "",
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
    
    Returns:
        Dict con la configurazione
    """
    ensure_config_dir()
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # Merge con default per nuove chiavi
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
            
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


def get_download_path() -> str:
    """
    Restituisce il path di download configurato.
    
    Returns:
        Path di download o la cartella Downloads di default
    """
    path = get_config_value("download_path", "")
    
    if path and os.path.isdir(path):
        return path
    
    # Default alla cartella Downloads
    default_download = Path.home() / "Downloads"
    if default_download.exists():
        return str(default_download)
    
    return str(Path.home())


def get_fornitori() -> list:
    """
    Restituisce la lista dei fornitori configurati.
    
    Returns:
        Lista dei fornitori
    """
    return get_config_value("fornitori", [])


def add_fornitore(fornitore: str) -> bool:
    """
    Aggiunge un fornitore alla lista.
    
    Args:
        fornitore: Nome del fornitore da aggiungere
        
    Returns:
        True se aggiunto, False se già presente
    """
    fornitori = get_fornitori()
    
    if fornitore not in fornitori:
        fornitori.append(fornitore)
        set_config_value("fornitori", fornitori)
        return True
    
    return False


def remove_fornitore(fornitore: str) -> bool:
    """
    Rimuove un fornitore dalla lista.
    
    Args:
        fornitore: Nome del fornitore da rimuovere
        
    Returns:
        True se rimosso, False se non presente
    """
    fornitori = get_fornitori()
    
    if fornitore in fornitori:
        fornitori.remove(fornitore)
        set_config_value("fornitori", fornitori)
        return True
    
    return False
