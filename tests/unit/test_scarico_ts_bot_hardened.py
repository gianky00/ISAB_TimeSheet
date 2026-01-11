
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot


class TestScaricaTSBotHardened:

    @pytest.fixture
    def bot(self, mock_driver):
        # We need to mock the super().__init__ calls that might try to init driver
        with patch("src.bots.base.base_bot.BaseBot._init_driver", return_value=mock_driver):
            bot = ScaricaTSBot(username="test_user", password="test_password", fornitore="TEST_VENDOR")
            bot.driver = mock_driver
            # Manually set waits to our mocks
            bot.wait = MagicMock()
            bot.long_wait = MagicMock()
            return bot

    def test_navigate_to_timesheet_success(self, bot):
        """Test the navigation flow to the timesheet page."""
        # Setup: mock wait.until to return a mock element (clickable)
        mock_el = MagicMock()
        bot.wait.until.return_value = mock_el

        # We also need to mock _attendi_scomparsa_overlay which is in BaseBot
        with patch.object(ScaricaTSBot, "_attendi_scomparsa_overlay"):
            success = bot._navigate_to_timesheet()

        assert success is True
        # Verify calls to wait.until
        assert bot.wait.until.call_count >= 2
        # Check if it looked for 'Report' and 'Timesheet'
        # calls[0] is the EC.element_to_be_clickable for Report
        # calls[1] is the EC.element_to_be_clickable for Timesheet
        # calls[2] is the visibility check for fornitore dropdown

    def test_setup_filters_success(self, bot):
        """Test the filter setup logic (Vendor selection and Date)."""
        bot.fornitore = "VENDOR_XYZ"
        bot.data_da = "10.01.2026"

        mock_el = MagicMock()
        bot.wait.until.return_value = mock_el
        bot.long_wait.until.return_value = mock_el

        with patch.object(ScaricaTSBot, "_attendi_scomparsa_overlay"):
                success = bot._setup_filters()

        assert success is True
        # Verify that send_keys was called with the date
        mock_el.send_keys.assert_called_with("10.01.2026")

    def test_run_loop_handles_exception_and_continues(self, bot):
        """Test that run() continues to next row if one fails."""
        data = [
            {"numero_oda": "ODA1", "posizione_oda": "10"},
            {"numero_oda": "ODA2", "posizione_oda": "20"}
        ]

        # Mock dependencies to return success for first and fail for second (or viceversa)
        with patch.object(bot, "_navigate_to_timesheet", return_value=True):
            with patch.object(bot, "_setup_filters", return_value=True):
                # Mock _download_excel: fail first, succeed second
                with patch.object(bot, "_download_excel") as mock_download:
                    mock_download.side_effect = [Exception("Crashed"), Path("test.xlsx")]

                    # We also need to mock the UI interactions inside the loop
                    bot.wait.until.return_value = MagicMock()

                    success = bot.run(data)

                    # Should be false because not ALL rows succeeded (success_count == len(rows))
                    assert success is False
                    assert mock_download.call_count == 2
