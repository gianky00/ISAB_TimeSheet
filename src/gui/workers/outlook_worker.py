"""SyncroJob - Outlook Email Worker.

Worker asincrono per l'invio di email tramite Outlook (win32com).
Evita il freeze della GUI durante l'automazione COM e il caricamento di Outlook.
"""

import logging
from collections.abc import Callable

from PySide6.QtCore import QThread, Signal

logger = logging.getLogger(__name__)


class OutlookEmailWorker(QThread):
    """Worker che gestisce l'apertura e l'invio di email Outlook in background.

    Inizializza il worker.

    Args:
      email_func: La funzione che esegue l'invio della mail (già configurata).

    Attributes:
        finished_signal: Segnale o attributo della classe.
    """

    finished_signal = Signal(bool, str)  # (success, error_message)

    def __init__(self, email_func: Callable[[], None]) -> None:
        super().__init__()
        self.email_func = email_func

    def run(self) -> None:
        """Esegue l'automazione Outlook in background."""
        try:
            logger.info("[OutlookEmailWorker] Avvio automazione Outlook...")
            # L'automazione COM richiede che la funzione sia eseguita nel thread
            # Tuttavia, win32com.client.Dispatch deve essere chiamato nello stesso thread
            # in cui viene usato. La funzione passata dovrebbe gestire il Dispatch interno.
            self.email_func()
            self.finished_signal.emit(True, "")
        except Exception as e:
            logger.exception("Errore durante l'automazione Outlook")
            self.finished_signal.emit(False, str(e))
