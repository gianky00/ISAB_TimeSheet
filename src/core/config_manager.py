"""
Bot TS - Configuration Manager
Gestisce la configurazione persistente dell'applicazione.
"""
import os
import sys
import json
import logging
import platform
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    "download_path": "",  # Empty = default Downloads folder
    "isab_username": "",
    "isab_password": "",
    "browser_headless": False,
    "browser_timeout": 30,
    "last_ts_data": [],  # Last Scarico TS data
    "last_oda_data": []  # Last Dettagli OdA data
}


def get_base_path():
    """Returns the base path of the application executable (read-only)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_data_path():
    """Returns the writable data path for the application (AppData)."""
    system = platform.system()

    if system == "Windows":
        base = os.getenv('LOCALAPPDATA')
        if not base:
            base = os.path.expanduser("~")
        path = os.path.join(base, "Programs", "Bot TS")
    else:
        # Linux/Mac fallback
        path = os.path.join(os.path.expanduser("~"), ".local", "share", "Bot TS")

    # Ensure directory exists
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            logging.error(f"Error creating data directory {path}: {e}")

    return path


def get_download_path():
    """Returns the configured download path or the default Downloads folder."""
    config = load_config()
    custom_path = config.get("download_path", "").strip()
    
    if custom_path and os.path.isdir(custom_path):
        return custom_path
    
    # Default to user's Downloads folder
    if platform.system() == "Windows":
        return str(Path.home() / "Downloads")
    else:
        return str(Path.home() / "Downloads")


def get_config_file_path():
    """Returns the path to the config file."""
    return os.path.join(get_data_path(), "config.json")


def load_config():
    """Loads configuration from config.json, or returns defaults if not found."""
    config_file = get_config_file_path()
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # Merge with defaults to ensure all keys exist
                config = DEFAULT_CONFIG.copy()
                config.update(user_config)
                return config
        except Exception as e:
            logging.error(f"Error loading config.json: {e}")
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config_data):
    """Saves configuration to config.json."""
    try:
        path = get_data_path()
        if not os.path.exists(path):
            os.makedirs(path)

        config_file = get_config_file_path()
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        logging.error(f"Error saving config.json: {e}")
        return False


def get_config_value(key, default=None):
    """Gets a single config value."""
    config = load_config()
    return config.get(key, default)


def set_config_value(key, value):
    """Sets a single config value and saves."""
    config = load_config()
    config[key] = value
    return save_config(config)


# Initialize config on module load
current_config = load_config()
