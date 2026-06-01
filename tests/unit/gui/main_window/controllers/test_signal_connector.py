"""Unit tests for SignalConnector."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMainWindow

from src.core.notification_manager import NotificationManager
from src.gui.main_window.controllers.signal_connector import SignalConnector


class MockSidebar(QObject):
    navigation_requested = Signal(int, int)
    palette_requested = Signal()

    def __init__(self):
        super().__init__()
        self.group_notifiche = MagicMock()
        self.group_notifiche.header_btn = MagicMock()


class MockAutopilot(QObject):
    bot_sync_requested = Signal(str)


@pytest.fixture
def real_main_window(qtbot):
    mw = QMainWindow()
    mw.navigation_controller = MagicMock()
    mw.service_controller = MagicMock()
    mw.sidebar = MockSidebar()
    mw.menu_bar_component = MagicMock()
    mw.tray_icon_component = MagicMock()
    qtbot.addWidget(mw)
    return mw


class TestSignalConnector:
    """Test suite per SignalConnector."""

    def test_connect_global_signals(self, real_main_window, mocker):
        mock_toast = mocker.patch("src.gui.widgets.toast.ToastManager.instance")
        mgr = NotificationManager.instance()

        conn = SignalConnector(real_main_window)
        conn.connect_global_signals()

        # Test Toast connection
        mgr.request_toast.emit("Msg", "success", 1000)
        assert mock_toast.return_value.show.called

        # Test Tray connection
        assert real_main_window.tray_icon_component.show_message.called

    def test_connect_sidebar_signals(self, real_main_window):
        conn = SignalConnector(real_main_window)
        conn.connect_sidebar_signals()

        # Navigation
        real_main_window.sidebar.navigation_requested.emit(1, 2)
        real_main_window.navigation_controller.navigate_to.assert_called_with(1, 2)

        # Palette
        real_main_window.sidebar.palette_requested.emit()
        assert real_main_window.menu_bar_component.open_command_palette.called

    def test_connect_autopilot_signals(self, real_main_window):
        mock_dash = MagicMock()
        mock_dash.autopilot_widget = MockAutopilot()
        real_main_window.navigation_controller.get_panel.return_value = mock_dash

        conn = SignalConnector(real_main_window)
        conn.connect_autopilot_signals()

        # Sync request
        mock_dash.autopilot_widget.bot_sync_requested.emit("timbrature")
        real_main_window.service_controller.handle_manual_sync_request.assert_called_with("timbrature")

    def test_connect_all(self, real_main_window, mocker):
        conn = SignalConnector(real_main_window)
        mock_global = mocker.patch.object(conn, "connect_global_signals")
        mock_sidebar = mocker.patch.object(conn, "connect_sidebar_signals")
        mock_auto = mocker.patch.object(conn, "connect_autopilot_signals")

        conn.connect_all()

        assert mock_global.called
        assert mock_sidebar.called
        assert mock_auto.called
