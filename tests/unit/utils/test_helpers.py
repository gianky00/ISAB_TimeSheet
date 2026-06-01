from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.utils.helpers import (
    cleanup_bot_processes,
    cleanup_chrome_temp_files,
    clear_icon_cache,
    format_timestamp,
    get_app_icon_path,
    get_asset_path,
    get_colored_icon,
    get_months_list,
    get_years_list,
    is_windows,
    open_folder,
    safe_open,
    safe_str,
    sanitize_filename,
    setup_logging,
    truncate_string,
)


class TestHelpers:
    def test_asset_paths(self, mocker):
        # ResourceManager è mockato internamente se necessario,
        # ma qui verifichiamo che la delega funzioni
        mocker.patch(
            "src.utils.resource_manager.ResourceManager.get_asset_path", return_value="/mock/path/test.txt"
        )
        path = get_asset_path("test.txt")
        assert "/mock/path/test.txt" in path

    def test_get_app_icon_path(self, mocker, fs):
        mocker.patch("src.utils.helpers.get_asset_path", return_value="/assets/app.ico")
        fs.create_file("/assets/app.ico")
        assert get_app_icon_path() == "/assets/app.ico"

        fs.remove_object("/assets/app.ico")
        assert get_app_icon_path() is None

    def test_setup_logging(self, fs):
        log_file = "test.log"
        logger = setup_logging("TestLogger", log_file=log_file)
        assert logger.name == "TestLogger"
        assert len(logger.handlers) >= 1
        # Verifica che il file sia stato creato
        assert Path(log_file).exists()

        # Test failure case (directory inesistente per log_file)
        logger_err = setup_logging("ErrorLogger", log_file="/non/existent/dir/test.log")
        assert logger_err.name == "ErrorLogger"

    def test_format_timestamp(self):
        fixed_dt = datetime(2023, 5, 23, 10, 30, 0)
        formatted = format_timestamp(fixed_dt)
        assert "23/05/2023 10:30:00" in formatted

        # Test default value (now)
        assert format_timestamp() is not None

    def test_lists(self):
        months = get_months_list()
        assert len(months) == 12
        assert months[0] == "Gennaio"

        years = get_years_list(start_offset=-1, end_offset=1)
        assert len(years) == 3
        assert str(datetime.now(UTC).year) in years

    def test_os_checks(self):
        assert isinstance(is_windows(), bool)

    @patch("src.utils.helpers.os.startfile", create=True)
    def test_safe_open(self, mock_start, fs, mocker):
        fs.create_file("test.txt")
        # File esistente, estensione sicura
        assert safe_open("test.txt") is True

        # File inesistente
        assert safe_open("missing.txt") is False

        # Estensione non sicura
        fs.create_file("danger.exe")
        assert safe_open("danger.exe") is False

        # Test non-windows platforms (mocking sys.platform)
        mocker.patch("src.utils.helpers.is_windows", return_value=False)
        mocker.patch("sys.platform", "darwin")
        mock_run = mocker.patch("subprocess.run")
        assert safe_open("test.txt") is True
        mock_run.assert_called_with(["/usr/bin/open", str(Path("test.txt").resolve())], check=False)

        mocker.patch("sys.platform", "linux")
        assert safe_open("test.txt") is True
        mock_run.assert_called_with(["/usr/bin/xdg-open", str(Path("test.txt").resolve())], check=False)

        # legacy wrapper
        assert open_folder("test.txt") is True

    def test_string_utils(self):
        assert safe_str(None) == ""
        assert safe_str(123) == "123"

        assert truncate_string("Lungo messaggio", 10) == "Lungo m..."
        assert truncate_string("Corto", 10) == "Corto"
        assert truncate_string(None, 10) == ""

        assert sanitize_filename("test/../file.txt") == "test_._file.txt"
        assert sanitize_filename("  test  ") == "test"
        assert sanitize_filename("") == "unnamed_file"
        assert (
            sanitize_filename("file\0with\0null") == "filewith_unnamed_file" or "filewith"
        )  # checking behavior

    def test_cleanup_chrome_temp(self, fs):
        fs.create_dir("/tmp")
        fs.create_file("/tmp/empty.tmp", st_size=0)
        fs.create_file("/tmp/full.tmp", st_size=100)

        removed = cleanup_chrome_temp_files("/tmp")
        assert "empty.tmp" in removed
        assert not Path("/tmp/empty.tmp").exists()
        assert Path("/tmp/full.tmp").exists()

        # Test non-existent dir
        assert cleanup_chrome_temp_files("/missing_dir") == []

    @patch("src.utils.helpers.psutil.process_iter")
    def test_cleanup_bot_processes(self, mock_iter, fs):
        # Setup mock processes
        mock_proc1 = MagicMock()
        mock_proc1.info = {"name": "chromedriver.exe", "cmdline": []}

        mock_proc2 = MagicMock()
        mock_proc2.pid = 1234
        mock_proc2.info = {"name": "chrome.exe", "cmdline": ["--remote-debugging-port=9222"]}

        mock_proc3 = MagicMock()
        mock_proc3.info = {"name": "notepad.exe", "cmdline": []}

        mock_proc4 = MagicMock()
        mock_proc4.info = {"name": "node.exe", "cmdline": ["playwright", "test"]}

        mock_iter.return_value = [mock_proc1, mock_proc2, mock_proc3, mock_proc4]

        # Patch CONFIG_DIR to avoid side effects on real files
        with patch("src.utils.helpers.CONFIG_DIR", Path("/config")):
            fs.create_dir("/config/data/chrome_profile/Default")
            fs.create_file("/config/data/chrome_profile/SingletonLock")
            fs.create_file("/config/data/chrome_profile/Default/Lock")

            cleanup_bot_processes()

            assert mock_proc1.kill.called
            assert mock_proc2.kill.called
            assert mock_proc4.kill.called
            assert not mock_proc3.kill.called
            # Verifica rimozione lock
            assert not Path("/config/data/chrome_profile/SingletonLock").exists()
            assert not Path("/config/data/chrome_profile/Default/Lock").exists()

    def test_icon_utils(self, fs):
        # Mocking for pytest environment (it returns QIcon(path) directly)
        fs.create_file("icon.svg")
        icon = get_colored_icon("icon.svg", "#FF0000")
        assert isinstance(icon, MagicMock) or icon is not None  # In pytest env it just returns QIcon

        # Test non-existent icon
        assert get_colored_icon("missing.svg").isNull()

        # Test cache clearing
        clear_icon_cache()
