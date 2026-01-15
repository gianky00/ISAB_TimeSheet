import json
from unittest.mock import patch

import pytest

from src.core.notification_manager import NotificationManager


class TestNotificationCoverage:
    """Test suite per src/core/notification_manager.py"""

    @pytest.fixture(autouse=True)
    def setup_manager(
        self, tmp_path, qapp
    ):  # qapp fixture from pytest-qt needed for signals
        """Setup isolato per NotificationManager."""
        # Reset Singleton
        NotificationManager._instance = None

        # Mock del file path
        self.fake_file = tmp_path / "notifications.json"

        with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
            self.manager = NotificationManager.instance()
            # Assicuriamoci che punti al file giusto
            self.manager.notifications_file = self.fake_file
            self.manager.notifications = []  # Pulisci in memoria

        yield

        NotificationManager._instance = None

    def test_add_notification(self, qtbot):
        """Test aggiunta notifica e segnali."""
        with qtbot.waitSignal(self.manager.notification_added, timeout=1000) as blocker:
            self.manager.add_notification("Test Title", "Test Body", "warning")

        assert len(self.manager.notifications) == 1
        n = self.manager.notifications[0]
        assert n["title"] == "Test Title"
        assert n["level"] == "warning"
        assert n["read"] is False

        # Verifica argomenti segnale
        assert blocker.args[0] == n

        # Verifica salvataggio file
        assert self.fake_file.exists()
        content = json.loads(self.fake_file.read_text())
        assert len(content) == 1

    def test_load_notifications(self):
        """Test caricamento da file esistente."""
        # Creiamo un file dummy
        data = [
            {
                "id": "1",
                "title": "Old",
                "timestamp": "2023-01-01T00:00:00",
                "read": True,
            },
            {
                "id": "2",
                "title": "New",
                "timestamp": "2024-01-01T00:00:00",
                "read": False,
            },
        ]
        self.fake_file.write_text(json.dumps(data))

        # Ricarichiamo manager (o chiamiamo _load)
        loaded = self.manager._load_notifications()

        # Deve essere ordinato per timestamp desc (New prima di Old)
        assert len(loaded) == 2
        assert loaded[0]["title"] == "New"
        assert loaded[1]["title"] == "Old"

    def test_get_notifications_filter(self):
        """Test filtri (letti/non letti)."""
        self.manager.notifications = [
            {"id": "1", "read": True},
            {"id": "2", "read": False},
        ]

        all_n = self.manager.get_notifications(filter_unread=False)
        unread_n = self.manager.get_notifications(filter_unread=True)

        assert len(all_n) == 2
        assert len(unread_n) == 1
        assert unread_n[0]["id"] == "2"

    def test_mark_as_read(self):
        """Test segna come letto."""
        self.manager.add_notification("A", "B", level="error")
        nid = self.manager.notifications[0]["id"]

        assert self.manager.get_unread_count() == 1

        self.manager.mark_as_read(nid)

        assert self.manager.get_unread_count() == 0
        assert self.manager.notifications[0]["read"] is True

    def test_mark_all_as_read(self):
        """Test segna tutto come letto."""
        self.manager.add_notification("A", "B", level="error")
        self.manager.add_notification("C", "D", level="error")

        assert self.manager.get_unread_count() == 2

        self.manager.mark_all_as_read()

        assert self.manager.get_unread_count() == 0

    def test_delete_notification(self):
        """Test cancellazione singola."""
        self.manager.add_notification("A", "B")
        nid = self.manager.notifications[0]["id"]

        self.manager.delete_notification(nid)

        assert len(self.manager.notifications) == 0
        assert self.manager.get_unread_count() == 0

    def test_clear_all(self):
        """Test pulizia totale."""
        self.manager.add_notification("A", "B")
        self.manager.add_notification("C", "D")

        self.manager.clear_all()

        assert len(self.manager.notifications) == 0
        assert not self.fake_file.exists() or self.fake_file.read_text() == "[]"
