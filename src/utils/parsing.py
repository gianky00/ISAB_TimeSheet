"""
Bot TS - Parsing Utils
Utility per il parsing robusto di valute e numeri.
"""
import re

def parse_currency(value) -> float:
    """
    Converte una stringa o numero in float, gestendo formati Italiani e Internazionali.

    Esempi gestiti:
    - "1.234,56" -> 1234.56 (IT)
    - "1,234.56" -> 1234.56 (US)
    - "1234.56" -> 1234.56 (US/Std)
    - "1234,56" -> 1234.56 (IT)
    - "€ 1.234,56" -> 1234.56
    - 1234.56 (float) -> 1234.56
    """
    if value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()
    if not s:
        return 0.0

    # Rimuovi simbolo valuta e spazi
    s = s.replace('€', '').strip()

    # Rimuovi eventuali caratteri invisibili
    s = "".join(c for c in s if c.isprintable())

    # Caso speciale: Numeri enormi scientifici o errori Excel (es. 50883250...)
    # Se il numero ha più di 15 cifre ed è intero, è sospetto.
    # Ma prima puliamo.

    # Rilevamento formato
    has_comma = ',' in s
    has_dot = '.' in s

    # 1. Formato chiaramente Italiano: punti e virgola finale
    # Es: 1.234,56
    if has_comma and has_dot:
        last_comma = s.rfind(',')
        last_dot = s.rfind('.')

        if last_comma > last_dot:
            # IT: Punti sono migliaia, virgola è decimale
            s = s.replace('.', '').replace(',', '.')
        else:
            # US: Virgole sono migliaia, punto è decimale
            s = s.replace(',', '')

    # 2. Solo virgola: "1234,56" (IT) o "1,234" (US migliaia)
    elif has_comma and not has_dot:
        # Ambiguo. Euristiche:
        # Se c'è una sola virgola ed è seguita da 1 o 2 cifre -> Decimale (IT)
        # Se seguita da 3 cifre -> Potrebbe essere migliaia (US) o 3 decimali (Gas/Finanza)
        # Assumiamo contesto CONTABILITÀ ITALIANA: Virgola è sempre Decimale.
        s = s.replace(',', '.')

    # 3. Solo punto: "1234.56" (US) o "1.234" (IT migliaia)
    elif has_dot and not has_comma:
        # Ambiguo.
        # "123.456" -> 123456 (IT) o 123.456 (US)
        # Contesto Italiano: Il punto è spesso migliaia.
        # TUTTAVIA, Pandas/Python usano punto per decimale nelle conversioni standard.
        # Se la stringa viene da un `astype(str)` di un float, sarà "123.456".

        # Controlliamo il numero di punti
        dots_count = s.count('.')
        if dots_count > 1:
            # "1.234.567" -> Sicuramente migliaia
            s = s.replace('.', '')
        else:
            # Un solo punto.
            # Se ha 3 decimali esatti ("1.234"), è ambiguo (Mille o Uno virgola due..).
            # Se ha 2 decimali ("10.50"), è quasi certamente decimale (US/Python standard).
            # Se ha 1 decimale ("10.5"), è decimale.

            parts = s.split('.')
            if len(parts[1]) != 3:
                # Non 3 cifre -> Decimale sicuro
                pass # Lascia il punto
            else:
                # 3 cifre ("1.234").
                # Qui rischiamo. "50.883" -> 50883 o 50.883?
                # Se è un prezzo unitario, potrebbe essere 50 euro.
                # Se è un totale, potrebbe essere 50 mila.
                # Se il valore originale era float, è decimale.
                # Nel dubbio, proviamo a parsare come float.
                pass

    try:
        val = float(s)

        # SANITY CHECK PER "NUMERI ESAGERATI"
        # Se il valore supera 1 trilione (10^12) ed è probabilmente un errore di parsing
        # (es. 50,883,250... invece di 508.83)
        # Proviamo a scalarlo?
        # No, meglio ritornare il valore parsato ma loggare se possibile, o applicare logica correttiva.
        # Caso specifico utente: 50.883.250.000.000.000 vs 508,83
        # Rapporto: 10^14.

        return val
    except ValueError:
        return 0.0

if __name__ == "__main__":
    # Test cases
    tests = [
        ("1.234,56", 1234.56),
        ("1,234.56", 1234.56),
        ("508,83", 508.83),
        ("508.83", 508.83),
        ("1.000", 1000.0), # Ambiguo, in IT solitamente 1000 se input manuale, ma 1.0 se float. Qui assumiamo float standard se ambiguo? No, parse logic sopra lascia il punto se != 3 cifre.
                           # "1.000" ha 3 cifre. Se lasciamo punto -> 1.0.
                           # Se rimuoviamo punto -> 1000.
                           # Vediamo output script.
        ("€ 50,00", 50.0),
        (50.5, 50.5)
    ]
    for i, o in tests:
        res = parse_currency(i)
        print(f"In: {i!r} -> Out: {res} ({'OK' if res == o else 'FAIL expected ' + str(o)})")
