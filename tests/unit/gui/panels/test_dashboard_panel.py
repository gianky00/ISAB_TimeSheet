from unittest.mock import MagicMock, patch

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget

from src.gui.panels.dashboard_panel import DashboardPanel


class MockSubWidget(QWidget):
    """Real QWidget to avoid addWidget failures."""

    area_selected = Signal(str)  # For PDLStatsWidget
    action_clicked = Signal(str)  # For QuickActions
    bot_sync_requested = Signal(str)  # For AutopilotWidget

    def __init__(self, *args, **kwargs):
        super().__init__()

    def refresh_stats(self):
        pass

    def refresh_weather(self):
        pass

    def refresh_events(self):
        pass

    def refresh_feed(self):
        pass

    def refresh_actions(self):
        pass


def test_dashboard_panel_init(qtbot):
    with (
        patch("src.gui.panels.dashboard_panel.WeatherWidget", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.BotSavingsWidget", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.PDLStatsWidget", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.AutopilotWidget", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.ActivityFeed", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.MultiWindowStatusWidget", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.QuickActions", return_value=MockSubWidget()),
    ):
        panel = DashboardPanel()
        qtbot.addWidget(panel)
        panel.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
        panel.show()

        assert panel.main_container is not None
        assert panel.scroll_area is not None
        assert panel.timer.isActive()


def test_dashboard_panel_refresh(qtbot):
    with (
        patch("src.gui.panels.dashboard_panel.WeatherWidget", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.BotSavingsWidget", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.PDLStatsWidget", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.AutopilotWidget", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.ActivityFeed", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.MultiWindowStatusWidget", return_value=MockSubWidget()),
        patch("src.gui.panels.dashboard_panel.QuickActions", return_value=MockSubWidget()),
    ):
        panel = DashboardPanel()
        qtbot.addWidget(panel)

        # Mock sub-widgets methods
        panel.roi_widget.refresh_stats = MagicMock()
        panel.card_pdl.refresh_stats = MagicMock()
        # weather doesn't seem to be in refresh_live_data in the code I read last?
        # Actually it is NOT in refresh_live_data in the version I saw.
        panel.autopilot_widget.refresh_events = MagicMock()
        panel.activity_feed.refresh_feed = MagicMock()
        panel.quick_actions.refresh_actions = MagicMock()

        panel.refresh_live_data()

        panel.roi_widget.refresh_stats.assert_called_once()
        panel.card_pdl.refresh_stats.assert_called_once()
        panel.autopilot_widget.refresh_events.assert_called_once()
        panel.activity_feed.refresh_feed.assert_called_once()
        panel.quick_actions.refresh_actions.assert_called_once()
