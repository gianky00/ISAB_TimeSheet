"""
Timesheet Service
Coordinate the timesheet processing pipeline.
"""

from pathlib import Path

from src.core.timesheet.pipeline import TimesheetPipeline


class TimesheetService:
    def __init__(self) -> None:
        self.pipeline = TimesheetPipeline()

    def process_file(self, file_path: Path, dest_dir: Path) -> tuple[bool, str]:
        try:
            # Esecuzione pipeline
            result = self.pipeline.execute_pipeline(file_path, dest_dir)
        except Exception as e:
            return False, str(e)
        else:
            return True, f"Salvato in: {result.name}"
