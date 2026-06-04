"""SyncroJob - PDL Stats Worker.

Worker asincrono per il calcolo delle metriche PDL.
"""

import logging

from PySide6.QtCore import QThread, Signal

from src.application.services.stats.pdl_stats_engine import PDLStatsEngine

logger = logging.getLogger(__name__)


class PDLStatsWorker(QThread):
    """Worker che ricalcola le metriche e i trend dei PDL in background."""

    finished_signal = Signal(object)  # Invia PDLMetrics
    error_signal = Signal(str)

    def run(self) -> None:
        """Esegue il calcolo pesante delle statistiche."""
        try:
            logger.info("[PDLStatsWorker] Calcolo metriche dashboard...")
            metrics = PDLStatsEngine.get_metrics()
            self.finished_signal.emit(metrics)
        except Exception as e:
            logger.exception("Errore calcolo PDL metrics")
            self.error_signal.emit(str(e))
