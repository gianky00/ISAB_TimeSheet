from unittest.mock import patch

from src.core.timesheet_processor import TimesheetProcessor


class TestTimesheetProcessorSimple:
    """Test suite per TimesheetProcessor (VBA Replacement)."""

    @patch("src.core.timesheet_processor.TimesheetProcessingPipeline")
    def test_process_file_logic(self, mock_pipeline_class, tmp_path):
        # Create a real file on disk
        file_path = tmp_path / "fake.xlsx"
        file_path.write_text("dummy")
        dest_dir = tmp_path / "dest"
        dest_dir.mkdir()

        # Setup mock pipeline
        mock_pipeline = mock_pipeline_class.return_value
        mock_pipeline.execute.return_value = {"success": True, "dest_path": dest_dir / "processed.xlsx"}

        # Execution
        success, msg = TimesheetProcessor.process_and_move(file_path, dest_dir)

        # Verification
        assert success is True
        assert "Salvato in" in msg
        mock_pipeline.execute.assert_called_once_with(file_path, dest_dir)
        # Check source unlinked (mocked resolve to avoid issues)
        assert not file_path.exists()
