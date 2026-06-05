"""SyncroJob - Filter Worker.

Thread worker per l'esecuzione asincrona dei filtri su grandi volumi di dati.
"""

from PySide6.QtCore import QObject, QThread, Signal


class FilterWorker(QThread):
    """Esegue il filtraggio dei dati dello Scarico Ore in background.

    Inizializza il worker per il filtraggio.

    Args:
      search_index: Indice di ricerca globalizzato.
      display_data: Dati visualizzati nella tabella.
      text: Testo cercato nella barra di ricerca.
      col_filters: Filtri applicati alle singole colonne.
      parent: Oggetto genitore Qt.

    Attributes:
        finished: Segnale o attributo della classe.
    """

    finished = Signal(list, int)  # visible_indices, filtered_count

    def __init__(
        self,
        search_index: list[str],
        display_data: list[list[str]],
        text: str,
        col_filters: dict[int, set[str]] | None = None,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self.search_index = search_index
        self.display_data = display_data
        self.text = text.lower().strip()
        self.col_filters = col_filters
        self._is_cancelled = False

    def cancel(self) -> None:
        """Annulla l'operazione di filtraggio corrente."""
        self._is_cancelled = True

    def _apply_global_search(self, indices: list[int], search_terms: list[str]) -> list[int]:
        if not search_terms:
            return indices
        s_idx = self.search_index
        return [i for i in indices if all(t in s_idx[i] for t in search_terms)]

    def _apply_column_filters(self, indices: list[int]) -> list[int]:
        if not self.col_filters:
            return indices
        d_data = self.display_data
        for col, allowed in self.col_filters.items():
            if self._is_cancelled:
                return indices
            indices = [i for i in indices if d_data[i][col].lower() in allowed]
        return indices

    def run(self) -> None:
        """Esegue il filtraggio."""
        if self._is_cancelled:
            return
        search_terms = self.text.split() if self.text else []
        indices = list(range(len(self.display_data)))

        indices = self._apply_global_search(indices, search_terms)

        indices = self._apply_column_filters(indices)

        if not self._is_cancelled:
            self.finished.emit(indices, len(indices))
