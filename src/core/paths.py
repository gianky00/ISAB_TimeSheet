"""
SyncroJob - Path Management
Centralized path definitions for the application.
"""

from pathlib import Path
from typing import Final

from platformdirs import user_data_dir

from src.core.constants import FileNames
from src.core.version import APP_NAME, __version__

# Configuration Directory (OS-dependent standard path)
CONFIG_DIR: Final[Path] = Path(user_data_dir(APP_NAME, appauthor=False))

# Main Configuration File
CONFIG_FILE: Final[Path] = CONFIG_DIR / FileNames.CONFIG

# Base Project Directory (absolute path to the project root)
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent

# Standard Subdirectories
DB_DIR: Final[Path] = CONFIG_DIR / "data"
LOGS_DIR: Final[Path] = CONFIG_DIR / "logs"
DRIVERS_DIR: Final[Path] = CONFIG_DIR / "drivers"
SECURITY_DIR: Final[Path] = CONFIG_DIR / "security"


def get_version() -> str:
    """Restituisce la versione corrente dell'applicazione."""
    return __version__


def get_data_path() -> str:
    """Restituisce il percorso della directory dati (per retrocompatibilità)."""
    return str(DB_DIR)


def get_logs_path() -> str:
    """Restituisce il percorso della directory log (per retrocompatibilità)."""
    return str(LOGS_DIR)
