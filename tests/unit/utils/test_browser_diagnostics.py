from pathlib import Path
from unittest.mock import MagicMock, patch

from src.utils.browser_diagnostics import (
    _check_filesystem,
    _check_processes,
    _test_bare_launch,
    emergency_profile_reset,
    run_browser_diagnostic,
)


class TestBrowserDiagnostics:
    def test_check_filesystem_pass(self, fs):
        path = Path("/fake/profile")
        fs.create_dir(str(path))

        res = _check_filesystem(path)
        assert res["status"] == "PASS"
        assert any("scrittura OK" in d for d in res["details"])

    def test_check_filesystem_fail_write(self, fs):
        # Usiamo un approccio con Mock senza spec per massima flessibilità
        path = MagicMock()
        path.name = "profile"
        path.exists.return_value = True

        test_file = MagicMock()
        test_file.write_text.side_effect = Exception("Write Error")
        path.__truediv__.return_value = test_file

        res = _check_filesystem(path)
        assert res["status"] == "FAIL"
        assert "Write Error" in res["details"][0]

    @patch("src.utils.browser_diagnostics.psutil.process_iter")
    def test_check_processes(self, mock_iter):
        path = Path("/myprofile")
        path_str = str(path)

        mock_proc = MagicMock()
        mock_proc.info = {"name": "chrome.exe", "cmdline": ["chrome.exe", f"--user-data-dir={path_str}"]}
        mock_proc.pid = 123
        mock_iter.return_value = [mock_proc]

        res = _check_processes(path)
        assert res["status"] == "WARNING"
        assert "chrome.exe (PID: 123)" in res["details"][0]

    @patch("src.utils.browser_diagnostics.sync_playwright")
    def test_test_bare_launch_success(self, mock_sync):
        mock_p = mock_sync.return_value.__enter__.return_value
        mock_browser = mock_p.chromium.launch.return_value

        res = _test_bare_launch()
        assert res["status"] == "PASS"
        assert mock_browser.new_page.called

    @patch("src.utils.browser_diagnostics.sync_playwright", side_effect=Exception("No binary"))
    def test_test_bare_launch_fail(self, mock_sync):
        res = _test_bare_launch()
        assert res["status"] == "FAIL"
        assert "No binary" in res["details"][0]

    @patch("src.utils.browser_diagnostics._check_filesystem")
    @patch("src.utils.browser_diagnostics._check_processes")
    @patch("src.utils.browser_diagnostics._test_bare_launch")
    @patch("src.utils.browser_diagnostics._save_report")
    def test_run_browser_diagnostic_integration(self, mock_save, mock_launch, mock_proc, mock_fs):
        mock_fs.return_value = {"status": "PASS", "details": []}
        mock_proc.return_value = {"status": "PASS", "details": []}
        mock_launch.return_value = {"status": "FAIL", "details": ["Err"]}

        report = run_browser_diagnostic("/tmp")

        assert report["overall_status"] == "FAIL"
        assert mock_save.called

    @patch("src.utils.browser_diagnostics.cleanup_bot_processes")
    @patch("src.utils.browser_diagnostics.shutil.move")
    def test_emergency_profile_reset_success(self, mock_move, mock_cleanup, fs):
        path = Path("/profile")
        fs.create_dir(str(path))

        res = emergency_profile_reset(path)
        assert res is True
        assert mock_move.called
        assert mock_cleanup.called

    def test_emergency_profile_reset_not_exists(self):
        assert emergency_profile_reset(Path("/nonexistent")) is False
