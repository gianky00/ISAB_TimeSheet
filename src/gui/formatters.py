from datetime import datetime

from PyQt6.QtCore import QAbstractTableModel, Qt


# --- FORMATTERS ---
def format_date_it(value):
    """
    Converte stringa ISO YYYY-MM-DD o datetime in DD/MM/YYYY.
    """
    if not value:
        return ""
    try:
        if isinstance(value, str):
            # Tenta vari formati comuni
            for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"):
                try:
                    dt = datetime.strptime(value.split(" ")[0], fmt)
                    return dt.strftime("%d/%m/%Y")
                except ValueError:
                    continue
            return value  # Fallback se non è una data riconosciuta
        elif isinstance(value, (datetime, float, int)):
            # Se è già datetime o timestamp (non supportato qui ma per sicurezza)
            return value.strftime("%d/%m/%Y")
    except Exception:
        pass
    return str(value)


def format_currency_smart(value):
    """
    Formatta numeri in stile Euro contabile:
    - 1200.00 -> 1.200
    - 1200.50 -> 1.200,50
    Elimina il rumore floating point (es. .00000000001) arrotondando a 2 decimali.
    """
    if value is None or value == "":
        return ""
    try:
        # 1. Pulizia e Conversione
        if isinstance(value, str):
            # Rimuove simboli valuta e spazi
            clean_val = value.replace("€", "").strip()
            # Gestione formati IT (1.234,56) vs EN (1,234.56)
            if "," in clean_val and "." in clean_val:
                # Se entrambi presenti, assumiamo IT (punto migliaia, virgola decimale)
                clean_val = clean_val.replace(".", "").replace(",", ".")
            elif "," in clean_val:
                # Solo virgola -> decimale IT
                clean_val = clean_val.replace(",", ".")
            f_val = float(clean_val)
        else:
            f_val = float(value)

        # 2. Arrotondamento per eliminare rumore (es. 8.650.500.000.000.001 -> 8650.5)
        # Se il numero è assurdamente grande (> 100M), probabilmente è un errore di scaling
        # ma per ora ci limitiamo a renderlo leggibile arrotondandolo.
        f_val = round(f_val, 2)

        # 3. Logica Visualizzazione: Se intero, niente decimali.
        if f_val.is_integer():
            return f"{int(f_val):,}".replace(",", ".")
        else:
            # 2 decimali fissi con separatori IT
            return f"{f_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    except (ValueError, TypeError):
        return str(value)


def format_number_smart(value):
    """Identico a currency_smart, usato per ORE SP e RESA."""
    return format_currency_smart(value)


class FastTableModel(QAbstractTableModel):
    """
    Modello dati ottimizzato con supporto per:
    - Formattazione specifica per colonna (DisplayRole).
    - Ordinamento nativo sui dati grezzi.
    - Allineamento intelligente (Numeri a destra).
    """

    def __init__(self, data=None, headers=None):
        super().__init__()
        self._data = data or []
        self._headers = headers or []
        # Mapping: {col_index: formatter_function}
        self._formatters = {}
        # Mapping: {col_index: Qt.AlignmentFlag}
        self._alignments = {}

    def set_column_formatter(self, col_idx, formatter_func):
        """Imposta una funzione di formattazione per una colonna."""
        self._formatters[col_idx] = formatter_func
        # Default: se formattiamo numeri/valuta, allineiamo a destra
        if formatter_func in (format_currency_smart, format_number_smart):
            self._alignments[col_idx] = (
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )

    def set_column_alignment(self, col_idx, alignment):
        """Forza allineamento per una colonna."""
        self._alignments[col_idx] = alignment

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row, col = index.row(), index.column()
        raw_value = self._data[row][col]

        if role == Qt.ItemDataRole.DisplayRole:
            if col in self._formatters:
                return self._formatters[col](raw_value)
            return str(raw_value) if raw_value is not None else ""

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return self._alignments.get(
                col, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )

        # Per ordinamento standard se la view non usa sort() del modello (ma QTableView lo fa)
        if role == Qt.ItemDataRole.EditRole:
            return raw_value

        return None

    def headerData(self, section, orientation, role):
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self._headers[section]
        return None

    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

    def sort(self, column, order):
        """Ordinamento personalizzato basato sui dati GREZZI (non stringhe formattate)."""
        self.layoutAboutToBeChanged.emit()
        try:
            # Funzione chiave per gestire None e tipi misti
            def sort_key(row):
                val = row[column]
                if val is None:
                    return "" if order == Qt.SortOrder.AscendingOrder else "zzzzzz"
                # Tenta conversione numerica per stringhe che sembrano numeri
                if isinstance(val, str) and val.replace(".", "").isdigit():
                    return float(val)
                return val

            reverse = order == Qt.SortOrder.DescendingOrder
            self._data.sort(key=sort_key, reverse=reverse)
        except Exception as e:
            print(f"Sort Error: {e}")
        finally:
            self.layoutChanged.emit()
