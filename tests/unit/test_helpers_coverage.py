
import os
import sys
import logging
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.utils import helpers

class TestHelpersCoverage:
    def test_sanitize_filename_empty(self):
        from src.utils.helpers import sanitize_filename
        # Stringa che diventa vuota dopo sanitizzazione e strip
        assert sanitize_filename(".") == "unnamed_file"
        assert sanitize_filename("..") == "unnamed_file"

    def test_get_asset_path_dev(self):
        """Test get_asset_path in dev mode (not frozen)."""
        with patch.object(sys, "frozen", False, create=True):
            # Percorso relativo atteso: src/utils/../../assets/test.txt -> root/assets/test.txt
            # helpers.py è in src/utils/
            path = helpers.get_asset_path("assets/test.txt")
            assert "assets" in path
            assert path.endswith(os.path.join("assets", "test.txt"))

    def test_get_asset_path_frozen(self):
        """Test get_asset_path in frozen mode (executable)."""
        with patch.object(sys, "frozen", True, create=True):
            with patch.object(sys, "executable", r"C:\App\app.exe"):
                path = helpers.get_asset_path("assets/test.txt")
                # Expected: C:\App\assets\test.txt
                assert path == os.path.join(r"C:\App", "assets", "test.txt")

    def test_get_app_icon_path(self):
        """Test get_app_icon_path functionality."""
        # Case 1: Icon exists
        with patch("os.path.exists", return_value=True):
            with patch("src.utils.helpers.get_asset_path", return_value="/path/to/icon.ico"):
                assert helpers.get_app_icon_path() == "/path/to/icon.ico"
        
        # Case 2: Icon does not exist
        with patch("os.path.exists", return_value=False):
             assert helpers.get_app_icon_path() is None

    def test_setup_logging(self, tmp_path):
        """Test logger configuration."""
        log_file = tmp_path / "test.log"
        logger = helpers.setup_logging("TestLogger", str(log_file))
        
        assert logger.name == "TestLogger"
        assert logger.level == logging.INFO
        assert len(logger.handlers) >= 1
        
        # Verify idempotency (calling again shouldn't add handlers)
        handlers_count = len(logger.handlers)
        helpers.setup_logging("TestLogger", str(log_file))
        assert len(logger.handlers) == handlers_count

        # Test exception on bad file
        with patch("logging.FileHandler", side_effect=Exception("Permesso negato")):
            logger_bad = helpers.setup_logging("BadLogger", "/root/bad.log")
            # Should not crash, just warn and log to console
            assert logger_bad.handlers  # Console handler should be there

    def test_format_timestamp(self):
        """Test format_timestamp."""
        dt = datetime(2023, 10, 25, 14, 30, 0)
        assert helpers.format_timestamp(dt) == "25/10/2023 14:30:00"
        
        # Test default (now) - just check format structure
        now_str = helpers.format_timestamp()
        assert len(now_str) == 19
        assert "/" in now_str
        assert ":" in now_str

    def test_get_months_list(self):
        months = helpers.get_months_list()
        assert len(months) == 12
        assert months[0] == "Gennaio"
        assert months[-1] == "Dicembre"

    def test_get_years_list(self):
        current = datetime.now().year
        # Default -2 to +2
        years = helpers.get_years_list()
        assert str(current) in years
        assert str(current - 2) in years
        assert str(current + 2) in years
        assert len(years) == 5

    def test_is_windows(self):
        with patch("sys.platform", "win32"):
            assert helpers.is_windows() is True
        with patch("sys.platform", "linux"):
            assert helpers.is_windows() is False

    def test_open_folder(self):
        """Test open_folder logic for different OS."""
        # Non-existent path
        with patch("os.path.exists", return_value=False):
            assert helpers.open_folder("bad/path") is False

        # Exists
        with patch("os.path.exists", return_value=True):
            # Windows
            with patch("sys.platform", "win32"):
                with patch("os.startfile") as mock_start:
                    assert helpers.open_folder("C:/Test") is True
                    mock_start.assert_called_with("C:/Test")
            
            # Darwin (Mac)
            with patch("sys.platform", "darwin"):
                with patch("subprocess.run") as mock_run:
                    assert helpers.open_folder("/tmp") is True
                    mock_run.assert_called_with(["open", "/tmp"])
            
            # Linux
            with patch("sys.platform", "linux"):
                with patch("subprocess.run") as mock_run:
                    assert helpers.open_folder("/tmp") is True
                    mock_run.assert_called_with(["xdg-open", "/tmp"])
            
            # Exception handling
            with patch("sys.platform", "win32"):
                with patch("os.startfile", side_effect=Exception("Error")):
                    assert helpers.open_folder("C:/Test") is False

    def test_safe_str(self):
        assert helpers.safe_str(None) == ""
        assert helpers.safe_str(None, "N/A") == "N/A"
        assert helpers.safe_str(123) == "123"
        assert helpers.safe_str("test") == "test"

    def test_truncate_string(self):
        assert helpers.truncate_string("Short") == "Short"
        assert helpers.truncate_string(None) == ""
        
        long_text = "Questa è una stringa molto lunga che deve essere troncata"
        truncated = helpers.truncate_string(long_text, max_length=10, suffix="..")
        assert len(truncated) == 10
        assert truncated.endswith("..")
        assert truncated == "Questa è.."

    def test_sanitize_filename(self):
        assert helpers.sanitize_filename("valid_file.txt") == "valid_file.txt"
        assert helpers.sanitize_filename("File Con Spazi.pdf") == "File Con Spazi.pdf"
        
        # Logic analysis: "../traversal.txt" -> ".._traversal.txt" -> "._traversal.txt" -> "_traversal.txt" (strip)
        # So we expect "_traversal.txt" not ".traversal.txt"
        assert helpers.sanitize_filename("../traversal.txt") == "_traversal.txt" 
        
        assert helpers.sanitize_filename("invalid|chars?.txt") == "invalid_chars_.txt"
        assert helpers.sanitize_filename(None) == "unnamed_file"
        assert helpers.sanitize_filename("") == "unnamed_file"
        # Test double underscores collapse
        assert helpers.sanitize_filename("a__b.txt") == "a_b.txt"
