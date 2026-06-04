"""SyncroJob - ROI Worker.

Worker asincrono per il calcolo delle metriche di risparmio (ROI).
Evita il freeze della GUI durante l'analisi dello storico esecuzioni bot.
"""

import logging

from PySide6.QtCore import QThread, Signal

from src.application.services.stats.roi_engine import ROIEngine

logger = logging.getLogger(__name__)


class ROIWorker(QThread):
    """Worker che esegue il calcolo del ROI in background.

    Inizializza la classe.
    """

    finished_signal = Signal(object)  # Restituisce l'oggetto ROIMetrics
    error_signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        """Esegue il calcolo effettivo del ROI."""
        try:
            logger.info("[ROIWorker] Avvio calcolo metriche efficienza...")
            metrics = ROIEngine.calculate_savings()
            logger.info(f"[ROIWorker] Calcolo completato. Operazioni totali: {metrics.total_operations}")
            self.finished_signal.emit(metrics)
        except Exception as e:
            logger.exception("[ROIWorker] Errore durante il calcolo ROI")
            self.error_signal.emit(str(e))
