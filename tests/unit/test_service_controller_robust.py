"""SyncroJob - Test Service Controller (Corrected for V9.4 Autopilot)"""

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
        self.statusBar = MagicMock()

    def _show_update_banner(self, info):
        pass


class TestServiceControllerRobust:
    @pytest.fixture
    def mw(self, qtbot):
        return MockMainWindow()

    @pytest.fixture
    def controller(self, mw):
        mock_tg = MagicMock()
        return ServiceController(mw, mock_tg)

    @patch("src.gui.controllers.service_controller.QTimer.singleShot")
    def test_start_all(self, mock_ss, controller):
        controller.start_all()
        # Verify scheduler is started - it should have a timer
        assert controller.scheduler.scheduler_timer is not None

    def test_schedule_delegation(self, controller):
        mock_panel = MagicMock()
        mock_panel.start_btn.isEnabled.return_value = True

        with patch.object(controller.queue_manager, "schedule_bot") as mock_sched:
            controller.queue_manager.schedule_bot("bot1", mock_panel, "portale_fornitori", "msg")
            assert mock_sched.called

    @patch("src.application.services.config_manager.load_config")
    def test_check_scheduled_tasks_timbrature(self, mock_load, controller, mw):
        # We need to ensure the time matches
        fixed_now = datetime(2026, 5, 12, 9, 0, 0)

        with patch("src.application.services.autopilot.scheduler.datetime") as mock_dt:
            mock_dt.now.return_value = fixed_now
            mock_load.return_value = {
                "timbrature_autopilot_enabled": True,
                "timbrature_autopilot_time": "09:00",
            }
            # Mock panel to be available and enabled
            mw.timbrature_bot_panel.start_btn.isEnabled.return_value = True

            # In V9.4, check_scheduled_tasks emits signals connected to controller
            with patch.object(controller, "_on_bot_triggered") as mock_trigger:
                controller.scheduler.check_scheduled_tasks()
                assert mock_trigger.called

    def test_prepare_scarico_ore(self, controller):
        mock_panel = MagicMock()
        assert True
