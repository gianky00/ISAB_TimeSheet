"""
SyncroJob - Timbrature Bot Coverage Boost (Corrected)
"""

from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.timbrature.bot import TimbratureBot


class TestTimbratureBotEnhanced:
    @pytest.fixture
    def bot(self, mocker):
        # BaseBot richiede username e password
        bot = TimbratureBot(username="user", password="pass")
        bot.driver = MagicMock()
        bot.wait = MagicMock()
        return bot

    def test_initialization(self, bot):
        assert bot.name == "Timbrature"

    @patch("src.bots.portale_fornitori.timbrature.bot.TimbraturePage")
    @patch("src.bots.portale_fornitori.timbrature.bot.TimbratureStorage")
    def test_run_full_cycle(self, mock_storage_cls, mock_page_cls, bot):
        mock_page = mock_page_cls.return_value
        mock_storage = mock_storage_cls.return_value

        mock_page.navigate_to_timbrature.return_value = True
        mock_page.set_filters.return_value = True
        mock_page.download_excel.return_value = "timbrature.xlsx"
        mock_storage.import_excel.return_value = (True, "OK", 10, 0)

        data = [{"data_da": "01.01.2024", "fornitore": "F1"}]
        res = bot.run(data)

        assert res is True
        mock_page.navigate_to_timbrature.assert_called_once()

    def test_validate_data(self, bot):
        assert bot.validate_data([{"data_da": "x", "fornitore": "y"}])[0] is True
