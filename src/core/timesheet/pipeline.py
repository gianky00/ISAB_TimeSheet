from pathlib import Path
from typing import Any, cast

from src.core.processing.base import Pipeline
from src.core.timesheet.steps.excel_steps import (
    CleanupStep,
    LoadWorkbookStep,
    SaveWorkbookStep,
    TransformSheetStep,
)


class TimesheetPipeline(Pipeline):
    def __init__(self) -> None:
        super().__init__()
        self.add_step(LoadWorkbookStep())
        self.add_step(TransformSheetStep())
        self.add_step(SaveWorkbookStep())
        self.add_step(CleanupStep())

    def execute_pipeline(self, file_path: Path, dest_dir: Path) -> Path:
        context: dict[str, Any] = {"file_path": file_path, "dest_dir": dest_dir}
        result_context = super().run(context)
        return cast("Path", result_context["dest_path"])
