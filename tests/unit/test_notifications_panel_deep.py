from unittest.mock import patch

from PyQt6.QtWidgets import QMessageBox

from src.gui.panels.notifications_panel import AuditLogWidget, NotificationsPanel


class TestNotificationsPanelDeep:
    def test_refresh_notifications_with_data(self, qapp, qtbot):
        with patch(
            "src.core.notification_manager.NotificationManager.instance"
        ) as mock_manager:
            mock_inst = mock_manager.return_value
            mock_inst.get_notifications.return_value = [
                {
                    "id": 1,
                    "title": "T1",
                    "message": "M1",
                    "level": "info",
                    "read": False,
                }
            ]

            panel = NotificationsPanel()
            qtbot.addWidget(panel)

            panel.refresh_notifications()
            # Check if scroll layout has items (one data item + one stretch)
            # In refactored version it uses groups, so it should have at least 1 group header + 1 container + 1 stretch
            assert panel.scroll_layout.count() >= 2

    def test_set_filter(self, qapp, qtbot):
        panel = NotificationsPanel()
        qtbot.addWidget(panel)

        # Test Unread via Toolbar
        panel.toolbar._on_filter_clicked("unread")
        assert panel.current_filter == "unread"
        assert panel.toolbar._filter_chips["unread"].isChecked() is True

        # Test All
        panel.toolbar._on_filter_clicked("all")
        assert panel.current_filter == "all"
        assert panel.toolbar._filter_chips["all"].isChecked() is True

        # Test Errors
        panel.toolbar._on_filter_clicked("error")
        assert panel.current_filter == "error"
        assert panel.toolbar._filter_chips["error"].isChecked() is True

    def test_filter_errors_logic(self, qapp, qtbot):
        with patch(
            "src.core.notification_manager.NotificationManager.instance"
        ) as mock_manager:
            mock_inst = mock_manager.return_value
            # Mock get_notifications to return a mix of info and error
            # Note: The panel calls get_notifications(filter_unread=False) by default
            mock_inst.get_notifications.return_value = [
                {
                    "id": 1,
                    "title": "InfoMsg",
                    "message": "M1",
                    "level": "info",
                    "read": False,
                },
                {
                    "id": 2,
                    "title": "ErrorMsg",
                    "message": "E1",
                    "level": "error",
                    "read": False,
                },
            ]

            panel = NotificationsPanel()
            qtbot.addWidget(panel)

            # Switch to 'error' filter
            panel.toolbar._on_filter_clicked("error")

            # Check widgets in scroll layout
            # The refactored panel uses grouping. We look into the container of the group.
            # But refresh_notifications is async/debounced via timer in real app.
            # Here we might need to force refresh or wait.
            panel.refresh_notifications()

            found_error = False
            for group_key in panel._group_widgets:
                container = panel._group_widgets[group_key]["container"]
                layout = container.layout()
                for i in range(layout.count()):
                    w = layout.itemAt(i).widget()
                    if w and hasattr(w, "data") and w.data.get("level") == "error":
                        found_error = True

            assert found_error is True

    def test_clear_notifications_confirm(self, qapp, qtbot):
        with patch(
            "src.core.notification_manager.NotificationManager.instance"
        ) as mock_manager:
            mock_inst = mock_manager.return_value
            panel = NotificationsPanel()
            qtbot.addWidget(panel)

            with patch(
                "PyQt6.QtWidgets.QMessageBox.question",
                return_value=QMessageBox.StandardButton.Yes,
            ):
                panel._clear_notifications()
                assert mock_inst.clear_all.called

    def test_audit_log_widget_refresh(self, qapp, qtbot):
        with patch(
            "src.gui.panels.notifications_panel.AuditManager.instance"
        ) as mock_audit:
            mock_inst = mock_audit.return_value
            mock_inst.verify_integrity.return_value = True
            # Mock get_filtered_logs used by widget
            mock_inst.get_filtered_logs.return_value = (
                [
                    {
                        "timestamp": "2024-01-01T12:00:00",
                        "user_id": "U1",
                        "action": "A1",
                        "status": "success",
                    }
                ],
                1,
            )

            widget = AuditLogWidget()
            qtbot.addWidget(widget)
            widget.refresh()

            assert widget.model.rowCount() == 1
            assert "Integro" in widget.integrity_lbl.text()
