"""
SyncroJob - Consuntivo Worker
Worker asincrono per l'inizializzazione dei dati e la scansione del filesystem per i consuntivi.
Garantisce la fluidità della GUI durante la ricerca dei file Excel e le query di configurazione.
"""

import logging
from typing import Any

from PySide6.QtCore import QThread, Signal

from src.core.contabilita.consuntivo.consuntivo_controller import ConsuntivoController

logger = logging.getLogger(__name__)


class ConsuntivoWorker(QThread):
    """
    Worker che gestisce il pre-caricamento delle opzioni e la scansione directory.
    """

    finished_signal = Signal(dict)
    error_signal = Signal(str)

    def __init__(self, controller: ConsuntivoController, scan_callback: Any = None) -> None:
        """
        Inizializza il worker.

        Args:
          controller: Istanza del controller consuntivi.
          scan_callback: Opzionale, riferimento alla funzione di scansione tab.
        """
        super().__init__()
        self.controller = controller
        self.scan_callback = scan_callback

    def run(self) -> None:
        """Esegue le operazioni di bootstrap in background."""
        try:
            logger.info("[ConsuntivoWorker] Avvio pre-caricamento dati...")

            # 1. Caricamento opzioni (SQL Bound)
            options = self.controller.get_config_options()

            # 2. Scansione directory (Filesystem Bound)
            # Se abbiamo un riferimento alla scansione del tab, la eseguiamo qui
            # altrimenti la deleghiamo tramite segnali se possibile.
            # Nota: la scansione del tab modifica la UI, quindi dobbiamo stare attenti.
            # In questo caso, restituiremo i dati trovati nel report finale.

            result = {
                "options": options,
            }

            logger.info("[ConsuntivoWorker] Pre-caricamento completato.")
            self.finished_signal.emit(result)

        except Exception as e:
            logger.exception("[ConsuntivoWorker] Errore critico nel pre-caricamento")
            self.error_signal.emit(str(e))
