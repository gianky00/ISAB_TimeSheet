"""
Bot TS - Utility Helpers
Funzioni di utilità generali.
"""
import os
import sys
import logging
import re
from datetime import datetime
from typing import Optional, List


def get_app_icon_path() -> Optional[str]:
    """Restituisce il percorso dell'icona dell'applicazione."""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    icon_path = os.path.join(base_path, "assets", "app.ico")
    
    if os.path.exists(icon_path):
        return icon_path
    return None


def setup_logging(name: str = "BotTS", log_file: Optional[str] = None) -> logging.Logger:
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
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (opzionale)
        if log_file:
            try:
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                logger.warning(f"Impossibile creare file di log: {e}")
    
    return logger


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Formatta un timestamp per la visualizzazione.
    
    Args:
        dt: Datetime da formattare (default: now)
    
    Returns:
        Stringa formattata
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def get_months_list() -> List[str]:
    """Restituisce la lista dei mesi in italiano."""
    return [
        "Gennaio", "Febbraio", "Marzo", "Aprile",
        "Maggio", "Giugno", "Luglio", "Agosto",
        "Settembre", "Ottobre", "Novembre", "Dicembre"
    ]


def get_years_list(start_offset: int = -2, end_offset: int = 2) -> List[str]:
    """
    Restituisce una lista di anni.
    
    Args:
        start_offset: Offset dall'anno corrente per l'inizio
        end_offset: Offset dall'anno corrente per la fine
    
    Returns:
        Lista di anni come stringhe
    """
    current_year = datetime.now().year
    return [str(year) for year in range(current_year + start_offset, current_year + end_offset + 1)]


def is_windows() -> bool:
    """Verifica se il sistema operativo è Windows."""
    return sys.platform.startswith('win')


def open_folder(path: str) -> bool:
    """
    Apre una cartella nel file manager.
    
    Args:
        path: Percorso della cartella
    
    Returns:
        True se successo, False altrimenti
    """
    import subprocess
    
    if not os.path.exists(path):
        return False
    
    try:
        if is_windows():
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.run(['open', path])
        else:
            subprocess.run(['xdg-open', path])
        return True
    except Exception:
        return False


def safe_str(value, default: str = "") -> str:
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
    
    text = str(text)
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


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
    filename = str(filename).replace('\0', '')
    
    # 2. Replace forbidden characters with underscore
    # We use a whitelist approach for maximum security: 
    # Alphanumeric, underscore, hyphen, dot, space, parenthesis, square brackets.
    # Excludes: / \ : * ? " < > |
    safe_filename = re.sub(r'[^a-zA-Z0-9_\-\.\(\)\[\] ]', '_', filename)
    
    # 3. Collapse multiple underscores
    safe_filename = re.sub(r'_+', '_', safe_filename)

    # 4. Collapse multiple dots (prevent ".." traversal patterns)
    safe_filename = re.sub(r'\.+', '.', safe_filename)
    
    # 5. Trim spaces and dots from ends (Windows doesn't like them)
    safe_filename = safe_filename.strip(' .')
    
    # 6. Ensure not empty after sanitization
    if not safe_filename:
        return "unnamed_file"
        
    return safe_filename
