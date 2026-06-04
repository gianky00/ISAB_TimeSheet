"""SyncroJob - Utility per Date.

Funzioni centralizzate per parsing, formattazione e calcoli su date.
"""

from datetime import UTC, date, datetime, timedelta
from typing import Final

# Formati di data comunemente usati nell'applicazione
DATE_FORMATS: Final[list[str]] = [
    "%Y-%m-%d",  # ISO format (2024-01-15)
    "%d/%m/%Y",  # Italian format (15/01/2024)
    "%d\\%m\\%Y",  # Escaped backslash format
    "%Y-%m-%d %H:%M:%S",  # ISO with time
    "%d/%m/%Y %H:%M:%S",  # Italian with time
]

# MESI ITALIANI (usato in grafici e report)
MONTHS_IT: Final[list[str]] = [
    "Gen",
    "Feb",
    "Mar",
    "Apr",
    "Mag",
    "Giu",
    "Lug",
    "Ago",
    "Set",
    "Ott",
    "Nov",
    "Dic",
]

MONTHS_IT_FULL: Final[list[str]] = [
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

MAX_MONTHS: Final[int] = 12


def parse_date_flexible(date_str: str | None, formats: list[str] | None = None) -> date | None:
    """Tenta di parsare una stringa data usando più formati.

    Args:
      date_str: La stringa da parsare
      formats: Lista di formati da provare (default: DATE_FORMATS)

    Returns:
      date object se il parsing ha successo, None altrimenti
    """
    if not date_str or date_str in ("None", "-", ""):
        return None

    formats_to_try = formats or DATE_FORMATS

    for fmt in formats_to_try:
        try:
            return datetime.strptime(date_str.strip(), fmt).replace(tzinfo=UTC).date()
        except ValueError:
            continue

    return None


def parse_datetime_flexible(date_str: str | None, formats: list[str] | None = None) -> datetime | None:
    """Tenta di parsare una stringa datetime usando più formati.

    Args:
      date_str: La stringa da parsare
      formats: Lista di formati da provare (default: DATE_FORMATS)

    Returns:
      datetime object se il parsing ha successo, None altrimenti
    """
    if not date_str or date_str in ("None", "-", ""):
        return None

    formats_to_try = formats or DATE_FORMATS

    for fmt in formats_to_try:
        try:
            return datetime.strptime(date_str.strip(), fmt).replace(tzinfo=UTC)
        except ValueError:
            continue

    return None


def format_date_it(date_obj: date | None, include_time: bool = False) -> str:
    """Formatta una data nel formato italiano.

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


def format_date_iso(date_obj: date | None) -> str:
    """Formatta una data nel formato ISO (YYYY-MM-DD).

    Args:
      date_obj: La data da formattare

    Returns:
      Stringa formattata o "-" se None
    """
    if date_obj is None:
        return "-"

    return date_obj.strftime("%Y-%m-%d")


def calculate_days_diff(date_obj: date | None, from_date: date | None = None) -> int | None:
    """Calcola la differenza in giorni tra due date.

    Args:
      date_obj: La data target
      from_date: La data di riferimento (default: oggi)

    Returns:
      Numero di giorni di differenza, None se date_obj  None
    """
    if date_obj is None:
        return None

    # Use aware datetime for calculation
    now = datetime.now(UTC).date()
    ref_date = from_date or now
    return (ref_date - date_obj).days


def get_status_by_days(days: int | None, thresholds: tuple[int, int] | None = None) -> tuple[str, str]:
    """Determina lo status e il colore in base ai giorni trascorsi.

    Args:
      days: Numero di giorni
      thresholds: Tuple opzionale (warning_threshold, expired_threshold)

    Returns:
      Tuple (status_type, color_hex)
    """
    # Importazione lazy per evitare dipendenze circolari tra core/utils e gui/styles
    from src.application.services.constants import THRESHOLD_DAYS  # noqa: PLC0415
    from src.gui.styles.constants import STATUS_COLORS  # noqa: PLC0415

    if days is None:
        return ("unknown", STATUS_COLORS["excluded"])

    if thresholds:
        warning_threshold, expired_threshold = thresholds
    else:
        warning_threshold = THRESHOLD_DAYS["warning"]
        expired_threshold = THRESHOLD_DAYS["expired"]

    if days <= warning_threshold:
        return ("ok", STATUS_COLORS["ok"])
    if days <= expired_threshold:
        return ("warning", STATUS_COLORS["warning"])
    return ("expired", STATUS_COLORS["expired"])


def format_days_ago(days: int | None) -> str:
    """Formatta il numero di giorni in una stringa leggibile.

    Args:
      days: Numero di giorni

    Returns:
      Stringa tipo "5 giorni fa" o "-" se None
    """
    if days is None:
        return "-"

    if days == 0:
        return "Oggi"
    if days == 1:
        return "Ieri"
    return f"{days} giorni fa"


def get_date_range(days_back: int, from_date: date | None = None) -> tuple[date, date]:
    """Calcola un range di date.

    Args:
      days_back: Numero di giorni indietro
      from_date: Data di fine range (default: oggi)

    Returns:
      Tuple (start_date, end_date)
    """
    now = datetime.now(UTC).date()
    end_date = from_date or now
    start_date = end_date - timedelta(days=days_back)
    return (start_date, end_date)


def format_datetime_for_filename(dt: datetime | None = None) -> str:
    """Formatta datetime per uso in nomi file (senza caratteri speciali).

    Args:
      dt: Datetime da formattare (default: now)

    Returns:
      Stringa tipo "15-01-2024_14-30"
    """
    return (dt or datetime.now(UTC)).strftime("%d-%m-%Y_%H-%M")


def is_same_day(dt1: datetime, dt2: datetime) -> bool:
    """Verifica se due datetime sono nello stesso giorno.

    Args:
      dt1: Prima datetime
      dt2: Seconda datetime

    Returns:
      True se stesso giorno
    """
    return dt1.date() == dt2.date()


def get_month_name_it(month: int, full: bool = False) -> str:
    """Ottiene il nome del mese in italiano.

    Args:
      month: Numero del mese (1-12)
      full: Se True, restituisce nome completo

    Returns:
      Nome del mese
    """
    if not 1 <= month <= MAX_MONTHS:
        return ""

    return (MONTHS_IT_FULL if full else MONTHS_IT)[month - 1]
