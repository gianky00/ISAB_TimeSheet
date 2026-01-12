
import json
import pytest
from unittest.mock import patch, MagicMock
from src.core import notification_manager, config_manager

# Resetta il singleton prima di ogni test se necessario
@pytest.fixture(autouse=True)
def reset_singleton():
    notification_manager.NotificationManager._instance = None
    yield
    notification_manager.NotificationManager._instance = None

class TestNotificationManagerCoverage:

    def test_singleton_instance(self, tmp_path):
        """Test singleton pattern."""
        with patch.object(config_manager, "CONFIG_DIR", tmp_path):
            instance1 = notification_manager.NotificationManager.instance()
            instance2 = notification_manager.NotificationManager.instance()
            assert instance1 is instance2

    def test_add_notification(self, tmp_path, qtbot):
        """Test adding a notification."""
        # Setup config dir
        with patch.object(config_manager, "CONFIG_DIR", tmp_path):
            mgr = notification_manager.NotificationManager.instance()
            
            # Watch signals
            with qtbot.waitSignal(mgr.notification_added, timeout=1000) as blocker:
                mgr.add_notification("Title", "Message", "success")
            
            assert blocker.args[0]["title"] == "Title"
            assert len(mgr.notifications) == 1
            assert mgr.get_unread_count() == 1
            
            # Verify file persistence
            assert (tmp_path / "notifications.json").exists()

    def test_load_notifications(self, tmp_path):
        """Test loading notifications from disk."""
        # Create fake file
        fake_data = [
            {"id": "1", "title": "Old", "timestamp": "2023-01-01T00:00:00", "read": True},
            {"id": "2", "title": "New", "timestamp": "2024-01-01T00:00:00", "read": False}
        ]
        file_path = tmp_path / "notifications.json"
        with open(file_path, "w") as f:
            json.dump(fake_data, f)

        with patch.object(config_manager, "CONFIG_DIR", tmp_path):
            mgr = notification_manager.NotificationManager.instance()
            # Should be sorted reverse timestamp (New first)
            assert len(mgr.notifications) == 2
            assert mgr.notifications[0]["id"] == "2"
            assert mgr.notifications[1]["id"] == "1"

    def test_mark_as_read(self, tmp_path):
        with patch.object(config_manager, "CONFIG_DIR", tmp_path):
            mgr = notification_manager.NotificationManager.instance()
            mgr.add_notification("T", "M")
            notif_id = mgr.notifications[0]["id"]
            
            assert mgr.get_unread_count() == 1
            mgr.mark_as_read(notif_id)
            assert mgr.get_unread_count() == 0
            assert mgr.notifications[0]["read"] is True

    def test_mark_all_as_read(self, tmp_path):
        with patch.object(config_manager, "CONFIG_DIR", tmp_path):
            mgr = notification_manager.NotificationManager.instance()
            mgr.add_notification("A", "M")
            mgr.add_notification("B", "M")
            
            assert mgr.get_unread_count() == 2
            mgr.mark_all_as_read()
            assert mgr.get_unread_count() == 0

    def test_delete_notification(self, tmp_path):
        with patch.object(config_manager, "CONFIG_DIR", tmp_path):
            mgr = notification_manager.NotificationManager.instance()
            mgr.add_notification("A", "M")
            notif_id = mgr.notifications[0]["id"]
            
            mgr.delete_notification(notif_id)
            assert len(mgr.notifications) == 0

    def test_clear_all(self, tmp_path):
        with patch.object(config_manager, "CONFIG_DIR", tmp_path):
            mgr = notification_manager.NotificationManager.instance()
            mgr.add_notification("A", "M")
            mgr.add_notification("B", "M")
            
            mgr.clear_all()
            assert len(mgr.notifications) == 0

    def test_get_notifications_filter(self, tmp_path):
        with patch.object(config_manager, "CONFIG_DIR", tmp_path):
            mgr = notification_manager.NotificationManager.instance()
            mgr.add_notification("Unread", "M")
            mgr.add_notification("Read", "M")
            mgr.mark_as_read(mgr.notifications[0]["id"]) # Mark 'Read' as read (it's at index 0 because add inserts at 0)
            
            # Wait, add_notification inserts at 0.
            # 1. Add "Unread". List: [Unread]
            # 2. Add "Read". List: [Read, Unread]
            # 3. Mark index 0 ("Read") as read.
            
            all_n = mgr.get_notifications(filter_unread=False)
            unread_n = mgr.get_notifications(filter_unread=True)
            
            assert len(all_n) == 2
            assert len(unread_n) == 1
            assert unread_n[0]["title"] == "Unread"
