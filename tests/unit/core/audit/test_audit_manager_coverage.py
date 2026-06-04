import json
import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from src.application.services.audit_manager import AuditManager


class TestAuditManager:
    """Test coverage for src/application/services/audit modular V2."""

    @pytest.fixture
    def temp_db_manager(self, tmp_path, mocker):
        db_file = tmp_path / "audit_test.db"
        # Patch the actual location in db_manager
        mocker.patch("src.application.services.database.db_manager.DB_AUDIT", db_file)
        # Patch AuditSignals to avoid PySide6 issues in headless
        mocker.patch("src.application.services.audit.manager.AuditSignals.instance")

        # Reset singleton
        AuditManager._instance = None
        manager = AuditManager()
        yield manager
        AuditManager._instance = None

    def test_singleton(self, temp_db_manager):
        m1 = AuditManager()
        m2 = AuditManager()
        assert m1 is m2

    def test_init_db_creation(self, temp_db_manager):
        # Verify table exists
        with sqlite3.connect(temp_db_manager.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_logs'")
            assert cursor.fetchone() is not None
            # Verify columns
            cursor.execute("PRAGMA table_info(audit_logs)")
            columns = {row[1] for row in cursor.fetchall()}
            assert "severity" in columns
            assert "row_hash" in columns

    def test_log_action_integrity(self, temp_db_manager):
        manager = temp_db_manager

        # Log action
        manager.log_action("LOGIN", "auth", "user1", {"ip": "127.0.0.1"})

        # Attendi che il worker asincrono finisca (necessario in V2)
        manager._log_queue.join()

        # Verify it's in DB
        logs = manager.get_logs()
        assert len(logs) == 1
        entry = logs[0]
        assert entry["action"] == "LOGIN"
        assert entry["entity"] == "user1"
        assert json.loads(entry["params"]) == {"ip": "127.0.0.1"}
        assert entry["row_hash"] != "0" * 64

        # Verify integrity
        assert manager.verify_integrity() is True

    def test_integrity_failure(self, temp_db_manager):
        manager = temp_db_manager
        manager.log_action("TEST", "test")
        manager._log_queue.join()

        # Tamper with DB
        with sqlite3.connect(manager.DB_PATH) as conn:
            conn.execute("UPDATE audit_logs SET action = 'HACKED' WHERE action = 'TEST'")
            conn.commit()

        assert manager.verify_integrity() is False

    def test_get_current_user_env(self, temp_db_manager):
        # Patch os in manager.py
        with patch("src.application.services.audit.manager.os.environ.get") as mock_env:
            mock_env.return_value = "TEST_USER"
            assert temp_db_manager._get_current_user() == "TEST_USER"

    @patch("src.application.services.notification_manager.NotificationManager.instance")
    def test_notification_trigger(self, mock_notify, temp_db_manager):
        mock_instance = MagicMock()
        mock_notify.return_value = mock_instance

        temp_db_manager.log_action(
            "UPDATE",
            status=AuditManager.Status.SUCCESS,
            severity=AuditManager.Severity.LOW,
            notify=True,
            params={"error_details": "Versione aggiornata a 2.0"},
        )

        # Attendi il worker asincrono
        temp_db_manager._log_queue.join()

        mock_instance.add_notification.assert_called_once()
        args, kwargs = mock_instance.add_notification.call_args
        assert kwargs["level"] == "success"
        assert "Versione aggiornata a 2.0" in args[1]

    def test_retention_policy(self, temp_db_manager):
        from datetime import datetime, timedelta

        # Insert old record
        old_date = (datetime.now() - timedelta(days=100)).isoformat()
        with sqlite3.connect(temp_db_manager.DB_PATH) as conn:
            conn.execute(
                "INSERT INTO audit_logs (timestamp, action, row_hash) VALUES (?, ?, ?)",
                (old_date, "OLD_ACTION", "dummy_hash"),
            )
            conn.commit()

        temp_db_manager.run_retention_policy(days=90)

        # Attendi il log di "Pulizia Log" emesso internamente
        temp_db_manager._log_queue.join()

        logs = temp_db_manager.get_logs(limit=100)
        # Should only have the log about retention, OLD_ACTION should be gone
        actions = [log_entry["action"] for log_entry in logs]
        assert "OLD_ACTION" not in actions
        assert "Pulizia Log" in actions  # The retention log itself
