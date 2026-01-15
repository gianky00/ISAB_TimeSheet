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

        # Patch the class-level attribute before instantiation
        mocker.patch("src.core.audit_manager.AuditManager.DB_PATH", db_path)
        # Patch CONFIG_DIR just in case
        mocker.patch("src.core.audit_manager.CONFIG_DIR", tmp_path)

        # Reset singleton
        AuditManager._instance = None
        return AuditManager()

    def test_log_action_and_integrity(self, manager):
        """Test logging an action and verifying chain integrity."""
        manager.log_action(
            "Test Action", "unit-test", entity="App", status=AuditManager.Status.SUCCESS
        )
        manager.log_action(
            "Test Action 2",
            "unit-test",
            entity="App",
            status=AuditManager.Status.SUCCESS,
        )

        # Verify integrity
        assert manager.verify_integrity() is True

        # Manually corrupt DB to test integrity failure
        with sqlite3.connect(manager.DB_PATH) as conn:
            conn.execute("UPDATE audit_logs SET action = 'Hacked' WHERE id = 1")
            conn.commit()

        assert manager.verify_integrity() is False

    def test_get_logs(self, manager):
        manager.log_action("A1")
        manager.log_action("A2")

        logs = manager.get_logs()
        assert len(logs) == 2
        assert logs[0]["action"] == "A2"  # Descending order

    def test_retention_policy(self, manager):
        manager.log_action("Old Action")

        # Manually set timestamp to old date
        with sqlite3.connect(manager.DB_PATH) as conn:
            conn.execute("UPDATE audit_logs SET timestamp = '2020-01-01 00:00:00'")
            conn.commit()

        manager.run_retention_policy(days=1)

        # Old action should be gone, but policy run itself logged
        logs = manager.get_logs()
        assert len(logs) == 1
        assert logs[0]["action"] == "Sistema"

    def test_notification_emission(self, manager):
        with patch(
            "src.core.notification_manager.NotificationManager.instance"
        ) as mock_notif:
            manager.log_action("Action", notify=True)
            mock_notif.return_value.add_notification.assert_called_once()

    def test_get_current_user(self, manager):
        with patch.dict("os.environ", {"USERNAME": "TestUser"}):
            assert manager._get_current_user() == "TestUser"

        with patch.dict("os.environ", {}, clear=True):
            with patch("getpass.getuser", return_value="PassUser"):
                assert manager._get_current_user() == "PassUser"
