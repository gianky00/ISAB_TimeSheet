import os
import zipfile
from unittest.mock import patch

import pytest

from src.core.bug_reporter import BugReporter


class TestBugReporter:
    @pytest.fixture
    def mock_structure(self, tmp_path):  # noqa: ANN001
        """Crea una struttura fittizia di log per il report."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        app_dir = log_dir / "application"
        app_dir.mkdir()
        (app_dir / "app.json").write_text('{"msg": "test"}')

        err_dir = log_dir / "errors"
        err_dir.mkdir()
        (err_dir / "error_screenshot.png").write_text("fake_image")

        reports_dir = tmp_path / "reports"
        reports_dir.mkdir()

        return tmp_path

    @patch("src.core.bug_reporter.CONFIG_DIR")
    @patch("src.core.bug_reporter.BugReporter._add_analytics_report")
    @patch("src.core.bug_reporter.BugReporter._add_audit_trail")
    def test_collect_diagnostics_success(self, mock_audit, mock_analytics, mock_config, mock_structure):  # noqa: ANN001
        """Verifica la creazione corretta dello ZIP con file attesi."""
        mock_config.__truediv__.side_effect = lambda x: mock_structure / x
        mock_analytics.return_value = ["analytics_report.json"]
        mock_audit.return_value = ["audit_trail.json"]

        zip_path, msg, files = BugReporter.collect_diagnostics()

        assert zip_path is not None
        assert zip_path.exists()
        assert "successo" in msg.lower()
        assert "system_info.json" in files

        # Verifica integrità ZIP
        with zipfile.ZipFile(zip_path, "r") as z:
            names = z.namelist()
            assert "system_info.json" in names
            assert "logs/application/app.json" in names
            assert "logs/errors/error_screenshot.png" in names

    def test_collect_system_info_security(self):
        """Verifica che le variabili d'ambiente sensibili siano filtrate."""
        with patch.dict("os.environ", {"API_KEY": "secret123", "USER_NAME": "admin"}):
            info = BugReporter._collect_system_info()
            env = info.get("env_filtered", {})

            assert "USER_NAME" in env
            assert "API_KEY" not in env  # Deve essere filtrato

    @patch("src.core.bug_reporter.CONFIG_DIR")
    def test_cleanup_old_reports(self, mock_config, tmp_path):  # noqa: ANN001
        """Verifica che vengano mantenuti solo gli ultimi N report."""
        reports_dir = tmp_path / "reports"
        reports_dir.mkdir()
        # Side effect per permettere / "reports"
        mock_config.__truediv__.side_effect = lambda x: tmp_path / x

        # Crea 7 report finti
        for i in range(7):
            f = reports_dir / f"report_{i}.zip"
            f.touch()
            # Imposta tempi di modifica diversi
            os.utime(f, (1000 + i, 1000 + i))

        BugReporter.cleanup_old_reports(max_reports=5)

        remaining = list(reports_dir.glob("*.zip"))
        assert len(remaining) == 5  # noqa: PLR2004
