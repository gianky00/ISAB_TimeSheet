from unittest.mock import MagicMock

from src.infrastructure.utils.helpers import (
    _kill_automation_browsers,
    _remove_profile_locks,
    cleanup_chrome_temp_files,
    clear_icon_cache,
    safe_open,
)


def test_safe_open_blacklist(tmp_path):
    bad_file = tmp_path / "test.exe"
    bad_file.write_text("dummy")
    assert safe_open(bad_file) is False


def test_safe_open_darwin(tmp_path, mocker):
    good_file = tmp_path / "test.txt"
    good_file.write_text("dummy")

    mocker.patch("src.infrastructure.utils.helpers.sys.platform", "darwin")
    mock_run = mocker.patch("src.infrastructure.utils.helpers.subprocess.run")
    assert safe_open(good_file) is True
    mock_run.assert_called_once()


def test_safe_open_linux(tmp_path, mocker):
    good_file = tmp_path / "test.txt"
    good_file.write_text("dummy")

    mocker.patch("src.infrastructure.utils.helpers.sys.platform", "linux")
    mock_run = mocker.patch("src.infrastructure.utils.helpers.subprocess.run")
    assert safe_open(good_file) is True
    mock_run.assert_called_once()


def test_cleanup_chrome_temp_files(tmp_path):
    good = tmp_path / "good.txt"
    good.write_text("hello")
    empty = tmp_path / "empty.txt"
    empty.touch()

    res = cleanup_chrome_temp_files(tmp_path)
    assert len(res) == 1
    assert "empty.txt" in res
    assert good.exists()
    assert not empty.exists()


def test_cleanup_chrome_temp_files_exception(tmp_path, mocker):
    empty = tmp_path / "empty.txt"
    empty.touch()
    mocker.patch("pathlib.Path.unlink", side_effect=PermissionError("Locked"))
    res = cleanup_chrome_temp_files(tmp_path)
    assert len(res) == 0


def test_remove_profile_locks(tmp_path, mocker):
    mocker.patch("src.infrastructure.utils.helpers.CONFIG_DIR", tmp_path)
    profile_dir = tmp_path / "data" / "chrome_profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    (profile_dir / "Lock").touch()
    (profile_dir / "Default").mkdir()
    (profile_dir / "Default" / "SingletonLock").touch()

    logger = MagicMock()
    _remove_profile_locks(logger)

    assert not (profile_dir / "Lock").exists()
    assert not (profile_dir / "Default" / "SingletonLock").exists()


def test_kill_automation_browsers(mocker):
    logger = MagicMock()
    mock_proc = MagicMock()
    mock_proc.info = {"name": "chrome.exe", "cmdline": ["--remote-debugging-port=9222"]}
    mocker.patch("src.infrastructure.utils.helpers.psutil.process_iter", return_value=[mock_proc])
    _kill_automation_browsers(logger)
    mock_proc.kill.assert_called_once()


def test_clear_icon_cache():
    clear_icon_cache()
