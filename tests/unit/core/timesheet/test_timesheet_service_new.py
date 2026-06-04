from pathlib import Path
from unittest.mock import patch

from src.application.services.timesheet.pipeline import TimesheetPipeline
from src.application.services.timesheet.service import TimesheetService


class TestTimesheetService:
    @patch("src.application.services.timesheet.service.TimesheetPipeline.execute_pipeline")
    def test_process_file_success(self, mock_exec):
        mock_exec.return_value = Path("/dest/processed.xlsx")
        service = TimesheetService()

        success, msg = service.process_file(Path("src.xlsx"), Path("/dest"))

        assert success is True
        assert "processed.xlsx" in msg

    @patch(
        "src.application.services.timesheet.service.TimesheetPipeline.execute_pipeline",
        side_effect=ValueError("Invalid file"),
    )
    def test_process_file_error(self, mock_exec):
        service = TimesheetService()
        success, msg = service.process_file(Path("src.xlsx"), Path("/dest"))

        assert success is False
        assert "Invalid file" in msg


class TestTimesheetPipeline:
    @patch("src.application.services.timesheet.pipeline.LoadWorkbookStep")
    @patch("src.application.services.timesheet.pipeline.TransformSheetStep")
    @patch("src.application.services.timesheet.pipeline.SaveWorkbookStep")
    @patch("src.application.services.timesheet.pipeline.CleanupStep")
    def test_execute_pipeline(self, mock_clean, mock_save, mock_trans, mock_load):
        # Setup mock steps
        def mock_save_exec(ctx):
            ctx["dest_path"] = Path("/dest/out.xlsx")
            ctx["success"] = True

        mock_save.return_value.execute.side_effect = mock_save_exec

        pipeline = TimesheetPipeline()
        res = pipeline.execute_pipeline(Path("in.xlsx"), Path("/dest"))

        assert res == Path("/dest/out.xlsx")
        assert mock_load.return_value.execute.called
        assert mock_trans.return_value.execute.called
        assert mock_save.return_value.execute.called
        assert mock_clean.return_value.execute.called
