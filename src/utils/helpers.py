"""
SyncroJob - Utility Helpers
Funzioni di utilità generali per la gestione del filesystem, formattazione dati e cleanup processi.
Include una robusta logica di terminazione per processi Chrome/Chromedriver "zombie".
"""

import logging
import os
import re
import sys
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def get_asset_path(relative_path: str) -> str:
    """
    Restituisce il percorso assoluto di un asset.
    Funziona sia in sviluppo che nell'app installata.
    Utilizza ResourceManager come fonte unica di verità.
    """
    from src.utils.resource_manager import ResourceManager

    return ResourceManager.get_asset_path(relative_path)


def get_app_icon_path() -> str | None:
    """Restituisce il percorso dell'icona dell'applicazione."""
    icon_path = get_asset_path("assets/app.ico")

    if Path(icon_path).exists():
        return icon_path
    return None


def setup_logging(name: str = "BotTS", log_file: str | None = None) -> logging.Logger:
    """
    Configura il sistema di logging.

    Args:
        name: Nome del logger
        log_file: Percorso opzionale per file di log

    Returns:
        Logger configurato
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (opzionale)
        if log_file:
            try:
                file_handler = logging.FileHandler(log_file, encoding="utf-8")
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                logger.warning(f"Impossibile creare file di log: {e}")

    return logger


def format_timestamp(dt: datetime | None = None) -> str:
    """
    Formatta un timestamp per la visualizzazione.

    Args:
        dt: Datetime da formattare (default: now)

    Returns:
        Stringa formattata
    """
    if dt is None:
        dt = datetime.now(UTC).astimezone()
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def get_months_list() -> list[str]:
    """Restituisce la lista dei mesi in italiano."""
    return [
        "Gennaio",
        "Febbraio",
        "Marzo",
        "Aprile",
        "Maggio",
        "Giugno",
        "Luglio",
        "Agosto",
        "Settembre",
        "Ottobre",
        "Novembre",
        "Dicembre",
    ]


def get_years_list(start_offset: int = -2, end_offset: int = 2) -> list[str]:
    """
    Restituisce una lista di anni intorno a quello corrente.

    Args:
        start_offset: Offset dall'anno corrente per l'inizio.
        end_offset: Offset dall'anno corrente per la fine.

    Returns:
        Lista di anni come stringhe.
    """
    current_year = datetime.now(UTC).astimezone().year
    return [str(year) for year in range(current_year + start_offset, current_year + end_offset + 1)]


def is_windows() -> bool:
    """Verifica se il sistema operativo corrente è Windows."""
    return sys.platform.startswith("win")


def open_folder(path: str) -> bool:
    """
    Apre una cartella nel file manager del sistema operativo.

    Args:
        path: Percorso della cartella da aprire.

    Returns:
        bool: True se la cartella è stata aperta correttamente, False altrimenti.
    """
    import subprocess

    path_obj = Path(path)
    if not path_obj.exists():
        return False

    try:
        if is_windows():
            os.startfile(str(path_obj))  # noqa: S606
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path_obj)], check=False)
        else:
            subprocess.run(["xdg-open", str(path_obj)], check=False)
        return True
    except Exception:
        return False


def safe_str(value: Any, default: str = "") -> str:
    """
    Esegue una conversione sicura a stringa gestendo i valori None.
    """
    return str(value) if value is not None else default


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Tronca una stringa se supera la lunghezza specificata.
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def sanitize_filename(filename: str) -> str:
    """
    Sanitizza una stringa per renderla sicura come nome file (previene Path Traversal).
    """
    if not filename:
        return "unnamed_file"

    filename = filename.replace("\0", "")
    # Whitelist: Alfanumerici, underscore, trattino, punto, parentesi, spazi.
    safe_filename = re.sub(r"[^a-zA-Z0-9_\-\.\(\)\[\] ]", "_", filename)
    safe_filename = re.sub(r"_+", "_", safe_filename)
    safe_filename = re.sub(r"\.+", ".", safe_filename).strip(" .")

    return safe_filename or "unnamed_file"


def cleanup_chrome_temp_files(directory: Path | str) -> list[str]:
    """
    Rimuove file da 0 KB nella directory (residui di download Selenium falliti).
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []

    removed = []
    try:
        for f in dir_path.iterdir():
            if f.is_file() and f.stat().st_size == 0:
                with suppress(Exception):
                    f.unlink()
                    removed.append(f.name)
    except Exception as e:
        logging.getLogger(__name__).warning(f"Error during temp cleanup: {e}")
    return removed


def cleanup_bot_processes() -> None:
    """
    Termina forzatamente le istanze 'zombie' di Chrome e Chromedriver legate all'applicazione.
    Rimuove i file di lock del profilo per prevenire errori di sessione (SessionNotCreated).
    """
    import psutil

    from src.core.config_manager import CONFIG_DIR
    from src.core.constants import BrowserConfig

    logger = logging.getLogger("Cleanup")

    # 1. Terminazione Chromedriver
    for proc in psutil.process_iter(["name"]):
        with suppress(Exception):
            if proc.info["name"] == "chromedriver.exe":
                proc.kill()

    # 2. Terminazione Chrome (Solo se utilizza il profilo dedicato di SyncroJob)
    profile_dir = "chrome_profile"
    for proc in psutil.process_iter(["name", "cmdline"]):
        with suppress(Exception):
            if proc.info["name"] == "chrome.exe":
                cmdline = " ".join(proc.info["cmdline"] or [])
                if profile_dir in cmdline.lower() and "syncrojob" in cmdline.lower():
                    proc.kill()

    # 3. Rimozione file di lock nel profilo
    profile_path = CONFIG_DIR / "data" / BrowserConfig.CACHE_DIR_NAME
    lock_files = ["SingletonLock", "SingletonSocket", "SingletonCookie"]

    if profile_path.exists():
        for lock_file in lock_files:
            f_path = profile_path / lock_file
            if f_path.exists():
                with suppress(Exception):
                    f_path.unlink()
                    logger.info(f"Removed stale lock file: {lock_file}")


def get_colored_icon(icon_path: str, color: str = "#000000") -> Any:
    """
    Applica un colore personalizzato a un'icona SVG tramite QPainter.
    """
    from PyQt6.QtGui import QColor, QIcon, QImage, QPainter, QPixmap

    if not Path(icon_path).exists():
        return QIcon()

    image = QImage(icon_path)
    if image.isNull():
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            return QIcon()
        image = pixmap.toImage()

    painter = QPainter(image)
    try:
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(image.rect(), QColor(color))
    finally:
        painter.end()

    return QIcon(QPixmap.fromImage(image))
