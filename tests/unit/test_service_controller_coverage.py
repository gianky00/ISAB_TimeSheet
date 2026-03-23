from unittest.mock import MagicMock, patch

import pytest

from src.gui.controllers.service_controller import ServiceController


@pytest.mark.skip(
    reason="Crash nativo in ambiente headless Windows V9.0 durante coordinamento servizi background."
)
class TestServiceControllerCoverage:
    @pytest.fixture
    def mw(self):
        mock_mw = MagicMock()
        mock_mw.monitoring_controller = MagicMock()
        return mock_mw

    @pytest.fixture
    def controller(self, mw):  # noqa: ANN001
        mock_tg = MagicMock()
        mock_sentinel = MagicMock()
        return ServiceController(mw, mock_tg, mock_sentinel)

    @patch("src.gui.controllers.service_controller.QTimer.singleShot")
    @patch("src.core.notification_manager.NotificationManager.instance")
    def test_start_all(self, mock_nm_cls, mock_ss, controller, mw):  # noqa: ANN001
        mock_nm = mock_nm_cls.return_value
        controller.start_all()
        controller.sentinel.anomalies_found.connect.assert_called_with(
            mw.monitoring_controller.handle_anomalies_found
        )
        assert mock_ss.called
        assert controller.scheduler_timer is not None

    @patch("src.gui.controllers.service_controller.check_for_updates")
    def test_check_updates(self, mock_check, controller, mw):  # noqa: ANN001
        controller._check_updates()
        mock_check.assert_called_with(parent=mw, silent=True, callback=mw._show_update_banner)

    def test_forward_notification_to_telegram_sent(self, controller):  # noqa: ANN001
        notif = {"title": "Error", "level": "error", "message": "msg"}
        controller._forward_notification_to_telegram(notif)
        controller.telegram.send_message_sync.assert_called()

    @pytest.mark.skip(
        reason="Crash nativo in ambiente headless Windows V9.0 durante coordinamento servizi background."
    )
    @patch("src.gui.controllers.service_controller.datetime")
    def test_check_scheduled_tasks_autopilot_trigger(self, mock_dt, controller, mw):  # noqa: ANN001
        mock_dt.now.return_value.strftime.return_value = "09:00"
        mock_panel = MagicMock()
        mw.timbrature_bot_panel = mock_panel
        with (
            patch("src.core.config_manager.load_config") as mock_load,
            patch.object(controller, "_schedule_bot_with_parallelism") as mock_sched,
        ):
            mock_load.return_value = {
                "timbrature_autopilot_enabled": True,
                "timbrature_autopilot_time": "09:00",
            }
            controller._check_scheduled_tasks()
        mock_sched.assert_called_once()

    @patch("src.gui.controllers.service_controller.datetime")
    def test_check_scheduled_tasks_no_trigger(self, mock_dt, controller):  # noqa: ANN001
        """Verifica che lo scheduler non parta se l'orario non coincide."""
        mock_dt.now.return_value.strftime.return_value = "10:00"

        # Configurazione completa per evitare TypeError in V9.0
        test_config = {
            "timbrature_autopilot_enabled": True,
            "timbrature_autopilot_time": "09:00",
            "report_email_autopilot_enabled": False,
            "report_email_autopilot_interval_days": 7,
        }

        with patch("src.core.config_manager.load_config", return_value=test_config):
            controller._check_scheduled_tasks()

        assert controller.running_bots_by_site["portale_fornitori"] == []
