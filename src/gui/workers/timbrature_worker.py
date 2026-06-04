"""SyncroJob - Timbrature Data Worker.

Worker asincrono per il recupero dei dati delle timbrature e il popolamento dei filtri.
Garantisce la fluidità della GUI durante le query SQL sul database timbrature.
"""

import logging
from typing import Any

from PySide6.QtCore import QThread, Signal

from src.infrastructure.bots.portale_fornitori.timbrature.storage import TimbratureStorage

logger = logging.getLogger(__name__)


class TimbratureDataWorker(QThread):
    """Worker per l'esecuzione di query sulle timbrature in background.

    Inizializza il worker.

    Args:
      storage: Istanza di TimbratureStorage.
      mode: 'fetch_data', 'fetch_filters' o 'import_excel'.
      *args: Argomenti posizionali aggiuntivi.
      **kwargs: Argomenti nominali per il filtraggio (filter_text, ecc).

    Attributes:
        data_ready: Segnale o attributo della classe.
        error_signal: Segnale o attributo della classe.
        filters_ready: Segnale o attributo della classe.
        import_finished: Segnale o attributo della classe.
    """

    data_ready = Signal(list)  # Dati per la tabella
    filters_ready = Signal(dict)  # Liste per i filtri (reparti, cantieri, anni)
    import_finished = Signal(bool, str)  # success, message
    error_signal = Signal(str)

    def __init__(self, storage: TimbratureStorage, mode: str, *args: Any, **kwargs: Any) -> None:
        super().__init__()

        self.storage = storage
        self.mode = mode
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        """Esegue l'operazione richiesta."""
        try:
            if self.mode == "fetch_data":
                self._fetch_data()
            elif self.mode == "fetch_filters":
                self._fetch_filters()
            elif self.mode == "import_excel":
                self._import_excel()
        except Exception as e:
            logger.exception(f"[TimbratureWorker] Errore in mode {self.mode}")
            self.error_signal.emit(str(e))

    def _fetch_data(self) -> None:
        """Recupera le timbrature filtrate."""
        rows = self.storage.get_timbrature_with_reparto(
            limit=self.kwargs.get("limit", 2000),
            filter_text=self.kwargs.get("filter_text", ""),
            filter_reparto=self.kwargs.get("filter_reparto", "Tutti"),
            filter_cantiere=self.kwargs.get("filter_cantiere", "Tutti"),
            filter_year=self.kwargs.get("filter_year", "Tutti"),
        )
        self.data_ready.emit(rows.copy())

    def _fetch_filters(self) -> None:
        """Recupera le liste uniche per i filtri UI."""
        lists = self.storage.get_lists()
        self.filters_ready.emit(lists)

    def _import_excel(self) -> None:
        """Esegue l'importazione di un file Excel in background."""
        file_path = self.args[0]
        # Usiamo un logger dummy per l'importazione
        success = self.storage.import_excel(file_path, logger.info)
        self.import_finished.emit(
            success, "Importazione completata" if success else "Errore durante l'importazione"
        )
