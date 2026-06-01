from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QObject

from src.gui.main_window.controllers.signal_connector import SignalConnector


class TestSignalConnector:
    @pytest.fixture
    def mw(self, qtbot):
        # Usiamo un QObject reale come base per il mock
        # così può essere passato a super().__init__(parent)
        mw = MagicMock(spec=QObject)
        # Ma MagicMock(spec=QObject) potrebbe non bastare se super() controlla il tipo C++
        # Usiamo un vero QObject e aggiungiamo i mock
        real_mw = QObject()
        real_mw.navigation_controller = MagicMock()
        real_mw.service_controller = MagicMock()
        real_mw.sidebar = MagicMock()
        real_mw.tray_icon_component = MagicMock()
        real_mw.menu_bar_component = MagicMock()
        return real_mw

    def test_init(self, mw):
        connector = SignalConnector(mw)
        assert connector.main_window == mw

    @patch("src.core.notification_manager.NotificationManager.instance")
    def test_connect_global_signals(self, mock_notif, mw):
        mock_instance = MagicMock()
        mock_notif.return_value = mock_instance

        connector = SignalConnector(mw)
        connector.connect_global_signals()

        assert mock_instance.request_toast.connect.called
        assert mock_instance.unread_count_changed.connect.called

    def test_connect_sidebar_signals(self, mw):
        connector = SignalConnector(mw)
        connector.connect_sidebar_signals()

        assert mw.sidebar.navigation_requested.connect.called
        assert mw.sidebar.palette_requested.connect.called

    def test_connect_autopilot_signals(self, mw):
        mock_dash = MagicMock()
        mw.navigation_controller.get_panel.return_value = mock_dash

        connector = SignalConnector(mw)
        connector.connect_autopilot_signals()

        assert mock_dash.autopilot_widget.bot_sync_requested.connect.called
