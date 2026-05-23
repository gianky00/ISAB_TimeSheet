import json
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.bug_reporter import BugReporter


class TestBugReporter:
    @pytest.fixture(autouse=True)
    def setup_dirs(self, fs):
        # Mocking CONFIG_DIR and log structure
        self.config_dir = Path("/config")
        fs.create_dir(str(self.config_dir))
        self.log_dir = self.config_dir / "logs"
        fs.create_dir(str(self.log_dir))
        fs.create_dir(str(self.log_dir / "application"))
        fs.create_dir(str(self.log_dir / "errors"))

        # Patch CONFIG_DIR in the module
        with patch("src.core.bug_reporter.CONFIG_DIR", self.config_dir):
            yield

    @patch("src.core.bug_reporter.DiagnosticsCollector.collect_system_info")
    @patch("src.core.bug_reporter.generate_analytics_report")
    @patch("src.core.bug_reporter.AuditManager.instance")
    def test_collect_diagnostics_success(self, mock_audit, mock_analytics, mock_sys_info, fs):
        mock_sys_info.return_value = {"os": "linux"}

        # Setup mock report
        mock_rep = MagicMock()
        mock_rep.health_score = 100
        mock_rep.anomalies = []
        mock_rep.patterns = []
        mock_analytics.return_value = mock_rep

        # Setup mock audit
        mock_audit.return_value.get_logs.return_value = [{"action": "test"}]

        # Create some log files
        fs.create_file(str(self.log_dir / "application" / "app.json"), contents='{"log":1}')
        fs.create_file(str(self.log_dir / "errors" / "error1.png"), contents=b"FAKE_PNG")

        zip_path, _msg, files = BugReporter.collect_diagnostics()

        assert zip_path.exists()
        assert "system_info.json" in files
        assert "analytics_report.json" in files
        assert "audit_trail.json" in files

        # Verify ZIP content
        with zipfile.ZipFile(zip_path, "r") as z:
            namelist = z.namelist()
            assert "system_info.json" in namelist
            assert "logs/application/app.json" in namelist
            assert "analytics_report.json" in namelist
            assert "audit_trail.json" in namelist

    @patch("src.core.bug_reporter.view_trace")
    def test_add_trace_timeline(self, mock_view_trace, fs):
        mock_view_trace.return_value = [{"event": "start"}]
        report_path = self.config_dir / "test_report.zip"

        with zipfile.ZipFile(report_path, "w") as zipf:
            added = BugReporter._add_trace_timeline(zipf, "TRACE-123")

        assert len(added) == 1
        assert "trace_TRACE-12.json" in added

        with zipfile.ZipFile(report_path, "r") as z:
            data = json.loads(z.read("trace_TRACE-12.json"))
            assert data["trace_id"] == "TRACE-123"

    def test_cleanup_old_reports(self, fs):
        reports_dir = self.config_dir / "reports"
        fs.create_dir(str(reports_dir))

        # Crea 10 vecchi report
        for i in range(10):
            fs.create_file(str(reports_dir / f"report_{i}.zip"))
            # Sostituito time.sleep con manipolazione mtime se possibile,
            # ma qui basta crearli in sequenza.

        BugReporter.cleanup_old_reports(max_reports=3)

        remaining = list(reports_dir.glob("*.zip"))
        assert len(remaining) == 3

    def test_get_estimated_size(self, fs):
        fs.create_file(str(self.log_dir / "application" / "app.json"), contents="A" * 2048)  # 2KB

        est = BugReporter.get_estimated_size()
        assert "KB" in est
        # 50 (base) + 2 (app.json) + 10 (analytics) + 20 (audit) = 82 KB
        assert "~82 KB" in est
