"""Modulo Pipeline."""

from pathlib import Path
from typing import Any

from src.core.processing.base import Pipeline
from src.core.processing.timesheet.steps import (
    ExtractMetadataStep,
    LoadWorkbookStep,
    SaveWorkbookStep,
    TransformSheetStep,
)


class TimesheetProcessingPipeline:
    """Pipeline per l'elaborazione dei file Timesheet."""

    def __init__(self) -> None:
        """Inizializza la classe."""
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
