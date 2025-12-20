"""
Unit tests for ScaricoTSBot logic (Mocked).
"""
import pytest
from unittest.mock import MagicMock, patch, ANY
from pathlib import Path

from src.bots.scarico_ts.scarico_ts_bot import ScaricaTSBot
from src.bots.scarico_ts.pages.scarico_ts_page import ScaricoTSPage

@pytest.fixture
def mock_driver():
    return MagicMock()

@pytest.fixture
def scarico_bot(mock_driver):
    with patch('src.bots.base.BaseBot.__init__', return_value=None):
        bot = ScaricaTSBot(username="test", password="pwd")
        bot.driver = mock_driver
        bot.log = MagicMock()
        bot.download_path = ""
        bot._stop_requested = False
        return bot

class TestScaricoTSPage:

    def test_navigate_success(self, mock_driver):
        page = ScaricoTSPage(mock_driver)
        page.wait = MagicMock()
        page._wait_for_overlay = MagicMock()

        assert page.navigate_to_timesheet() is True
        assert page.wait.until.call_count >= 2 # Report + Timesheet

    @patch('src.bots.scarico_ts.pages.scarico_ts_page.ActionChains')
    def test_setup_filters_success(self, MockActionChains, mock_driver):
        page = ScaricoTSPage(mock_driver)
        page.wait = MagicMock()
        page.long_wait = MagicMock()

        assert page.setup_filters("Supplier", "01.01.2025") is True

    def test_search_download_success(self, mock_driver):
        page = ScaricoTSPage(mock_driver)
        page.wait = MagicMock()
        page._download_excel = MagicMock(return_value=True)

        assert page.search_and_download("123", "1", Path(".")) is True
        mock_driver.execute_script.assert_called()

class TestScaricoTSBot:

    @patch('src.bots.scarico_ts.scarico_ts_bot.ScaricoTSPage')
    def test_run_success(self, MockPage, scarico_bot):
        page_instance = MockPage.return_value
        page_instance.navigate_to_timesheet.return_value = True
        page_instance.setup_filters.return_value = True
        page_instance.search_and_download.return_value = True

        data = [{'numero_oda': '123', 'posizione_oda': '1'}]
        result = scarico_bot.run(data)

        assert result is True
        page_instance.navigate_to_timesheet.assert_called_once()
        page_instance.search_and_download.assert_called_once()
