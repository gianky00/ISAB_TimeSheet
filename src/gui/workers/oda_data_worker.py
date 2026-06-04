"""SyncroJob - ODA Data Worker.

Worker asincrono per il recupero e raggruppamento degli Ordini di Acquisto.
Garantisce la fluidità della GUI durante la consultazione dello storico ODA.
"""

import logging

from PySide6.QtCore import QThread, Signal

from src.application.services.oda.oda_controller import ODAController

logger = logging.getLogger(__name__)


class ODADataWorker(QThread):
    """Worker che esegue query ODA e raggruppamento dati in background.

    Inizializza il worker.

    Args:
      controller: Istanza di ODAController.
      search_text: Filtro di ricerca testuale.

    Attributes:
        error_signal: Segnale o attributo della classe.
        finished_signal: Segnale o attributo della classe.
    """

    finished_signal = Signal(list)
    error_signal = Signal(str)

    def __init__(self, controller: ODAController, search_text: str = "") -> None:
        super().__init__()
        self.controller = controller
        self.search_text = search_text

    def run(self) -> None:
        """Esegue l'estrazione e il raggruppamento dati."""
        try:
            logger.info(f"[ODADataWorker] Caricamento ODA (query: '{self.search_text}')")

            # 1. Recupero dati raggruppati (SQL Bound)
            structured_data = self.controller.get_grouped_data(self.search_text)

            logger.info(f"[ODADataWorker] Caricati {len(structured_data)} gruppi ODA.")
            self.finished_signal.emit(structured_data)

        except Exception as e:
            logger.exception("[ODADataWorker] Errore durante il caricamento ODA")
            self.error_signal.emit(str(e))
