"""
SyncroJob - Scarico Ore Data Model
Modello tabellare ottimizzato per la gestione di grandi volumi di dati (130k+ righe).
"""

from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt, Signal
from PySide6.QtGui import QColor

from src.gui.components.scarico_ore.cache import CacheWorker
from src.gui.components.scarico_ore.filter_worker import FilterWorker


@dataclass(slots=True)
class ScaricoOreRow:
    """
    Modello dati che rappresenta una singola riga nella tabella 'Scarico Orè.
    Contiene le informazioni sui dipendenti, le ore lavorate e i dettagli della commessa.
    """

    id: str


class ScaricoOreTableModel(QAbstractTableModel):
    """
    Modello virtuale ULTRA-RAPIDO per Scarico Ore (130k+ righe).
    Integra la logica di filtraggio per evitare l'overhead di QSortFilterProxyModel.
    Usa dati pre-formattati per rendering O(1).
    """

    COLUMNS: ClassVar[list[str]] = [
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

    CACHE_PATH: ClassVar[Path] = Path("data/scarico_ore_cache.pkl")

    #   SINGLETON CACHE
    _global_cache: ClassVar[dict[str, Any]] = {
        "display_data": [],  # List[List[str]]
        "search_index": [],  # List[str]
        "totals": [],  # List[float]
        "styles": [],  # List[dict]
        "date_keys": [],  # List[str]
        "loaded": False,
    }

    cache_loaded = Signal()
    loading_progress = Signal(str)

    def __init__(self, data: list[tuple[Any, ...]] | None = None) -> None:
        """
        Inizializza il modello e carica i dati dalla cache globale se disponibili.

        Args:
          data: Dati iniziali opzionali.
        """
        super().__init__()
        self._display_data: list[list[str]] = []
        self._search_index: list[str] = []
        self._float_totals: list[float] = []
        self._styles_cache: list[dict[str, Any] | None] = []
        self._date_keys: list[str] = []

        self._visible_indices: list[int] = []
        self._filtered_count: int = 0

        self._worker: CacheWorker | None = None
        self._filter_worker: FilterWorker | None = None
        self.is_loading: bool = False
        self.is_filtering: bool = False

        self._current_search_terms: list[str] = []
        self._current_col_filters: dict[int, set[str]] = {}

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

    def load_data_async(
        self, raw_data: list[tuple[Any, ...]] | Callable[[], list[tuple[Any, ...]]] | None = None
    ) -> None:
        """
        Avvia il caricamento asincrono dei dati tramite CacheWorker.

        Args:
          raw_data: Dati grezzi da processare, funzione di caricamento o None per caricare da cache pkl.
        """
        if self._global_cache["loaded"] and raw_data is None:
            self.cache_loaded.emit()
            return

        if self.is_loading:
            return

        self.is_loading = True
        self.loading_progress.emit("Avvio..." if raw_data else "Caricamento Cache...")

        if self._worker and self._worker.isRunning():
            self._worker.terminate()  # CacheWorker could have cancel as well, but assuming less frequent
            self._worker.wait()

        self._worker = CacheWorker(self.CACHE_PATH, raw_data, parent=self)
        self._worker.progress.connect(self.loading_progress.emit)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.start()

    def _on_worker_finished(
        self,
        display_data: list[list[str]],
        search: list[str],
        totals: list[float],
        style_cache: list[dict[str, Any] | None],
        date_keys: list[str],
    ) -> None:
        """Slot chiamato al termine del worker per aggiornare il modello."""
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
        self.cache_loaded.emit()

    def update_data(self, new_data: list[tuple[Any, ...]]) -> None:
        """Aggiorna i dati del modello (triggera caricamento asincrono)."""
        self.load_data_async(new_data)

    def set_data(self, data: list[tuple[Any, ...]]) -> None:
        """
        Imposta i dati in modo sincrono (usato principalmente nei test o piccoli dataset).

        Args:
          data: Lista di tuple di dati grezzi.
        """
        worker = CacheWorker(self.CACHE_PATH)
        display_data, search, totals, style_cache, date_keys = worker._build_caches(data)
        self._on_worker_finished(display_data, search, totals, style_cache, date_keys)

    def set_filter(self, text: str, col_filters: dict[int, set[str]] | None = None) -> None:
        """
        Applica filtri globali e per colonna al modello in modo asincrono.
        """
        if self.is_filtering and self._filter_worker and self._filter_worker.isRunning():
            self._filter_worker.cancel()
            self._filter_worker.finished.disconnect()  # Disconnette per evitare update fantasma

        self.is_filtering = True
        self._filter_worker = FilterWorker(
            self._search_index, self._display_data, text, col_filters, parent=self
        )
        self._filter_worker.finished.connect(self._on_filter_finished)
        self._filter_worker.finished.connect(self._filter_worker.deleteLater)
        self._filter_worker.start()

    def _on_filter_finished(self, visible_indices: list[int], filtered_count: int) -> None:
        """Slot chiamato al termine del filtraggio per aggiornare la vista."""
        self.beginResetModel()
        self._visible_indices = visible_indices
        self._filtered_count = filtered_count
        self.endResetModel()
        self.is_filtering = False
        self.cache_loaded.emit()  # Riusiamo il segnale per notificare la UI

    def get_float_total_for_visible(self) -> float:
        """Calcola la somma delle ore per le sole righe visibili."""
        if not self._float_totals:
            return 0.0
        return sum(self._float_totals[i] for i in self._visible_indices)

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        """Restituisce il numero di righe filtrate."""
        if parent is not None and parent.isValid():
            return 0
        return self._filtered_count

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        """Restituisce il numero di colonne del modello."""
        if parent is not None and parent.isValid():
            return 0
        return len(self.COLUMNS)

    def data(
        self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        """Restituisce i dati per una specifica cella e ruolo."""
        if not index.isValid():
            return None

        row = index.row()
        if row >= self._filtered_count:
            return None

        real_row_idx = self._visible_indices[row]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            return self._display_data[real_row_idx][col]

        if role == Qt.ItemDataRole.BackgroundRole:
            return self._get_style(real_row_idx, col, "bg")

        if role == Qt.ItemDataRole.ForegroundRole:
            return self._get_style(real_row_idx, col, "fg")

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col in (3, 4, 5, 6, 7):
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            if col == 0:
                return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        return None

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        """Ordina i dati per la colonna specificata."""
        self.layoutAboutToBeChanged.emit()

        reverse = order == Qt.SortOrder.DescendingOrder

        def get_key(idx: int) -> Any:
            """Estrae la chiave di ordinamento per una riga e colonna specifica."""
            try:
                if column == 0:
                    return self._date_keys[idx]
                if column == 7:
                    return self._float_totals[idx]
                val = self._display_data[idx][column]
                return val.lower() if val else ""
            except IndexError:
                return ""

        self._visible_indices.sort(key=get_key, reverse=reverse)
        self.layoutChanged.emit()

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        """Restituisce l'header per le colonne."""
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.COLUMNS[section]
        return None

    def _get_style(self, real_row: int, col: int, style_type: str) -> QColor | None:
        """Recupera il colore di sfondo o testo dalla cache degli stili."""
        with suppress(Exception):
            if real_row >= len(self._styles_cache):
                return None
            styles = self._styles_cache[real_row]
            if not styles:
                return None

            keys = (
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
            )
            key = keys[col]
            if key in styles:
                color_hex = styles[key].get(style_type)
                if color_hex:
                    return QColor(color_hex)
        return None
