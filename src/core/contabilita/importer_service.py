"""SyncroJob - Contabilita Importer Service.

Servizio per il coordinamento delle operazioni di importazione dati della Contabilità.
"""

from collections.abc import Callable
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path

from src.core.data_synchronizer import DataSynchronizer
from src.core.database import db_manager
from src.core.excel_importer import ExcelImporter
from src.core.logging import get_logger
from src.core.processing.base import Pipeline
from src.core.processing.contabilita.import_steps import DatabaseSyncStep, ExcelReadStep

logger = get_logger(__name__)


class ContabilitaImporterService:
    """Servizio per la gestione dell'importazione Excel nel database della Contabilità."""

    @classmethod
    def scan_workload(cls, file_path: str, giornaliere_path: str) -> tuple[int, int]:
        """Scansiona rapidamente il carico di lavoro per stima ETA."""
        return ExcelImporter.scan_workload(file_path, giornaliere_path)

    @classmethod
    def import_main_data(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Importa i dati della Tabella Dati utilizzando la Pipeline."""
        pipeline = Pipeline()
        pipeline.add_step(ExcelReadStep(progress_callback, importer=ExcelImporter))
        pipeline.add_step(DatabaseSyncStep(synchronizer=DataSynchronizer))

        context = {"file_path": file_path}

        try:
            result = pipeline.run(context)
            return (
                result.get("success", False),
                result.get("message", ""),
                result.get("total_added", 0),
                result.get("total_removed", 0),
            )
        except Exception:
            logger.exception("Errore nella pipeline di importazione Excel")
            return False, "Errore critico pipeline", 0, 0

    @classmethod
    def import_giornaliere(
        cls,
        root_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Scansione e importa i dati dalle cartelle delle giornaliere."""
        root = Path(root_path)
        if not root.exists():
            return False, "Directory Giornaliere non trovata.", 0, 0

        current_year = datetime.now(UTC).year

        try:
            # 1. Lookup Map Preparation (Estrae mapping ODC da Tabella Dati)
            lookup_map = cls._prepare_odc_lookup_map()

            # 2. Import Giornaliere data via ExcelImporter
            (
                success,
                message,
                all_new_rows,
                years_encountered,
            ) = ExcelImporter.import_giornaliere(root_path, lookup_map, progress_callback)

            if not success:
                return False, message, 0, 0

            # 3. Synchronize with database via DataSynchronizer
            total_added, total_removed = DataSynchronizer.sync_giornaliere(
                db_manager.DB_CONTABILITA, all_new_rows, years_encountered
            )

            if not years_encountered and not all_new_rows:
                return (
                    True,
                    f"Nessuna nuova giornaliera trovata (check anno >= {current_year}).",
                    0,
                    0,
                )

            return (
                True,
                f"Importate Giornaliere per anni: {sorted(set(years_encountered))}",
                total_added,
                total_removed,
            )

        except Exception as e:
            logger.exception("Errore importazione Giornaliere")
            return False, f"Errore importazione Giornaliere: {e}", 0, 0

    @staticmethod
    def _prepare_odc_lookup_map() -> dict[str, str]:
        """Prepara una mappa n_prev -> odc per arricchire le giornaliere."""
        lookup_map = {}
        with (
            suppress(Exception),
            db_manager.get_connection(db_manager.DB_CONTABILITA, read_only=True) as conn,
        ):
            lookup_query = "SELECT n_prev, odc FROM contabilita WHERE odc IS NOT NULL AND odc != ''"
            cursor = conn.cursor()
            cursor.execute(lookup_query)
            rows = cursor.fetchall()
            lookup_map = {row[0]: row[1] for row in rows if row[0]}
        return lookup_map

    @classmethod
    def import_attivita_programmate(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Importa il file Attività Programmate."""
        success, message, imported_rows = ExcelImporter.import_attivita_programmate(
            file_path, progress_callback
        )
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_attivita_programmate(
            db_manager.DB_CONTABILITA, imported_rows
        )
        return True, message, total_added, total_removed

    @classmethod
    def import_scarico_ore(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Importa il file Scarico Ore Cantiere."""
        success, message, imported_rows = ExcelImporter.import_scarico_ore(file_path, progress_callback)
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_scarico_ore(
            db_manager.DB_CONTABILITA, imported_rows
        )
        return True, message, total_added, total_removed

    @classmethod
    def import_certificati_campione(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, int, int]:
        """Importa il file Certificati Campione."""
        from src.core.importers.certificati import CertificatiImporter  # noqa: PLC0415

        success, message, imported_rows = CertificatiImporter.import_certificati_campione(
            file_path, progress_callback
        )
        if not success:
            return False, message, 0, 0

        total_added, total_removed = DataSynchronizer.sync_certificati_campione(
            db_manager.DB_CONTABILITA, imported_rows
        )
        return True, f"Importati {len(imported_rows)} certificati.", total_added, total_removed
