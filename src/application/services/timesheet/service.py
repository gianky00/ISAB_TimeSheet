"""Timesheet Service.

Coordinate the timesheet processing pipeline.
"""

from pathlib import Path

from src.application.services.timesheet.pipeline import TimesheetPipeline


class TimesheetService:
    """Servizio per il processamento dei file Timesheet."""

    def __init__(self) -> None:
        self.pipeline = TimesheetPipeline()

    def process_file(self, file_path: Path, dest_dir: Path) -> tuple[bool, str]:
        """Processa un singolo file Excel Timesheet."""
        try:
            # Esecuzione pipeline
            result = self.pipeline.execute_pipeline(file_path, dest_dir)
        except Exception as e:
            return False, str(e)
        else:
            return True, f"Salvato in: {result.name}"
