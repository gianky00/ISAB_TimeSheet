from unittest.mock import MagicMock

import pytest

from src.core.notification_manager import NotificationManager


class TestNotificationManager:
    @pytest.fixture(autouse=True)
    def setup_manager(self, fs):
        from src.core.paths import CONFIG_DIR

        fs.create_dir(str(CONFIG_DIR))
        NotificationManager._reset_instance_for_testing()
        self.manager = NotificationManager.instance()
        return self.manager

    def test_load_empty(self, fs):
        assert self.manager.notifications == []

    def test_add_notification_basic(self, fs):
        self.manager.add_notification("Title", "Message", level="error")
        assert len(self.manager.notifications) == 1
        notif = self.manager.notifications[0]
        assert notif["title"] == "Title"
        assert notif["level"] == "error"
        assert notif["read"] is False
        assert self.manager.get_unread_count() == 1

    def test_add_notification_toast(self):
        # Spia del segnale
        mock_slot = MagicMock()
        self.manager.request_toast.connect(mock_slot)

        self.manager.add_notification("T", "Msg", show_toast=True)

        assert mock_slot.called
        # Verifica troncamento messaggio lungo
        long_msg = "X" * 200
        self.manager.add_notification("T", long_msg, show_toast=True)
        args = mock_slot.call_args_list[-1][0]
        assert len(args[0]) <= self.manager.MAX_MESSAGE_LEN + 10  # Titolo + Msg + "..."

    def test_mark_as_read(self):
        self.manager.add_notification("T", "M", level="error")
        notif_id = self.manager.notifications[0]["id"]

        self.manager.mark_as_read(notif_id)
        assert self.manager.notifications[0]["read"] is True
        assert self.manager.get_unread_count() == 0

    def test_mark_all_as_read(self):
        self.manager.add_notification("T1", "M1", level="error")
        self.manager.add_notification("T2", "M2", level="error")

        self.manager.mark_all_as_read()
        assert all(n["read"] for n in self.manager.notifications)
        assert self.manager.get_unread_count() == 0

    def test_delete_notification(self):
        self.manager.add_notification("T", "M")
        notif_id = self.manager.notifications[0]["id"]

        self.manager.delete_notification(notif_id)
        assert len(self.manager.notifications) == 0

    def test_clear_all(self):
        self.manager.add_notification("T", "M")
        self.manager.clear_all()
        assert len(self.manager.notifications) == 0

    def test_migrate_notification(self):
        old_notif = {"title": "Old"}
        migrated = self.manager._migrate_notification(old_notif)
        assert migrated["category"] == "system"
        assert migrated["title"] == "Old"

    def test_load_corrupt(self, fs):
        from src.core.constants import FileNames
        from src.core.paths import CONFIG_DIR

        fs.create_file(str(CONFIG_DIR / FileNames.NOTIFICATIONS), contents="{invalid}")

        # Reload notifications
        res = self.manager._load_notifications()
        assert res == []
