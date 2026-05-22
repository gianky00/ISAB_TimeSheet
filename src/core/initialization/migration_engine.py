"""Database Migration Engine.

Gestisce l'inizializzazione del database SQLite e il backup post-migrazione in sicurezza.
"""

from collections.abc import Callable

from src.core.database import db_manager
from src.core.database.backup_manager import DatabaseBackupManager
from src.core.logging import get_logger

logger = get_logger("DatabaseMigrationEngine")


class DatabaseMigrationEngine:
    """Motore delegato per l'inizializzazione del database e gestione dello schema SQLite."""

    @staticmethod
    def initialize_database(step_callback: Callable[[str, int], None]) -> None:
        """Inizializza l'engine SQLite3, crea le tabelle ed esegue il backup preventivo."""
        step_callback("Inizializzazione Engine SQLite3...", 34)
        try:
            db_manager.init_db()

            step_callback("Creazione Backup di Sicurezza Database...", 37)
            DatabaseBackupManager.execute_backup()
            logger.info("Database inizializzato ed eseguito backup di sicurezza con successo.")
        except Exception:
            logger.exception("Errore critico durante l'inizializzazione del database")
            raise
