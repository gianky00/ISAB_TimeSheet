"""
Unit tests for BaseBot logic (Mocked).
"""
import pytest
from unittest.mock import MagicMock, patch
from src.bots.base.base_bot import BaseBot, BotStatus

class ConcreteBot(BaseBot):
    """Concrete implementation for testing."""
    @property
    def name(self): return "TestBot"
    @property
    def description(self): return "Test Description"
    def run(self, data): return True

@pytest.fixture
def base_bot():
    return ConcreteBot("user", "pass", headless=True)

class TestBaseBotLogic:

    @patch('selenium.webdriver.Chrome')
    @patch('webdriver_manager.chrome.ChromeDriverManager.install')
    def test_init_driver(self, mock_install, mock_chrome, base_bot):
        """Should initialize driver with correct options."""
        base_bot._init_driver()

        assert base_bot.status == BotStatus.INITIALIZING
        mock_chrome.assert_called()

        # Verify options
        call_args = mock_chrome.call_args
        options = call_args.kwargs['options']
        args = [arg for arg in options.arguments]

        assert "--headless=new" in args
        assert "--disable-notifications" in args
        assert "--no-restore-session-state" in args

    def test_check_stop_raises(self, base_bot):
        """Should raise InterruptedError if stop requested."""
        base_bot.request_stop()
        with pytest.raises(InterruptedError):
            base_bot._check_stop()

    def test_verify_login_url(self, base_bot):
        """Should return False if URL contains 'login'."""
        base_bot.driver = MagicMock()
        base_bot.driver.current_url = "https://site.com/Ui/Login"
        assert base_bot._verify_login() is False

        base_bot.driver.current_url = "https://site.com/Ui/Dashboard"
        assert base_bot._verify_login() is True
