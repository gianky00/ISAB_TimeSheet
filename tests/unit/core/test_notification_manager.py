import json
from unittest.mock import MagicMock

import pytest

from src.core.notification_manager import NotificationManager


class TestNotificationManager:
    @pytest.fixture(autouse=True)
    def setup_manager(self, fs):
        # Reset singleton
        NotificationManager._reset_instance_for_testing()
        # Mock directory di configurazione
        fs.create_dir(str(NotificationManager.instance().notifications_file.parent))
        self.mgr = NotificationManager.instance()

    def test_singleton(self):
        assert NotificationManager.instance() is self.mgr

    def test_add_notification_and_persistence(self, fs):
        self.mgr.add_notification("Title", "Message", level="error")

        assert len(self.mgr.notifications) == 1
        assert self.mgr.notifications[0]["title"] == "Title"
        assert self.mgr.get_unread_count() == 1

        # Verifica file
        assert self.mgr.notifications_file.exists()
        data = json.loads(self.mgr.notifications_file.read_text())
        assert data[0]["title"] == "Title"

    def test_mark_as_read(self):
        self.mgr.add_notification("T", "M", level="error")
        notif_id = self.mgr.notifications[0]["id"]

        self.mgr.mark_as_read(notif_id)
        assert self.mgr.notifications[0]["read"] is True
        assert self.mgr.get_unread_count() == 0

    def test_mark_all_as_read(self):
        self.mgr.add_notification("T1", "M1", level="error")
        self.mgr.add_notification("T2", "M2", level="error")

        self.mgr.mark_all_as_read()
        assert all(n["read"] for n in self.mgr.notifications)
        assert self.mgr.get_unread_count() == 0

    def test_delete_notification(self):
        self.mgr.add_notification("T", "M")
        notif_id = self.mgr.notifications[0]["id"]

        self.mgr.delete_notification(notif_id)
        assert len(self.mgr.notifications) == 0

    def test_clear_all(self):
        self.mgr.add_notification("T1", "M1")
        self.mgr.add_notification("T2", "M2")

        self.mgr.clear_all()
        assert len(self.mgr.notifications) == 0

    def test_truncate_long_toast_message(self):
        long_msg = "A" * 200
        mock_signal = MagicMock()
        self.mgr.request_toast.connect(mock_signal)

        self.mgr.add_notification("Title", long_msg, show_toast=True)

        # Il segnale deve contenere il messaggio troncato
        emitted_msg = mock_signal.call_args[0][0]
        assert len(emitted_msg) <= self.mgr.MAX_MESSAGE_LEN + len("Title: ")
        assert emitted_msg.endswith("...")

    def test_load_and_migrate(self, fs):
        # Scrive un file con schema vecchio (mancano campi come 'pinned')
        old_data = [{"id": "1", "title": "Old", "timestamp": "2023-01-01T10:00:00Z"}]
        fs.create_file(str(self.mgr.notifications_file), contents=json.dumps(old_data))

        # Forza ricaricamento (creando nuova istanza o resettando)
        NotificationManager._reset_instance_for_testing()
        new_mgr = NotificationManager.instance()

        assert len(new_mgr.notifications) == 1
        assert new_mgr.notifications[0]["pinned"] is False  # Default migrato
        assert new_mgr.notifications[0]["source"] == "Sistema"
