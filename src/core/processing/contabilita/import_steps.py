"""Passaggi di elaborazione per l'importazione della contabilità."""

from collections.abc import Callable
from typing import Any

from src.core.data_synchronizer import DataSynchronizer
from src.core.database import db_manager
from src.core.importers.contabilita import ContabilitaImporter
from src.core.processing.base import ProcessingStep


class ExcelReadStep(ProcessingStep):
    """Passaggio per la lettura dei dati dal file Excel."""

    def __init__(
        self, progress_callback: Callable[[int, int], None] | None = None, importer: Any = None
    ) -> None:
        """Inizializza il passaggio con i callback e l'importer specificato."""
        self.progress_callback = progress_callback
        self.importer = importer or ContabilitaImporter

    def execute(self, context: dict[str, Any]) -> None:
        """Esegue la lettura del file Excel."""
        file_path = context.get("file_path")
        if not file_path:
            raise ValueError("file_path mancante nel contesto")

        success, message, imported_rows, imported_years = self.importer.import_contabilita_dati(
            file_path, self.progress_callback
        )

        context["success"] = success
        context["message"] = message
        context["imported_rows"] = imported_rows
        context["imported_years"] = imported_years


class DatabaseSyncStep(ProcessingStep):
    """Passaggio per la sincronizzazione dei dati con il database."""

    def __init__(self, synchronizer: Any = None) -> None:
        """Inizializza il passaggio con il sincronizzatore specificato."""
        self.synchronizer = synchronizer or DataSynchronizer

    def execute(self, context: dict[str, Any]) -> None:
        """Esegue la sincronizzazione del database."""
        if not context.get("success"):
            return

        imported_rows = context.get("imported_rows", [])
        imported_years = context.get("imported_years", [])

        total_added, total_removed = self.synchronizer.sync_contabilita_dati(
            db_manager.DB_CONTABILITA, imported_rows, imported_years
        )

        context["total_added"] = total_added
        context["total_removed"] = total_removed
        context["success"] = True
