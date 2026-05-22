"""SyncroJob - Search Controller (Refactored).

Controller per la ricerca universale asincrona con debouncing.
Garantisce la fluidità della GUI delegando le query al SearchWorker e
la visualizzazione dei risultati a SearchResultsMenu.
"""

import logging
import warnings
from typing import Any

from PySide6.QtCore import QObject, QTimer

from src.gui.components.search.results_menu import SearchResultsMenu
from src.gui.workers.search_worker import SearchWorker

logger = logging.getLogger(__name__)


class SearchController(QObject):
    """Controller per la ricerca universale e la navigazione ai risultati.

    Gestisce il flusso logico asincrono e il debouncing dell'input di ricerca.
    """

    def __init__(self, main_window: Any) -> None:
        """Inizializza il controller di ricerca.

        Args:
            main_window: Riferimento alla finestra principale per la navigazione
                e la visualizzazione grafica dei risultati.
        """
        super().__init__()
        self.mw = main_window
        self.worker: SearchWorker | None = None

        # Timer per il debouncing (attende 300ms di inattività prima di cercare)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._execute_async_search)
        self._last_query = ""

    def perform_search(self, query: str) -> None:
        """Avvia il processo di ricerca con debouncing.

        Args:
            query: La stringa digitata dall'utente.
        """
        query = query.strip()
        if not query or len(query) < 2:
            self._last_query = ""
            return

        self._last_query = query
        self.search_timer.start(300)

    def _execute_async_search(self) -> None:
        """Crea e avvia il worker per la ricerca asincrona."""
        if not self._last_query:
            return

        # Interrompe in modo sicuro eventuali ricerche precedenti ancora in corso
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                self.worker.results_ready.disconnect()  # Previene update da vecchi thread

        self.worker = SearchWorker(self._last_query, parent=self)
        self.worker.results_ready.connect(self._show_results_menu)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.start()

    def _show_results_menu(self, results: dict[str, Any]) -> None:
        """Istanzia e delega la visualizzazione del menu dei risultati.

        Args:
            results: Dizionario dei risultati prodotto dal SearchWorker/SearchService.
        """
        if not hasattr(self.mw, "global_search"):
            logger.warning("MainWindow non possiede l'attributo 'global_search'.")
            return

        # Delega interamente alla vista dedicata (SearchResultsMenu) rispettando l'SRP
        menu = SearchResultsMenu(self.mw, self._last_query, parent=self.mw)
        menu.build_and_exec(results, self.mw.global_search)
