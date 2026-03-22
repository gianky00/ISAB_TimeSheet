"""
SyncroJob - Filter Worker
Thread worker per l'esecuzione asincrona dei filtri su grandi volumi di dati.
"""

from PyQt6.QtCore import QThread, pyqtSignal


class FilterWorker(QThread):
    """Esegue il filtraggio dei dati dello Scarico Ore in background."""

    finished = pyqtSignal(list, int)  # visible_indices, filtered_count

    def __init__(
        self,
        search_index: list[str],
        display_data: list[list[str]],
        text: str,
        col_filters: dict[int, set[str]] | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.search_index = search_index
        self.display_data = display_data
        self.text = text.lower().strip()
        self.col_filters = col_filters
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        """Esegue il filtraggio."""
        if self._is_cancelled:
            return
        search_terms = self.text.split() if self.text else []
        indices = list(range(len(self.display_data)))

        # 1. Global Search
        if search_terms:
            s_idx = self.search_index
            indices = [i for i in indices if all(t in s_idx[i] for t in search_terms)]
            if self._is_cancelled:
                return  # type: ignore[unreachable]

        # 2. Column Filters
        if self.col_filters:
            d_data = self.display_data
            for col, allowed in self.col_filters.items():
                if self._is_cancelled:
                    return  # type: ignore[unreachable]
                indices = [i for i in indices if d_data[i][col].lower() in allowed]

        if not self._is_cancelled:
            self.finished.emit(indices, len(indices))
