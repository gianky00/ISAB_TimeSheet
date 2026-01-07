"""
Bot TS - GUI Formatters
Funzioni di utilità per la formattazione dei dati da visualizzare nell'interfaccia grafica.
"""
from datetime import datetime

def format_currency(val: float) -> str:
    """Formatta un valore numerico come valuta in formato italiano (€ 1.234,56)."""
    if val is None:
        return ""
    try:
        return f"€ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return ""

def format_number(val) -> str:
    """Formatta un numero per la visualizzazione: max 2 decimali, virgola, e rimuove .0 se intero."""
    if val is None:
        return ""
    try:
        val_f = float(val)
        val_f = round(val_f, 2)
        if val_f.is_integer():
            return f"{int(val_f)}"
        else:
            # Converte in stringa con punto, poi sostituisce con virgola
            return f"{val_f:.2f}".replace(".", ",")
    except (ValueError, TypeError):
        return str(val)

def format_date(val: str) -> str:
    """Formatta una stringa di data (da YYYY-MM-DD o altri formati) a DD/MM/YYYY."""
    if not val:
        return ""
    str_val = str(val).strip()
    if " " in str_val:
        str_val = str_val.split(" ")[0]
    
    dt = None
    # Formati comuni da provare
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            dt = datetime.strptime(str_val, fmt)
            break
        except ValueError:
            continue
            
    if dt:
        return dt.strftime("%d/%m/%Y")
    return str_val # Ritorna il valore originale se il parsing fallisce

def parse_float(text: str) -> float:
    """Converte una stringa (potenzialmente in formato italiano) in un float."""
    if not isinstance(text, str):
        text = str(text)
    try:
        # Gestisce sia "1.234,56" che "1234.56"
        clean_text = text.replace(".", "").replace(",", ".").strip()
        return float(clean_text)
    except (ValueError, TypeError):
        return 0.0

def parse_currency(text: str) -> float:
    """Converte una stringa di valuta (es. '€ 1.234,56') in un float."""
    if not isinstance(text, str):
        text = str(text)
    try:
        clean_text = text.replace("€", "").replace(".", "").replace(",", ".").strip()
        return float(clean_text)
    except (ValueError, TypeError):
        return 0.0
