import zipfile
from unittest.mock import patch

from src.core.bug_reporter import BugReporter


class TestBugReporter:
    @patch("src.core.bug_reporter.CONFIG_DIR")
    def test_collect_diagnostics_creates_zip(self, mock_config_dir, tmp_path):
        mock_config_dir.__truediv__ = lambda self, x: tmp_path / x
        mock_config_dir.exists.return_value = True

        # Create mock log directory
        logs_dir = tmp_path / "logs"
        logs_dir.mkdir(parents=True)

        with (
            patch(
                "src.core.bug_reporter.BugReporter._add_enterprise_logs",
                return_value=["log1.txt"],
            ),
            patch(
                "src.core.bug_reporter.BugReporter._add_analytics_report",
                return_value=[],
            ),
            patch(
                "src.core.bug_reporter.BugReporter._add_audit_trail",
                return_value=[],
            ),
        ):
            path, msg, files = BugReporter.collect_diagnostics(
                include_enterprise_logs=True,
                include_analytics=False,
                include_audit=False,
            )

        assert path is not None
        assert "Report generato" in msg
        assert "system_info.json" in files

    def test_collect_system_info(self):
        info = BugReporter._collect_system_info()

        assert "app_version" in info
        assert "os" in info
        assert "python_version" in info
        assert "timestamp" in info

    def test_system_info_filters_sensitive_env(self):
        with patch.dict(
            "os.environ",
            {"NORMAL_VAR": "ok", "API_KEY": "secret", "MY_TOKEN": "hidden"},
        ):
            info = BugReporter._collect_system_info()

            env = info.get("env_filtered", {})
            assert "NORMAL_VAR" in env
            assert "API_KEY" not in env
            assert "MY_TOKEN" not in env

    def test_get_estimated_size(self, tmp_path):
        with patch("src.core.bug_reporter.CONFIG_DIR", tmp_path):
            size = BugReporter.get_estimated_size(
                include_enterprise_logs=False,
                include_analytics=True,
                include_audit=True,
            )

            assert "KB" in size or "MB" in size

    @patch("src.core.bug_reporter.CONFIG_DIR")
    def test_cleanup_old_reports(self, mock_config_dir, tmp_path):
        reports_dir = tmp_path / "reports"
        reports_dir.mkdir(parents=True)

        # Create 7 fake reports
        for i in range(7):
            (reports_dir / f"report_{i}.zip").touch()

        mock_config_dir.__truediv__ = lambda self, x: tmp_path / x

        BugReporter.cleanup_old_reports(max_reports=5)

        remaining = list(reports_dir.glob("*.zip"))
        assert len(remaining) == 5

    def test_add_bot_errors(self, tmp_path):
        error_dir = tmp_path / "errors"
        error_dir.mkdir(parents=True)

        # Create mock error files
        for i in range(15):
            (error_dir / f"screenshot_{i}.png").touch()

        with zipfile.ZipFile(tmp_path / "test.zip", "w") as zipf:
            added = BugReporter._add_bot_errors(zipf, error_dir)

        # Should only add 10 most recent
        assert len(added) == 10
