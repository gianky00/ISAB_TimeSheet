from unittest.mock import MagicMock, patch

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from src.gui.widgets.activity_feed import ActivityFeed, ActivityItem


def test_activity_item_init(qtbot):
    log_entry = {
        "status": "success",
        "message": "Test message",
        "timestamp": "2024-05-24 10:00:00",
        "type": "audit",
    }

    # Use real widget but avoid complex side effects if possible
    # get_colored_icon returns a QIcon, which HAS a .pixmap() method
    with (
        patch("src.gui.widgets.activity_feed.get_colored_icon", return_value=QIcon()),
        patch("src.gui.widgets.activity_feed.get_asset_path", return_value="dummy.svg"),
    ):
        item = ActivityItem(log_entry, animate=False)
        qtbot.addWidget(item)

        assert item.log_entry == log_entry
        assert item.width() == 300


def test_activity_feed_init(qtbot):
    # Avoid real signals from AuditManager
    with patch("src.application.services.audit_manager.AuditManager"):
        feed = ActivityFeed()
        qtbot.addWidget(feed)
        feed.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
        feed.show()

        assert feed.feed_layout is not None
        assert feed.scroll_area is not None


def test_activity_feed_refresh(qtbot):
    # Avoid real signals from AuditManager
    with patch("src.application.services.audit_manager.AuditManager") as mock_audit_cls:
        mock_audit = MagicMock()
        mock_audit.get_logs.return_value = [
            {"status": "success", "message": "Log 1"},
            {"status": "error", "message": "Log 2"},
        ]
        mock_audit_cls.instance.return_value = mock_audit

        feed = ActivityFeed()
        qtbot.addWidget(feed)

        # Patch dependencies inside refresh_feed
        with (
            patch("src.gui.widgets.activity_feed.get_colored_icon", return_value=QIcon()),
            patch("src.gui.widgets.activity_feed.get_asset_path", return_value="dummy.svg"),
        ):
            feed.refresh_feed()

            assert mock_audit.get_logs.called
            # Verify we have items in the layout (count > 1 because of stretch)
            assert feed.feed_layout.count() > 1
