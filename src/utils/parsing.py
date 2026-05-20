"""
SyncroJob - Parsing Utils
Utility per il parsing robusto di valute e numeri.
"""

import re
from contextlib import suppress


def parse_currency(value: float | int | str | None) -> float:
    """
    Converte una stringa o numero in float, gestendo formati Italiani e Internazionali.
    Versione Enterprise V5.1: Gestione robusta di rumore e notazione scientifica.
    """
    # 0. Gestione rapida tipi numerici e nulli
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)

    s_raw = str(value).strip()
    if not s_raw or s_raw.lower() == "nan":
        return 0.0

    # 1. Pulizia e Segno
    s = s_raw.replace("\x00", "").replace("\u200b", "")
    is_negative = _is_value_negative(s)

    # 2. Validazione integrità(whitelist termini permessi)
    # 3. Notazione scientifica
    # 4. Estrazione parte numerica standard
    res = 0.0
    if _validate_currency_integrity(s):
        sci_val = _try_parse_scientific(s)
        res = sci_val if sci_val is not None else _parse_standard_currency(s, is_negative)

    return res


def _parse_standard_currency(s: str, is_negative: bool) -> float:
    """Helper per il parsing della valuta standard (non scientifica)."""
    # Estrazione cifre e separatori
    s_num = re.sub(r"[^0-9,.]", "", s)
    if not any(c.isdigit() for c in s_num):
        return 0.0

    # Gestione separatori consecutivi
    s_num = re.sub(r"[,]{2,}", ",", s_num)
    s_num = re.sub(r"[.]{2,}", ".", s_num)

    try:
        val = _smart_convert(s_num)
    except (ValueError, IndexError):
        return 0.0

    return -val if is_negative else val


def _is_value_negative(s: str) -> bool:
    """Rileva se il valore indica un numero negativo."""
    has_explicit_neg = "-" in s and not re.search(r"[eE]-", s)
    return has_explicit_neg or ("(" in s and ")" in s)


def _validate_currency_integrity(s: str) -> bool:
    """Verifica che il testo alfabetico residuo sia rumore ammesso."""
    if not re.search(r"[a-zA-Z]", s):
        return True

    # Notazione scientifica semplice
    if re.search(r"^-?\d*[.,]?\d+[eE][-+]?\d+$", s.replace(" ", "")):
        return True

    # Whitelist
    allowed = r"(?i)\b(Euro|EUR|Dollari|USD|Sterline|GBP|JPY|CHF|Prezzo|Totale|Importo|ODA|POS|Valuta|Netto|Lordo|Sconto|Circa)\b"
    clean_check = re.sub(allowed, "", s)
    noise = re.sub(r"[0-9,.\s$ %\-+:]", "", clean_check)
    return not (noise and re.search(r"[a-zA-Z]", noise))


def _try_parse_scientific(s: str) -> float | None:
    """Tenta il parsing della notazione scientifica."""
    match = re.search(r"[-+]?\d*\.?\d+[eE][-+]?\d+", s.replace(",", "."))
    if match:
        with suppress(ValueError):
            return float(match.group(0))
    return None


def _smart_convert(s: str) -> float:
    """Logica di conversione basata sulla posizione dei separatori."""
    # Caso 1: Entrambi i separatori presenti (es. 1.234,56 o 1,234.56)
    if "," in s and "." in s:
        if s.find(".") < s.find(","):
            return float(s.replace(".", "").replace(",", "."))
        return float(s.replace(",", ""))

    # Caso 2: Solo virgola (es. 1234,56)
    if "," in s:
        return float(s.replace(",", "."))

    # Caso 3: Solo punto (es. 1.234 o 10.50 o 1.234.567)
    # Rileviamo se il punto è migliaia (3 cifre dopo) o decimale
    parts = s.split(".")
    it_thousands_len = 3

    # Se ci sono più di 2 parti, sono sicuramente migliaia (es. 1.234.567)
    if len(parts) > 2:  # noqa: PLR2004
        return float(s.replace(".", ""))

    # Se ci sono 2 parti (un solo punto), verifichiamo se sono migliaia o decimali
    if len(parts) == 2 and len(parts[-1]) == it_thousands_len:  # noqa: PLR2004
        return float(s.replace(".", ""))

    return float(s)
