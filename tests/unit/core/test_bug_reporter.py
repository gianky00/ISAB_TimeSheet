from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.bug_reporter import BugReporter


class TestBugReporter:
    @pytest.fixture(autouse=True)
    def setup_bug_env(self, fs):
        self.fake_config = Path("/fake_config")
        fs.create_dir(str(self.fake_config))
        fs.create_dir(str(self.fake_config / "logs" / "application"))
        fs.create_dir(str(self.fake_config / "logs" / "errors"))
        fs.create_dir(str(self.fake_config / "reports"))

        # Create some fake logs
        fs.create_file(str(self.fake_config / "logs" / "application" / "app.log"), contents=b"log content")
        fs.create_file(str(self.fake_config / "logs" / "errors" / "error1.png"), contents=b"fake png")

        # Patching CONFIG_DIR inside bug_reporter
        with patch("src.core.bug_reporter.CONFIG_DIR", self.fake_config):
            yield

    @patch("src.core.bug_reporter.DiagnosticsCollector.collect_system_info")
    @patch("src.core.bug_reporter.AuditManager.instance")
    @patch("src.core.bug_reporter.generate_analytics_report")
    def test_collect_diagnostics_success(self, mock_analytics, mock_audit, mock_sys):
        mock_sys.return_value = {"os": "windows"}
        mock_audit.return_value.get_logs.return_value = []
        mock_analytics.return_value = MagicMock(health_score=100, anomalies=[], patterns=[])

        path, msg, files = BugReporter.collect_diagnostics()

        assert path is not None
        assert path.exists()
        assert "successo" in msg
        assert "system_info.json" in files

    def test_collect_diagnostics_failure(self):
        # Forza errore patchando datetime
        with patch("src.core.bug_reporter.datetime") as mock_dt:
            mock_dt.now.side_effect = Exception("Crash")
            path, msg, _files = BugReporter.collect_diagnostics()
            assert path is None
            assert "Errore" in msg

    def test_cleanup_old_reports(self, fs):
        reports_dir = self.fake_config / "reports"
        # Creiamo 10 report finti
        for i in range(10):
            fs.create_file(str(reports_dir / f"report_{i}.zip"))

        BugReporter.cleanup_old_reports(max_reports=5)

        remaining = list(reports_dir.glob("*.zip"))
        assert len(remaining) == 5

    def test_get_estimated_size(self):
        size_str = BugReporter.get_estimated_size()
        assert "KB" in size_str or "MB" in size_str
