import sqlite3
from unittest.mock import patch

import pytest

from src.core.audit_manager import AuditManager


class TestAuditManager:
    @pytest.fixture
    def manager(self, tmp_path, mocker):
        # Ensure data dir exists
        db_dir = tmp_path / "data"
        db_dir.mkdir()
        db_path = db_dir / "audit_log.db"

        # Patch DatabaseManager properties on the CLASS to affect all instances (and the singleton)
        # Note: We must patch it where it's DEFINED
        mocker.patch(
            "src.core.database.db_manager.DB_AUDIT",
            db_path,
        )

        # Patch Signals singleton instance
        mocker.patch("src.core.audit.manager.AuditSignals.instance")

        # Reset singleton
        AuditManager._instance = None
        mgr = AuditManager()
        # Force the DB path in the instance's database object
        mgr.db.db_path = db_path
        # Ensure DB is initialized at the fake path
        mgr.db._init_db()

        yield mgr
        AuditManager._instance = None

    def test_log_action_and_integrity(self, manager):
        """Test logging an action and verifying chain integrity."""
        # Reset chain state
        with sqlite3.connect(manager.db.db_path) as conn:
            conn.execute("DELETE FROM audit_logs")
            conn.commit()

        manager.log_action("Test Action", "unit-test", entity="App", status=AuditManager.Status.SUCCESS)
        manager.log_action(
            "Test Action 2",
            "unit-test",
            entity="App",
            status=AuditManager.Status.SUCCESS,
        )
        # Attendi il worker asincrono
        manager._log_queue.join()

        # Verify integrity
        assert manager.verify_integrity() is True

        # Manually corrupt DB to test integrity failure
        with sqlite3.connect(manager.db.db_path) as conn:
            # Modifichiamo l'azione mantenendo lo stesso row_hash
            conn.execute("UPDATE audit_logs SET action = 'Hacked' WHERE action = 'Test Action'")
            conn.commit()

        # Ora verify_integrity deve fallire perché l'hash calcolato sui dati non corrisponde a row_hash
        assert manager.verify_integrity() is False

    def test_retention_policy(self, manager):
        """Verifica che la policy di retention elimini i log vecchi e registri l'operazione."""
        # Pulisci tutto prima del test
        with sqlite3.connect(manager.db.db_path) as conn:
            conn.execute("DELETE FROM audit_logs")
            conn.commit()

        manager.log_action("Old Action")
        manager._log_queue.join()

        # Impostiamo una data molto vecchia in formato compatibile SQLite
        with sqlite3.connect(manager.db.db_path) as conn:
            conn.execute(
                "UPDATE audit_logs SET timestamp = '2020-01-01 00:00:00' WHERE action = 'Old Action'"
            )
            conn.commit()

        # Esegui retention (days=1 significa elimina tutto ciò che è più vecchio di ieri)
        manager.run_retention_policy(days=1)
        manager._log_queue.join()

        # Old action deve essere sparita
        logs = manager.get_logs()
        # Il log della pulizia deve essere presente (perché Old Action è stata eliminata)
        assert any(log_entry["action"] == "Pulizia Log" for log_entry in logs)
        # Il log originale deve essere sparito
        assert not any(log_entry["action"] == "Old Action" for log_entry in logs)

    def test_notification_emission(self, manager):
        with patch("src.core.notification_manager.NotificationManager.instance") as mock_notif:
            manager.log_action("Action", notify=True)
            manager._log_queue.join()
            mock_notif.return_value.add_notification.assert_called_once()

    def test_get_current_user(self, manager):
        # Il metodo reale usa os.getenv('USERNAME') su Windows o getpass.getuser()
        with patch.dict("os.environ", {"USERNAME": "TestUser"}):
            assert manager._get_current_user() == "TestUser"
