"""
SyncroJob - Database Maintenance Worker
Worker asincrono per l'ottimizzazione e manutenzione periodica dei database SQLite.
"""

import logging
from pathlib import Path
from threading import Thread

from src.core.database import db_manager

logger = logging.getLogger(__name__)


class DatabaseMaintenanceWorker(Thread):
    """
    Worker in background per eseguire operazioni di manutenzione come VACUUM e ANALYZE.
    """

    def __init__(self) -> None:
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
        """Esegue la manutenzione su tutti i database configurati."""
        logger.info("[Maintenance] Avvio manutenzione database in background...")
        for db_path in self.databases:
            if not db_path.exists():
                continue

            try:
                self._optimize_db(db_path)
            except Exception:
                logger.exception(f"[Maintenance] Errore ottimizzazione {db_path.name}")

        logger.info("[Maintenance] Manutenzione database completata.")

    def _optimize_db(self, db_path: Path) -> None:
        """Esegue VACUUM e ANALYZE sul database specificato."""
        logger.info(f"[Maintenance] Ottimizzazione {db_path.name}...")

        # Tentativo di acquisizione lock di scrittura
        with db_manager.get_write_connection(db_path) as conn:
            conn.execute("ANALYZE")
            conn.execute("VACUUM")

        logger.info(f"[Maintenance] {db_path.name} ottimizzato.")
