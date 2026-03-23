import sqlite3
from unittest.mock import patch

import pytest

from src.core.audit_manager import AuditManager


class TestAuditManager:
    @pytest.fixture
    def manager(self, tmp_path, mocker):  # noqa: ANN001
        # Ensure data dir exists
        db_dir = tmp_path / "data"
        db_dir.mkdir()
        db_path = db_dir / "audit_log.db"

        # Patch the class-level attribute in AuditDatabase where it's actually used
        mocker.patch("src.core.audit.database.AuditDatabase.DB_PATH", db_path)
        # Patch CONFIG_DIR in the new modules
        mocker.patch("src.core.audit.database.CONFIG_DIR", tmp_path)
        mocker.patch("src.core.audit.manager.AuditSignals.instance")

        # Reset singleton
        AuditManager._instance = None
        mgr = AuditManager()
        yield mgr
        AuditManager._instance = None

    def test_log_action_and_integrity(self, manager):  # noqa: ANN001
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
        with sqlite3.connect(manager.DB_PATH) as conn:
            conn.execute("UPDATE audit_logs SET action = 'Hacked' WHERE action = 'Test Action'")
            conn.commit()

        assert manager.verify_integrity() is False

    def test_get_logs(self, manager):  # noqa: ANN001
        manager.log_action("A1")
        manager.log_action("A2")
        manager._log_queue.join()

        logs = manager.get_logs()
        assert len(logs) == 2  # noqa: PLR2004
        assert logs[0]["action"] == "A2"  # Descending order

    def test_retention_policy(self, manager):  # noqa: ANN001
        manager.log_action("Old Action")
        manager._log_queue.join()

        # Manually set timestamp to old date
        with sqlite3.connect(manager.DB_PATH) as conn:
            conn.execute("UPDATE audit_logs SET timestamp = '2020-01-01 00:00:00'")
            conn.commit()

        manager.run_retention_policy(days=1)
        manager._log_queue.join()

        # Old action should be gone, but policy run itself logged
        logs = manager.get_logs()
        assert len(logs) == 1
        assert logs[0]["action"] == "Pulizia Log"

    def test_notification_emission(self, manager):  # noqa: ANN001
        with patch("src.core.notification_manager.NotificationManager.instance") as mock_notif:
            manager.log_action("Action", notify=True)
            manager._log_queue.join()
            mock_notif.return_value.add_notification.assert_called_once()

    def test_get_current_user(self, manager):  # noqa: ANN001
        with patch.dict("os.environ", {"USERNAME": "TestUser"}):
            assert manager._get_current_user() == "TestUser"

        with patch.dict("os.environ", {}, clear=True):
            with patch("getpass.getuser", return_value="PassUser"):
                assert manager._get_current_user() == "PassUser"
