"""
SyncroJob - Utility Helpers
Funzioni di utilità generali.
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
    Restituisce una lista di anni.

    Args:
        start_offset: Offset dall'anno corrente per l'inizio
        end_offset: Offset dall'anno corrente per la fine

    Returns:
        Lista di anni come stringhe
    """
    current_year = datetime.now(UTC).astimezone().year
    return [str(year) for year in range(current_year + start_offset, current_year + end_offset + 1)]


def is_windows() -> bool:
    """Verifica se il sistema operativo è Windows."""
    return sys.platform.startswith("win")


def open_folder(path: str) -> bool:
    """
    Apre una cartella nel file manager.

    Args:
        path: Percorso della cartella

    Returns:
        True se successo, False altrimenti
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
    Conversione sicura a stringa.

    Args:
        value: Valore da convertire
        default: Valore default se None

    Returns:
        Stringa
    """
    if value is None:
        return default
    return str(value)


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Tronca una stringa alla lunghezza massima.

    Args:
        text: Testo da troncare
        max_length: Lunghezza massima
        suffix: Suffisso da aggiungere se troncato

    Returns:
        Stringa troncata
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def sanitize_filename(filename: str) -> str:
    """
    Sanitizes a string to be safe for use as a filename.
    Removes path traversal characters and other unsafe symbols.

    Args:
        filename: The input string (e.g., user input).

    Returns:
        A safe filename string.
    """
    if not filename:
        return "unnamed_file"

    # 1. Strip null bytes
    filename = filename.replace("\0", "")

    # 2. Replace forbidden characters with underscore
    # We use a whitelist approach for maximum security:
    # Alphanumeric, underscore, hyphen, dot, parenthesis, square brackets and spaces.
    # Excludes: / \ : * ? " < > |
    safe_filename = re.sub(r"[^a-zA-Z0-9_\-\.\(\)\[\] ]", "_", filename)

    # 3. Collapse multiple underscores
    safe_filename = re.sub(r"_+", "_", safe_filename)

    # 4. Collapse multiple dots and trim (prevent ".." traversal patterns)
    safe_filename = re.sub(r"\.+", ".", safe_filename).strip(" .")

    # 6. Ensure not empty after sanitization
    if not safe_filename:
        return "unnamed_file"

    return safe_filename


def cleanup_chrome_temp_files(directory: Path | str) -> list[str]:
    """
    Rimuove tutti i file da 0 KB (residui di download o placeholder) nella directory.

    Returns:
        Lista dei nomi dei file rimossi.
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []

    removed = []
    try:
        for f in dir_path.iterdir():
            if f.is_file() and f.stat().st_size == 0:
                try:
                    f.unlink()
                    removed.append(f.name)
                except Exception as e:
                    # Se non riusciamo a cancellare un file specifico (es. locked), passiamo al prossimo
                    import logging

                    logging.getLogger(__name__).warning(f"Impossibile eliminare {f}: {e}")
                    continue
    except Exception:
        # Se la directory non è leggibile o iterabile, ritorniamo quello che abbiamo trovato finora
        with suppress(Exception):
            pass
    return removed


def get_colored_icon(icon_path: str, color: str = "#000000") -> Any:
    """
    Carica un'icona SVG e ne cambia il colore in modo sicuro.
    Usa QImage per evitare conflitti di pittura su QPixmap.
    """
    from PyQt6.QtGui import QColor, QIcon, QImage, QPainter, QPixmap

    if not Path(icon_path).exists():
        return QIcon()

    # Tentativo caricamento diretto
    image = QImage(icon_path)
    if image.isNull():
        # Fallback via pixmap per SVG complessi
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            return QIcon()
        image = pixmap.toImage()

    # Crea un pittore per ricolorare l'immagine (software buffer sicuro)
    painter = QPainter(image)
    try:
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(image.rect(), QColor(color))
    finally:
        painter.end()

    return QIcon(QPixmap.fromImage(image))
