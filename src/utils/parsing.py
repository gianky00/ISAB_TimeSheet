"""
SyncroJob - Parsing Utils
Utility per il parsing robusto di valute e numeri.
"""

import re


def parse_currency(value: float | int | str | None) -> float:
    """
    Converte una stringa o numero in float, gestendo formati Italiani e Internazionali.
    Versione Enterprise V5: Bilanciamento perfetto tra tolleranza e precisione.
    """
    if value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    s_raw = str(value).strip()
    if not s_raw or s_raw.lower() == "nan":
        return 0.0

    # 1. Pulizia caratteri non stampabili e nulli
    s = s_raw.replace("\x00", "").replace("\u200b", "")

    # 2. Rilevamento segno negativo (ovunque nella stringa)
    is_negative = "-" in s or ("(" in s and ")" in s)

    # 3. Estrazione parte numerica e separatori (inclusa 'e' per scientifica)
    # Rimuoviamo tutto ciò che non è numero, punto, virgola o 'e'
    s = re.sub(r"[^0-9,.eE]", "", s)

    if not any(c.isdigit() for c in s):
        return 0.0

    # 4. Gestione separatori consecutivi
    s = re.sub(r"[,]{2,}", ",", s)
    s = re.sub(r"[.]{2,}", ".", s)

    # 5. Conversione intelligente
    try:
        val = _smart_convert(s)
    except (ValueError, IndexError):
        return 0.0
    else:
        return -val if is_negative else val


def _smart_convert(s: str) -> float:
    """Determina il formato e converte in float."""
    # Se la stringa segue la notazione scientifica pura (es. 1.23e2)
    if "e" in s.lower() and s.count(".") <= 1 and "," not in s:
        return float(s)

    has_comma = "," in s
    has_dot = "." in s

    # Caso: Entrambi (1.234,56 o 1,234.56)
    if has_comma and has_dot:
        return _convert_both_separators(s)

    # Caso: Solo virgole
    if has_comma:
        return float(s.replace(",", "")) if s.count(",") > 1 else float(s.replace(",", "."))

    # Caso: Solo punti
    if has_dot:
        return _convert_only_dots(s)

    return float(s)


def _convert_both_separators(s: str) -> float:
    """Helper per stringhe con sia virgola che punto."""
    last_comma = s.rfind(",")
    last_dot = s.rfind(".")
    if last_comma > last_dot:
        # IT Style (1.234,56)
        return float(s.replace(".", "").replace(",", "."))
    # US Style (1,234.56)
    return float(s.replace(",", ""))


def _convert_only_dots(s: str) -> float:
    """Helper per stringhe con solo punti."""
    if s.count(".") > 1:
        return float(s.replace(".", ""))

    # Singolo punto: 1.234 (IT migliaia) o 10.50 (Decimale)
    parts = s.split(".")
    it_thousands_len = 3
    if len(parts[1]) == it_thousands_len and parts[0]:
        return float(s.replace(".", ""))
    return float(s)
