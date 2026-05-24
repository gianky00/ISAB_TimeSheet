"""Unit tests for DashboardPanel."""

from unittest.mock import MagicMock

import pytest

from src.gui.panels.dashboard_panel import DashboardPanel


@pytest.fixture
def panel(qtbot, mocker):
    """Istanza di DashboardPanel con i widget interni mockati per isolamento."""
    mocker.patch("src.gui.widgets.activity_feed.ActivityFeed")
    mocker.patch("src.gui.widgets.autopilot.AutopilotWidget")
    mocker.patch("src.gui.widgets.dashboard.multi_window_status.MultiWindowStatusWidget")
    mocker.patch("src.gui.widgets.dashboard.pdl_stats_widget.PDLStatsWidget")
    mocker.patch("src.gui.widgets.dashboard.roi_widget.BotSavingsWidget")
    mocker.patch("src.gui.widgets.dashboard.weather_widget.WeatherWidget")
    mocker.patch("src.gui.widgets.quick_actions.QuickActions")

    p = DashboardPanel()
    qtbot.addWidget(p)
    return p


class TestDashboardPanel:
    """Test suite per DashboardPanel."""

    def test_initialization(self, panel):
        """Verifica lbl'inizializzazione della dashboard."""
        assert panel.main_container is not None
        assert panel.scroll_area is not None
        assert panel.multi_window_card is not None
        assert panel.weather_widget is not None
        assert panel.roi_widget is not None
        assert panel.card_pdl is not None
        assert panel.quick_actions is not None
        assert panel.autopilot_widget is not None
        assert panel.activity_feed is not None
        assert panel.timer.isActive()

    def test_refresh_data_delegation(self, panel):
        """Verifica che il refresh deleghi ai singoli widget."""
        panel.activity_feed.refresh_feed = MagicMock()
        panel.quick_actions.refresh_actions = MagicMock()
        panel.autopilot_widget.refresh_events = MagicMock()
        panel.roi_widget.refresh_stats = MagicMock()
        panel.card_pdl.refresh_stats = MagicMock()

        panel.refresh_data()

        assert panel.activity_feed.refresh_feed.called
        assert panel.quick_actions.refresh_actions.called
        assert panel.autopilot_widget.refresh_events.called
        assert panel.roi_widget.refresh_stats.called
        assert panel.card_pdl.refresh_stats.called

    def test_handle_pdl_area_click(self, panel, mocker):
        """Verifica la navigazione al click su un'area PDL."""
        mock_win = MagicMock()
        mock_nav = MagicMock()
        mock_win.navigation_controller = mock_nav
        mocker.patch.object(panel, "window", return_value=mock_win)

        panel._handle_pdl_area_click("Area 1")

        mock_nav.navigate_to_pdl.assert_called_with(site="ISAB Sud", area="Process Area 1")

    def test_handle_quick_action_navigation(self, panel, mocker):
        """Verifica la navigazione tramite azioni rapide."""
        mock_win = MagicMock()
        mock_nav = MagicMock()
        mock_win.navigation_controller = mock_nav
        mocker.patch.object(panel, "window", return_value=mock_win)

        # Test navigazione pannello
        panel._handle_quick_action("nav_scarico_ts")
        mock_nav.navigate_to_panel.assert_called_with("scarico_ts")

        # Test navigazione pagina fissa
        panel._handle_quick_action("nav_page_8")  # Guida
        mock_nav.navigate_to.assert_called_with(8)

    def test_handle_bot_sync_requested(self, panel, mocker):
        """Verifica lbl'avvio manuale di un bot dall'autopilot."""
        mock_win = MagicMock()
        mock_svc_ctrl = MagicMock()
        mock_win.service_controller = mock_svc_ctrl
        mocker.patch.object(panel, "window", return_value=mock_win)

        # Simuliamo presenza del pannello timbrature in MainWindow
        mock_panel = MagicMock()
        mock_win.timbrature_bot_panel = mock_panel

        panel._handle_bot_sync_requested("timbrature")

        assert mock_svc_ctrl._schedule_bot_with_parallelism.called
        args = mock_svc_ctrl._schedule_bot_with_parallelism.call_args[0]
        assert args[0] == "timbrature"
        assert args[1] == mock_panel
