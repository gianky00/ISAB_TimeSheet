from unittest.mock import patch

import pytest

from src.core.audit.manager import AuditManager
from src.core.audit.models import Severity, Status


class TestAuditManager:
    @pytest.fixture(autouse=True)
    def setup_manager(self, tmp_path, mocker):  # noqa: ANN001
        """Setup AuditManager with a temp DB."""
        # Patch AuditSignals to avoid PyQt6 issues in headless
        mocker.patch("src.core.audit.manager.AuditSignals.instance")

        AuditManager._instance = None  # Reset Singleton
        db_path = tmp_path / "audit_test.db"

        with patch("src.core.audit.database.AuditDatabase.DB_PATH", db_path):
            manager = AuditManager()
            yield manager
            AuditManager._instance = None

    def test_log_action_success(self, setup_manager):  # noqa: ANN001
        manager = setup_manager
        # log_action in V2 returns None (asynchronous)
        manager.log_action(
            action="Test Action",
            category="Test Cat",
            entity="Test Entity",
            severity=Severity.HIGH,
            status=Status.SUCCESS,
        )

        manager._log_queue.join()

        logs, total = manager.get_filtered_logs()
        assert total == 1
        assert logs[0]["action"] == "Test Action"
        assert logs[0]["severity"] == "high"
        assert logs[0]["row_hash"] is not None

    def test_log_action_with_params(self, setup_manager):  # noqa: ANN001
        manager = setup_manager
        params = {"key": "value", "nested": 123}
        manager.log_action("Action with params", params=params)

        manager._log_queue.join()

        logs, _ = manager.get_filtered_logs()
        import json  # noqa: PLC0415

        saved_params = json.loads(logs[0]["params"])
        assert saved_params["key"] == "value"

    def test_verify_integrity_ok(self, setup_manager):  # noqa: ANN001
        manager = setup_manager
        manager.log_action("Action 1")
        manager.log_action("Action 2")

        manager._log_queue.join()

        assert manager.verify_integrity() is True

    def test_verify_integrity_fail(self, setup_manager, tmp_path):  # noqa: ANN001
        manager = setup_manager
        manager.log_action("Action 1")

        manager._log_queue.join()

        # Tamper with the database manually
        import sqlite3  # noqa: PLC0415

        conn = sqlite3.connect(manager.db.DB_PATH)
        conn.execute("UPDATE audit_logs SET action = 'TAMPERED' WHERE id = 1")
        conn.commit()
        conn.close()

        # Integrity should fail because action changed but hash remains same
        assert manager.verify_integrity() is False

    def test_run_retention_policy(self, setup_manager):  # noqa: ANN001
        manager = setup_manager
        # Manually insert an old record
        import sqlite3  # noqa: PLC0415
        from datetime import UTC, datetime, timedelta  # noqa: PLC0415

        old_ts = (datetime.now(UTC) - timedelta(days=100)).isoformat()

        with sqlite3.connect(manager.db.DB_PATH) as conn:
            conn.execute(
                "INSERT INTO audit_logs (timestamp, action) VALUES (?, ?)",
                (old_ts, "Old Action"),
            )

        # Sync check
        logs, total = manager.get_filtered_logs()
        assert total == 1

        manager.run_retention_policy(days=90)

        # Attendi il log di pulizia asincrono
        manager._log_queue.join()

        # Old record should be deleted
        _, total = manager.get_filtered_logs()
        assert total == 1  # Still 1 because we logged the "Pulizia Log" action!

        logs = manager.get_logs()
        assert logs[0]["action"] == "Pulizia Log"
        assert "Old Action" not in [log["action"] for log in logs]

    def test_get_stats_by_day(self, setup_manager):  # noqa: ANN001
        manager = setup_manager
        manager.log_action("A1", status=Status.SUCCESS)
        manager.log_action("A2", status=Status.ERROR)

        manager._log_queue.join()

        stats = manager.get_stats_by_day(days=1)
        # Sort keys to get today (last one)
        today = sorted(stats.keys())[-1]
        assert stats[today]["success"] >= 1
        assert stats[today]["error"] >= 1
