import sqlite3
from unittest.mock import PropertyMock, patch

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
            "src.core.database.manager.DatabaseManager.DB_AUDIT",
            new_callable=PropertyMock,
            return_value=db_path,
        )

        # Patch Signals singleton instance
        mocker.patch("src.core.audit.manager.AuditSignals.instance")

        # Reset singleton
        AuditManager._instance = None
        mgr = AuditManager()
        # Ensure DB is initialized at the fake path
        mgr.db._init_db()

        yield mgr
        AuditManager._instance = None

    def test_log_action_and_integrity(self, manager):
        """Test logging an action and verifying chain integrity."""
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
        # Usiamo manager.db.DB_PATH che ora punta al nostro file temporaneo
        with sqlite3.connect(manager.db.DB_PATH) as conn:
            conn.execute("UPDATE audit_logs SET action = 'Hacked' WHERE action = 'Test Action'")
            conn.commit()

        assert manager.verify_integrity() is False

    def test_get_logs(self, manager):
        manager.log_action("A1")
        manager.log_action("A2")
        manager._log_queue.join()

        logs = manager.get_logs()
        assert len(logs) == 2
        assert logs[0]["action"] == "A2"  # Descending order

    def test_retention_policy(self, manager):
        manager.log_action("Old Action")
        manager._log_queue.join()

        # Manually set timestamp to old date
        with sqlite3.connect(manager.db.DB_PATH) as conn:
            conn.execute("UPDATE audit_logs SET timestamp = '2020-01-01 00:00:00'")
            conn.commit()

        manager.run_retention_policy(days=1)
        manager._log_queue.join()

        # Old action should be gone, but policy run itself logged
        logs = manager.get_logs()
        # Cerca il log della pulizia
        assert any(log_entry["action"] == "Pulizia Log" for log_entry in logs)
        # Il log originale dovrebbe essere sparito
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
