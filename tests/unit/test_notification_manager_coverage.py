

import pytest

from src.core.notification_manager import NotificationManager


class TestNotificationManagerCoverage:
    @pytest.fixture
    def manager(self, tmp_path, mocker):
        # Patch della directory config
        mocker.patch("src.core.config_manager.CONFIG_DIR", tmp_path)
        # Forza reset singleton
        NotificationManager._instance = None
        return NotificationManager.instance()

    def test_add_notification_and_signals(self, manager, mocker):
        """Verifica aggiunta notifica e invio segnali Qt."""
        mock_added = mocker.Mock()
        mock_updated = mocker.Mock()
        mock_count = mocker.Mock()

        manager.notification_added.connect(mock_added)
        manager.notifications_updated.connect(mock_updated)
        manager.unread_count_changed.connect(mock_count)

        manager.add_notification("Titolo", "Messaggio", level="error")

        assert len(manager.notifications) == 1
        assert manager.notifications[0]["title"] == "Titolo"
        assert manager.get_unread_count() == 1

        mock_added.assert_called_once()
        mock_updated.assert_called_once()
        mock_count.assert_called_with(1)

    def test_persistence_load_save(self, manager, tmp_path):
        """Verifica che le notifiche sopravvivano al riavvio del manager."""
        manager.add_notification("Persistente", "Dato")

        # Simula riavvio singleton
        NotificationManager._instance = None
        nuovo_manager = NotificationManager.instance()

        assert len(nuovo_manager.notifications) == 1
        assert nuovo_manager.notifications[0]["title"] == "Persistente"

    def test_mark_as_read_logic(self, manager):
        """Verifica gestione dello stato letto/non letto."""
        manager.add_notification("N1", "M1", level="error")
        nid = manager.notifications[0]["id"]

        assert manager.get_unread_count() == 1
        manager.mark_as_read(nid)
        assert manager.get_unread_count() == 0
        assert manager.notifications[0]["read"] is True

    def test_mark_all_as_read(self, manager):
        """Verifica segna tutto come letto."""
        manager.add_notification("N1", "M1", level="error")
        manager.add_notification("N2", "M2", level="error")

        manager.mark_all_as_read()
        assert manager.get_unread_count() == 0

    def test_delete_notification(self, manager):
        """Verifica rimozione singola notifica."""
        manager.add_notification("Delete Me", "Bye")
        nid = manager.notifications[0]["id"]

        manager.delete_notification(nid)
        assert len(manager.notifications) == 0

    def test_clear_all(self, manager):
        """Verifica svuotamento totale."""
        manager.add_notification("N1", "M1")
        manager.clear_all()
        assert len(manager.notifications) == 0
