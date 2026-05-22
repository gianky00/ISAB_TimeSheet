"""Tests for NotificationManager."""

from unittest.mock import patch

import pytest

from src.core.notification_manager import NotificationManager


@pytest.fixture
def notification_manager(tmp_path):
    """Fixture per il NotificationManager con file temporaneo."""
    # Reset singleton
    NotificationManager._instance = None
    # Patch CONFIG_DIR direttamente nel modulo dove viene usato per caricare/salvare
    with patch("src.core.notification_manager.CONFIG_DIR", tmp_path):
        manager = NotificationManager.instance()
        yield manager
    # Cleanup
    NotificationManager._instance = None


def test_add_notification(notification_manager):
    notification_manager.add_notification("Test Title", "Test Message", level="info")
    notifications = notification_manager.get_notifications()
    assert len(notifications) == 1
    assert notifications[0]["title"] == "Test Title"
    assert notifications[0]["message"] == "Test Message"
    assert notifications[0]["level"] == "info"
    assert notifications[0]["read"] is False


def test_mark_as_read(notification_manager):
    notification_manager.add_notification("Test", "Msg", level="error")
    notifications = notification_manager.get_notifications()
    n_id = notifications[0]["id"]

    assert notification_manager.get_unread_count() == 1

    notification_manager.mark_as_read(n_id)

    assert notification_manager.get_unread_count() == 0
    notifications = notification_manager.get_notifications()
    assert notifications[0]["read"] is True


def test_mark_all_as_read(notification_manager):
    notification_manager.add_notification("1", "1", level="error")
    notification_manager.add_notification("2", "2", level="error")

    assert notification_manager.get_unread_count() == 2

    notification_manager.mark_all_as_read()

    assert notification_manager.get_unread_count() == 0


def test_delete_notification(notification_manager):
    notification_manager.add_notification("1", "1")
    notifications = notification_manager.get_notifications()
    n_id = notifications[0]["id"]

    notification_manager.delete_notification(n_id)

    assert len(notification_manager.get_notifications()) == 0


def test_persistence(notification_manager, tmp_path):
    notification_manager.add_notification("Persistent", "Data")

    # Simulate app restart
    NotificationManager._instance = None
    with patch("src.core.notification_manager.CONFIG_DIR", tmp_path):
        new_manager = NotificationManager.instance()
        assert len(new_manager.get_notifications()) == 1
        assert new_manager.get_notifications()[0]["title"] == "Persistent"
