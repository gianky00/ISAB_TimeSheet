"""
Thread-safe tests for NotificationManager.
"""

import json
import threading
from unittest.mock import patch

import pytest

from src.core.notification_manager import NotificationManager


class TestNotificationManagerThreadSafe:
    @pytest.fixture
    def manager(self, tmp_path):
        """Fixture per un manager isolato."""
        with patch("src.core.notification_manager.CONFIG_DIR", tmp_path):
            NotificationManager._instance = None  # Reset singleton
            return NotificationManager.instance()

    def test_persistence(self, manager, tmp_path):
        """Verifica che le notifiche siano salvate su disco."""
        manager.add_notification("Titolo", "Messaggio", level="success")

        # Verifica file esiste
        notif_file = tmp_path / "notifications.json"
        assert notif_file.exists()

        # Carica dati
        with notif_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            assert len(data) == 1
            assert data[0]["title"] == "Titolo"
            assert data[0]["level"] == "success"

    def test_concurrent_additions(self, manager):
        """Verifica la thread-safety aggiungendo notifiche da più thread."""
        num_threads = 5
        adds_per_thread = 20

        def worker():
            for i in range(adds_per_thread):
                manager.add_notification(f"Thread {threading.get_ident()}", f"Msg {i}")

        threads = [threading.Thread(target=worker) for _ in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verifica totale (inclusa la notifica di default se presente, ma qui è pulito)
        assert len(manager.get_notifications()) == num_threads * adds_per_thread

    def test_unread_count_only_errors(self, manager):
        """Verifica che unread_count conti solo le notifiche di livello 'error'."""
        manager.clear_all()
        manager.add_notification("Info", "Msg", level="info")
        manager.add_notification("Err 1", "Msg", level="error")
        manager.add_notification("Err 2", "Msg", level="error")
        manager.add_notification("Warn", "Msg", level="warning")

        assert manager.get_unread_count() == 2

        # Segna una come letta
        notifs = manager.get_notifications()
        err_id = next(n["id"] for n in notifs if n["level"] == "error")
        manager.mark_as_read(err_id)

        assert manager.get_unread_count() == 1

    def test_signals_emission(self, manager, qtbot):
        """Verifica l'emissione dei segnali Qt."""
        # Spy sui segnali
        with qtbot.waitSignal(manager.notification_added, timeout=1000) as blocker:
            manager.add_notification("Test Signal", "Content")

        assert blocker.args[0]["title"] == "Test Signal"

    def test_toast_request_signal(self, manager, qtbot):
        """Verifica che venga emesso il segnale per il toast se richiesto."""
        with qtbot.waitSignal(manager.request_toast, timeout=1000) as blocker:
            manager.add_notification("Toast", "Message", level="warning", show_toast=True)

        # args: (messaggio, tipo, durata)
        assert "Toast" in blocker.args[0]
        assert blocker.args[1] == "warning"
        assert blocker.args[2] == 10000  # Duration for warning
