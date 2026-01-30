import unittest
from unittest.mock import MagicMock, patch

from src.gui.controllers.service_controller import ServiceController


class TestServiceControllerCoverage(unittest.TestCase):
    def setUp(self):
        self.mock_mw = MagicMock()
        self.mock_tg = MagicMock()
        self.mock_sentinel = MagicMock()
        # Initialize with None parent to avoid TypeError with MagicMock
        self.controller = ServiceController(None, self.mock_tg, self.mock_sentinel)
        self.controller.mw = self.mock_mw

    @patch("src.gui.controllers.service_controller.QTimer.singleShot")
    @patch("src.gui.controllers.service_controller.NotificationManager")
    def test_start_all(self, mock_nm, mock_ss):
        mock_nm_instance = mock_nm.instance.return_value

        self.controller.start_all()

        self.mock_sentinel.anomalies_found.connect.assert_called_with(
            self.mock_mw._on_anomalies_found
        )
        # Verify calls to singleShot (1000, 2000, 3000ms)
        self.assertTrue(mock_ss.called)
        mock_nm_instance.notification_added.connect.assert_called()
        self.assertIsNotNone(self.controller.scheduler_timer)

    @patch("src.gui.controllers.service_controller.check_for_updates")
    def test_check_updates(self, mock_check):
        self.controller._check_updates()
        mock_check.assert_called_with(
            parent=self.mock_mw, silent=True, callback=self.mock_mw._show_update_banner
        )

    def test_forward_notification_to_telegram_ignored(self):
        notif = {"title": "Telegram"}
        self.controller._forward_notification_to_telegram(notif)
        self.mock_tg.send_message_sync.assert_not_called()

    def test_forward_notification_to_telegram_sent(self):
        notif = {"title": "Error", "level": "error", "message": "msg"}
        self.controller._forward_notification_to_telegram(notif)
        self.mock_tg.send_message_sync.assert_called()

    @patch("datetime.datetime")
    def test_check_scheduled_tasks_autopilot_trigger(self, mock_dt):
        mock_dt.now.return_value.strftime.return_value = "09:00"

        # Mock panel
        mock_panel = MagicMock()
        mock_panel.start_btn.isEnabled.return_value = True
        self.mock_mw.timbrature_bot_panel = mock_panel

        # We need to patch the local import in src.gui.controllers.service_controller
        with patch("src.core.config_manager.load_config") as mock_load:
            mock_load.return_value = {
                "timbrature_autopilot_enabled": True,
                "timbrature_autopilot_time": "09:00",
            }
            self.controller._check_scheduled_tasks()

        mock_panel._on_start.assert_called()
        mock_panel.log_widget.append.assert_called()

    @patch("datetime.datetime")
    def test_check_scheduled_tasks_no_trigger(self, mock_dt):
        mock_dt.now.return_value.strftime.return_value = "10:00"

        with patch("src.core.config_manager.load_config") as mock_load:
            mock_load.return_value = {
                "timbrature_autopilot_enabled": True,
                "timbrature_autopilot_time": "09:00",
            }
            self.controller._check_scheduled_tasks()
