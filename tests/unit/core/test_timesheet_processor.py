from pathlib import Path
from unittest.mock import patch

from src.core.timesheet_processor import TimesheetProcessor


class TestTimesheetProcessor:
    @patch("src.core.timesheet_processor.TimesheetProcessingPipeline")
    def test_process_and_move_success(self, mock_pipeline_class, fs):
        src = Path("/src/test.xlsx")
        dest_dir = Path("/dest")
        fs.create_file(str(src))
        fs.create_dir(str(dest_dir))

        mock_pipeline = mock_pipeline_class.return_value
        dest_path = dest_dir / "processed.xlsx"
        mock_pipeline.execute.return_value = {"dest_path": dest_path, "is_empty": False}

        # Simula creazione file destinazione (per cleanup logic)
        fs.create_file(str(dest_path))

        success, msg = TimesheetProcessor.process_and_move(src, dest_dir)

        assert success is True
        assert "processed.xlsx" in msg
        assert not src.exists()  # Verifichiamo il cleanup

    @patch("src.core.timesheet_processor.TimesheetProcessingPipeline")
    def test_process_and_move_empty(self, mock_pipeline_class, fs):
        src = Path("/src/empty.xlsx")
        fs.create_file(str(src))

        mock_pipeline = mock_pipeline_class.return_value
        mock_pipeline.execute.return_value = {"is_empty": True}

        success, msg = TimesheetProcessor.process_and_move(src, Path("/dest"))
        assert success is False
        assert "EMPTY" in msg

    def test_process_and_move_not_found(self):
        success, msg = TimesheetProcessor.process_and_move(Path("missing.xlsx"), Path("."))
        assert success is False
        assert "non trovato" in msg

    def test_cleanup_source(self, fs):
        src = Path("/src/f1.txt")
        dest = Path("/dest/f1.txt")
        fs.create_file(str(src))
        fs.create_file(str(dest))

        TimesheetProcessor._cleanup_source(src, dest)
        assert not src.exists()

        # Se sono uguali non cancella
        fs.create_file(str(src))
        TimesheetProcessor._cleanup_source(src, src)
        assert src.exists()

    def test_clean_pos_value(self):
        # Test diretto tramite ExtractMetadataStep (alias)
        res = TimesheetProcessor._clean_pos_value("  10  ")
        assert res == "10"
        assert TimesheetProcessor._clean_pos_value("10.0") == "10"
        assert TimesheetProcessor._clean_pos_value(None) == ""
