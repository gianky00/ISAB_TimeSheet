"""
SyncroJob - Resource Manager
Gestione centralizzata di percorsi file, asset e risorse temporanee.
Supporta sia l'esecuzione da sorgenti che da pacchetto PyInstaller (congelato).
"""

import os
import sys
from pathlib import Path


class ResourceManager:
    """
    Gestore centralizzato per percorsi e risorse del sistema.
    Risolve dinamicamente la root del progetto e fornisce metodi helper per accedere ad asset e configurazioni.
    """

    # Root del progetto (gestisce sia sorgenti che eseguibili congelati)
    if getattr(sys, "frozen", False):
        exe_path = Path(sys.executable).parent
        meipass_path = Path(getattr(sys, "_MEIPASS", exe_path))

        # Priorità 1: Cartelle esterne (SVILUPPATORE/ADMIN OVERRIDE)
        # Se esistono 'assets' o 'drivers' accanto all'exe, usiamo quella come root
        if (exe_path / "assets").exists() or (exe_path / "drivers").exists():
            PROJECT_ROOT = exe_path
        # Priorità 2: Cartelle interne (DEFAULT PYINSTALLER)
        elif (exe_path / "_internal" / "assets").exists():
            PROJECT_ROOT = exe_path / "_internal"
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
        """
        Importazione lazy di CONFIG_DIR per evitare dipendenze circolari.

        Returns:
            Path: Il percorso della cartella di configurazione utente.
        """
        from src.core.config_manager import CONFIG_DIR

        return CONFIG_DIR

    @classmethod
    def get_logs_dir(cls) -> Path:
        """
        Restituisce il percorso della cartella dei log.

        Returns:
            Path: Percorso della directory log.
        """
        return cls._get_config_dir() / "logs"

    @classmethod
    def get_data_dir(cls) -> Path:
        """
        Restituisce il percorso della cartella dati utente.

        Returns:
            Path: Percorso della directory data.
        """
        return cls._get_config_dir() / "data"

    @classmethod
    def get_writable_drivers_dir(cls) -> Path:
        """
        Restituisce il path della cartella drivers nella directory dati utente (sempre scrivibile).

        Returns:
            Path: Percorso della directory drivers scrivibile.
        """
        path = cls._get_config_dir() / "drivers"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @classmethod
    def get_asset_path(cls, relative_path: str) -> str:
        """
        Restituisce il path assoluto di un asset basandosi sulla PROJECT_ROOT.

        Args:
            relative_path: Percorso relativo all'interno della cartella assets.

        Returns:
            str: Percorso assoluto convertito per il sistema operativo corrente.
        """
        relative_path = relative_path.removeprefix("assets/")

        path = cls.ASSETS_DIR / relative_path.replace("/", os.sep)
        return str(path)

    @classmethod
    def get_icon(cls, name: str) -> str:
        """
        Restituisce il path assoluto di un'icona cercandola tra gli asset.

        Args:
            name: Nome del file icona (con o senza estensione).

        Returns:
            str: Percorso assoluto del file icona o stringa vuota se non trovato.
        """
        if "assets/icons/" in name:
            name = name.split("/")[-1]

        if not name.endswith((".svg", ".png", ".ico")):
            name += ".svg"
        path = cls.ICONS_DIR / name
        return str(path) if path.exists() else ""

    @classmethod
    def get_style(cls, theme: str = "light") -> str:
        """
        Restituisce il path di un file di stile QSS.

        Args:
            theme: Nome del tema (light o dark).

        Returns:
            str: Percorso del file .qss.
        """
        path = cls.STYLES_DIR / f"{theme}.qss"
        return str(path) if path.exists() else ""

    @classmethod
    def get_temp_path(cls, filename: str) -> Path:
        """
        Genera un percorso sicuro nella cartella temporanea del sistema.

        Args:
            filename: Nome del file desiderato.

        Returns:
            Path: Percorso completo all'interno della directory temp.
        """
        cls.TEMP_DIR.mkdir(exist_ok=True)
        return cls.TEMP_DIR / filename

    @classmethod
    def ensure_structure(cls) -> None:
        """Assicura che tutte le cartelle vitali per l'applicazione esistano sul filesystem."""
        config_dir = cls._get_config_dir()
        for d in (cls.TEMP_DIR, config_dir / "logs", config_dir / "data"):
            d.mkdir(parents=True, exist_ok=True)


# Inizializzazione struttura all'import
ResourceManager.ensure_structure()
