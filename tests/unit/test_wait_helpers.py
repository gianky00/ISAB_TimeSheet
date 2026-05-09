"""
Unit Tests for Selenium Wait Helpers
=====================================
Test suite per wait_helpers.py usando mock WebDriver e Temporary Directory.
"""

import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from src.bots.base.wait_helpers import (
    execute_with_wait,
    poll_for_download_complete,
    poll_for_file,
    poll_for_new_file,
    safe_click_with_retry,
    wait_for_element_clickable,
    wait_for_element_staleness,
    wait_for_overlay_to_disappear,
)

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_driver():
    """Mock WebDriver per test."""
    driver = MagicMock()
    driver.find_element = MagicMock()
    driver.find_elements = MagicMock()
    return driver


@pytest.fixture
def mock_element():
    """Mock WebElement."""
    element = MagicMock()
    element.click = MagicMock()
    element.text = "initial"
    return element


@pytest.fixture
def temp_download_dir(tmp_path):
    """Directory temporanea per test download."""
    download_dir = tmp_path / "downloads"
    download_dir.mkdir()
    return download_dir


# ============================================================================
# TEST WAIT HELPERS
# ============================================================================


class TestWaitForOverlay:
    """Test wait_for_overlay_to_disappear()."""

    @patch("src.bots.base.wait_helpers.WebDriverWait")
    def test_overlay_disappears_success(self, mock_wait_class, mock_driver):
        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = True

        result = wait_for_overlay_to_disappear(mock_driver, (By.ID, "overlay"), timeout=10)
        assert result is True

    @patch("src.bots.base.wait_helpers.WebDriverWait")
    def test_overlay_timeout(self, mock_wait_class, mock_driver):
        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.side_effect = TimeoutException()

        result = wait_for_overlay_to_disappear(mock_driver, (By.ID, "overlay"), timeout=1)
        assert result is False


class TestWaitForElementClickable:
    """Test wait_for_element_clickable()."""

    @patch("src.bots.base.wait_helpers.WebDriverWait")
    def test_element_clickable(self, mock_wait_class, mock_driver, mock_element):
        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = mock_element

        result = wait_for_element_clickable(mock_driver, (By.ID, "button"))
        assert result == mock_element

    @patch("src.bots.base.wait_helpers.WebDriverWait")
    def test_element_not_clickable_timeout(self, mock_wait_class, mock_driver):
        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.side_effect = TimeoutException()

        result = wait_for_element_clickable(mock_driver, (By.ID, "button"), timeout=1)
        assert result is None


class TestWaitForElementStaleness:
    """Test wait_for_element_staleness()."""

    @patch("src.bots.base.wait_helpers.WebDriverWait")
    def test_element_becomes_stale(self, mock_wait_class, mock_driver, mock_element):
        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = True

        result = wait_for_element_staleness(mock_driver, mock_element)
        assert result is True


# ============================================================================
# TEST FILE POLLING (FILE EXISTING / CREATED)
# ============================================================================


class TestPollForFile:
    """Test poll_for_file()."""

    def test_file_not_found_timeout(self, temp_download_dir):
        """Test timeout se file non appare."""
        result = poll_for_file(temp_download_dir, pattern="nonexistent.txt", timeout=1, poll_interval=0.1)
        assert result is None


class TestPollForDownloadComplete:
    """Test poll_for_download_complete()."""

    def test_download_complete(self, temp_download_dir):
        (temp_download_dir / "report.xlsx").write_text("data")
        result = poll_for_download_complete(
            temp_download_dir, pattern="report.xlsx", timeout=2, poll_interval=0.1
        )
        assert result is not None
        assert result.endswith("report.xlsx")

    def test_download_incomplete_excluded(self, temp_download_dir):
        (temp_download_dir / "report.xlsx.crdownload").write_text("partial")
        result = poll_for_download_complete(
            temp_download_dir, pattern="report.xlsx*", timeout=1, poll_interval=0.1
        )
        assert result is None


# ============================================================================
# TEST NEW FILE POLLING (SNAPSHOT BASED)
# ============================================================================


class TestPollForNewFile:
    """Test poll_for_new_file()."""

    def test_detects_new_file(self, temp_download_dir):
        """Rileva file non presente nello snapshot."""
        # 1. Snapshot iniziale
        (temp_download_dir / "existing.txt").write_text("old")
        files_before = {str(f.resolve()) for f in temp_download_dir.glob("*")}

        # 2. Crea file nuovo in thread
        def create_new():
            time.sleep(0.3)
            (temp_download_dir / "new.txt").write_text("new")

        threading.Thread(target=create_new).start()

        # 3. Poll
        result = poll_for_new_file(
            temp_download_dir,
            files_before,
            pattern="*.txt",
            timeout=3,
            poll_interval=0.1,
        )

        assert result is not None
        assert Path(result).name == "new.txt"

    def test_detects_overwrite_file(self, temp_download_dir):
        """Rileva file esistente ma aggiornato (overwrite)."""
        target_file = temp_download_dir / "updated.txt"
        target_file.write_text("version1")

        # Snapshot include file originale
        files_before = {str(f.resolve()) for f in temp_download_dir.glob("*")}

        # Modifica file in thread (simulate overwrite)
        def overwrite_file():
            time.sleep(1.2)  # Sleep > 1s per garantire cambio mtime rilevabile (tolleranza è 1.0s)
            target_file.write_text("version2")

        threading.Thread(target=overwrite_file).start()

        result = poll_for_new_file(
            temp_download_dir,
            files_before,
            pattern="*.txt",
            timeout=4,
            poll_interval=0.1,
        )

        assert result is not None
        assert Path(result).name == "updated.txt"
        assert Path(result).read_text() == "version2"

    def test_timeout_no_change(self, temp_download_dir):
        """Nessun cambiamento -> timeout."""
        files_before = {str(f.resolve()) for f in temp_download_dir.glob("*")}

        result = poll_for_new_file(temp_download_dir, files_before, timeout=0.5, poll_interval=0.1)
        assert result is None


# ============================================================================
# TEST UTILITY FUNCTIONS
# ============================================================================


class TestSafeClickWithRetry:
    """Test safe_click_with_retry()."""

    @patch("src.bots.base.wait_helpers.wait_for_element_clickable")
    def test_click_success_first_try(self, mock_wait_clickable, mock_driver):
        mock_element = MagicMock()
        mock_wait_clickable.return_value = mock_element

        result = safe_click_with_retry(mock_driver, (By.ID, "button"))
        assert result is True
        mock_element.click.assert_called_once()

    @patch("src.bots.base.wait_helpers.wait_for_element_clickable")
    @patch("src.bots.base.wait_helpers.time.sleep")
    def test_click_retry_on_intercept(self, mock_sleep, mock_wait_clickable, mock_driver):
        from selenium.common.exceptions import ElementClickInterceptedException

        mock_element = MagicMock()
        mock_wait_clickable.return_value = mock_element

        # First call raises, second succeeds
        mock_element.click.side_effect = [
            ElementClickInterceptedException("Overlay"),
            None,
        ]

        result = safe_click_with_retry(mock_driver, (By.ID, "button"), retries=3, retry_delay=0.1)
        assert result is True
        assert mock_element.click.call_count == 2


class TestExecuteWithWait:
    """Test execute_with_wait()."""

    @patch("src.bots.base.wait_helpers.wait_for_overlay_to_disappear")
    def test_execute_action_with_wait(self, mock_wait_overlay, mock_driver):
        mock_wait_overlay.return_value = True
        action_called = False

        def test_action():
            nonlocal action_called
            action_called = True
            return True

        result = execute_with_wait(
            action=test_action,
            driver=mock_driver,
            wait_locator=(By.CLASS_NAME, "overlay"),
        )
        assert result is True
        assert action_called is True
