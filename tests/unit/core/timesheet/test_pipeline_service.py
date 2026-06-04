from pathlib import Path
from unittest.mock import patch

from src.application.services.timesheet.pipeline import TimesheetPipeline
from src.application.services.timesheet.service import TimesheetService


class TestTimesheetPipelineAndService:
    @patch("src.application.services.timesheet.pipeline.LoadWorkbookStep.execute")
    @patch("src.application.services.timesheet.pipeline.TransformSheetStep.execute")
    @patch("src.application.services.timesheet.pipeline.SaveWorkbookStep.execute")
    @patch("src.application.services.timesheet.pipeline.CleanupStep.execute")
    def test_pipeline_execution(self, mock_cleanup, mock_save, mock_transform, mock_load):
        # Setup context return
        def side_effect(context):
            context["dest_path"] = Path("/dest/processed.xlsx")
            return context

        mock_save.side_effect = side_effect

        pipeline = TimesheetPipeline()
        res_path = pipeline.execute_pipeline(Path("src.xlsx"), Path("/dest"))

        assert res_path == Path("/dest/processed.xlsx")
        assert mock_load.called
        assert mock_transform.called
        assert mock_save.called
        assert mock_cleanup.called

    @patch("src.application.services.timesheet.service.TimesheetPipeline.execute_pipeline")
    def test_service_process_file_success(self, mock_exec):
        mock_exec.return_value = Path("/dest/file.xlsx")

        service = TimesheetService()
        success, msg = service.process_file(Path("src.xlsx"), Path("/dest"))

        assert success is True
        assert "file.xlsx" in msg

    @patch("src.application.services.timesheet.service.TimesheetPipeline.execute_pipeline")
    def test_service_process_file_failure(self, mock_exec):
        mock_exec.side_effect = Exception("Crash")

        service = TimesheetService()
        success, msg = service.process_file(Path("src.xlsx"), Path("/dest"))

        assert success is False
        assert "Crash" in msg
