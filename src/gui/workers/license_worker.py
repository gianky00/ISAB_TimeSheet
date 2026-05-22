"""
SyncroJob - License Heartbeat Worker
Worker asincrono per la verifica periodica della licenza cloud.
"""

import logging

from PySide6.QtCore import QThread, Signal

from src.core.license_updater import run_update

logger = logging.getLogger(__name__)


class LicenseWorker(QThread):
    """
    Worker che sincronizza la licenza con GitHub in background.
    """

    finished_signal = Signal(bool, str)  # (success, error_message)

    def run(self) -> None:
        """Esegue run_update in un thread secondario."""
        try:
            logger.info("[LicenseWorker] Sincronizzazione licenza cloud...")
            success = run_update()
            self.finished_signal.emit(success, "")
        except Exception as e:
            # Cattura l'eccezione REVOCATA per gestirla nella UI
            msg = str(e)
            logger.exception("Errore critico durante heartbeat licenza")
            self.finished_signal.emit(False, msg)
