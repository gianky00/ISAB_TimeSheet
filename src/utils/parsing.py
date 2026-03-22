"""
SyncroJob - Parsing Utils
Utility per il parsing robusto di valute e numeri.
"""

import re
from typing import Any


def parse_currency(value: Any) -> float:
    """
    Converte una stringa o numero in float, gestendo formati Italiani e Internazionali.
    """
    if value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()
    if not s or s.lower() == "nan":
        return 0.0

    # 1. Pulizia e Normalizzazione
    s, is_negative = _normalize_string(s)

    # 2. Rilevamento e gestione separatori
    s = _process_separators(s)

    try:
        val = float(s)
        return -val if is_negative else val
    except ValueError:
        return 0.0


def _normalize_string(s: str) -> tuple[str, bool]:
    """Rimuove simboli, testo inutile e gestisce il segno negativo."""
    # Gestione segno negativo (cerca il meno prima di pulire tutto)
    is_negative = False
    if "-" in s:
        is_negative = True
        s = s.replace("-", "").strip()

    # Rimuovi tutto ciò che non è numero, punto o virgola
    # Manteniamo i separatori per il processing successivo
    s = re.sub(r"[^0-9,.]", "", s).strip()

    return s, is_negative


def _process_separators(s: str) -> str:
    """Gestisce la logica di conversione dei separatori (punti e virgole)."""
    has_comma = "," in s
    has_dot = "." in s

    if has_comma and has_dot:
        return _handle_mixed_separators(s)
    if has_comma:
        return s.replace(",", ".")
    if has_dot:
        return _handle_single_dot(s)

    return s


def _handle_mixed_separators(s: str) -> str:
    """Gestisce stringhe con sia punto che virgola (es. 1.234,56 o 1,234.56)."""
    last_comma = s.rfind(",")
    last_dot = s.rfind(".")

    if last_comma > last_dot:
        # IT: Punti sono migliaia, virgola è decimale
        return s.replace(".", "").replace(",", ".")

    # US: Virgole sono migliaia, punto è decimale
    return s.replace(",", "")


def _handle_single_dot(s: str) -> str:
    """Gestisce stringhe con solo punti."""
    if s.count(".") > 1:
        # "1.234.567" -> Sicuramente migliaia
        return s.replace(".", "")

    # Un solo punto: trattalo come migliaia se seguito da esattamente 3 cifre
    parts = s.split(".")
    if len(parts) > 1 and len(parts[1]) == 3:
        return s.replace(".", "")

    return s
