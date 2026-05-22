"""
SyncroJob - Autopilot Report Worker
Worker asincrono per l'invio automatico del report accessi.
Evita il freeze della GUI durante le query SQL massive e l'automazione Outlook.
"""

import logging

from PySide6.QtCore import QThread, Signal

from src.core.report_service import ReportService

logger = logging.getLogger(__name__)


class AutopilotReportWorker(QThread):
    """
    Worker che esegue il workflow di invio report programmato in background.
    """

    finished_signal = Signal(bool)

    def run(self) -> None:
        """Esegue l'invio del report."""
        try:
            logger.info("[AutopilotReportWorker] Avvio invio report programmato...")
            ReportService.send_scheduled_report_email()
            self.finished_signal.emit(True)
        except Exception:
            logger.exception("Errore durante l'invio report autopilot")
            self.finished_signal.emit(False)
