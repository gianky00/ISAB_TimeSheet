"""
SyncroJob - Oda Manager
Gestione dell'importazione e archiviazione Storico OdA.
"""

from typing import Callable, Optional, Tuple

from src.core.config_manager import CONFIG_DIR
from src.core.data_synchronizer import DataSynchronizer
from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter


class OdaManager:
    """Manager per la gestione del database Storico OdA."""

    DB_PATH = CONFIG_DIR / "data" / "storico_oda.db"

    @classmethod
    def init_db(cls):
        """Inizializza il database tramite DatabaseManager."""
        db_manager.init_db()

    @classmethod
    def import_oda_from_excel(
        cls,
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, int, int]:
        """Importa i dati dal file Excel Storico OdA."""
        import time

        from src.core.sync_tracker import SyncTracker

        start_time = time.time()

        success, message, imported_rows = ExcelImporter.import_storico_oda(
            file_path, progress_callback
        )
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_storico_oda(
            cls.DB_PATH, imported_rows
        )

        duration = time.time() - start_time
        SyncTracker.update_status("storico_oda", total_added, total_removed, duration)

        return True, message, total_added, total_removed
