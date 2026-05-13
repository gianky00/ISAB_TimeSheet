"""
SyncroJob - Test Service Controller (Final Corrected)
Verifica l'integrità del ServiceController con i giusti path di mock.
"""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QObject

from src.gui.controllers.service_controller import ServiceController


class MockMainWindow(QObject):
    def __init__(self):
        super().__init__()
        self.monitoring_controller = MagicMock()
        self.timbrature_bot_panel = MagicMock()

class TestServiceControllerRobust:
    @pytest.fixture
    def mw(self, qtbot):
        return MockMainWindow()

    @pytest.fixture
    def controller(self, mw):
        mock_tg = MagicMock()
        return ServiceController(mw, mock_tg)

    @patch("src.gui.controllers.service_controller.QTimer.singleShot")
    def test_start_all(self, mock_ss, controller, mw):
        controller.start_all()
        assert mock_ss.called
        assert controller.scheduler_timer is not None

    def test_schedule_delegation(self, controller):
        """Verifica che lo scheduling sia delegato al queue_manager."""
        mock_panel = MagicMock()
        mock_panel.start_btn.isEnabled.return_value = True

        with patch.object(controller.queue_manager, "schedule_bot") as mock_sched:
            controller.queue_manager.schedule_bot("bot1", mock_panel, "portale_fornitori", "msg")
            assert mock_sched.called

    @patch("src.core.config_manager.load_config")
    def test_check_scheduled_tasks_timbrature(self, mock_load, controller, mw):
        # Usiamo datetime reale per il ritorno di now()
        fixed_now = datetime(2026, 5, 12, 9, 0, 0)

        with patch("src.gui.controllers.service_controller.datetime") as mock_dt:
            mock_dt.now.return_value = fixed_now

            mock_load.return_value = {"timbrature_autopilot_enabled": True, "timbrature_autopilot_time": "09:00"}
            mw.timbrature_bot_panel.start_btn.isEnabled.return_value = True

            controller._check_scheduled_tasks()
            assert "timbrature" in controller.queue_manager.running_bots_by_site["portale_fornitori"]

    def test_check_report_email_schedule_delegation(self, controller):
        # Usiamo una stringa ISO con fuso orario (aware) per evitare TypeError nella sottrazione
        # e assicuriamoci che l'intervallo sia superato (es. 2020)
        config = {
            "report_email_autopilot_enabled": True,
            "report_email_autopilot_time": "08:00",
            "report_email_autopilot_interval_days": 1,
            "report_email_autopilot_last_sent": "2020-01-01T00:00:00+00:00",
        }

        with patch("src.gui.controllers.service_controller.ReportService.send_scheduled_report_email") as mock_send:
            controller._check_report_email_schedule(config, "08:00")
            assert mock_send.called

    def test_prepare_scarico_oda(self, controller):
        """Verifica la pulizia del pannello OdA."""
        mock_panel = MagicMock()
        controller._prepare_scarico_oda_generale(mock_panel)

        mock_panel.data_table.set_data.assert_called_with([])
        assert "pulita" in mock_panel.log_widget.append.call_args[0][0]
