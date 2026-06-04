"""SyncroJob - Contabilita Data Worker.

Worker versatile per il recupero asincrono di dati dal modulo Contabilità.
Supporta Giornaliere, Attività Programmate e Scarico Ore.
"""

import logging
from typing import Any

from PySide6.QtCore import QThread, Signal

from src.application.services.contabilita_manager import ContabilitaManager

logger = logging.getLogger(__name__)


class ContabilitaDataWorker(QThread):
    """Worker per il caricamento generico di liste dati dal database contabilità.

    Inizializza il worker.

    Args:
      fetch_func_name: Nome del metodo di ContabilitaManager da chiamare.
      *args: Argomenti posizionali per la funzione.
      **kwargs: Argomenti nominali per la funzione.

    Attributes:
        error_signal: Segnale o attributo della classe.
        finished_signal: Segnale o attributo della classe.
    """

    finished_signal = Signal(list)
    error_signal = Signal(str)

    def __init__(self, fetch_func_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__()
        self.fetch_func_name = fetch_func_name
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        """Esegue la fetch dei dati dal manager."""
        try:
            logger.info(f"[ContabilitaDataWorker] Esecuzione {self.fetch_func_name}...")

            func = getattr(ContabilitaManager, self.fetch_func_name)
            data = func(*self.args, **self.kwargs)

            # Assicuriamoci che i dati siano una lista (sqlite ritorna liste di tuple)
            if data is None:
                data = []

            self.finished_signal.emit(list(data))
            logger.info(f"[ContabilitaDataWorker] {self.fetch_func_name} completata ({len(data)} record).")

        except Exception as e:
            logger.exception(f"[ContabilitaDataWorker] Errore durante {self.fetch_func_name}")
            self.error_signal.emit(str(e))
