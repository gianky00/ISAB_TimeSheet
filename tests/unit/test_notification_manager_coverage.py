from unittest.mock import MagicMock

import pytest

from src.application.services.notification_manager import NotificationManager


class TestNotificationManager:
    @pytest.fixture(autouse=True)
    def reset_singleton(self, mocker, tmp_path):
        """Reset automatico dell'istanza per ogni test."""
        mocker.patch("src.application.services.notification_manager.CONFIG_DIR", tmp_path)
        NotificationManager._reset_instance_for_testing()
        yield

    @pytest.fixture
    def manager(self):
        return NotificationManager.instance()

    def test_singleton(self, manager):
        assert NotificationManager.instance() is manager

    def test_add_notification(self, manager):
        # Mock signals explicitly
        manager.notification_added = MagicMock()
        manager.notifications_updated = MagicMock()
        manager.unread_count_changed = MagicMock()

        manager.add_notification("Title", "Message", "error")

        assert len(manager.notifications) == 1
        assert manager.notifications[0]["title"] == "Title"
        assert manager.notifications[0]["level"] == "error"
        assert manager.notifications[0]["read"] is False

        manager.notification_added.emit.assert_called_once()
        args = manager.notification_added.emit.call_args[0][0]
        assert args["title"] == "Title"

    def test_get_unread_count(self, manager):
        manager.add_notification("T1", "M1", "info")
        manager.add_notification("T2", "M2", "error")  # Unread error
        manager.add_notification("T3", "M3", "error")  # Unread error

        assert manager.get_unread_count() == 2

        # Mark one as read
        manager.mark_as_read(manager.notifications[0]["id"])  # notifications[0] is most recent (T3)
        assert manager.get_unread_count() == 1

    def test_mark_all_as_read(self, manager):
        manager.add_notification("T1", "M1", "error")
        manager.add_notification("T2", "M2", "error")
        assert manager.get_unread_count() == 2

        manager.mark_all_as_read()
        assert manager.get_unread_count() == 0
        assert all(n["read"] for n in manager.notifications)

    def test_delete_notification(self, manager):
        manager.add_notification("T1", "M1")
        id_to_del = manager.notifications[0]["id"]

        manager.delete_notification(id_to_del)
        assert len(manager.notifications) == 0

    def test_clear_all(self, manager):
        manager.add_notification("T1", "M1")
        manager.add_notification("T2", "M2")

        manager.clear_all()
        assert len(manager.notifications) == 0

    def test_persistence(self, manager, tmp_path, mocker):
        manager.add_notification("Persist Me", "Important")

        # Create new instance, should load from file
        # Dobbiamo ri-mockare CONFIG_DIR per la nuova istanza se non autouse
        NotificationManager._reset_instance_for_testing()
        new_manager = NotificationManager.instance()

        assert len(new_manager.notifications) == 1
        assert new_manager.notifications[0]["title"] == "Persist Me"

    def test_load_corrupted_file(self, tmp_path, mocker):
        notif_file = tmp_path / "notifications.json"
        notif_file.write_text("invalid json")

        # CONFIG_DIR è già mockato da reset_singleton autouse
        NotificationManager._reset_instance_for_testing()
        manager = NotificationManager.instance()
        assert manager.notifications == []
