from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSignal
from PyQt6.QtGui import QColor

from src.gui.components.scarico_ore.cache import CacheWorker


@dataclass
class ScaricoOreRow:
    """
    Data model representing a single row in the 'Scarico Ore' table.
    Contains employee info, hours worked, and job order details.
    """

    id: str


class ScaricoOreTableModel(QAbstractTableModel):
    """
    Modello virtuale ULTRA-RAPIDO per Scarico Ore (130k+ righe).
    Integra la logica di filtraggio per evitare l'overhead di QSortFilterProxyModel.
    Usa dati pre-formattati per rendering O(1).
    """

    COLUMNS = [
        "DATA",
        "PERS1",
        "PERS2",
        "ODC",
        "POS",
        "DALLE",
        "ALLE",
        "TOTALE\nORE",
        "DESCRIZIONE",
        "FINITO",
        "COMMESSA",
    ]

    CACHE_PATH = Path("data/scarico_ore_cache.pkl")

    # ⚡ SINGLETON CACHE
    _global_cache = {
        "display_data": [],  # List[List[str]]
        "search_index": [],  # List[str]
        "totals": [],  # List[float]
        "styles": [],  # List[dict]
        "date_keys": [],  # List[str]
        "loaded": False,
    }

    cache_loaded = pyqtSignal()
    loading_progress = pyqtSignal(str)

    def __init__(self, data=None):
        super().__init__()
        self._display_data = []
        self._search_index = []
        self._float_totals = []
        self._styles_cache = []
        self._date_keys = []

        self._visible_indices = []
        self._filtered_count = 0

        self._worker = None
        self.is_loading = False

        self._current_search_terms = []
        self._current_col_filters = {}

        if self._global_cache["loaded"]:
            self._display_data = self._global_cache["display_data"]
            self._search_index = self._global_cache["search_index"]
            self._float_totals = self._global_cache["totals"]
            self._styles_cache = self._global_cache["styles"]
            self._date_keys = self._global_cache["date_keys"]
            self._visible_indices = list(range(len(self._display_data)))
            self._filtered_count = len(self._visible_indices)

        if data:
            self.update_data(data)

    def load_data_async(self, raw_data=None):
        if self._global_cache["loaded"] and raw_data is None:
            self.cache_loaded.emit()
            return

        if self.is_loading:
            return

        self.is_loading = True
        self.loading_progress.emit("Avvio..." if raw_data else "Caricamento Cache...")

        self._worker = CacheWorker(self.CACHE_PATH, raw_data)
        self._worker.progress.connect(self.loading_progress.emit)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.start()

    def _on_worker_finished(self, display_data, search, totals, style_cache, date_keys):
        self.beginResetModel()
        self._display_data = display_data
        self._search_index = search
        self._float_totals = totals
        self._styles_cache = style_cache
        self._date_keys = date_keys

        self._visible_indices = list(range(len(display_data)))
        self._filtered_count = len(self._visible_indices)

        self.endResetModel()

        self._global_cache["display_data"] = display_data
        self._global_cache["search_index"] = search
        self._global_cache["totals"] = totals
        self._global_cache["styles"] = style_cache
        self._global_cache["date_keys"] = date_keys
        self._global_cache["loaded"] = True

        self.is_loading = False
        self._worker = None
        self.cache_loaded.emit()

    def update_data(self, new_data):
        self.load_data_async(new_data)

    def set_data(self, data):
        worker = CacheWorker(self.CACHE_PATH)
        display_data, search, totals, style_cache, date_keys = worker._build_caches(
            data
        )
        self._on_worker_finished(display_data, search, totals, style_cache, date_keys)

    def set_filter(self, text, col_filters=None):
        text = text.lower().strip()
        search_terms = text.split() if text else []

        self.beginResetModel()

        if not search_terms and not col_filters:
            self._visible_indices = list(range(len(self._display_data)))
        else:
            indices = list(range(len(self._display_data)))
            indices = self._apply_global_search(indices, search_terms)
            indices = self._apply_column_filters(indices, col_filters)
            self._visible_indices = indices

        self._filtered_count = len(self._visible_indices)
        self.endResetModel()

    def _apply_global_search(self, indices: List[int], terms: List[str]) -> List[int]:
        if not terms:
            return indices
        s_idx = self._search_index
        return [i for i in indices if all(t in s_idx[i] for t in terms)]

    def _apply_column_filters(
        self, indices: List[int], col_filters: Optional[dict]
    ) -> List[int]:
        if not col_filters:
            return indices

        filtered = indices
        d_data = self._display_data
        for col, allowed in col_filters.items():
            filtered = [i for i in filtered if d_data[i][col].lower() in allowed]
        return filtered

    def get_float_total_for_visible(self):
        if not self._float_totals:
            return 0.0
        total = sum(self._float_totals[i] for i in self._visible_indices)
        return total

    def rowCount(self, parent=None):
        if parent is None:
            parent = QModelIndex()
        return self._filtered_count

    def columnCount(self, parent=None):
        if parent is None:
            parent = QModelIndex()
        return len(self.COLUMNS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        if row >= self._filtered_count:
            return None

        real_row_idx = self._visible_indices[row]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            return self._display_data[real_row_idx][col]

        elif role == Qt.ItemDataRole.BackgroundRole:
            return self._get_style(real_row_idx, col, "bg")

        elif role == Qt.ItemDataRole.ForegroundRole:
            return self._get_style(real_row_idx, col, "fg")

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if col in [3, 4, 5, 6, 7]:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            if col == 0:
                return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        return None

    def sort(
        self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder
    ) -> None:
        self.layoutAboutToBeChanged.emit()

        reverse = order == Qt.SortOrder.DescendingOrder

        def get_key(idx):
            try:
                if column == 0:
                    return self._date_keys[idx]
                elif column == 7:
                    return self._float_totals[idx]
                else:
                    val = self._display_data[idx][column]
                    return val.lower() if val else ""
            except IndexError:
                return ""

        self._visible_indices.sort(key=get_key, reverse=reverse)
        self.layoutChanged.emit()

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self.COLUMNS[section]
        return None

    def _get_style(self, real_row, col, style_type):
        try:
            if real_row >= len(self._styles_cache):
                return None
            styles = self._styles_cache[real_row]
            if not styles:
                return None

            keys = [
                "data",
                "pers1",
                "pers2",
                "odc",
                "pos",
                "dalle",
                "alle",
                "totale_ore",
                "descrizione",
                "finito",
                "commessa",
            ]
            key = keys[col]
            if key in styles:
                color_hex = styles[key].get(style_type)
                if color_hex:
                    return QColor(color_hex)
        except Exception:
            pass
        return None
