from unittest.mock import MagicMock, patch

from src.infrastructure.bots.base import StepStatus
from src.infrastructure.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot


class TestScaricaTSBot:
    def test_validate_data_missing_fornitore(self):
        bot = ScaricaTSBot(username="u", password="p", fornitore="")
        valid, msg = bot.validate_data([{"numero_oda": "123"}])
        assert valid is False
        assert "Fornitore non specificato" in msg

    def test_validate_data_empty_rows(self):
        bot = ScaricaTSBot(username="u", password="p", fornitore="COEMI")
        valid, msg = bot.validate_data([])
        assert valid is False
        assert "Nessun dato da elaborare" in msg

    def test_validate_data_success(self):
        bot = ScaricaTSBot(username="u", password="p", fornitore="COEMI")
        valid, _msg = bot.validate_data([{"numero_oda": "123"}])
        assert valid is True

    @patch("src.infrastructure.bots.portale_fornitori.scarico_ts.bot.ScaricaTSBot._setup_timesheet_view")
    @patch("src.infrastructure.bots.portale_fornitori.scarico_ts.bot.ScaricaTSBot._process_oda_rows")
    @patch("src.infrastructure.bots.portale_fornitori.scarico_ts.bot.ScaricaTSBot._handle_vba_processing")
    def test_run_success_flow(self, mock_vba, mock_process, mock_setup):
        bot = ScaricaTSBot(fornitore="COEMI", elabora_ts=True)
        bot.update_step = MagicMock()

        mock_setup.return_value = True
        mock_process.return_value = (1, ["file1.xlsx"])

        data = [{"numero_oda": "ODA1"}]
        res = bot.run(data)

        assert res is True
        assert mock_setup.called
        assert mock_process.called
        assert mock_vba.called
        # Check step updates
        bot.update_step.assert_any_call("login", StepStatus.COMPLETED)
        bot.update_step.assert_any_call("download", StepStatus.COMPLETED)

    @patch("src.infrastructure.bots.portale_fornitori.scarico_ts.bot.ScaricaTSBot._setup_timesheet_view")
    def test_run_setup_fail(self, mock_setup):
        bot = ScaricaTSBot(fornitore="COEMI")
        mock_setup.return_value = False

        res = bot.run([{"oda": "1"}])
        assert res is False

    def test_get_final_download_path(self, tmp_path):
        bot = ScaricaTSBot(elabora_ts=False)
        dest_dir = tmp_path / "dest"
        source_dir = tmp_path / "source"

        path = bot._get_final_download_path(source_dir, dest_dir, "ODA123", "10", ".xlsx")
        assert path == dest_dir / "TS_ODA123-10.xlsx"

        # Test naming without pos
        path_no_pos = bot._get_final_download_path(source_dir, dest_dir, "ODA456", "", ".xls")
        assert path_no_pos == dest_dir / "TS_ODA456.xls"

    def test_move_to_destination_success(self, tmp_path):
        bot = ScaricaTSBot()
        src = tmp_path / "src.txt"
        src.write_text("content")
        dest = tmp_path / "sub" / "dest.txt"

        res = bot._move_to_destination(src, dest)
        assert res == dest
        assert dest.exists()
        assert not src.exists()

    @patch("src.infrastructure.bots.portale_fornitori.scarico_ts.bot.TimesheetProcessor.process_and_move")
    def test_handle_vba_processing(self, mock_processor, tmp_path):
        bot = ScaricaTSBot()
        bot.update_step = MagicMock()
        mock_processor.return_value = (True, "Processed")

        bot._handle_vba_processing(["file1.xlsx"], tmp_path)
        assert mock_processor.called
        bot.update_step.assert_any_call("process", StepStatus.COMPLETED)
