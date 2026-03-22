"""
SyncroJob - Search Worker
Thread worker per l'esecuzione asincrona delle ricerche universali.
"""

from PyQt6.QtCore import QThread, pyqtSignal

from src.core.search.search_service import SearchService


class SearchWorker(QThread):
    """Worker che esegue la ricerca in un thread separato per non bloccare la GUI."""

    results_ready = pyqtSignal(dict)

    def __init__(self, query: str, limit: int = 10, parent=None):
        super().__init__(parent)
        self.query = query
        self.limit = limit
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        """Esegue la ricerca tramite il SearchService e invia i risultati."""
        if self._is_cancelled:
            return
        results = SearchService.search_all(self.query, self.limit)
        if not self._is_cancelled:
            self.results_ready.emit(results)
