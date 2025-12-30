import pytest
import os
from unittest.mock import MagicMock, patch
from src.core.notification_manager import NotificationManager

@pytest.fixture
def notification_manager(tmp_path):
    # Reset singleton
    NotificationManager._instance = None
    
    # Mock config_manager to return a temp path
    with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
        manager = NotificationManager.instance()
        yield manager
        # Clean up
        manager.clear_all()
        NotificationManager._instance = None

def test_singleton(notification_manager):
    m2 = NotificationManager.instance()
    assert notification_manager is m2

def test_add_notification(notification_manager):
    notification_manager.add_notification("Test Title", "Test Message", "info")
    notifications = notification_manager.get_notifications()
    assert len(notifications) == 1
    assert notifications[0]["title"] == "Test Title"
    assert notifications[0]["message"] == "Test Message"
    assert notifications[0]["level"] == "info"
    assert notifications[0]["read"] is False

def test_mark_as_read(notification_manager):
    notification_manager.add_notification("Test", "Msg")
    notifications = notification_manager.get_notifications()
    n_id = notifications[0]["id"]
    
    assert notification_manager.get_unread_count() == 1
    
    notification_manager.mark_as_read(n_id)
    
    assert notification_manager.get_unread_count() == 0
    notifications = notification_manager.get_notifications()
    assert notifications[0]["read"] is True

def test_mark_all_as_read(notification_manager):
    notification_manager.add_notification("1", "1")
    notification_manager.add_notification("2", "2")
    
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
    with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
        new_manager = NotificationManager.instance()
        assert len(new_manager.get_notifications()) == 1
        assert new_manager.get_notifications()[0]["title"] == "Persistent"