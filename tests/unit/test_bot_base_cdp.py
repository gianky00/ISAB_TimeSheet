"""Tests for BaseBot CDP command integration."""

from pathlib import Path
from unittest.mock import MagicMock

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from src.infrastructure.bots.base.selenium_base_bot import SeleniumBaseBot
from src.infrastructure.bots.base.selenium_bot_config import SeleniumBotConfig


class ConcreteBot(SeleniumBaseBot):
    @property
    def name(self) -> str:
        return "ConcreteBot"

    @property
    def description(self) -> str:
        return "Description"

    def run(self, data):
        return True

    @staticmethod
    def get_columns():
        return []

    def _login(self):
        return True

    def _save_error_state(self, e):
        pass

    def cleanup(self):
        pass

    def _handle_unsaved_changes_popup(self):
        pass


class TestBaseBotCDP:
    def test_setup_driver_instance_calls_cdp(self, mocker):
        """Verifica che _setup_driver_instance chiami Page.setDownloadBehavior via CDP."""
        mock_driver = MagicMock()
        mocker.patch("selenium.webdriver.Chrome", return_value=mock_driver)

        # Risoluzione deterministica
        dl_path = str(Path("/tmp/downloads").resolve())
        cfg = SeleniumBotConfig(download_path=dl_path)
        bot = ConcreteBot(config=cfg)

        bot._setup_driver_instance(MagicMock(spec=Service), MagicMock(spec=Options))

        # Percorsi normalizzati per Windows
        mock_driver.execute_cdp_cmd.assert_any_call(
            "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": dl_path}
        )

    def test_setup_driver_no_download_path(self, mocker):
        mock_driver = MagicMock()
        mocker.patch("selenium.webdriver.Chrome", return_value=mock_driver)

        bot = ConcreteBot(config=SeleniumBotConfig(download_path=None))
        bot._setup_driver_instance(MagicMock(), MagicMock())

        expected_fallback = str(Path.home() / "Downloads")
        mock_driver.execute_cdp_cmd.assert_any_call(
            "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": expected_fallback}
        )
