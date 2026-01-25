"""
Unit Tests for Selenium Wait Helpers
=====================================
Test suite per wait_helpers.py usando mock WebDriver.
"""

import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from src.bots.base.wait_helpers import (
    alert_appears_with_text,
    element_count_is,
    element_text_changes,
    execute_with_wait,
    poll_for_download_complete,
    poll_for_file,
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
        """Test overlay scompare correttamente."""
        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = True

        result = wait_for_overlay_to_disappear(
            mock_driver, (By.ID, "overlay"), timeout=10
        )

        assert result is True
        mock_wait.until.assert_called_once()

    @patch("src.bots.base.wait_helpers.WebDriverWait")
    def test_overlay_timeout(self, mock_wait_class, mock_driver):
        """Test timeout su overlay."""
        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.side_effect = TimeoutException()

        result = wait_for_overlay_to_disappear(
            mock_driver, (By.ID, "overlay"), timeout=1
        )

        assert result is False


class TestWaitForElementClickable:
    """Test wait_for_element_clickable()."""

    @patch("src.bots.base.wait_helpers.WebDriverWait")
    def test_element_clickable(self, mock_wait_class, mock_driver, mock_element):
        """Test elemento cliccabile."""
        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = mock_element

        result = wait_for_element_clickable(mock_driver, (By.ID, "button"))

        assert result == mock_element

    @patch("src.bots.base.wait_helpers.WebDriverWait")
    def test_element_not_clickable_timeout(self, mock_wait_class, mock_driver):
        """Test timeout su elemento non cliccabile."""
        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.side_effect = TimeoutException()

        result = wait_for_element_clickable(mock_driver, (By.ID, "button"), timeout=1)

        assert result is None


class TestWaitForElementStaleness:
    """Test wait_for_element_staleness()."""

    @patch("src.bots.base.wait_helpers.WebDriverWait")
    def test_element_becomes_stale(self, mock_wait_class, mock_driver, mock_element):
        """Test elemento diventa stale."""
        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait
        mock_wait.until.return_value = True

        result = wait_for_element_staleness(mock_driver, mock_element)

        assert result is True


# ============================================================================
# TEST FILE POLLING
# ============================================================================


class TestPollForFile:
    """Test poll_for_file()."""

    def test_file_found_immediately(self, temp_download_dir):
        """Test file già presente."""
        test_file = temp_download_dir / "test.txt"
        test_file.write_text("content")

        result = poll_for_file(temp_download_dir, pattern="*.txt", timeout=5)

        assert result is not None
        assert Path(result).name == "test.txt"

    def test_file_appears_during_poll(self, temp_download_dir):
        """Test file appare durante polling."""

        def create_file_delayed():
            time.sleep(0.5)
            (temp_download_dir / "delayed.txt").write_text("content")

        import threading

        thread = threading.Thread(target=create_file_delayed)
        thread.start()

        result = poll_for_file(
            temp_download_dir, pattern="delayed.txt", timeout=3, poll_interval=0.2
        )

        thread.join()
        assert result is not None

    def test_file_not_found_timeout(self, temp_download_dir):
        """Test timeout se file non appare."""
        result = poll_for_file(
            temp_download_dir, pattern="nonexistent.txt", timeout=1, poll_interval=0.2
        )

        assert result is None

    def test_exclude_patterns(self, temp_download_dir):
        """Test esclusione pattern (.crdownload)."""
        (temp_download_dir / "file.txt").write_text("complete")
        (temp_download_dir / "file.txt.crdownload").write_text("incomplete")

        result = poll_for_file(
            temp_download_dir,
            pattern="file.txt*",
            timeout=2,
            exclude_patterns=[".crdownload"],
        )

        assert result is not None
        assert not result.endswith(".crdownload")

    def test_min_age_filter(self, temp_download_dir):
        """Test filtro età minima file."""
        old_file = temp_download_dir / "old.txt"
        old_file.write_text("old")

        # Timestamp nel passato
        min_age = time.time() + 10  # Futuro: nessun file dovrebbe matchare

        result = poll_for_file(
            temp_download_dir, pattern="*.txt", timeout=1, min_age=min_age
        )

        assert result is None  # Old file escluso


class TestPollForDownloadComplete:
    """Test poll_for_download_complete()."""

    def test_download_complete(self, temp_download_dir):
        """Test download completato (no .crdownload)."""
        (temp_download_dir / "report.xlsx").write_text("data")

        result = poll_for_download_complete(
            temp_download_dir, pattern="report.xlsx", timeout=2
        )

        assert result is not None
        assert result.endswith("report.xlsx")

    def test_download_incomplete_excluded(self, temp_download_dir):
        """Test .crdownload escluso."""
        (temp_download_dir / "report.xlsx.crdownload").write_text("partial")

        result = poll_for_download_complete(
            temp_download_dir, pattern="report.xlsx*", timeout=1, poll_interval=0.2
        )

        assert result is None


# ============================================================================
# TEST CUSTOM EXPECTED CONDITIONS
# ============================================================================


class TestElementTextChanges:
    """Test custom EC element_text_changes."""

    def test_text_changes(self, mock_driver, mock_element):
        """Test rilevamento cambio testo."""
        mock_driver.find_element.return_value = mock_element
        condition = element_text_changes((By.ID, "counter"), "initial")

        # Prima chiamata: testo uguale
        mock_element.text = "initial"
        assert condition(mock_driver) is False

        # Seconda chiamata: testo cambiato
        mock_element.text = "updated"
        assert condition(mock_driver) is True


class TestAlertAppearsWithText:
    """Test custom EC alert_appears_with_text."""

    def test_alert_with_correct_text(self, mock_driver):
        """Test alert con testo corretto."""
        mock_alert = MagicMock()
        mock_alert.text = "Operazione completata"
        mock_driver.switch_to.alert = mock_alert

        condition = alert_appears_with_text("Operazione completata")
        assert condition(mock_driver) is True

    def test_alert_with_wrong_text(self, mock_driver):
        """Test alert con testo diverso."""
        mock_alert = MagicMock()
        mock_alert.text = "Errore!"
        mock_driver.switch_to.alert = mock_alert

        condition = alert_appears_with_text("Successo")
        assert condition(mock_driver) is False


class TestElementCountIs:
    """Test custom EC element_count_is."""

    def test_exact_count_match(self, mock_driver):
        """Test conteggio esatto."""
        mock_driver.find_elements.return_value = [MagicMock()] * 5
        condition = element_count_is((By.CSS_SELECTOR, "tr"), exact_count=5)

        assert condition(mock_driver) is True

    def test_min_count(self, mock_driver):
        """Test conteggio minimo."""
        mock_driver.find_elements.return_value = [MagicMock()] * 10
        condition = element_count_is((By.CSS_SELECTOR, "tr"), min_count=5)

        assert condition(mock_driver) is True

    def test_max_count_exceeded(self, mock_driver):
        """Test conteggio massimo superato."""
        mock_driver.find_elements.return_value = [MagicMock()] * 20
        condition = element_count_is((By.CSS_SELECTOR, "tr"), max_count=10)

        assert condition(mock_driver) is False


# ============================================================================
# TEST UTILITY FUNCTIONS
# ============================================================================


class TestSafeClickWithRetry:
    """Test safe_click_with_retry()."""

    @patch("src.bots.base.wait_helpers.wait_for_element_clickable")
    def test_click_success_first_try(self, mock_wait_clickable, mock_driver):
        """Test click riuscito al primo tentativo."""
        mock_element = MagicMock()
        mock_wait_clickable.return_value = mock_element

        result = safe_click_with_retry(mock_driver, (By.ID, "button"))

        assert result is True
        mock_element.click.assert_called_once()

    @patch("src.bots.base.wait_helpers.wait_for_element_clickable")
    @patch("src.bots.base.wait_helpers.time.sleep")
    def test_click_retry_on_intercept(
        self, mock_sleep, mock_wait_clickable, mock_driver
    ):
        """Test retry su ElementClickInterceptedException."""
        from selenium.common.exceptions import ElementClickInterceptedException

        mock_element = MagicMock()
        mock_wait_clickable.return_value = mock_element

        # First call raises, second succeeds
        mock_element.click.side_effect = [
            ElementClickInterceptedException("Overlay"),
            None,
        ]

        result = safe_click_with_retry(
            mock_driver, (By.ID, "button"), retries=3, retry_delay=0.1
        )

        assert result is True
        assert mock_element.click.call_count == 2


class TestExecuteWithWait:
    """Test execute_with_wait()."""

    @patch("src.bots.base.wait_helpers.wait_for_overlay_to_disappear")
    def test_execute_action_with_wait(self, mock_wait_overlay, mock_driver):
        """Test esecuzione azione + wait."""
        mock_wait_overlay.return_value = True
        action_called = False

        def test_action():
            nonlocal action_called
            action_called = True

        result = execute_with_wait(
            action=test_action,
            driver=mock_driver,
            wait_locator=(By.CLASS_NAME, "overlay"),
        )

        assert result is True
        assert action_called is True
        mock_wait_overlay.assert_called_once()

    def test_execute_action_without_wait(self, mock_driver):
        """Test esecuzione azione senza wait."""
        action_called = False

        def test_action():
            nonlocal action_called
            action_called = True

        result = execute_with_wait(action=test_action, driver=mock_driver)

        assert result is True
        assert action_called is True
