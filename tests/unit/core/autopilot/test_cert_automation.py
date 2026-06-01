from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from src.core.autopilot.cert_automation import CertCampioneAutomator


class TestCertCampioneAutomator:
    @pytest.fixture
    def mock_mw(self):
        return MagicMock()

    @pytest.fixture
    def automator(self, mock_mw):
        return CertCampioneAutomator(mock_mw)

    def test_check_and_run_never_sent(self, automator):
        with patch.object(automator, "run") as mock_run:
            config = {"certificati_autopilot_interval_days": 1, "certificati_autopilot_last_sent": None}
            automator.check_and_run(config)
            mock_run.assert_called_once_with(config)

    def test_check_and_run_recent(self, automator):
        with patch.object(automator, "run") as mock_run:
            last_sent = datetime.now() - timedelta(hours=12)
            config = {
                "certificati_autopilot_interval_days": 1,
                "certificati_autopilot_last_sent": last_sent.isoformat(),
            }
            automator.check_and_run(config)
            mock_run.assert_not_called()

    def test_check_and_run_expired(self, automator):
        with patch.object(automator, "run") as mock_run:
            last_sent = datetime.now() - timedelta(days=2)
            config = {
                "certificati_autopilot_interval_days": 1,
                "certificati_autopilot_last_sent": last_sent.isoformat(),
            }
            automator.check_and_run(config)
            mock_run.assert_called_once_with(config)

    def test_run_invalid_path(self, automator):
        config = {"certificati_campione_path": "C:/invalid/path.xlsx"}
        with patch("src.core.autopilot.cert_automation.Path.exists", return_value=False):
            automator.run(config)
            assert automator._cert_worker is None

    def test_run_success_start(self, automator):
        config = {"certificati_campione_path": "C:/valid/path.xlsx"}
        with patch("src.core.autopilot.cert_automation.Path.exists", return_value=True):
            # Patch explicitly where it's used inside the method (dynamic import)
            with patch("src.core.contabilita_worker.ContabilitaWorker") as mock_worker_class:
                automator.run(config)
                assert automator._cert_worker is not None
                mock_worker_class.assert_called_once()
                automator._cert_worker.start.assert_called_once()

    def test_on_worker_finished_critical_error(self, automator):
        automator._cert_worker = MagicMock()
        with patch("src.core.autopilot.cert_automation.NotificationManager") as mock_nm:
            automator._on_worker_finished(False, "Errore critico: DB locked", 0, 0, 1.0)
            mock_nm.instance().add_notification.assert_called_once()
            args = mock_nm.instance().add_notification.call_args[1]
            assert args["level"] == "error"

    def test_on_worker_finished_success(self, automator):
        automator._cert_worker = MagicMock()
        with patch("src.core.autopilot.cert_automation.NotificationManager") as mock_nm:
            with patch.object(automator, "_generate_outlook_draft") as mock_gen:
                with patch("src.core.autopilot.cert_automation.config_manager") as mock_cfg:
                    automator._on_worker_finished(True, "OK", 5, 0, 2.0)
                    mock_gen.assert_called_once()
                    mock_cfg.set_config_value.assert_called_once()
                    mock_nm.instance().add_notification.assert_called_once()
                    args = mock_nm.instance().add_notification.call_args[1]
                    assert args["level"] == "success"

    def test_on_worker_finished_exception(self, automator):
        automator._cert_worker = MagicMock()
        with patch("src.core.autopilot.cert_automation.NotificationManager") as mock_nm:
            with patch.object(automator, "_generate_outlook_draft", side_effect=Exception("Gen Error")):
                automator._on_worker_finished(True, "OK", 0, 0, 0.5)
                mock_nm.instance().add_notification.assert_called_once()
                args = mock_nm.instance().add_notification.call_args[1]
                assert args["level"] == "error"
                assert "Errore durante l'analisi" in args["message"]

    def test_generate_outlook_draft_ui_logic(self, automator, mock_mw):
        # Setup UI hierarchy
        mock_mw.navigation_controller = MagicMock()
        mock_panel = MagicMock()
        mock_mw.navigation_controller.get_panel.return_value = mock_panel

        automator._generate_outlook_draft()

        mock_panel.certificati_widget.refresh_data.assert_called_once()
        mock_panel.certificati_widget._run_analysis_and_send_email.assert_called_once()

    def test_generate_outlook_draft_fallback(self, automator, mock_mw):
        # No navigation_controller -> fallback
        del mock_mw.navigation_controller

        with patch("src.gui.workers.autopilot_cert_worker.AutopilotCertWorker") as mock_fallback_class:
            automator._generate_outlook_draft()

            assert automator._fallback_worker is not None
            mock_fallback_class.assert_called_once()
            automator._fallback_worker.start.assert_called_once()

            # Test already running
            automator._fallback_worker.isRunning.return_value = True
            automator._generate_outlook_draft()
            assert mock_fallback_class.call_count == 1  # Still 1
