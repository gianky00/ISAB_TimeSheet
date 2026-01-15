import os
import time
from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.timbrature.pages.timbrature_page import TimbraturePage


@pytest.fixture
def mock_driver():
    driver = MagicMock()
    return driver

def test_wait_for_overlay(mock_driver):
    page = TimbraturePage(mock_driver)
    # Patch time.sleep to avoid waiting
    with patch("time.sleep"), \
         patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_wait:
        page._wait_for_overlay()
        mock_wait.assert_called()

@patch("src.bots.portale_fornitori.timbrature.pages.timbrature_page.ActionChains")
def test_navigate_to_timbrature(mock_actions, mock_driver):
    page = TimbraturePage(mock_driver)

    # Mock locators finding and patch time.sleep
    with patch("time.sleep"), \
         patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_wait:

        mock_btn = MagicMock()
        mock_wait.return_value = mock_btn

        # Ensure Actions chains perform doesn't crash
        mock_actions_instance = mock_actions.return_value
        mock_actions_instance.send_keys.return_value = mock_actions_instance
        mock_actions_instance.pause.return_value = mock_actions_instance

        res = page.navigate_to_timbrature()
        assert res is True
        mock_btn.click.assert_called()
        mock_actions_instance.perform.assert_called()

def test_set_filters(mock_driver):
    page = TimbraturePage(mock_driver)

    with patch("time.sleep"), \
         patch.object(page, "_select_supplier") as mock_sel, \
         patch("src.bots.portale_fornitori.timbrature.pages.timbrature_page.ActionChains") as mock_actions, \
         patch("selenium.webdriver.support.ui.WebDriverWait.until"): # Mock wait too

        mock_actions_instance = mock_actions.return_value
        mock_actions_instance.send_keys.return_value = mock_actions_instance
        mock_actions_instance.key_down.return_value = mock_actions_instance
        mock_actions_instance.key_up.return_value = mock_actions_instance
        mock_actions_instance.pause.return_value = mock_actions_instance

        res = page.set_filters("Fornitore", "01/01/2024", "01/01/2024")
        assert res is True
        mock_sel.assert_called_with("Fornitore")
        mock_actions_instance.perform.assert_called()

def test_download_excel_success(mock_driver):
    page = TimbraturePage(mock_driver)
    mock_btn = MagicMock()
    with patch("time.sleep"), \
         patch.object(page, "_find_excel_button", return_value=mock_btn), \
         patch.object(page, "_rename_latest_download", return_value="path/to/file.xlsx"):
        path = page.download_excel()
        assert path == "path/to/file.xlsx"
        assert mock_btn.click.called or mock_driver.execute_script.called

@patch("src.bots.portale_fornitori.timbrature.pages.timbrature_page.Path.home")
def test_rename_latest_download(mock_home, mock_driver, tmp_path):
    mock_home.return_value = tmp_path
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    test_file = downloads / "test.xlsx"
    test_file.write_text("data")

    # Ensure file is "recent"
    os.utime(test_file, (time.time(), time.time()))

    page = TimbraturePage(mock_driver)
    with patch("time.sleep"), \
         patch("src.core.config_manager.CONFIG_DIR", tmp_path), \
         patch("src.core.constants.Timeouts.DOWNLOAD", 1):
        res = page._rename_latest_download("timbrature_temp")
        assert "timbrature_temp" in res
        assert os.path.exists(res)

def test_find_excel_button(mock_driver):
    page = TimbraturePage(mock_driver)
    with patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_wait:
        mock_btn = MagicMock()
        mock_wait.return_value = mock_btn
        btn = page._find_excel_button()
        assert btn == mock_btn
