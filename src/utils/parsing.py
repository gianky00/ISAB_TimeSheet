"""
SyncroJob - Parsing Utils
Utility per il parsing robusto di valute e numeri.
"""

import re


def parse_currency(value) -> float:
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
    # Rimuovi simbolo valuta e testo "Euro"
    s = s.replace("€", "")
    s = re.sub(r"(?i)euro", "", s).strip()

    # Gestione segno negativo
    is_negative = False
    if s.startswith("-") or " - " in s or s.endswith("-"):
        is_negative = True
        s = s.replace("-", "").strip()

    # Rimuovi caratteri invisibili
    s = "".join(c for c in s if c.isprintable())

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

    # Un solo punto: ambiguo se ha 3 cifre dopo (es. "1.234")
    # Manteniamo la logica originale: se non sono 3 cifre, è decimale.
    # Se sono 3 cifre, per ora lo lasciamo così (float standard).
    parts = s.split(".")
    if len(parts) > 1 and len(parts[1]) == 3:
        # Qui potremmo decidere se trattarlo come migliaia,
        # ma l'originale faceva 'pass' lasciandolo come float.
        pass

    return s


if __name__ == "__main__":
    # Test cases
    tests = [
        ("1.234,56", 1234.56),
        ("1,234.56", 1234.56),
        ("508,83", 508.83),
        ("508.83", 508.83),
        (
            "1.000",
            1000.0,
        ),  # Ambiguo, in IT solitamente 1000 se input manuale, ma 1.0 se float. Qui assumiamo float standard se ambiguo? No, parse logic sopra lascia il punto se != 3 cifre.
        # "1.000" ha 3 cifre. Se lasciamo punto -> 1.0.
        # Se rimuoviamo punto -> 1000.
        # Vediamo output script.
        ("€ 50,00", 50.0),
        (50.5, 50.5),
    ]
    for i, o in tests:
        res = parse_currency(i)
        print(f"In: {i!r} -> Out: {res} ({'OK' if res == o else 'FAIL expected ' + str(o)})")
