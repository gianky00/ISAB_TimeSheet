"""
Unit tests for CaricoTSBot.
"""
import pytest
from unittest.mock import MagicMock, patch
from src.bots.carico_ts.bot import CaricoTSBot
from src.bots.carico_ts.pages.carico_ts_page import CaricoTSPage

@pytest.fixture
def mock_driver(): return MagicMock()

@pytest.fixture
def carico_bot(mock_driver):
    with patch('src.bots.base.BaseBot.__init__', return_value=None):
        bot = CaricoTSBot("u", "p")
        bot.driver = mock_driver
        bot.log = MagicMock()
        bot._stop_requested = False
        return bot

class TestCaricoTSPage:
    @patch('src.bots.carico_ts.pages.carico_ts_page.ActionChains')
    def test_flow(self, MockActionChains, mock_driver):
        page = CaricoTSPage(mock_driver)
        page.wait = MagicMock()
        page._wait_overlay = MagicMock() # Mock overlay wait

        assert page.navigate() is True
        assert page.select_supplier("Sup") is True
        assert page.process_oda("123") is True

class TestCaricoTSBot:
    @patch('src.bots.carico_ts.bot.CaricoTSPage')
    def test_run(self, MockPage, carico_bot):
        page = MockPage.return_value
        page.navigate.return_value = True
        page.select_supplier.return_value = True
        page.process_oda.return_value = True

        # Test with single row (as per logic)
        res = carico_bot.run([{'numero_oda': '999'}])
        assert res is True
        page.process_oda.assert_called_with('999')
