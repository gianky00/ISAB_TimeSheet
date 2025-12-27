"""
Bot TS - Configuration Manager
Gestione della configurazione dell'applicazione (Singleton Pattern).
"""
import json
import copy
import traceback
from pathlib import Path
from typing import Any, Dict, Optional, List
from platformdirs import user_data_dir

from src.core.secrets_manager import SecretsManager

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

class ConfigManager:
    """Gestisce la configurazione dell'applicazione (Singleton)."""

    _instance: Optional['ConfigManager'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.app_name = "BotTS"
        self.app_author = "GiancarloAllegretti"
        self._config_dir = Path(user_data_dir(self.app_name, self.app_author))
        self._config_file = self._config_dir / "config.json"
        self._config_cache: Optional[Dict[str, Any]] = None
        self._ensure_config_dir()

    @property
    def config_dir(self) -> Path:
        return self._config_dir

    @property
    def config_file(self) -> Path:
        return self._config_file

    def _ensure_config_dir(self):
        """Assicura che la directory di configurazione esista."""
        self._config_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any]:
        """
        Carica la configurazione, la decripta e la mette in cache.
        """
        if self._config_cache is not None:
            return copy.deepcopy(self._config_cache)

        self._ensure_config_dir()
        config = DEFAULT_CONFIG.copy()

        if self._config_file.exists():
            try:
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                config.update(loaded_config)
            except (json.JSONDecodeError, IOError):
                pass

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
            self.save(config) # Salva subito la configurazione migrata

        self._config_cache = copy.deepcopy(config)
        return config

    def save(self, config: Dict[str, Any]):
        """
        Salva la configurazione. Tenta di usare keyring, altrimenti cripta nel file.
        Aggiorna la cache con la versione decriptata.
        """
        self._ensure_config_dir()

        config_to_process = copy.deepcopy(config)

        if "accounts" in config_to_process:
            from src.utils.security import password_manager
            for acc in config_to_process["accounts"]:
                username = acc.get("username")
                password = acc.get("password")

                if not (username and password):
                    continue

                try:
                    if SecretsManager.is_available():
                        SecretsManager.store_credential('isab_portal', username, password)
                        acc.pop("password", None)
                        continue
                except Exception as e:
                    print(f"Keyring non disponibile, uso fallback: {e}")

                acc["password"] = password_manager.encrypt(password)

        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_process, f, indent=2, ensure_ascii=False)

            # Update cache with original (unencrypted) config
            self._config_cache = copy.deepcopy(config)
        except IOError as e:
            print(f"Errore salvataggio configurazione: {e}")
        except Exception:
            print(f"Errore critico durante il salvataggio:\n{traceback.format_exc()}")

    def get_value(self, key: str, default: Any = None) -> Any:
        return self.load().get(key, default)

    def set_value(self, key: str, value: Any):
        config = self.load()
        config[key] = value
        self.save(config)

    def get_data_path(self) -> str:
        data_dir = self._config_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return str(data_dir)

    def get_download_path(self) -> str:
        path = self.get_value("download_path", "")
        if path and Path(path).is_dir():
            return path

        # Fallback to standard Downloads
        try:
            # Try to get system download dir, else fallback to home/Downloads or home
            from pathlib import Path
            home = Path.home()
            downloads = home / "Downloads"
            return str(downloads) if downloads.exists() else str(home)
        except:
            return str(Path.home())


# --- Module-Level Wrappers (Backward Compatibility) ---

_instance = ConfigManager()

CONFIG_DIR = _instance.config_dir
CONFIG_FILE = _instance.config_file

def load_config() -> Dict[str, Any]:
    return _instance.load()

def save_config(config: Dict[str, Any]):
    _instance.save(config)

def get_config_value(key: str, default: Any = None) -> Any:
    return _instance.get_value(key, default)

def set_config_value(key: str, value: Any):
    _instance.set_value(key, value)

def get_data_path() -> str:
    return _instance.get_data_path()

def get_download_path() -> str:
    return _instance.get_download_path()

def get_accounts() -> List[Dict[str, Any]]:
    return get_config_value("accounts", [])

def add_account(username: str, password: str, is_default: bool = False):
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
    accounts = get_accounts()
    if not accounts:
        return None
    return next((acc for acc in accounts if acc.get("default")), accounts[0])

def get_fornitori() -> list:
    return get_config_value("fornitori", [])
