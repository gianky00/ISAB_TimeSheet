from unittest.mock import MagicMock, patch

import pytest

from src.bots.base.login_page import LoginPage
from src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page import ScaricoTSPage


class TestBotPages:
    @pytest.fixture
    def mock_driver(self):
        return MagicMock()

    @pytest.fixture
    def mock_wait(self):
        return MagicMock()

    def test_login_page_verify_logged_in_success(self, mock_driver, mock_wait):
        page = LoginPage(mock_driver, mock_wait)

        # Simula presenza del bottone settings (successo login)
        with patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_until:
            mock_until.return_value = True
            assert page._verify_logged_in_via_ui() is True

    def test_login_page_verify_logged_in_failure(self, mock_driver, mock_wait):
        page = LoginPage(mock_driver, mock_wait)

        # Simula assenza bottone (errore/timeout)
        with patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_until:
            mock_until.side_effect = Exception("Timeout")
            assert page._verify_logged_in_via_ui() is False

    def test_scarico_ts_page_log(self, mock_driver):
        log_msgs = []

        def my_log(msg):
            log_msgs.append(msg)

        page = ScaricoTSPage(mock_driver, log_callback=my_log)
        page.log("Test message")
        assert "Test message" in log_msgs

    def test_scarico_ts_page_wait_for_overlay_success(self, mock_driver):
        page = ScaricoTSPage(mock_driver)

        with patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_until:
            mock_until.return_value = True  # Invisibility success
            # Should not raise exception
            page._wait_for_overlay()

    def test_scarico_ts_page_resolve_unique_path(self, mock_driver, tmp_path):
        page = ScaricoTSPage(mock_driver)

        # Caso base: file non esiste
        res = page._resolve_unique_path(tmp_path, "ODA123", "10", tmp_path / "old.xlsx")
        assert res.name == "ODA123-10.xlsx"

        # Caso collisione: file esiste già
        (tmp_path / "ODA123-10.xlsx").touch()
        res = page._resolve_unique_path(tmp_path, "ODA123", "10", tmp_path / "old.xlsx")
        assert "ODA123-10" in res.name
        assert res.name != "ODA123-10.xlsx"  # Avrà timestamp o counter
