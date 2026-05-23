"""Tests for BaseBot._init_driver refactoring."""

from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
from selenium.common.exceptions import SessionNotCreatedException

from src.bots.base.selenium_base_bot import SeleniumBaseBot
from src.core.constants import BotStatus


class ConcreteBot(SeleniumBaseBot):
    @property
    def name(self) -> str:
        return "TestBot"

    @property
    def description(self) -> str:
        return "Test Bot Description"

    @staticmethod
    def get_columns() -> list[dict[str, Any]]:
        return []

    def run(self, data):
        return True

    def _login(self) -> bool:
        return True

    def _save_error_state(self, error_msg: str):
        pass

    def cleanup(self):
        pass

    def _handle_unsaved_changes_popup(self):
        pass


@pytest.fixture
def bot(mocker):
    # Mock profile patching globally for bot tests to avoid FileNotFoundError in headless
    mocker.patch("src.bots.base.selenium_base_bot.patch_browser_profile")
    return ConcreteBot("user", "pass")


def test_init_driver_success(bot, mocker):
    mocker.patch("src.bots.base.selenium_base_bot.Options")
    m_chrome = mocker.patch("src.bots.base.selenium_base_bot.webdriver.Chrome")
    m_manager = mocker.patch("webdriver_manager.chrome.ChromeDriverManager")
    m_manager.return_value.install.return_value = "chromedriver.exe"

    bot._init_driver()

    assert bot.status == BotStatus.INITIALIZING
    assert bot.driver is not None
    m_chrome.assert_called_once()


def test_init_driver_headless_config(bot, mocker):
    mocker.patch("src.core.config_manager.load_config", return_value={"browser_headless": True})
    m_options = mocker.patch("src.bots.base.selenium_base_bot.Options")
    mocker.patch("src.bots.base.selenium_base_bot.webdriver.Chrome")
    mocker.patch(
        "webdriver_manager.chrome.ChromeDriverManager"
    ).return_value.install.return_value = "chromedriver.exe"

    bot._init_driver()
    m_options.return_value.add_argument.assert_any_call("--headless=new")


def test_init_driver_failure_handling(bot, mocker):
    mocker.patch(
        "src.utils.resource_manager.ResourceManager.ensure_automation_driver", return_value="chromedriver.exe"
    )
    mocker.patch(
        "src.bots.base.selenium_base_bot.webdriver.Chrome", side_effect=Exception("chrome instance exited")
    )

    logs = []
    bot.set_log_callback(lambda m: logs.append(m))

    with pytest.raises(Exception, match="chrome instance exited"):
        bot._init_driver()

    # Verifica flessibile del messaggio di errore (senza emoji per evitare mismatch di encoding)
    assert any("Chrome si è chiuso all'avvio" in log for log in logs)


def test_init_driver_version_error(bot, mocker):
    mocker.patch(
        "src.utils.resource_manager.ResourceManager.ensure_automation_driver", return_value="chromedriver.exe"
    )
    fake_dir = Path("/tmp/drivers")
    mocker.patch("src.utils.resource_manager.ResourceManager.get_writable_drivers_dir", return_value=fake_dir)

    # Mock exists/unlink to avoid side effects
    mocker.patch("pathlib.Path.exists", return_value=True)
    mocker.patch("pathlib.Path.unlink")

    with patch("src.bots.base.selenium_base_bot.webdriver.Chrome") as mock_chrome:
        mock_chrome.side_effect = SessionNotCreatedException("version mismatch")
        logs = []
        bot.set_log_callback(lambda m: logs.append(m))
        with pytest.raises(SessionNotCreatedException):
            bot._init_driver()

    assert any("ERRORE CRITICO DRIVER: Versione incompatibile" in log for log in logs)
