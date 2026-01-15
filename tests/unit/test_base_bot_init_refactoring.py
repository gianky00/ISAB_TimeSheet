"""
Tests for BaseBot._init_driver refactoring.
Ensures 100% coverage and parity before refactoring.
"""

import pytest

from src.bots.base.base_bot import BaseBot
from src.core.constants import BotStatus


class ConcreteBot(BaseBot):
    @property
    def name(self) -> str:
        return "TestBot"

    @property
    def description(self) -> str:
        return "Test Bot Description"

    def run(self, data):
        return True

    def _handle_unsaved_changes_popup(self):
        pass


@pytest.fixture
def bot():
    return ConcreteBot("user", "pass")


def test_init_driver_success(bot, mocker):
    """Test standard driver initialization."""
    # Mocking external dependencies
    mocker.patch("src.bots.base.base_bot.Options")
    m_chrome = mocker.patch("src.bots.base.base_bot.webdriver.Chrome")
    m_manager = mocker.patch("src.bots.base.base_bot.ChromeDriverManager")
    m_manager.return_value.install.return_value = "chromedriver.exe"

    bot._init_driver()

    assert bot.status == BotStatus.INITIALIZING
    assert bot.driver is not None
    assert bot.wait is not None
    assert bot.login_page is not None
    m_chrome.assert_called_once()


def test_init_driver_headless_config(bot, mocker):
    """Test headless mode from config."""
    mocker.patch(
        "src.core.config_manager.load_config", return_value={"browser_headless": True}
    )
    m_options = mocker.patch("src.bots.base.base_bot.Options")
    mocker.patch("src.bots.base.base_bot.webdriver.Chrome")
    mocker.patch(
        "src.bots.base.base_bot.ChromeDriverManager"
    ).return_value.install.return_value = "chromedriver.exe"

    bot._init_driver()

    # Verify headless flag was added to options
    m_options.return_value.add_argument.assert_any_call("--headless=new")


def test_init_driver_fallback_local(bot, mocker):
    """Test fallback to local driver if manager fails."""
    mocker.patch(
        "src.bots.base.base_bot.ChromeDriverManager"
    ).return_value.install.side_effect = Exception("Network error")
    mocker.patch("src.bots.base.base_bot.Path.exists", return_value=True)
    mocker.patch(
        "src.bots.base.base_bot.Path.absolute",
        return_value="/abs/path/chromedriver.exe",
    )
    m_service = mocker.patch("src.bots.base.base_bot.Service")
    mocker.patch("src.bots.base.base_bot.webdriver.Chrome")

    bot._init_driver()

    m_service.assert_called_with("/abs/path/chromedriver.exe")
    assert bot.driver is not None


def test_init_driver_failure_handling(bot, mocker):
    """Test error handling and suggestions when Chrome fails to start."""
    mocker.patch(
        "src.bots.base.base_bot.webdriver.Chrome",
        side_effect=Exception("chrome instance exited"),
    )
    mocker.patch(
        "src.bots.base.base_bot.ChromeDriverManager"
    ).return_value.install.return_value = "chromedriver.exe"

    # Capture logs
    logs = []
    bot.set_log_callback(lambda m: logs.append(m))

    with pytest.raises(Exception, match="chrome instance exited"):
        bot._init_driver()

    assert any("SUGGERIMENTO: Chrome è crashato" in log for log in logs)


def test_init_driver_version_error(bot, mocker):
    """Test error handling for version mismatch."""
    mocker.patch(
        "src.bots.base.base_bot.webdriver.Chrome",
        side_effect=Exception("sessionnotcreatedexception: version mismatch"),
    )
    mocker.patch(
        "src.bots.base.base_bot.ChromeDriverManager"
    ).return_value.install.return_value = "chromedriver.exe"

    logs = []
    bot.set_log_callback(lambda m: logs.append(m))

    with pytest.raises(Exception, match="version mismatch"):
        bot._init_driver()

    assert any("SUGGERIMENTO: La tua versione di Chrome" in log for log in logs)
