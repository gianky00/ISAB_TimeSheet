from collections.abc import Callable
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

# --- FORMATTERS ---


def format_currency_smart(value: Any) -> str:
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
            clean_val = value.replace("  ", "").strip()
            # Gestione intelligente formati IT (1.234,56) vs EN (1,234.56)
            if "," in clean_val and "." in clean_val:
                if clean_val.find(".") < clean_val.find(","):
                    # Punto prima della virgola -> IT (1.234,56)
                    clean_val = clean_val.replace(".", "").replace(",", ".")
                else:
                    # Virgola prima del punto -> EN (1,234.56)
                    clean_val = clean_val.replace(",", "")
            elif "," in clean_val:
                # Solo virgola -> decimale IT
                clean_val = clean_val.replace(",", ".")
            f_val = float(clean_val)
        else:
            f_val = float(value)

        # 2. Arrotondamento per eliminare rumore
        f_val = round(f_val, 2)

        # 3. Logica Visualizzazione: Se intero, niente decimali.
        if f_val.is_integer():
            return f"{int(f_val):,}".replace(",", ".")
        # 2 decimali fissi con separatori IT
        return f"{f_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    except (ValueError, TypeError):
        return str(value)


def format_number_smart(value: Any) -> str:
    """Identico a currency_smart, usato per ORE SP e RESA."""
    return format_currency_smart(value)


def _try_parse_numeric(val_str: str) -> float | None:
    """Tenta il parsing di una stringa in numero (IT/EN)."""
    with suppress(ValueError):
        clean_val = val_str.replace("  ", "").replace("$", "").strip()
        if "," in clean_val and "." in clean_val:
            if clean_val.find(".") < clean_val.find(","):
                clean_val = clean_val.replace(".", "").replace(",", ".")
            else:
                clean_val = clean_val.replace(",", "")
        elif "," in clean_val:
            clean_val = clean_val.replace(",", ".")
        return float(clean_val)
    return None


def _try_parse_date(val_str: str) -> float | None:
    """Tenta il parsing di una stringa in data -> timestamp."""
    date_formats = (
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
    )
    for fmt in date_formats:
        try:
            dt = datetime.strptime(val_str, fmt).replace(tzinfo=UTC)
            return dt.timestamp()
        except ValueError:
            continue
    return None


def _handle_string_sort(val_str: str) -> tuple[int, Any]:
    """Gestisce il parsing intelligente delle stringhe per l'ordinamento."""
    val_clean = val_str.strip()
    if not val_clean:
        return (0, 0)

    # Tentativo Numero
    num = _try_parse_numeric(val_clean)
    if num is not None:
        return (1, num)

    # Tentativo Data
    ts = _try_parse_date(val_clean)
    if ts is not None:
        return (1, ts)

    return (2, val_clean.lower())


def _get_sort_key_value(val: Any, _column: int) -> tuple[int, Any]:
    """Sotto-funzione helper per determinare la chiave di ordinamento di un singolo valore."""
    if val is None:
        return (0, 0)

    if isinstance(val, (int, float)):
        return (1, val)

    if isinstance(val, datetime):
        return (1, val.replace(tzinfo=UTC).timestamp())

    if isinstance(val, str):
        return _handle_string_sort(val)

    return (2, str(val))


class FastTableModel(QAbstractTableModel):
    """
    Modello dati ottimizzato con supporto per:
    - Formattazione specifica per colonna (DisplayRole).
    - Ordinamento nativo sui dati grezzi.
    - Allineamento intelligente (Numeri a destra).
    """

    def __init__(
        self,
        data: list[list[Any]] | None = None,
        headers: list[str] | None = None,
        metadata: list[Any] | None = None,
    ) -> None:
        super().__init__()
        self._data: list[list[Any]] = data or []
        self._headers: list[str] = headers or []
        # Support for parallel metadata list (e.g. valid DB IDs)
        self._metadata: list[Any] = metadata or ([None] * len(self._data))
        self._formatters: dict[int, Callable[[Any], str]] = {}
        self._alignments: dict[int, Qt.AlignmentFlag] = {}

    def set_column_formatter(self, col_idx: int, formatter_func: Callable[[Any], str]) -> None:
        """Imposta una funzione di formattazione per una colonna."""
        self._formatters[col_idx] = formatter_func
        # Default: se formattiamo numeri/valuta, allineiamo a destra
        if formatter_func in (format_currency_smart, format_number_smart):
            self._alignments[col_idx] = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

    def set_column_alignment(self, col_idx: int, alignment: Qt.AlignmentFlag) -> None:
        """Forza allineamento per una colonna."""
        self._alignments[col_idx] = alignment

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        """Restituisce il numero di righe nel modello."""
        if parent is not None and parent.isValid():
            return 0
        return len(self._data)

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        """Restituisce il numero di colonne basato sull'header."""
        if parent is not None and parent.isValid():
            return 0
        return len(self._headers)

    def data(
        self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        """Recupera il valore per una cella applicando formattazione e allineamento."""
        if not index.isValid():
            return None

        row, col = index.row(), index.column()
        raw_value = self._data[row][col]

        # Dispatch basato sul Role per ridurre complessit
        if role == Qt.ItemDataRole.DisplayRole:
            return self._get_display_value(col, raw_value)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return self._alignments.get(col, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        if role == Qt.ItemDataRole.UserRole:
            return self._metadata[row] if row < len(self._metadata) else None

        if role == Qt.ItemDataRole.EditRole:
            return raw_value

        return None

    def _get_display_value(self, col: int, raw_value: Any) -> str:
        """Helper per DisplayRole."""
        if col in self._formatters:
            return self._formatters[col](raw_value)
        return str(raw_value) if raw_value is not None else ""

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        """Restituisce l'intestazione della colonna."""
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._headers[section]
        return None

    def update_data(self, new_data: list[list[Any]], new_metadata: list[Any] | None = None) -> None:
        """Sostituisce i dati del modello e notifica la vista."""
        self.beginResetModel()
        self._data = new_data
        self._metadata = new_metadata or ([None] * len(new_data))
        self.endResetModel()

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        """Ordinamento personalizzato basato sui dati GREZZI (non stringhe formattate)."""
        self.layoutAboutToBeChanged.emit()
        try:

            def sort_key(row_tuple: tuple[list[Any], Any]) -> tuple[int, Any]:
                return _get_sort_key_value(row_tuple[0][column], column)

            reverse = order == Qt.SortOrder.DescendingOrder

            # Combine data and metadata, sort, then split
            combined = list(zip(self._data, self._metadata, strict=False))
            combined.sort(key=sort_key, reverse=reverse)

            # Unzip
            if combined:
                unzipped = list(zip(*combined, strict=False))
                self._data = list(unzipped[0])
                self._metadata = list(unzipped[1])
            else:
                self._data = []
                self._metadata = []

        except Exception as e:
            print(f"Sort Error: {e}")
        finally:
            self.layoutChanged.emit()

    def get_raw_row(self, row_idx: int) -> list[Any] | None:
        """Restituisce i dati grezzi di una riga specifica."""
        if 0 <= row_idx < len(self._data):
            return self._data[row_idx]
        return None
