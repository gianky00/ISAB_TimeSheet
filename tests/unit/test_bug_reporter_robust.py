import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.core.bug_reporter import BugReporter


class TestBugReporterRobust:
    @pytest.fixture
    def mock_config_dir(self):
        with patch("src.core.bug_reporter.CONFIG_DIR", Path("/mock/config")) as p:
            yield p

    @patch("src.core.bug_reporter.zipfile.ZipFile")
    @patch("src.core.bug_reporter.BugReporter._add_enterprise_logs")
    @patch("src.core.bug_reporter.BugReporter._add_bot_errors")
    @patch("src.core.bug_reporter.BugReporter._add_analytics_report")
    @patch("src.core.bug_reporter.BugReporter._add_audit_trail")
    @patch("src.core.bug_reporter.BugReporter._collect_system_info")
    def test_collect_diagnostics_full(
        self,
        mock_sys,
        mock_audit,
        mock_analytics,
        mock_errors,
        mock_logs,
        mock_zip,
        mock_config_dir,
    ):
        # Setup mocks
        mock_zip_instance = mock_zip.return_value.__enter__.return_value
        mock_sys.return_value = {"os": "Windows"}
        mock_logs.return_value = ["app.log"]
        mock_audit.return_value = ["audit.json"]

        # Simuliamo esistenza cartelle
        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "mkdir"):
                path, msg, files = BugReporter.collect_diagnostics(trace_id="123")

                assert path is not None
                assert "app.log" in files
                assert "audit.json" in files

                # Verifiche chiamate
                mock_logs.assert_called()
                mock_errors.assert_called()
                mock_analytics.assert_called()
                mock_audit.assert_called()
                mock_sys.assert_called()

                # Verify system info write
                mock_zip_instance.writestr.assert_any_call(
                    "system_info.json", json.dumps({"os": "Windows"}, indent=2)
                )

    def test_collect_system_info(self):
        with patch("platform.system", return_value="TestOS"):
            with patch("platform.release", return_value="1.0"):
                with patch("src.core.bug_reporter.get_version", return_value="1.0.0"):
                    info = BugReporter._collect_system_info()
                    assert info["os"] == "TestOS"
                    assert info["app_version"] == "1.0.0"

    @patch("src.core.bug_reporter.zipfile.ZipFile")
    def test_collect_diagnostics_no_permissions(self, mock_zip, mock_config_dir):
        # Simuliamo errore permessi
        mock_zip.side_effect = PermissionError("Access Denied")

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "mkdir"):
                path, msg, files = BugReporter.collect_diagnostics()

                assert path is None
                assert "Errore" in msg or "Access Denied" in str(msg)
