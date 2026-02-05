"""
SyncroJob - Resource Manager
Centralized management of file paths, assets, and temporary resources.
"""

import os
import sys
from pathlib import Path


class ResourceManager:
    """Gestore centralizzato per percorsi e risorse del sistema."""

    # Root del progetto (gestisce sia sorgenti che eseguibili congelati)
    if getattr(sys, "frozen", False):
        exe_path = Path(sys.executable).parent
        meipass_path = Path(getattr(sys, "_MEIPASS", exe_path))

        if (exe_path / "_internal" / "assets").exists():
            PROJECT_ROOT = exe_path / "_internal"
        elif (meipass_path / "assets").exists():
            PROJECT_ROOT = meipass_path
        elif (exe_path / "assets").exists():
            PROJECT_ROOT = exe_path
        else:
            PROJECT_ROOT = meipass_path
    else:
        PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

    # Directory Standard (Sola Lettura Asset)
    ASSETS_DIR = PROJECT_ROOT / "assets"
    ICONS_DIR = ASSETS_DIR / "icons"
    STYLES_DIR = ASSETS_DIR / "styles"
    TEMP_DIR = PROJECT_ROOT / "temp"

    @classmethod
    def _get_config_dir(cls) -> Path:
        """Importazione lazy di CONFIG_DIR per evitare dipendenze circolari."""
        from src.core.config_manager import CONFIG_DIR

        return CONFIG_DIR

    @classmethod
    def get_logs_dir(cls) -> Path:
        return cls._get_config_dir() / "logs"

    @classmethod
    def get_data_dir(cls) -> Path:
        return cls._get_config_dir() / "data"

    @classmethod
    def get_asset_path(cls, relative_path: str) -> str:
        """Restituisce il path assoluto di un asset basandosi sulla PROJECT_ROOT."""
        if relative_path.startswith("assets/"):
            relative_path = relative_path[len("assets/") :]

        path = cls.ASSETS_DIR / relative_path.replace("/", os.sep)
        return str(path)

    @classmethod
    def get_icon(cls, name: str) -> str:
        """Restituisce il path assoluto di un'icona."""
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
        config_dir = cls._get_config_dir()
        for d in (cls.TEMP_DIR, config_dir / "logs", config_dir / "data"):
            d.mkdir(parents=True, exist_ok=True)


# Inizializzazione struttura all'import
ResourceManager.ensure_structure()
