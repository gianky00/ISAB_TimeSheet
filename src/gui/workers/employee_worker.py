"""SyncroJob - Employee Worker.

Worker asincrono per il caricamento e processing dei dati anagrafici.
Evita il freeze della GUI durante il calcolo degli stati di migliaia di dipendenti.
"""

import logging

from PySide6.QtCore import QThread, Signal

from src.core.dipendenti.anagrafica_controller import AnagraficaController

logger = logging.getLogger(__name__)


class EmployeeWorker(QThread):
    """Worker che gestisce l'estrazione e il processing dei dati dipendenti in background.

    Inizializza il worker.

    Args:
      controller: Istanza di AnagraficaController.
      search_text: Testo di ricerca.
      current_filter: Filtro di stato corrente.

    Attributes:
        error_signal: Segnale o attributo della classe.
        finished_signal: Segnale o attributo della classe.
    """

    finished_signal = Signal(list, dict)  # (dtos, counts)
    error_signal = Signal(str)

    def __init__(
        self, controller: AnagraficaController, search_text: str, current_filter: str | None
    ) -> None:
        super().__init__()
        self.controller = controller
        self.search_text = search_text
        self.current_filter = current_filter

    def run(self) -> None:
        """Esegue l'elaborazione pesante in background."""
        try:
            logger.info(f"[EmployeeWorker] Caricamento dipendenti (query: '{self.search_text}')")

            # 1. Recupero dati grezzi (I/O Bound)
            full_rows = self.controller.get_employees(self.search_text)

            # 2. Processing calcoli (CPU Bound)
            dtos, counts = self.controller.process_rows(full_rows, self.current_filter)

            logger.info(f"[EmployeeWorker] Processing completato: {len(dtos)} record.")
            self.finished_signal.emit(dtos, counts)

        except Exception as e:
            logger.exception("[EmployeeWorker] Errore critico nel processing dipendenti")
            self.error_signal.emit(str(e))
