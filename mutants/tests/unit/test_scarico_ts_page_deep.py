from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page import ScaricoTSPage


@pytest.fixture
def mock_driver():
    driver = MagicMock()
    return driver


def test_wait_for_overlay(mock_driver):
    page = ScaricoTSPage(mock_driver)
    with (
        patch("time.sleep"),
        patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_wait,
    ):
        page._wait_for_overlay()
        mock_wait.assert_called()


def test_navigate_to_timesheet(mock_driver):
    page = ScaricoTSPage(mock_driver)
    with (
        patch("time.sleep"),
        patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_wait,
        patch.object(page, "_wait_for_overlay"),
    ):
        mock_el = MagicMock()
        mock_wait.return_value = mock_el

        assert page.navigate_to_timesheet() is True
        assert mock_el.click.call_count >= 2


def test_setup_filters(mock_driver):
    page = ScaricoTSPage(mock_driver)
    with (
        patch("time.sleep"),
        patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_wait,
        patch(
            "src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page.ActionChains"
        ) as mock_chains,
        patch.object(page, "_wait_for_overlay"),
    ):
        mock_wait.return_value = MagicMock()
        assert page.setup_filters("Supplier", "01.01.2025") is True
        mock_chains.return_value.move_to_element.return_value.click.return_value.perform.assert_called()


def test_search_and_download(mock_driver, tmp_path):
    page = ScaricoTSPage(mock_driver)
    with (
        patch("time.sleep"),
        patch("selenium.webdriver.support.ui.WebDriverWait.until") as mock_wait,
        patch.object(page, "_wait_for_overlay"),
        patch.object(page, "_download_excel", return_value=True),
    ):
        mock_wait.return_value = MagicMock()
        assert page.search_and_download("123", "10", tmp_path) is True
        assert mock_driver.execute_script.call_count >= 4


def test_download_excel_logic(mock_driver, tmp_path):
    page = ScaricoTSPage(mock_driver)

    # Create a dummy file to simulate download
    dummy_file = tmp_path / "downloaded.xlsx"
    dummy_file.touch()

    # We need to simulate that the file appears AFTER click
    # But files_before is calculated at start.
    # If we already have the file, we need to ensure it's considered "new"
    # or clear directory before.

    # Let's mock time to control loop
    with (
        patch("time.time", side_effect=[100, 101, 105]),
        patch("time.sleep"),
        patch("selenium.webdriver.support.ui.WebDriverWait.until"),
    ):
        # Scenario: File appears
        # files_before = empty
        # loop 1: file exists

        # We need to make sure iterdir returns empty first, then file
        # Mocking iterdir is hard on real path.
        # Let's clean tmp_path first
        dummy_file.unlink()

        def side_effect_click():
            dummy_file.touch()  # Create file when button clicked

        mock_btn = MagicMock()
        mock_btn.click.side_effect = side_effect_click

        with patch(
            "selenium.webdriver.support.ui.WebDriverWait.until", return_value=mock_btn
        ):
            res = page._download_excel(tmp_path, "ODA123", "10")
            assert res is True
            assert (tmp_path / "ODA123-10.xlsx").exists()
