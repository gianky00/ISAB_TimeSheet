import queue
from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

from src.core.audit.manager import AuditManager
from src.core.audit.models import Severity, Status


class TestAuditManager:
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        AuditManager._instance = None
        with patch("threading.Thread"):
            self.manager = AuditManager.instance()
            self.manager._initialized = True
            self.manager.db = MagicMock()
            self.manager.signals = MagicMock()
            self.manager._log_queue = queue.Queue()

    def test_log_action_enqueues(self):
        self.manager.log_action("Test Action", category="Test")
        assert self.manager._log_queue.qsize() == 1
        task = self.manager._log_queue.get()
        assert task["action"] == "Test Action"

    @patch("src.core.audit.manager.AuditIntegrity.calculate_hash", return_value="hash123")
    @patch("src.core.audit.manager.AuditManager._get_current_user", return_value="testuser")
    def test_execute_log_internal(self, mock_user, mock_hash):
        self.manager.db.get_last_hash.return_value = "prev"
        self.manager.db.insert_log.return_value = 100

        audit_id = self.manager._execute_log_internal(
            action="Save",
            category="DB",
            entity="Emp",
            params={"id": 1},
            status=Status.SUCCESS,
            severity=Severity.LOW,
            duration_ms=10,
            module="core",
            error_code=None,
            notify=True,
            trace_id="T1",
        )

        assert audit_id == 100
        assert self.manager.db.insert_log.called

    def test_verify_integrity_success(self):
        mock_conn = MagicMock()
        self.manager.db.get_connection.return_value.__enter__.return_value = mock_conn
        rows = [{"id": 1, "row_hash": "h1"}]
        mock_conn.execute.return_value.fetchall.return_value = rows
        with patch.object(self.manager, "_check_row_integrity", return_value=True):
            assert self.manager.verify_integrity() is True

    def test_run_retention_policy(self):
        self.manager.db.delete_older_than.return_value = 5
        self.manager.run_retention_policy(days=30)
        assert self.manager.db.delete_older_than.called

    def test_get_stats_by_day(self):
        # Invece di patchare datetime, accettiamo che usi la data odierna
        # e simuliamo i dati nel DB per la data odierna.
        today_str = datetime.now(UTC).strftime("%Y-%m-%d")

        mock_conn = MagicMock()
        self.manager.db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value.fetchall.return_value = [(today_str, "success", 10)]

        stats = self.manager.get_stats_by_day(days=1)
        assert today_str in stats
        assert stats[today_str]["success"] == 10
