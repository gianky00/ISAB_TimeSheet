"""SyncroJob - Database Maintenance Worker.

Worker asincrono per l'ottimizzazione e manutenzione periodica dei database SQLite e pulizia log/file.
"""

import logging
from datetime import UTC, datetime, timedelta
from pathlib import Path
from threading import Thread

from src.core.database import db_manager
from src.core.paths import LOGS_DIR

logger = logging.getLogger(__name__)


class DatabaseMaintenanceWorker(Thread):
    """Worker in background per eseguire operazioni di manutenzione database e pulizia file."""

    def __init__(self) -> None:
        """Inizializza la classe."""
        super().__init__(daemon=True, name="DatabaseMaintenanceWorker")
        self.databases = [
            db_manager.DB_CONTABILITA,
            db_manager.DB_TIMBRATURE,
            db_manager.DB_PDL,
            db_manager.DB_STORICO_ODA,
            db_manager.DB_DIPENDENTI,
            db_manager.DB_CERTIFICATI,
            db_manager.DB_SCARICO_ORE,
            db_manager.DB_GIORNALIERE,
            db_manager.DB_AUDIT,
        ]

    def run(self) -> None:
        """Esegue la manutenzione su tutti i database e pulizia file configurati."""
        logger.info("[Maintenance] Avvio operazioni di manutenzione e pulizia...")

        # 1. Manutenzione DB
        for db_path in self.databases:
            if db_path.exists():
                try:
                    self._optimize_db(db_path)
                except Exception:
                    logger.exception(f"[Maintenance] Errore ottimizzazione {db_path.name}")

        # 2. Pulizia Log (mantieni ultimi 30 giorni)
        self._clean_logs(days=30)

        logger.info("[Maintenance] Manutenzione e pulizia completate.")

    def _optimize_db(self, db_path: Path) -> None:
        """Esegue VACUUM e ANALYZE sul database specificato."""
        logger.info(f"[Maintenance] Ottimizzazione {db_path.name}...")
        with db_manager.get_write_connection(db_path) as conn:
            conn.execute("ANALYZE")
            conn.execute("VACUUM")
        logger.info(f"[Maintenance] {db_path.name} ottimizzato.")

    def _clean_logs(self, days: int) -> None:
        """Elimina i file di log più vecchi della soglia specificata."""
        if not LOGS_DIR.exists():
            return

        logger.info(f"[Maintenance] Pulizia log più vecchi di {days} giorni...")
        cutoff = datetime.now(UTC) - timedelta(days=days)

        for log_file in LOGS_DIR.glob("*.log"):
            try:
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime, tz=UTC)
                if file_time < cutoff:
                    log_file.unlink()
                    logger.debug(f"[Maintenance] Rimosso log obsoleto: {log_file.name}")
            except Exception:
                logger.exception(f"[Maintenance] Errore rimozione log {log_file.name}")
