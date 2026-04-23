"""
Tests for BaseBot CDP command integration.
"""

from pathlib import Path
from unittest.mock import MagicMock

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from src.bots.base.selenium_base_bot import SeleniumBaseBot


class ConcreteBot(SeleniumBaseBot):
    """Sottoclasse concreta per testare SeleniumBaseBot."""

    @property
    def name(self) -> str:
        return "ConcreteBot"

    @property
    def description(self) -> str:
        return "Description"

    def run(self, data):
        return True

    def get_columns(self):
        return []

    def _login(self):
        return True


class TestBaseBotCDP:
    def test_setup_driver_instance_calls_cdp(self, mocker):
        """Verifica che _setup_driver_instance chiami Page.setDownloadBehavior via CDP."""
        # Setup mock driver
        mock_driver = MagicMock()
        mocker.patch("selenium.webdriver.Chrome", return_value=mock_driver)

        bot = ConcreteBot("user", "pass", download_path="C:/downloads")

        service = MagicMock(spec=Service)
        options = MagicMock(spec=Options)

        bot._setup_driver_instance(service, options)

        # Verifica chiamata CDP per il download
        expected_path = str(Path("C:/downloads").resolve())
        mock_driver.execute_cdp_cmd.assert_any_call(
            "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": expected_path}
        )

        # Verifica anche l'anti-detection
        mock_driver.execute_cdp_cmd.assert_any_call("Page.addScriptToEvaluateOnNewDocument", mocker.ANY)

    def test_setup_driver_no_download_path(self, mocker):
        """Verifica che venga usato il fallback Downloads se non c'è download_path."""
        mock_driver = MagicMock()
        mocker.patch("selenium.webdriver.Chrome", return_value=mock_driver)

        bot = ConcreteBot("user", "pass", download_path=None)

        bot._setup_driver_instance(MagicMock(), MagicMock())

        # Ora viene chiamato SEMPRE, usando il fallback Home/Downloads
        expected_fallback = str(Path.home() / "Downloads")
        mock_driver.execute_cdp_cmd.assert_any_call(
            "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": expected_fallback}
        )
