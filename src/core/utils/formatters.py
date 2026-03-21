"""
SyncroJob - Core Formatters
Funzioni di formattazione agnostiche rispetto alla GUI, usate per il processing dei dati.
"""

from contextlib import suppress
from datetime import UTC, datetime
from typing import Any


def format_date_it(value: Any) -> str:
    """
    Converte stringa ISO YYYY-MM-DD o datetime in DD/MM/YYYY.
    """
    if not value:
        return ""
    with suppress(Exception):
        if isinstance(value, str):
            # Tenta vari formati comuni
            for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"):
                with suppress(ValueError):
                    dt = datetime.strptime(value.split(" ")[0], fmt).replace(tzinfo=UTC)
                    return dt.strftime("%d/%m/%Y")
            return value  # Fallback se non è una data riconosciuta
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y")
        if isinstance(value, (float, int)):
            return datetime.fromtimestamp(value, tz=UTC).strftime("%d/%m/%Y")
    return str(value)
