from pathlib import Path
from unittest.mock import MagicMock, patch

from src.bots.base import StepStatus
from src.bots.portale_fornitori.timbrature.bot import TimbratureBot


class TestTimbratureBot:
    def test_initialization_defaults(self):
        bot = TimbratureBot()
        assert bot.fornitore == "SYNCROJOB"
        assert "01.01." in bot.data_da
        assert "31.12." in bot.data_a

    @patch("src.bots.portale_fornitori.timbrature.bot.TimbraturePage")
    @patch("src.bots.portale_fornitori.timbrature.bot.TimbratureStorage")
    def test_run_success_flow(self, mock_storage_class, mock_page_class):
        bot = TimbratureBot(username="u", password="p")
        bot.update_step = MagicMock()

        # MOCK DRIVER - Critical fix
        bot.driver = MagicMock()

        mock_page = mock_page_class.return_value
        mock_page.navigate_to_timbrature.return_value = True
        mock_page.download_timbrature.return_value = "report.xlsx"

        mock_storage = mock_storage_class.return_value
        # import_excel returns bool now
        mock_storage.import_excel.return_value = True

        # Mock file unlink
        with patch("src.bots.portale_fornitori.timbrature.bot.Path") as mock_path:
            mock_path.return_value.name = "report.xlsx"
            res = bot.run([])
            assert res is True
            assert mock_path.return_value.unlink.called

        assert mock_page.navigate_to_timbrature.called
        assert mock_page.download_timbrature.called
        assert mock_storage.import_excel.called
        bot.update_step.assert_any_call("import", StepStatus.COMPLETED)

    @patch("src.bots.portale_fornitori.timbrature.bot.TimbraturePage")
    def test_run_navigation_fail(self, mock_page_class):
        bot = TimbratureBot(username="u", password="p")
        bot.driver = MagicMock()

        mock_page = mock_page_class.return_value
        mock_page.navigate_to_timbrature.return_value = False

        res = bot.run([])
        assert res is False

    @patch("src.bots.portale_fornitori.timbrature.bot.TimbratureStorage")
    def test_import_to_db_static(self, mock_storage_class):
        mock_storage = mock_storage_class.return_value
        mock_storage.import_excel.return_value = True

        res = TimbratureBot.import_to_db_static("file.xlsx", Path("db.db"))
        assert res is True
        assert mock_storage_class.called
