"""SyncroJob - Health Worker.

Worker asincrono per l'analisi della salute del sistema e la scansione dei log.
Evita il freeze della GUI durante l'elaborazione di analytics e diagnostica.
"""

import logging
from datetime import UTC, datetime

from PySide6.QtCore import QThread, Signal

from src.core.logging.analytics import generate_analytics_report
from src.core.logging.viewer import LogViewer

logger = logging.getLogger(__name__)


class HealthWorker(QThread):
    """Worker che esegue analisi pesanti sui log e calcola l'Health Score in background."""

    finished_signal = Signal(dict)
    error_signal = Signal(str)

    def __init__(self, hours: int = 24) -> None:
        """Inizializza il worker.

        Args:
          hours: Intervallo temporale di analisi (default 24h).
        """
        super().__init__()
        self.hours = hours

    def run(self) -> None:
        """Esegue la generazione del report analytics e l'ispezione log."""
        try:
            logger.info(f"[HealthWorker] Avvio analisi sistema (ultime {self.hours} ore)...")

            # 1. Generazione Report Analytics (CPU & I/O Bound)
            analytics_report = generate_analytics_report(hours=self.hours)

            # 2. Ispezione Log via LogViewer (I/O Bound)
            health_log_data = LogViewer().generate_health_report()

            # 3. Assemblaggio Risultato
            result = {
                "health_score": analytics_report.health_score,
                "anomalies": analytics_report.anomalies,
                "bot_runs_ok": health_log_data.get("bot_runs", {}).get("successful", 0),
                "bot_runs_fail": health_log_data.get("bot_runs", {}).get("failed", 0),
                "error_rate": health_log_data.get("error_rate_percent", 0),
                "timestamp": datetime.now(UTC).astimezone().strftime("%H:%M:%S"),
            }

            logger.info(f"[HealthWorker] Analisi completata. Score: {result['health_score']}%")
            self.finished_signal.emit(result)

        except Exception as e:
            logger.exception("[HealthWorker] Errore durante l'analisi di salute")
            self.error_signal.emit(str(e))
