import os
import time
import zipfile
from unittest.mock import MagicMock, patch

import pytest

from src.core.bug_reporter import BugReporter


class TestBugReporter:
    @pytest.fixture(autouse=True)
    def setup_dirs(self, tmp_path):
        """Setup temporary directory and mock CONFIG_DIR."""
        self.temp_config = tmp_path / "config"
        self.temp_config.mkdir()
        self.log_dir = self.temp_config / "logs"
        self.log_dir.mkdir()
        (self.log_dir / "application").mkdir()
        (self.log_dir / "errors").mkdir()
        self.report_dir = self.temp_config / "reports"
        self.report_dir.mkdir()

        # Patch CONFIG_DIR in bug_reporter module
        with patch("src.core.bug_reporter.CONFIG_DIR", self.temp_config):
            yield

    @patch("src.core.bug_reporter.AuditManager.instance")
    @patch("src.core.bug_reporter.generate_analytics_report")
    def test_collect_diagnostics_success(self, mock_analytics, mock_audit):
        # 1. Setup mock data
        log_file = self.log_dir / "application" / "app.log"
        log_file.write_text("log content")

        mock_audit_inst = mock_audit.return_value
        mock_audit_inst.get_logs.return_value = [{"action": "test"}]

        mock_report = MagicMock()
        mock_report.health_score = 90
        mock_report.anomalies = []
        mock_report.patterns = []
        mock_analytics.return_value = mock_report

        # 2. Run
        with patch("src.core.bug_reporter.CONFIG_DIR", self.temp_config):
            zip_path, msg, files = BugReporter.collect_diagnostics()

        # 3. Verify
        assert zip_path is not None
        assert zip_path.exists()
        assert "successo" in msg

        # Verify returned list
        assert any("app.log" in f for f in files)

        # Verify ZIP content
        with zipfile.ZipFile(zip_path, "r") as z:
            names = z.namelist()
            assert "system_info.json" in names
            assert "logs/application/app.log" in names
            assert "audit_trail.json" in names
            assert "analytics_report.json" in names

    def test_collect_system_info(self):
        info = BugReporter._collect_system_info()
        assert "app_version" in info
        assert "os" in info

        # Check environment filtering
        os.environ["MY_SECRET_KEY"] = "hidden"
        os.environ["SAFE_VAR"] = "visible"
        info = BugReporter._collect_system_info()
        assert "MY_SECRET_KEY" not in info["env_filtered"]
        assert "SAFE_VAR" in info["env_filtered"]

    def test_cleanup_old_reports(self):
        # Create files with explicit modification times
        now = time.time()
        for i in range(10):
            p = self.report_dir / f"report_{i}.zip"
            p.write_text("zip")
            os.utime(p, (now + i, now + i))

        with patch("src.core.bug_reporter.CONFIG_DIR", self.temp_config):
            BugReporter.cleanup_old_reports(max_reports=3)

        reports = list(self.report_dir.glob("*.zip"))
        assert len(reports) == 3

    def test_get_estimated_size(self):
        log_file = self.log_dir / "application" / "big.log"
        log_file.write_text("x" * 1024 * 500)  # 500KB

        with patch("src.core.bug_reporter.CONFIG_DIR", self.temp_config):
            size_str = BugReporter.get_estimated_size()
        assert "KB" in size_str or "MB" in size_str
        assert "~5" in size_str or "~0.5" in size_str
