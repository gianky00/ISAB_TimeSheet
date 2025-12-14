import json
import os
from pathlib import Path
from platformdirs import user_downloads_dir

DATA_DIR = Path(__file__).parent.parent / "data"
CONFIG_FILE = DATA_DIR / "config.json"

DEFAULT_CONFIG = {
    "username": "9psaraceno",
    "password": "Mascara@13"
}

def ensure_data_dir():
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)

def load_config():
    ensure_data_dir()
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return DEFAULT_CONFIG

def save_config(config_data):
    ensure_data_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)

def get_downloads_path():
    return Path(user_downloads_dir())
