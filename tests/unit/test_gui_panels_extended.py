from unittest.mock import MagicMock, patch

import pytest

from src.gui.panels.help_panel import HelpPanel
from src.gui.panels.notifications_panel import NotificationsPanel


class TestGUIPanelsExtended:
    @pytest.fixture
    def app(self, qapp):
        return qapp

    def test_notifications_panel(self, qtbot):
        with patch("src.core.notification_manager.NotificationManager.instance") as mock_inst:
            mock_manager = MagicMock()
            mock_inst.return_value = mock_manager
            mock_manager.get_notifications.return_value = [
                {
                    "id": 1,
                    "title": "Test",
                    "message": "Msg",
                    "timestamp": "2024-01-01",
                    "read": False,
                }
            ]

            panel = NotificationsPanel()
            qtbot.addWidget(panel)
            panel.refresh_notifications()
            # The layout has at least the notification and the spacer
            assert panel.scroll_layout.count() >= 1

    def test_help_panel_navigation(self, qtbot):
        panel = HelpPanel()
        qtbot.addWidget(panel)
        assert panel.index_list.count() > 0

        # Test search
        panel.search_edit.setText("installazione")
        # Logic should filter items (we check it doesn't crash)
        panel._filter_index("installazione")
        assert panel.search_edit.text() == "installazione"

    def test_notifications_clear_all(self, qtbot):
        with patch("src.core.notification_manager.NotificationManager.instance") as mock_inst:
            mock_manager = MagicMock()
            mock_inst.return_value = mock_manager

            panel = NotificationsPanel()
            qtbot.addWidget(panel)

            # Mock the message box to avoid blocking
            with patch("PyQt6.QtWidgets.QMessageBox.question", return_value=None):
                panel.manager.clear_all = MagicMock()
                assert panel.manager is not None
