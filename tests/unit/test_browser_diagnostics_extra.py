from unittest.mock import MagicMock

import psutil

from src.infrastructure.utils.browser_diagnostics import (
    _check_filesystem,
    _check_processes,
    _save_report,
    _test_bare_launch,
    emergency_profile_reset,
    run_browser_diagnostic,
)


def test_run_browser_diagnostic_fail_overall(tmp_path, mocker):
    mocker.patch(
        "src.infrastructure.utils.browser_diagnostics._check_filesystem",
        return_value={"status": "FAIL", "details": []},
    )
    mocker.patch("src.infrastructure.utils.browser_diagnostics._save_report")
    report = run_browser_diagnostic(tmp_path)
    assert report["overall_status"] == "FAIL"


def test_check_filesystem_mkdir_error(tmp_path, mocker):
    target = tmp_path / "foo"
    mocker.patch("pathlib.Path.mkdir", side_effect=Exception("Mocked error"))
    res = _check_filesystem(target)
    assert res["status"] == "FAIL"


def test_check_filesystem_write_error(tmp_path, mocker):
    target = tmp_path / "foo"
    target.mkdir()
    mocker.patch("pathlib.Path.write_text", side_effect=Exception("Write error"))
    res = _check_filesystem(target)
    assert res["status"] == "FAIL"


def test_check_processes_exceptions(tmp_path, mocker):
    # Simulate an access denied exception when trying to inspect a process
    mock_proc = MagicMock()
    type(mock_proc).info = mocker.PropertyMock(side_effect=psutil.AccessDenied(pid=123))
    mocker.patch("psutil.process_iter", return_value=[mock_proc])

    res = _check_processes(tmp_path)
    # The exception should be ignored, returning PASS
    assert res["status"] == "PASS"


def test_test_bare_launch_exception(mocker):
    mocker.patch(
        "src.infrastructure.utils.browser_diagnostics.sync_playwright",
        side_effect=Exception("Playwright failure"),
    )
    res = _test_bare_launch()
    assert res["status"] == "FAIL"


def test_save_report_exception(tmp_path, mocker):
    # Mock CONFIG_DIR
    mocker.patch("src.infrastructure.utils.browser_diagnostics.config_manager.CONFIG_DIR", tmp_path)
    mocker.patch("pathlib.Path.open", side_effect=Exception("JSON error"))
    # Should not raise
    _save_report({"status": "PASS"})


def test_emergency_profile_reset_exception(tmp_path, mocker):
    target = tmp_path / "profile"
    target.mkdir()
    mocker.patch("shutil.move", side_effect=Exception("Move error"))
    assert emergency_profile_reset(target) is False
