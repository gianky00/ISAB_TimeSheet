"""
SyncroJob - Utility per Date
Funzioni centralizzate per parsing, formattazione e calcoli su date.
"""

from datetime import date, datetime, timedelta
from typing import Optional, Tuple

# Formati di data comunemente usati nell'applicazione
DATE_FORMATS = [
    "%Y-%m-%d",      # ISO format (2024-01-15)
    "%d/%m/%Y",      # Italian format (15/01/2024)
    "%d\\%m\\%Y",    # Escaped backslash format
    "%Y-%m-%d %H:%M:%S",  # ISO with time
    "%d/%m/%Y %H:%M:%S",  # Italian with time
]


def parse_date_flexible(
    date_str: Optional[str],
    formats: Optional[list[str]] = None
) -> Optional[date]:
    """
    Tenta di parsare una stringa data usando più formati.

    Args:
        date_str: La stringa da parsare
        formats: Lista di formati da provare (default: DATE_FORMATS)

    Returns:
        date object se il parsing ha successo, None altrimenti
    """
    if not date_str or date_str in ("None", "-", ""):
        return None

    formats = formats or DATE_FORMATS

    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue

    return None


def parse_datetime_flexible(
    date_str: Optional[str],
    formats: Optional[list[str]] = None
) -> Optional[datetime]:
    """
    Tenta di parsare una stringa datetime usando più formati.

    Args:
        date_str: La stringa da parsare
        formats: Lista di formati da provare (default: DATE_FORMATS)

    Returns:
        datetime object se il parsing ha successo, None altrimenti
    """
    if not date_str or date_str in ("None", "-", ""):
        return None

    formats = formats or DATE_FORMATS

    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue

    return None


def format_date_it(
    date_obj: Optional[date],
    include_time: bool = False
) -> str:
    """
    Formatta una data nel formato italiano.

    Args:
        date_obj: La data da formattare
        include_time: Se True, include anche l'orario (se datetime)

    Returns:
        Stringa formattata o "-" se None
    """
    if date_obj is None:
        return "-"

    if include_time and isinstance(date_obj, datetime):
        return date_obj.strftime("%d/%m/%Y %H:%M:%S")

    return date_obj.strftime("%d/%m/%Y")


def format_date_iso(date_obj: Optional[date]) -> str:
    """
    Formatta una data nel formato ISO (YYYY-MM-DD).

    Args:
        date_obj: La data da formattare

    Returns:
        Stringa formattata o "-" se None
    """
    if date_obj is None:
        return "-"

    return date_obj.strftime("%Y-%m-%d")


def calculate_days_diff(
    date_obj: Optional[date],
    from_date: Optional[date] = None
) -> Optional[int]:
    """
    Calcola la differenza in giorni tra due date.

    Args:
        date_obj: La data target
        from_date: La data di riferimento (default: oggi)

    Returns:
        Numero di giorni di differenza, None se date_obj è None
    """
    if date_obj is None:
        return None

    from_date = from_date or date.today()
    return (from_date - date_obj).days


def get_status_by_days(
    days: Optional[int],
    thresholds: Tuple[int, int] = (20, 30)
) -> Tuple[str, str]:
    """
    Determina lo status e il colore in base ai giorni trascorsi.

    Args:
        days: Numero di giorni
        thresholds: Tuple (warning_threshold, expired_threshold)

    Returns:
        Tuple (status_type, color_hex)
    """
    if days is None:
        return ("unknown", "#6c757d")

    warning_threshold, expired_threshold = thresholds

    if days <= warning_threshold:
        return ("ok", "#198754")
    elif days <= expired_threshold:
        return ("warning", "#fd7e14")
    else:
        return ("expired", "#dc3545")


def format_days_ago(days: Optional[int]) -> str:
    """
    Formatta il numero di giorni in una stringa leggibile.

    Args:
        days: Numero di giorni

    Returns:
        Stringa tipo "5 giorni fa" o "-" se None
    """
    if days is None:
        return "-"

    if days == 0:
        return "Oggi"
    elif days == 1:
        return "Ieri"
    else:
        return f"{days} giorni fa"


def get_date_range(
    days_back: int,
    from_date: Optional[date] = None
) -> Tuple[date, date]:
    """
    Calcola un range di date.

    Args:
        days_back: Numero di giorni indietro
        from_date: Data di fine range (default: oggi)

    Returns:
        Tuple (start_date, end_date)
    """
    end_date = from_date or date.today()
    start_date = end_date - timedelta(days=days_back)
    return (start_date, end_date)


def format_datetime_for_filename(dt: Optional[datetime] = None) -> str:
    """
    Formatta datetime per uso in nomi file (senza caratteri speciali).

    Args:
        dt: Datetime da formattare (default: now)

    Returns:
        Stringa tipo "15-01-2024_14-30"
    """
    dt = dt or datetime.now()
    return dt.strftime("%d-%m-%Y_%H-%M")


def is_same_day(dt1: datetime, dt2: datetime) -> bool:
    """
    Verifica se due datetime sono nello stesso giorno.

    Args:
        dt1: Prima datetime
        dt2: Seconda datetime

    Returns:
        True se stesso giorno
    """
    return dt1.date() == dt2.date()


def get_month_name_it(month: int, full: bool = False) -> str:
    """
    Ottiene il nome del mese in italiano.

    Args:
        month: Numero del mese (1-12)
        full: Se True, restituisce nome completo

    Returns:
        Nome del mese
    """
    from src.gui.styles.constants import MONTHS_IT, MONTHS_IT_FULL

    if not 1 <= month <= 12:
        return ""

    return MONTHS_IT_FULL[month - 1] if full else MONTHS_IT[month - 1]
