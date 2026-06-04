"""SyncroJob - Search Worker.

Thread worker per l'esecuzione asincrona delle ricerche universali.
"""

from typing import Any

from PySide6.QtCore import QThread, Signal

from src.application.services.search.search_service import SearchService


class SearchWorker(QThread):
    """Worker che esegue la ricerca in un thread separato per non bloccare la GUI.

    Inizializza il worker di ricerca.

    Args:
      query: Stringa di ricerca.
      limit: Numero massimo di risultati per categoria.
      parent: Oggetto genitore Qt.

    Attributes:
        results_ready: Segnale o attributo della classe.
    """

    results_ready = Signal(dict)

    def __init__(self, query: str, limit: int = 10, parent: Any = None) -> None:
        super().__init__(parent)
        self.query = query
        self.limit = limit
        self._is_cancelled = False

    def cancel(self) -> None:
        """Annulla la ricerca in corso."""
        self._is_cancelled = True

    def run(self) -> None:
        """Esegue la ricerca tramite il SearchService e invia i risultati."""
        if self._is_cancelled:
            return
        results = SearchService.search_all(self.query, self.limit)
        if not self._is_cancelled:
            self.results_ready.emit(results)
