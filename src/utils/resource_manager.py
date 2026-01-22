"""
SyncroJob - Resource Manager
Centralized management of file paths, assets, and temporary resources.
"""

import os
import sys
from pathlib import Path

from src.core.config_manager import CONFIG_DIR


class ResourceManager:
    """Gestore centralizzato per percorsi e risorse del sistema."""

    # Root del progetto (gestisce sia sorgenti che eseguibili congelati)
    if getattr(sys, "frozen", False):
        # PyInstaller crea sys._MEIPASS (directory temporanea/interna)
        # In onefile: _MEIPASS è la root temporanea.
        # In onedir (PyInstaller 6+): contenuti in _internal accanto all'exe.

        exe_dir = Path(os.path.dirname(sys.executable))
        base_dir = Path(getattr(sys, "_MEIPASS", exe_dir))

        # 1. Check in _MEIPASS (onefile or explicitly set)
        if (base_dir / "assets").exists():
            PROJECT_ROOT = base_dir
        # 2. Check in _internal (onedir default for PyInstaller > 6)
        elif (exe_dir / "_internal" / "assets").exists():
            PROJECT_ROOT = exe_dir / "_internal"
        # 3. Check directly next to exe (legacy onedir or manual copy)
        elif (exe_dir / "assets").exists():
            PROJECT_ROOT = exe_dir
        else:
            # Fallback safe
            PROJECT_ROOT = base_dir
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
        # Se il nome è già un path relativo completo (es. assets/icons/home.svg), estrai solo il nome
        if "assets/icons/" in name:
            name = name.split("/")[-1]

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
        for d in (cls.TEMP_DIR, cls.LOGS_DIR, cls.DATA_DIR):
            d.mkdir(parents=True, exist_ok=True)


# Inizializzazione struttura all'import
ResourceManager.ensure_structure()
