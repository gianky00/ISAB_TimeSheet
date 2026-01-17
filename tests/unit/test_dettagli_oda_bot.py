from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.dettagli_oda.bot import DettagliOdABot
from src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page import (
    DettagliOdAPage,
)


@pytest.fixture
def mock_driver():
    return MagicMock()


@pytest.fixture
def dettagli_bot(mock_driver):
    with patch("src.bots.base.BaseBot.__init__", return_value=None):
        bot = DettagliOdABot("u", "p")
        bot.driver = mock_driver
        bot.log = MagicMock()
        bot.download_path = "."  # Add missing attribute
        bot._stop_requested = False
        return bot


class TestDettagliOdAPage:
    def test_process(self, mock_driver):
        page = DettagliOdAPage(mock_driver)
        page.wait = MagicMock()
        page._wait_for_overlay = MagicMock()  # Avoid waiting for overlay in tests
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

        assert page.process_oda("123", "C1", "01.01.2024", "01.01.2025", Path("."), Path(".")) is True


class TestDettagliOdABot:
    @patch("src.bots.portale_fornitori.dettagli_oda.bot.DettagliOdAPage")
    def test_run_empty_rows(self, MockPage, dettagli_bot):
        page_instance = MockPage.return_value
        page_instance.navigate_to_dettagli.return_value = True
        page_instance.setup_supplier.return_value = True
        page_instance.process_oda.return_value = True

        # Test with empty rows list
        result = dettagli_bot.run(
            {
                "rows": [],
                "fornitore": "Forn",
                "data_da": "01.01.2024",
                "data_a": "01.01.2025",
            }
        )

        assert result is True
        # process_oda should have been called once with empty oda/contract
        page_instance.process_oda.assert_called_once()
        args = page_instance.process_oda.call_args[0]
        assert args[0] == ""  # oda
        assert args[1] == ""  # contract
