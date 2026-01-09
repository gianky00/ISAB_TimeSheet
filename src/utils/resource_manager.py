"""
SyncroJob - Resource Manager
Centralized management of file paths, assets, and temporary resources.
"""

import os
import sys
from pathlib import Path
from typing import Optional

from src.core.config_manager import CONFIG_DIR

class ResourceManager:
    """Gestore centralizzato per percorsi e risorse del sistema."""
    
    # Root del progetto (gestisce sia sorgenti che eseguibili congelati)
    if getattr(sys, "frozen", False):
        PROJECT_ROOT = Path(os.path.dirname(sys.executable))
    else:
        PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent

    # Directory Standard
    ASSETS_DIR = PROJECT_ROOT / "assets"
    ICONS_DIR = ASSETS_DIR / "icons"
    STYLES_DIR = ASSETS_DIR / "styles"
    TEMP_DIR = PROJECT_ROOT / "temp"
    
    # User Data (Config & Logs)
    LOGS_DIR = CONFIG_DIR / "logs"
    DATA_DIR = CONFIG_DIR / "data"

    @classmethod
    def get_icon(cls, name: str) -> str:
        """Restituisce il path assoluto di un'icona."""
        if not name.endswith((".svg", ".png", ".ico")):
            name += ".svg"
        path = cls.ICONS_DIR / name
        return str(path) if path.exists() else ""

    @classmethod
    def get_style(cls, theme: str = "light") -> str:
        """Restituisce il path di un file QSS."""
        path = cls.STYLES_DIR / f"{theme}.qss"
        return str(path) if path.exists() else ""

    @classmethod
    def get_temp_path(cls, filename: str) -> Path:
        """Genera un percorso sicuro nella cartella temp."""
        cls.TEMP_DIR.mkdir(exist_ok=True)
        return cls.TEMP_DIR / filename

    @classmethod
    def ensure_structure(cls):
        """Assicura che tutte le cartelle necessarie esistano."""
        for d in [cls.TEMP_DIR, cls.LOGS_DIR, cls.DATA_DIR]:
            d.mkdir(parents=True, exist_ok=True)

# Inizializzazione struttura all'import
ResourceManager.ensure_structure()
