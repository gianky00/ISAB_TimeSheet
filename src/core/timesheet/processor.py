"""Timesheet Module Facade.

Maintains backward compatibility for the existing TimesheetProcessor API.
"""

from pathlib import Path

from src.core.timesheet.service import TimesheetService


class TimesheetProcessor:
    """Facade class for Timesheet processing.

    Delegates to the new architecture while preserving original API.
    """

    @staticmethod
    def process_and_move(file_path: Path, dest_dir: Path) -> tuple[bool, str]:
        """Elabora il file Excel delegando al nuovo servizio."""
        return TimesheetService().process_file(file_path, dest_dir)
