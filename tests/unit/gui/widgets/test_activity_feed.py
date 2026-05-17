import pytest
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QApplication, QLabel

from src.core.audit_manager import AuditManager
from src.gui.styles import COLORS
from src.gui.widgets.activity_feed import ActivityFeed, ActivityItem


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_activity_item_initialization_success(qapp):
    log = {
        "status": "success",
        "action": "Test Action",
        "entity": "Test Entity",
        "timestamp": "2026-01-01T12:00:00",
    }
    item = ActivityItem(log_entry=log)
    assert item.border_color == COLORS["success_dark"]
    assert "Test Action - Test Entity" in item.toolTip()

    # Check animation
    assert item.fade_in_animation is not None


def test_activity_item_initialization_error(qapp):
    log = {"status": "error", "action": "Test Error", "timestamp": "invalid_date"}
    item = ActivityItem(log_entry=log, animate=False)
    assert item.border_color == COLORS["error_red"]
    assert item.fade_in_animation is None


def test_activity_item_initialization_warning(qapp):
    log = {"status": "warning"}
    item = ActivityItem(log_entry=log, animate=False)
    assert item.border_color == COLORS["warning_yellow"]


def test_activity_item_show_event(qapp):
    log = {"status": "success"}
    item = ActivityItem(log_entry=log)
    show_event = QShowEvent()
    item.showEvent(show_event)
    assert item.fade_in_animation.state() == item.fade_in_animation.State.Running


def test_activity_item_remove_opacity(qapp):
    log = {"status": "success"}
    item = ActivityItem(log_entry=log)
    item._remove_opacity_effect()
    assert item.graphicsEffect() is None


def test_activity_feed_initialization(qapp, monkeypatch):
    feed = ActivityFeed()
    assert feed.scroll_area is not None
    assert feed.feed_layout.count() == 1  # Stretch


def test_activity_feed_refresh_empty(qapp, monkeypatch):
    monkeypatch.setattr(AuditManager.instance(), "get_logs", lambda limit: [])
    feed = ActivityFeed()
    feed.refresh_feed()
    assert feed.feed_layout.count() == 2  # Stretch + empty label
    assert isinstance(feed.feed_layout.itemAt(0).widget(), QLabel)


def test_activity_feed_refresh_with_logs(qapp, monkeypatch):
    logs = [
        {"status": "success", "action": "Login", "timestamp": "2026-01-01T12:00:00"},
        {"status": "error", "action": "Crash", "timestamp": "2026-01-01T12:01:00"},
    ]
    monkeypatch.setattr(AuditManager.instance(), "get_logs", lambda limit: logs)

    feed = ActivityFeed()
    feed.refresh_feed()

    assert feed.feed_layout.count() == 3  # 2 items + stretch
    assert isinstance(feed.feed_layout.itemAt(0).widget(), ActivityItem)
    assert isinstance(feed.feed_layout.itemAt(1).widget(), ActivityItem)

    # Test refresh again to check cleanup
    feed.refresh_feed()
    assert feed.feed_layout.count() == 3


def test_activity_feed_on_new_log(qapp, monkeypatch):
    feed = ActivityFeed()
    import unittest.mock

    with unittest.mock.patch.object(feed, "refresh_feed") as mock_refresh:
        feed._on_new_log_added({})
        mock_refresh.assert_called_once()
