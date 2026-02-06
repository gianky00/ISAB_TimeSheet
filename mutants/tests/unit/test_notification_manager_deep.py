import json
from unittest.mock import patch

import pytest

from src.core.notification_manager import NotificationManager


class TestNotificationManagerDeep:
    @pytest.fixture
    def manager(self, tmp_path):
        """Crea istanza con file temporaneo per i test."""
        with patch.object(NotificationManager, "_instance", None):
            with patch(
                "src.core.notification_manager.config_manager.CONFIG_DIR", tmp_path
            ):
                nm = NotificationManager()
                nm.notifications_file = tmp_path / "notifications.json"
                yield nm

    def test_add_notification_signals(self, manager, qtbot):
        with qtbot.waitSignal(manager.notification_added, timeout=1000):
            manager.add_notification("Test", "Messaggio di test", level="info")
        assert len(manager.notifications) == 1

    def test_notification_persistence(self, manager, tmp_path):
        manager.add_notification("Persist", "Test persist", level="warning")

        # Reload to check persistence
        data = json.loads(manager.notifications_file.read_text())
        assert len(data) == 1
        assert data[0]["title"] == "Persist"

    def test_mark_as_read(self, manager):
        manager.add_notification("Read Test", "msg", level="error")
        notif_id = manager.notifications[0]["id"]

        assert manager.get_unread_count() == 1
        manager.mark_as_read(notif_id)
        assert manager.get_unread_count() == 0

    def test_mark_all_as_read(self, manager):
        manager.add_notification("E1", "m1", level="error")
        manager.add_notification("E2", "m2", level="error")
        assert manager.get_unread_count() == 2

        manager.mark_all_as_read()
        assert manager.get_unread_count() == 0

    def test_delete_notification(self, manager):
        manager.add_notification("Del", "msg")
        notif_id = manager.notifications[0]["id"]

        manager.delete_notification(notif_id)
        assert len(manager.notifications) == 0

    def test_clear_all(self, manager):
        for i in range(5):
            manager.add_notification(f"N{i}", f"m{i}")
        assert len(manager.notifications) == 5

        manager.clear_all()
        assert len(manager.notifications) == 0

    def test_migration_old_schema(self, manager):
        old_notif = {"id": "123", "title": "Old", "message": "Msg"}
        migrated = manager._migrate_notification(old_notif)

        assert migrated["category"] == "system"
        assert migrated["priority"] == "low"
        assert migrated["pinned"] is False
