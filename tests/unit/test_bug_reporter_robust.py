from unittest.mock import ANY, MagicMock, patch

import pytest

from src.core.bug_reporter import BugReporter


class TestBugReporterRobust:
    @pytest.fixture
    def mock_config_dir(self, tmp_path):
        """Mocka CONFIG_DIR con una directory temporanea."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Crea struttura logs
        log_dir = config_dir / "logs"
        log_dir.mkdir()
        (log_dir / "application").mkdir()
        (log_dir / "application" / "app.log").write_text("Log Content")

        with patch("src.core.bug_reporter.CONFIG_DIR", config_dir):
            yield config_dir

    @patch("src.core.bug_reporter.zipfile.ZipFile")
    @patch("src.core.bug_reporter.datetime")
    @patch("src.core.bug_reporter.BugReporter._collect_system_info")
    def test_collect_diagnostics_success(self, mock_sys_info, mock_datetime, mock_zip, mock_config_dir):
        """Test creazione report con successo."""
        mock_datetime.now.return_value.strftime.return_value = "20230101_120000"
        mock_zip_instance = mock_zip.return_value.__enter__.return_value

        # Mock system info sicuro per JSON
        mock_sys_info.return_value = {"os": "TestOS", "version": "1.0"}

        path, msg, files = BugReporter.collect_diagnostics(
            include_enterprise_logs=True,
            include_analytics=False,  # Evitiamo import complessi per ora
            include_audit=False,
        )

        assert path is not None
        assert path.name == "syncrojob_report_20230101_120000.zip"
        assert "Report generato" in msg
        assert "logs/application/app.log" in files
        assert "system_info.json" in files

        # Verifica scrittura ZIP
        mock_zip_instance.write.assert_any_call(
            mock_config_dir / "logs" / "application" / "app.log",
            arcname="logs/application/app.log",
        )

    @patch("src.core.logging.generate_analytics_report")
    @patch("src.core.bug_reporter.zipfile.ZipFile")
    def test_add_analytics_report(self, mock_zip, mock_gen_report):
        """Test aggiunta report analytics."""
        mock_zip_instance = mock_zip.return_value

        # Mock report object
        mock_report = MagicMock()
        mock_report.health_score = 95
        mock_report.anomalies = []
        mock_report.patterns = []
        mock_gen_report.return_value = mock_report

        # Non serve patchare sys.modules se patchiamo direttamente il target
        # Assumiamo che src.core.logging sia importabile
        files = BugReporter._add_analytics_report(mock_zip_instance, hours=24)

        assert "analytics_report.json" in files
        mock_zip_instance.writestr.assert_called_with("analytics_report.json", ANY)

    @patch("src.core.audit.AuditManager")
    @patch("src.core.bug_reporter.zipfile.ZipFile")
    def test_add_audit_trail(self, mock_zip, mock_audit_cls):
        """Test aggiunta audit trail."""
        mock_zip_instance = mock_zip.return_value
        mock_manager = mock_audit_cls.instance.return_value
        mock_manager.get_recent_actions.return_value = [{"action": "Test"}]

        with patch.dict("sys.modules", {"src.core.audit": MagicMock(AuditManager=mock_audit_cls)}):
            files = BugReporter._add_audit_trail(mock_zip_instance)

        assert "audit_trail.json" in files
        mock_zip_instance.writestr.assert_called_with("audit_trail.json", ANY)

    def test_collect_system_info(self):
        """Test raccolta info sistema."""
        with patch("platform.system", return_value="TestOS"):
            with patch("src.core.bug_reporter.get_version", return_value="1.0.0"):
                info = BugReporter._collect_system_info()
                assert info["os"] == "TestOS"
                assert info["app_version"] == "1.0.0"
                # Verifica filtro env
                assert "env_filtered" in info

    def test_cleanup_old_reports(self, mock_config_dir):
        """Test pulizia vecchi report."""
        reports_dir = mock_config_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        # Crea 10 report
        for i in range(10):
            (reports_dir / f"report_{i}.zip").touch()

        BugReporter.cleanup_old_reports(max_reports=5)

        remaining = list(reports_dir.glob("*.zip"))
        assert len(remaining) == 5

    def test_get_estimated_size(self, mock_config_dir):
        """Test stima dimensione."""
        size_str = BugReporter.get_estimated_size()
        assert "KB" in size_str or "MB" in size_str

    @patch("src.core.bug_reporter.zipfile.ZipFile")
    def test_collect_diagnostics_error(self, mock_zip, mock_config_dir):
        """Test gestione errore durante creazione ZIP."""
        mock_zip.side_effect = Exception("Disk Full")

        path, msg, _files = BugReporter.collect_diagnostics()

        assert path is None
        assert "Errore creazione report" in msg
        assert "Disk Full" in msg

    @patch("src.core.bug_reporter.zipfile.ZipFile")
    def test_add_bot_errors(self, mock_zip, mock_config_dir):
        """Test aggiunta screenshot errori."""
        error_dir = mock_config_dir / "logs" / "errors"
        error_dir.mkdir(parents=True, exist_ok=True)
        (error_dir / "screenshot.png").touch()

        mock_zip_instance = mock_zip.return_value

        files = BugReporter._add_bot_errors(mock_zip_instance, error_dir)

        assert "logs/errors/screenshot.png" in files
        mock_zip_instance.write.assert_called()
