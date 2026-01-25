from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from src.gui.panels.dashboard_panel import DashboardPanel
from src.gui.widgets.activity_feed import ActivityFeed
from src.gui.widgets.quick_actions import QuickActions


class TestDashboardComponents:
    """Tests for individual new dashboard components."""

    def test_quick_actions_signals(self, qapp, qtbot):
        """Verify QuickActions emits correct signals."""
        widget = QuickActions()
        qtbot.addWidget(widget)

        with qtbot.waitSignal(widget.action_clicked, timeout=1000) as blocker:
            # Helper to find a button by text
            tgt_btn = None
            layout = widget.chips_layout
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget() and "Scarico" in item.widget().text():
                    tgt_btn = item.widget()
                    break

            assert tgt_btn is not None
            qtbot.mouseClick(tgt_btn, Qt.MouseButton.LeftButton)

        assert blocker.args == ["nav_scarico_ts"]

    def test_activity_feed_refresh(self, qapp, mocker):
        """Verify ActivityFeed handles data from AuditManager."""
        # Mock AuditManager at its source
        mock_audit_class = mocker.patch("src.core.audit_manager.AuditManager")
        mock_instance = mock_audit_class.instance.return_value

        mock_instance.get_logs.return_value = [
            {
                "action": "Test Action",
                "entity": "Test Entity",
                "status": "success",
                "timestamp": "2023-01-01T12:00:00",
            },
            {
                "action": "Error Action",
                "entity": "-",
                "status": "error",
                "timestamp": "2023-01-01T12:05:00",
            },
        ]

        feed = ActivityFeed()
        feed.refresh_feed()

        all_labels_text = [lbl.text() for lbl in feed.findChildren(QLabel)]
        matching = [t for t in all_labels_text if "Test Action" in t]
        assert len(matching) > 0
        assert any("Test Entity" in t for t in matching)


class TestDashboardPanelFull:
    """Integration test for the full Dashboard Panel."""

    def test_dashboard_initialization(self, qapp, mocker):
        """Verify the dashboard assembles all parts correctly."""
        # Mock Stats
        mocker.patch(
            "src.core.stats_manager.StatsManager.get_all_stats", return_value={}
        )
        # Mock Audit
        mocker.patch("src.core.audit_manager.AuditManager.get_logs", return_value=[])

        panel = DashboardPanel()

        assert panel.activity_feed is not None
        assert panel.quick_actions is not None

        # Verify Greeting Exists
        found_greeting = False
        for lbl in panel.findChildren(QLabel):
            if "Dashboard Operativa" in lbl.text():
                found_greeting = True
                break
        assert found_greeting

    def test_dashboard_quick_action_integration(self, qapp, mocker, qtbot):
        """Verify Quick Action click triggers navigation on MainWindow."""
        # Mock Stats & Audit to avoid side effects
        mocker.patch(
            "src.core.stats_manager.StatsManager.get_all_stats", return_value={}
        )
        mocker.patch("src.core.audit_manager.AuditManager.get_logs", return_value=[])

        panel = DashboardPanel()

        # We simulate a "nav_page_2" (Lyra) click
        mw_mock = mocker.Mock()
        mocker.patch.object(panel, "window", return_value=mw_mock)

        # Trigger internal handler directly to verify logic
        panel._handle_quick_action("nav_page_2")

        # Verify it called the correct method on main_window
        mw_mock._navigate_to.assert_called_with(2)


class TestQuickActionsConfig:
    """Tests for the Quick Actions configuration dialog."""

    def test_dialog_load_save(self, qapp, mocker, qtbot):
        """Verify the dialog loads current config and saves new selection."""
        from PyQt6.QtWidgets import QTreeWidgetItemIterator

        from src.gui.dialogs.quick_actions_config import QuickActionsConfigDialog

        mocker.patch(
            "src.gui.dialogs.quick_actions_config.get_config_value",
            return_value=["nav_dettagli_oda"],
        )
        mock_set = mocker.patch("src.gui.dialogs.quick_actions_config.set_config_value")

        dlg = QuickActionsConfigDialog()
        qtbot.addWidget(dlg)

        def find_item(key_to_find):
            iterator = QTreeWidgetItemIterator(dlg.tree)
            while iterator.value():
                item = iterator.value()
                if item.data(0, Qt.ItemDataRole.UserRole) == key_to_find:
                    return item
                iterator += 1
            return None

        # Check initial state
        sync_item = find_item("nav_dettagli_oda")
        assert sync_item is not None
        assert sync_item.checkState(0) == Qt.CheckState.Checked

        # Simulate user selection
        lyra_item = find_item("nav_page_2")
        assert lyra_item is not None
        lyra_item.setCheckState(0, Qt.CheckState.Checked)

        # Accept dialog
        dlg.accept()

        # Verify save
        call_args = mock_set.call_args
        assert call_args[0][0] == "quick_actions"
        saved_list = call_args[0][1]
        assert "nav_dettagli_oda" in saved_list
        assert "nav_page_2" in saved_list
