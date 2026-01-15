import os
from datetime import datetime
from unittest.mock import patch

from src.utils.helpers import (
    format_timestamp,
    get_asset_path,
    get_months_list,
    get_years_list,
    safe_str,
    sanitize_filename,
    setup_logging,
    truncate_string,
)


class TestHelpers:
    def test_get_asset_path(self):
        # Development mode
        with patch("sys.frozen", False, create=True):
            path = get_asset_path("assets/test.txt")
            assert "assets" in path
            assert "test.txt" in path

        # Frozen mode
        with patch("sys.frozen", True, create=True):
            with patch("sys.executable", "C:\\App\\app.exe"):
                path = get_asset_path("assets/test.txt")
                assert path.startswith("C:\\App")

    def test_format_timestamp(self):
        dt = datetime(2026, 1, 15, 10, 30, 0)
        assert format_timestamp(dt) == "15/01/2026 10:30:00"
        # Test default now
        assert "2026" in format_timestamp()

    def test_get_months_list(self):
        months = get_months_list()
        assert len(months) == 12
        assert months[0] == "Gennaio"

    def test_get_years_list(self):
        years = get_years_list(start_offset=-1, end_offset=1)
        current_year = datetime.now().year
        assert str(current_year) in years
        assert str(current_year - 1) in years
        assert str(current_year + 1) in years
        assert len(years) == 3

    def test_safe_str(self):
        assert safe_str(None, "default") == "default"
        assert safe_str(123) == "123"
        assert safe_str("hello") == "hello"

    def test_truncate_string(self):
        text = "This is a very long string that should be truncated"
        assert truncate_string(text, 10) == "This is..."
        assert truncate_string("short", 50) == "short"
        assert truncate_string("", 10) == ""

    def test_sanitize_filename(self):
        assert sanitize_filename("test/file.txt") == "test_file.txt"
        assert sanitize_filename("file*with?chars.png") == "file_with_chars.png"
        assert sanitize_filename("..\\") == "_"
        assert sanitize_filename("   spaced file   ") == "spaced file"
        assert sanitize_filename(None) == "unnamed_file"

    def test_setup_logging(self, tmp_path):
        log_file = str(tmp_path / "test.log")
        logger = setup_logging("TestLogger", log_file)

        assert logger.name == "TestLogger"
        assert len(logger.handlers) >= 1

        logger.info("Test message")
        assert os.path.exists(log_file)
        with open(log_file, "r") as f:
            assert "Test message" in f.read()
