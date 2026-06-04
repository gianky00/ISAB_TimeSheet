"""Modulo Pipeline."""

from pathlib import Path
from typing import Any

from src.application.services.processing.base import Pipeline
from src.application.services.processing.timesheet.steps import (
    ExtractMetadataStep,
    LoadWorkbookStep,
    SaveWorkbookStep,
    TransformSheetStep,
)


class TimesheetProcessingPipeline:
    """Pipeline per l'elaborazione dei file Timesheet.

    Inizializza la classe.
    """

    def __init__(self) -> None:
        self.pipeline = Pipeline()
        self.pipeline.add_step(LoadWorkbookStep())
        self.pipeline.add_step(ExtractMetadataStep())
        self.pipeline.add_step(TransformSheetStep())
        self.pipeline.add_step(SaveWorkbookStep())

    def execute(self, file_path: Path, dest_dir: Path) -> dict[str, Any]:
        """Esegue l'intera pipeline di elaborazione."""
        initial_context = {
            "file_path": file_path,
            "dest_dir": dest_dir,
        }
        return self.pipeline.run(initial_context)
