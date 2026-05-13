from collections.abc import Callable
from typing import Any

from src.core.data_synchronizer import DataSynchronizer
from src.core.database import db_manager
from src.core.importers.storico_oda import StoricoOdaImporter
from src.core.processing.base import ProcessingStep


class OdaExcelReadStep(ProcessingStep):
    """Passaggio per la lettura dei dati OdA dal file Excel."""

    def __init__(self, progress_callback: Callable[[int, int], None] | None = None, importer: Any = None) -> None:
        self.progress_callback = progress_callback
        self.importer = importer or StoricoOdaImporter

    def execute(self, context: dict[str, Any]) -> None:
        file_path = context.get("file_path")
        if not file_path:
            raise ValueError("file_path mancante nel contesto")

        success, message, imported_rows = self.importer.import_storico_oda(
            file_path, self.progress_callback
        )

        context["success"] = success
        context["message"] = message
        context["imported_rows"] = imported_rows

class OdaDatabaseSyncStep(ProcessingStep):
    """Passaggio per la sincronizzazione dei dati OdA con il database."""

    def __init__(self, synchronizer: Any = None) -> None:
        self.synchronizer = synchronizer or DataSynchronizer

    def execute(self, context: dict[str, Any]) -> None:
        if not context.get("success"):
            return

        imported_rows = context.get("imported_rows", [])

        total_added, total_removed = self.synchronizer.sync_storico_oda(
            db_manager.DB_STORICO_ODA, imported_rows
        )

        context["total_added"] = total_added
        context["total_removed"] = total_removed
        context["success"] = True
