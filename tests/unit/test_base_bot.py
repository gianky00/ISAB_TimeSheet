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
        """Should initialize driver with correct Chrome setup."""
        # Mock _get_chrome_options and verify it's called + Chrome is instantiated
        mock_options = MagicMock()

        with patch.object(
            base_bot, "_get_chrome_options", return_value=mock_options
        ) as mock_get_options:
            base_bot._init_driver()

        # Verify state and key method calls
        assert base_bot.status == BotStatus.INITIALIZING
        mock_get_options.assert_called_once()  # Chrome options were generated
        mock_chrome.assert_called()  # Chrome was instantiated

        # Verify Chrome was called with options from _get_chrome_options
        # Handle both old (args, kwargs tuple) and new (.args, .kwargs) API
        if hasattr(mock_chrome.call_args, "kwargs"):
            # New API (Python 3.8+)
            call_kwargs = mock_chrome.call_args.kwargs
            assert "options" in call_kwargs
            assert call_kwargs["options"] is mock_options
        else:
            # Old API - call_args is (args, kwargs) tuple
            args, kwargs = mock_chrome.call_args
            assert "options" in kwargs
            assert kwargs["options"] is mock_options

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
