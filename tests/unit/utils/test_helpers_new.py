import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from PySide6.QtGui import QIcon

from src.core.constants import BrowserConfig
from src.utils.helpers import (
    cleanup_bot_processes,
    cleanup_chrome_temp_files,
    clear_icon_cache,
    format_timestamp,
    get_app_icon_path,
    get_asset_path,
    get_colored_icon,
    get_years_list,
    safe_str,
    sanitize_filename,
    setup_logging,
    truncate_string,
)


class TestHelpers:
    def test_get_asset_path(self):
        path = get_asset_path("test.txt")
        assert "assets" in path
        assert "test.txt" in path

    def test_get_app_icon_path(self, fs):
        # Setup fake asset path
        with patch("src.utils.helpers.get_asset_path", return_value="/assets/app.ico"):
            fs.create_file("/assets/app.ico")
            assert get_app_icon_path() == "/assets/app.ico"

    def test_setup_logging(self):
        logger = setup_logging("TestLogger")
        assert logger.name == "TestLogger"
        assert len(logger.handlers) >= 1

    def test_format_timestamp(self):
        from datetime import datetime

        dt = datetime(2023, 5, 23, 10, 0, 0)
        assert "23/05/2023 10:00:00" in format_timestamp(dt)

    def test_get_years_list(self):
        years = get_years_list(start_offset=-1, end_offset=1)
        assert len(years) == 3
        assert "2026" in years

    def test_truncate_string(self):
        assert truncate_string("Hello World", 5) == "He..."
        assert truncate_string("Short", 20) == "Short"
        assert truncate_string("", 5) == ""

    def test_sanitize_filename(self):
        assert sanitize_filename("test/../file.txt") == "test_._file.txt"
        assert sanitize_filename("  test file  ") == "test file"
        assert sanitize_filename(None) == "unnamed_file"

    def test_safe_str(self):
        assert safe_str(123) == "123"
        assert safe_str(None, "N/A") == "N/A"

    def test_cleanup_chrome_temp_files(self, fs):
        fs.create_dir("/tmp")
        fs.create_file("/tmp/empty.txt", contents=b"")
        fs.create_file("/tmp/full.txt", contents=b"data")

        removed = cleanup_chrome_temp_files("/tmp")
        assert "empty.txt" in removed
        assert not os.path.exists("/tmp/empty.txt")
        assert os.path.exists("/tmp/full.txt")

    @patch("src.utils.helpers.psutil.process_iter")
    def test_cleanup_bot_processes(self, mock_iter, fs):
        # Simula processo zombie
        mock_proc = MagicMock()
        mock_proc.info = {"name": "chromedriver.exe", "cmdline": ["chromedriver.exe"]}
        mock_iter.return_value = [mock_proc]

        # Patching CONFIG_DIR in helpers directly to ensure pyfakefs works on it
        fake_config_dir = Path("/fake_config")
        fs.create_dir("/fake_config/data/" + BrowserConfig.CACHE_DIR_NAME)
        lock_file = fake_config_dir / "data" / BrowserConfig.CACHE_DIR_NAME / "SingletonLock"
        fs.create_file(str(lock_file))

        with patch("src.utils.helpers.CONFIG_DIR", fake_config_dir):
            with patch("src.utils.helpers.logging.getLogger"):
                cleanup_bot_processes()

        assert mock_proc.kill.called
        assert not os.path.exists(str(lock_file))

    def test_icon_logic(self, fs):
        fs.create_file("icon.svg")
        clear_icon_cache()
        icon = get_colored_icon("icon.svg", "#FF0000")
        assert isinstance(icon, QIcon)
        clear_icon_cache()
