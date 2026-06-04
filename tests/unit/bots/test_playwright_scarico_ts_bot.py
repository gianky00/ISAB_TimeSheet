from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.infrastructure.bots.base import StepStatus
from src.infrastructure.bots.base.selenium_bot_config import SeleniumBotConfig
from src.infrastructure.bots.portale_fornitori.scarico_ts.playwright_bot import PlaywrightScaricaTSBot


class TestPlaywrightScaricaTSBot:
    @pytest.fixture
    def bot_config(self):
        return SeleniumBotConfig(username="user", password="pass", headless=True)

    @pytest.fixture
    def bot(self, bot_config):
        bot = PlaywrightScaricaTSBot(
            username="user",
            password="pass",
            config=bot_config,
            data_da="01/01/2023",
            fornitore="TEST_SUPPLIER",
            elabora_ts=False,
        )
        return bot

    def test_validate_data(self, bot):
        # Valido
        data = {"rows": [{"numero_oda": "123", "posizione_oda": "10"}], "fornitore": "TEST"}
        valid, msg = bot.validate_data(data)
        assert valid is True

        # Senza fornitore
        bot.fornitore = ""
        valid, msg = bot.validate_data({"rows": [1]})
        assert valid is False
        assert "Fornitore" in msg

        # Senza righe
        bot.fornitore = "TEST"
        valid, msg = bot.validate_data({"rows": []})
        assert valid is False
        assert "Nessun OdA" in msg

    @patch("src.infrastructure.bots.base.playwright_base_bot.sync_playwright")
    def test_run_success(self, mock_sync, bot):
        # Setup mocks per Playwright
        mock_pw = MagicMock()
        mock_sync.return_value.start.return_value = mock_pw
        mock_context = MagicMock()
        mock_pw.chromium.launch_persistent_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.pages = [mock_page]

        bot._init_driver()

        # Mocking internal steps
        with patch.object(bot, "_navigate_to_timesheet", return_value=True):
            with patch.object(bot, "_setup_filters", return_value=True):
                with patch.object(bot, "_process_oda_rows", return_value=(1, ["file.xlsx"])):
                    res = bot.run({"rows": [{"numero_oda": "1"}]})
                    assert res is True
                    # Verifica lo stato dello step 'download' (indice 3)
                    assert bot.step_manager._states[3] == StepStatus.COMPLETED

    @patch("src.infrastructure.bots.base.playwright_base_bot.sync_playwright")
    def test_run_failure_nav(self, mock_sync, bot):
        mock_pw = MagicMock()
        mock_sync.return_value.start.return_value = mock_pw
        mock_context = MagicMock()
        mock_pw.chromium.launch_persistent_context.return_value = mock_context
        mock_page = MagicMock()
        mock_context.pages = [mock_page]
        bot._init_driver()

        with patch.object(bot, "_navigate_to_timesheet", return_value=False):
            res = bot.run({"rows": [{"numero_oda": "1"}]})
            assert res is False
            # Verifica lo stato dello step 'nav' (indice 1)
            assert bot.step_manager._states[1] == StepStatus.ERROR

    def test_navigate_to_timesheet(self, bot):
        mock_page = MagicMock()
        bot.page = mock_page

        # Simula navigazione OK
        mock_page.wait_for_selector.return_value = MagicMock()
        assert bot._navigate_to_timesheet() is True

        # Simula errore
        mock_page.wait_for_selector.side_effect = Exception("Not found")
        assert bot._navigate_to_timesheet() is False

    def test_setup_filters(self, bot):
        mock_page = MagicMock()
        bot.page = mock_page

        # Patching _select_combobox_item (inherited from base)
        with patch.object(bot, "_select_combobox_item", return_value=True):
            assert bot._setup_filters() is True

    def test_search_oda_found(self, bot):
        mock_page = MagicMock()
        bot.page = mock_page
        mock_page.locator.return_value.is_visible.return_value = False  # Non vuoto

        assert bot._search_oda("123", "10") is True
        assert mock_page.wait_for_selector.called

    def test_search_oda_not_found(self, bot):
        mock_page = MagicMock()
        bot.page = mock_page
        mock_page.locator.return_value.is_visible.return_value = True  # Vuoto

        assert bot._search_oda("123", "10") is False

    @patch("src.application.services.timesheet_processor.TimesheetProcessor.process_and_move")
    def test_run_vba_processing(self, mock_vba, bot):
        mock_vba.return_value = (True, "OK")
        bot._run_vba_processing(["file1.xlsx", "file2.xlsx"], Path("/dest"))
        assert mock_vba.call_count == 2
