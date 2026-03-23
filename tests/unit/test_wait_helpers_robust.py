import time
from unittest.mock import MagicMock, patch

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By

from src.bots.base import wait_helpers


class TestWaitHelpersRobust:
    # --- Wait Helpers Tests ---

    def test_wait_for_overlay_disappear_success(self):
        """Test overlay scompare."""
        mock_driver = MagicMock()
        with patch("src.bots.base.wait_helpers.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = True
            res = wait_helpers.wait_for_overlay_to_disappear(mock_driver, (By.ID, "overlay"))
            assert res is True

    def test_wait_for_overlay_timeout(self):
        """Test overlay timeout."""
        mock_driver = MagicMock()
        with patch("src.bots.base.wait_helpers.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.side_effect = TimeoutException()
            res = wait_helpers.wait_for_overlay_to_disappear(mock_driver, (By.ID, "overlay"))
            assert res is False

    def test_wait_for_element_staleness(self):
        """Test elemento diventa stale."""
        mock_elem = MagicMock()
        mock_driver = MagicMock()
        with patch("src.bots.base.wait_helpers.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = True
            assert wait_helpers.wait_for_element_staleness(mock_driver, mock_elem) is True

    def test_wait_for_element_clickable(self):
        """Test elemento cliccabile."""
        mock_elem = MagicMock()
        mock_driver = MagicMock()
        with patch("src.bots.base.wait_helpers.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = mock_elem
            res = wait_helpers.wait_for_element_clickable(mock_driver, (By.ID, "btn"))
            assert res == mock_elem

    # --- File Polling Tests (Mocked File System for Stability) ---

    @patch("src.bots.base.wait_helpers.Path.glob")
    def test_poll_for_file_found(self, mock_glob, tmp_path):
        """Test polling file trovato (mocked file object)."""
        # Mock file
        f = MagicMock()
        f.is_file.return_value = True
        f.stat.return_value.st_mtime = time.time()
        f.stat.return_value.st_ctime = time.time()
        f.name = "test_download.xlsx"
        expected_path = str(tmp_path / "test_download.xlsx")
        f.absolute.return_value = expected_path

        # Mock glob intelligente
        def glob_side_effect(pattern):
            if any(ext in pattern for ext in [".crdownload", ".tmp", ".part"]):
                return []
            if pattern == "*.xlsx":
                return [f]
            return []

        mock_glob.side_effect = glob_side_effect

        # Poll
        found = wait_helpers.poll_for_file(directory=tmp_path, pattern="*.xlsx", timeout=1, poll_interval=0.1)
        assert found == expected_path

    @patch("src.bots.base.wait_helpers.Path.glob")
    def test_poll_for_file_timeout(self, mock_glob, tmp_path):
        """Test polling timeout (mocked glob)."""
        mock_glob.return_value = []  # Nessun file

        found = wait_helpers.poll_for_file(
            directory=tmp_path, pattern="*.xlsx", timeout=0.2, poll_interval=0.1
        )
        assert found is None

    @patch("src.bots.base.wait_helpers.Path.glob")
    def test_poll_for_file_exclude_temp(self, mock_glob, tmp_path):
        """Test esclusione file temporanei (mocked)."""
        f_ignore = MagicMock()
        f_ignore.is_file.return_value = True
        f_ignore.suffix = ".ignoreme"
        f_ignore.name = "file.ignoreme"

        f_valid = MagicMock()
        f_valid.is_file.return_value = True
        f_valid.suffix = ".xlsx"
        f_valid.name = "file.xlsx"
        f_valid.stat.return_value.st_mtime = time.time()
        f_valid.stat.return_value.st_ctime = time.time()
        expected_path = str(tmp_path / "file.xlsx")
        f_valid.absolute.return_value = expected_path

        # Glob ritorna entrambi
        mock_glob.side_effect = lambda pat: [f_ignore, f_valid] if pat == "*" else []

        # Dovrebbe trovare file.xlsx e ignorare .ignoreme
        found = wait_helpers.poll_for_file(
            directory=tmp_path,
            pattern="*",
            exclude_patterns=[".ignoreme"],
            timeout=1,
            poll_interval=0.1,
        )
        assert found == expected_path

    @patch("src.bots.base.wait_helpers.Path.glob")
    def test_poll_for_file_min_age(self, mock_glob, tmp_path):
        """Test filtro per età minima (mocked stat)."""
        f = MagicMock()
        f.name = "old.txt"
        f.is_file.return_value = True
        f.suffix = ".txt"  # Importante per exclude_patterns check

        # Mock stat per avere timestamp precisi
        now = time.time()
        stat_old = MagicMock()
        stat_old.st_mtime = now - 100
        stat_old.st_ctime = now - 100
        f.stat.return_value = stat_old
        f.absolute.return_value = str(tmp_path / "old.txt")

        def glob_side_effect(pattern):
            # Vuoto per controlli temp file
            if any(ext in pattern for ext in [".crdownload", ".tmp", ".part"]):
                return []
            # Ritorna il file mockato per il resto
            return [f]

        mock_glob.side_effect = glob_side_effect

        # Cerca file più recente di 50 secondi fa -> False
        found = wait_helpers.poll_for_file(
            directory=tmp_path, min_age=now - 50, timeout=0.2, poll_interval=0.1
        )
        assert found is None

        # Cerca file più recente di 200 secondi fa -> True
        found = wait_helpers.poll_for_file(
            directory=tmp_path, min_age=now - 200, timeout=0.2, poll_interval=0.1
        )
        assert found is not None

    def test_poll_for_new_file(self, tmp_path):
        """Test rilevamento nuovo file rispetto a snapshot."""
        # Snapshot iniziale
        f1 = tmp_path / "existing.txt"
        f1.touch()
        snapshot = {str(f1)}

        # Crea nuovo file
        f2 = tmp_path / "new.txt"
        f2.touch()

        found = wait_helpers.poll_for_new_file(
            directory=tmp_path,
            files_before=snapshot,
            pattern="*",
            timeout=1,
            poll_interval=0.1,
        )
        assert found == str(f2.absolute())

    # --- Custom Conditions Tests ---

    def test_condition_text_changes(self):
        """Test custom condition text_changes."""
        mock_driver = MagicMock()
        mock_elem = MagicMock()
        mock_elem.text = "New Text"
        mock_driver.find_element.return_value = mock_elem

        cond = wait_helpers.element_text_changes((By.ID, "cnt"), "Old Text")
        assert cond(mock_driver) is True  # Text changed

        mock_elem.text = "Old Text"
        assert cond(mock_driver) is False  # Text same

    def test_condition_element_count(self):
        """Test custom condition element_count."""
        mock_driver = MagicMock()
        mock_driver.find_elements.return_value = [1, 2, 3]  # 3 elements

        cond_exact = wait_helpers.element_count_is((By.TAG_NAME, "li"), exact_count=3)
        assert cond_exact(mock_driver) is True

        cond_min = wait_helpers.element_count_is((By.TAG_NAME, "li"), min_count=2)
        assert cond_min(mock_driver) is True

        cond_max = wait_helpers.element_count_is((By.TAG_NAME, "li"), max_count=2)
        assert cond_max(mock_driver) is False

    # --- Utility Functions Tests ---

    def test_safe_click_success(self):
        """Test click sicuro successo."""
        mock_driver = MagicMock()
        mock_elem = MagicMock()

        with patch(
            "src.bots.base.wait_helpers.wait_for_element_clickable",
            return_value=mock_elem,
        ):
            res = wait_helpers.safe_click_with_retry(mock_driver, (By.ID, "btn"))
            assert res is True
            mock_elem.click.assert_called()

    def test_safe_click_retry(self):
        """Test click con retry su intercettazione."""
        mock_driver = MagicMock()
        mock_elem = MagicMock()

        # Primo tentativo fallisce (Intercepted), secondo riesce
        mock_elem.click.side_effect = [ElementClickInterceptedException(), None]

        with patch(
            "src.bots.base.wait_helpers.wait_for_element_clickable",
            return_value=mock_elem,
        ):
            res = wait_helpers.safe_click_with_retry(mock_driver, (By.ID, "btn"), retry_delay=0.01)

            assert res is True
            assert mock_elem.click.call_count == 2

    def test_execute_with_wait(self):
        """Test execute with wait."""
        action = MagicMock(return_value=True)
        mock_driver = MagicMock()

        with patch(
            "src.bots.base.wait_helpers.wait_for_overlay_to_disappear",
            return_value=True,
        ):
            res = wait_helpers.execute_with_wait(action, mock_driver, (By.ID, "loader"))
            assert res is True
            action.assert_called()
