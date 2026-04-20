"""
SyncroJob - Parsing Utils
Utility per il parsing robusto di valute e numeri.
"""

import re
from contextlib import suppress


def parse_currency(value: float | int | str | None) -> float:  # noqa: PLR0911
    """
    Converte una stringa o numero in float, gestendo formati Italiani e Internazionali.
    Versione Enterprise V5.1: Gestione robusta di rumore e notazione scientifica.
    """
    if value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    s_raw = str(value).strip()
    if not s_raw or s_raw.lower() == "nan":
        return 0.0

    # 1. Pulizia caratteri nulli/invisibili
    s = s_raw.replace("\x00", "").replace("\u200b", "")

    # 2. Rilevamento segno negativo (ovunque nella stringa)
    # Nota: Escludiamo il trattino se fa parte della notazione scientifica (es. e-2)
    has_explicit_neg = "-" in s and not re.search(r"[eE]-", s)
    is_negative = has_explicit_neg or ("(" in s and ")" in s)

    # 3. Validazione integrità: se ci sono lettere, devono essere simboli o parole chiave permesse
    if re.search(r"[a-zA-Z]", s):
        # Caso 1: Notazione scientifica (es. 1.23e-2)
        if re.search(r"^-?\d*\.?\d+[eE][-+]?\d+$", s.replace(" ", "")):
            pass  # Valido
        else:
            # Caso 2: Rimuoviamo simboli e parole chiave comuni (whitelist)
            # Permettiamo: EUR, Euro, USD, Dollari, GBP, Sterline, JPY, CHF, Prezzo, Totale, Importo, ODA, POS, Valuta, Netto, Lordo, Sconto, Circa
            allowed_terms = r"(?i)\b(Euro|EUR|Dollari|USD|Sterline|GBP|JPY|CHF|Prezzo|Totale|Importo|ODA|POS|Valuta|Netto|Lordo|Sconto|Circa)\b"
            clean_check = re.sub(allowed_terms, "", s)

            noise = re.sub(r"[0-9,.\s€$£%\-+:]", "", clean_check)
            if noise and re.search(r"[a-zA-Z]", noise):
                # Se rimane ancora testo alfabetico sconosciuto, è probabilmente rumore invalido
                return 0.0

    # 4. Estrazione parte numerica pulita
    # Se è notazione scientifica, la isoliamo
    sci_match = re.search(r"[-+]?\d*\.?\d+[eE][-+]?\d+", s.replace(",", "."))
    if sci_match:
        with suppress(ValueError):
            return float(sci_match.group(0))

    # Altrimenti procediamo con il parsing valuta standard
    s = re.sub(r"[^0-9,.]", "", s)
    if not any(c.isdigit() for c in s):
        return 0.0

    # 5. Gestione separatori consecutivi
    s = re.sub(r"[,]{2,}", ",", s)
    s = re.sub(r"[.]{2,}", ".", s)

    # 6. Conversione intelligente
    try:
        val = _smart_convert(s)
    except (ValueError, IndexError):
        return 0.0
    else:
        return -val if is_negative else val


def _smart_convert(s: str) -> float:
    """Determina il formato e converte in float."""
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
