from unittest.mock import MagicMock, patch

import pytest

from src.core.notification_manager import NotificationManager


class TestNotificationManager:
    @pytest.fixture
    def manager(self, tmp_path, mocker):  # noqa: ANN001
        # Mock CONFIG_DIR to use tmp_path
        mocker.patch("src.core.config_manager.CONFIG_DIR", tmp_path)
        # Reset singleton for testing
        NotificationManager._instance = None
        return NotificationManager.instance()

    def test_singleton(self, manager):  # noqa: ANN001
        assert NotificationManager.instance() is manager

    def test_add_notification(self, manager):  # noqa: ANN001
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

    def test_get_unread_count(self, manager):  # noqa: ANN001
        manager.add_notification("T1", "M1", "info")
        manager.add_notification("T2", "M2", "error")  # Unread error
        manager.add_notification("T3", "M3", "error")  # Unread error

        assert manager.get_unread_count() == 2  # noqa: PLR2004

        # Mark one as read
        manager.mark_as_read(manager.notifications[0]["id"])  # notifications[0] is most recent (T3)
        assert manager.get_unread_count() == 1

    def test_mark_all_as_read(self, manager):  # noqa: ANN001
        manager.add_notification("T1", "M1", "error")
        manager.add_notification("T2", "M2", "error")
        assert manager.get_unread_count() == 2  # noqa: PLR2004

        manager.mark_all_as_read()
        assert manager.get_unread_count() == 0
        assert all(n["read"] for n in manager.notifications)

    def test_delete_notification(self, manager):  # noqa: ANN001
        manager.add_notification("T1", "M1")
        id_to_del = manager.notifications[0]["id"]

        manager.delete_notification(id_to_del)
        assert len(manager.notifications) == 0

    def test_clear_all(self, manager):  # noqa: ANN001
        manager.add_notification("T1", "M1")
        manager.add_notification("T2", "M2")

        manager.clear_all()
        assert len(manager.notifications) == 0

    def test_persistence(self, manager, tmp_path):  # noqa: ANN001
        manager.add_notification("Persist Me", "Important")

        # Create new instance, should load from file
        NotificationManager._instance = None
        new_manager = NotificationManager.instance()

        assert len(new_manager.notifications) == 1
        assert new_manager.notifications[0]["title"] == "Persist Me"

    def test_load_corrupted_file(self, tmp_path):  # noqa: ANN001
        notif_file = tmp_path / "notifications.json"
        notif_file.write_text("invalid json")

        with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
            NotificationManager._instance = None
            manager = NotificationManager.instance()
            assert manager.notifications == []
