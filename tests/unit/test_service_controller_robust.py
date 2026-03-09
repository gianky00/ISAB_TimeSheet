import pytest
from unittest.mock import MagicMock, patch
from src.gui.controllers.service_controller import ServiceController

@pytest.mark.skip(reason="Crash nativo in ambiente headless Windows V9.0 durante coordinamento servizi background.")
class TestServiceControllerRobust:
    @pytest.fixture
    def mw(self):
        mock_mw = MagicMock()
        mock_mw.monitoring_controller = MagicMock()
        return mock_mw

    @pytest.fixture
    def controller(self, mw):
        mock_tg = MagicMock()
        mock_sentinel = MagicMock()
        return ServiceController(mw, mock_tg, mock_sentinel)

    @patch("src.gui.controllers.service_controller.QTimer.singleShot")
    def test_start_all(self, mock_ss, controller, mw):
        controller.start_all()
        assert mock_ss.called
        assert controller.scheduler_timer is not None

    def test_schedule_parallelism_free_site(self, controller):
        """Verifica avvio immediato se il sito è libero."""
        mock_panel = MagicMock()
        mock_panel.start_btn.isEnabled.return_value = True
        controller._schedule_bot_with_parallelism("bot1", mock_panel, "portale_fornitori", "msg")
        
        assert "bot1" in controller.running_bots_by_site["portale_fornitori"]
        assert mock_panel._on_start.called

    def test_schedule_parallelism_busy_site(self, controller):
        """Verifica accodamento se il sito è occupato."""
        controller.running_bots_by_site["portale_fornitori"] = ["other_bot"]
        mock_panel = MagicMock()
        
        controller._schedule_bot_with_parallelism("bot1", mock_panel, "portale_fornitori", "msg")
        
        assert "bot1" not in controller.running_bots_by_site["portale_fornitori"]
        assert len(controller.pending_bots_by_site["portale_fornitori"]) == 1

    def test_on_bot_completed_triggers_next(self, controller):
        """Verifica che il completamento di un bot avvii il successivo in coda."""
        controller.running_bots_by_site["portale_fornitori"] = ["bot1"]
        next_panel = MagicMock()
        next_panel.start_btn.isEnabled.return_value = True
        controller.pending_bots_by_site["portale_fornitori"] = [("bot2", next_panel, "msg2")]

        controller._on_bot_completed("bot1", "portale_fornitori", MagicMock())

        assert "bot1" not in controller.running_bots_by_site["portale_fornitori"]
        assert "bot2" in controller.running_bots_by_site["portale_fornitori"]
        assert next_panel._on_start.called

    @patch("src.gui.controllers.service_controller.datetime")
    @patch("src.core.config_manager.load_config")
    def test_check_scheduled_tasks_timbrature(self, mock_load, mock_dt, controller, mw):
        mock_dt.now.return_value.strftime.return_value = "09:00"
        mock_load.return_value = {"timbrature_autopilot_enabled": True, "timbrature_autopilot_time": "09:00"}
        
        mock_panel = MagicMock()
        mock_panel.start_btn.isEnabled.return_value = True
        mw.timbrature_bot_panel = mock_panel

        controller._check_scheduled_tasks()
        assert "timbrature" in controller.running_bots_by_site["portale_fornitori"]

    @patch("src.gui.controllers.service_controller.datetime")
    def test_check_report_email_schedule_interval(self, mock_dt, controller):
        mock_dt.now.return_value.strftime.return_value = "08:00"
        config = {
            "report_email_autopilot_enabled": True,
            "report_email_autopilot_time": "08:00",
            "report_email_autopilot_interval_days": 1,
            "report_email_autopilot_last_sent": "2020-01-01T00:00:00"
        }
        
        with patch.object(controller, "_send_scheduled_report_email") as mock_send:
            controller._check_report_email_schedule(config, "08:00")
            assert mock_send.called

    def test_prepare_scarico_oda(self, controller):
        """Verifica la pulizia del pannello OdA (V9.0 naming)."""
        mock_panel = MagicMock()
        # In V9.0 il metodo è _prepare_scarico_oda_generale
        controller._prepare_scarico_oda_generale(mock_panel)
        
        mock_panel.data_table.set_data.assert_called_with([])
        assert "pulita" in mock_panel.log_widget.append.call_args[0][0]
