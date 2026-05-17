from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from src.gui.widgets.activity_feed import ActivityFeed
from src.gui.widgets.quick_actions import QuickActions


class TestDashboardComponents:
    def test_quick_actions_signals(self, qapp, qtbot):
        widget = QuickActions()
        qtbot.addWidget(widget)
        with qtbot.waitSignal(widget.action_clicked, timeout=1000) as blocker:
            tgt_btn = None
            layout = widget.chips_layout
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget() and "Scarico" in item.widget().text():
                    tgt_btn = item.widget()
                    break
            assert tgt_btn is not None
            qtbot.mouseClick(tgt_btn, Qt.MouseButton.LeftButton)
        assert blocker.args is not None

    def test_activity_feed_refresh(self, qapp, mocker):
        # Patch corretta della fonte del singleton
        mock_audit = mocker.patch("src.core.audit_manager.AuditManager.instance")
        mock_audit.return_value.get_logs.return_value = [
            {"action": "A", "entity": "E", "status": "success", "timestamp": "2023-01-01"}
        ]
        feed = ActivityFeed()
        feed.refresh_feed()
        all_text = [lbl.text() for lbl in feed.findChildren(QLabel)]
        assert any("A" in t for t in all_text)
