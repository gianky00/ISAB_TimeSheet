"""
Unit tests for BaseBot logic (Mocked).
"""

from unittest.mock import MagicMock, patch

import pytest

from src.bots.base.base_bot import BaseBot, BotStatus


class ConcreteBot(BaseBot):
    """Concrete implementation for testing."""

    @property
    def name(self):
        return "TestBot"

    @property
    def description(self):
        return "Test Description"

    def run(self, data):
        return True

    def _handle_unsaved_changes_popup(self):
        pass


@pytest.fixture
def base_bot():
    return ConcreteBot("user", "pass", headless=True)


class TestBaseBotLogic:
    @patch("selenium.webdriver.Chrome")
    @patch("webdriver_manager.chrome.ChromeDriverManager.install")
    def test_init_driver(self, mock_install, mock_chrome, base_bot):
        """Should initialize driver with correct options."""
        # Mock options to track add_argument calls
        mock_options = MagicMock()
        with patch("src.bots.base.base_bot.Options", return_value=mock_options):
            base_bot._init_driver()

        assert base_bot.status == BotStatus.INITIALIZING
        mock_chrome.assert_called()

        # Verify critical options via add_argument calls
        add_argument_calls = [
            call[0][0] for call in mock_options.add_argument.call_args_list
        ]

        # Check headless mode (since base_bot.headless=True)
        assert any("--headless=new" in arg for arg in add_argument_calls)
        assert any("--disable-notifications" in arg for arg in add_argument_calls)
        assert any("--no-restore-session-state" in arg for arg in add_argument_calls)

        # Verify user-data-dir uses config_manager path
        user_data_arg = next(
            (arg for arg in add_argument_calls if "user-data-dir=" in arg), None
        )
        assert user_data_arg is not None
        # It should contain syncrojob (part of the config dir path)
        assert "syncrojob" in user_data_arg.lower()

    def test_check_stop_raises(self, base_bot):
        """Should raise InterruptedError if stop requested."""
        base_bot.request_stop()
        with pytest.raises(InterruptedError):
            base_bot._check_stop()

    def test_verify_login_url(self, base_bot):
        """Should delegate to login_page."""
        base_bot.login_page = MagicMock()

        base_bot.login_page._verify_logged_in_via_ui.return_value = False
        assert base_bot._verify_login() is False

        base_bot.login_page._verify_logged_in_via_ui.return_value = True
        assert base_bot._verify_login() is True
