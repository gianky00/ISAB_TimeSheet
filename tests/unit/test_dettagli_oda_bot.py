"""
Unit tests for DettagliOdABot (Mocked).
"""
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from src.bots.dettagli_oda.bot import DettagliOdABot
from src.bots.dettagli_oda.pages.dettagli_oda_page import DettagliOdAPage

@pytest.fixture
def mock_driver(): return MagicMock()

@pytest.fixture
def dettagli_bot(mock_driver):
    with patch('src.bots.base.BaseBot.__init__', return_value=None):
        bot = DettagliOdABot("user", "pass")
        bot.driver = mock_driver
        bot.log = MagicMock()
        bot.download_path = ""
        bot._stop_requested = False
        return bot

class TestDettagliOdAPage:
    def test_navigate(self, mock_driver):
        page = DettagliOdAPage(mock_driver)
        page.wait = MagicMock()
        page._wait_for_overlay = MagicMock() # Speed up test
        assert page.navigate_to_dettagli() is True

    def test_process(self, mock_driver):
        page = DettagliOdAPage(mock_driver)
        page.wait = MagicMock()
        page._wait_for_overlay = MagicMock() # Avoid waiting for overlay in tests
        page._download = MagicMock(return_value=True)
        # Assuming process_oda(oda, contract, date_da, date_a, download_dir)
        # Mock the results count check
        count_label = MagicMock()
        count_label.text = "Trovati : 1"
        page.wait.until.return_value = count_label

        # Break infinite loop in _close_all_tabs by raising exception for close button
        def side_effect(*args, **kwargs):
            val = args[1] if len(args) > 1 else str(args[0])
            if "x-tab-close-btn" in str(val):
                raise Exception("No more tabs")
            return MagicMock()

        mock_driver.find_element.side_effect = side_effect

        assert page.process_oda("123", "C1", "01.01.2024", "01.01.2025", Path(".")) is True

class TestDettagliOdABot:
    @patch('src.bots.dettagli_oda.bot.DettagliOdAPage')
    def test_run(self, MockPage, dettagli_bot):
        page = MockPage.return_value
        page.navigate_to_dettagli.return_value = True
        page.setup_supplier.return_value = True
        page.process_oda.return_value = True

        res = dettagli_bot.run([{'numero_oda': '1', 'numero_contratto': 'C'}])
        assert res is True
