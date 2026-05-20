import pytest

from src.core.audit.manager import AuditManager
from src.core.audit.models import Severity, Status


class TestAuditManager:
    @pytest.fixture(autouse=True)
    def setup_manager(self, tmp_path, mocker):
        """Setup AuditManager with a temp DB."""
        # Patch AuditSignals to avoid PySide6 issues in headless
        mocker.patch("src.core.audit.manager.AuditSignals.instance")

        AuditManager._instance = None  # Reset Singleton
        db_path = tmp_path / "audit_test.db"

        # Patch the source in db_manager which is used by AuditDatabase property
        mocker.patch("src.core.database.db_manager.DB_AUDIT", db_path)

        manager = AuditManager()
        yield manager
        AuditManager._instance = None

    def test_log_action_success(self, setup_manager):
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

    def test_log_action_with_params(self, setup_manager):
        manager = setup_manager
        params = {"key": "value", "nested": 123}
        manager.log_action("Action with params", params=params)

        manager._log_queue.join()

        logs, _ = manager.get_filtered_logs()
        import json

        saved_params = json.loads(logs[0]["params"])
        assert saved_params["key"] == "value"

    def test_verify_integrity_ok(self, setup_manager):
        manager = setup_manager
        manager.log_action("Action 1")
        manager.log_action("Action 2")

        manager._log_queue.join()

        assert manager.verify_integrity() is True

    def test_get_stats_by_day(self, setup_manager):
        manager = setup_manager
        manager.log_action("A1", status=Status.SUCCESS)
        manager.log_action("A2", status=Status.ERROR)

        manager._log_queue.join()

        stats = manager.get_stats_by_day(days=1)
        # Sort keys to get today (last one)
        today = sorted(stats.keys())[-1]
        assert stats[today]["success"] >= 1
        assert stats[today]["error"] >= 1
