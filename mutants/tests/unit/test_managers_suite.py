import sqlite3
from unittest.mock import patch

import pytest

from src.core.audit_manager import AuditManager
from src.core.stats_manager import StatsManager


@pytest.fixture
def temp_audit_db(tmp_path, mocker):
    db_file = tmp_path / "audit_log.db"
    # Patch the real DB_PATH in AuditDatabase
    mocker.patch("src.core.audit.database.AuditDatabase.DB_PATH", db_file)
    # Patch signals to avoid PyQt6 issues
    mocker.patch("src.core.audit.manager.AuditSignals.instance")

    # Force re-initialization for the singleton in test
    AuditManager._instance = None
    manager = AuditManager()
    yield manager


@pytest.fixture
def mock_config_stats():
    with patch("src.core.stats_manager.config_manager") as mock_cfg:
        mock_cfg.load_config.return_value = {}
        # Force re-initialization
        StatsManager._instance = None
        manager = StatsManager()
        yield manager, mock_cfg


class TestAuditManager:
    def test_log_action(self, temp_audit_db):
        manager = temp_audit_db
        manager.log_action(
            "Test Action", category="test", entity="user", params={"p": 1}
        )

        # Verify data
        logs = manager.get_logs(limit=1)
        assert len(logs) == 1
        assert logs[0]["action"] == "Test Action"
        assert logs[0]["category"] == "test"

    def test_integrity_check(self, temp_audit_db):
        manager = temp_audit_db
        manager.log_action("A1")
        manager.log_action("A2")

        assert manager.verify_integrity() is True

        # Tamper with the DB
        with sqlite3.connect(manager.DB_PATH) as conn:
            conn.execute("UPDATE audit_logs SET action = 'HACKED' WHERE id = 1")
            conn.commit()

        assert manager.verify_integrity() is False


class TestStatsManager:
    def test_increment_usage(self, mock_config_stats):
        manager, mock_cfg = mock_config_stats
        manager.increment_usage("bot_1")

        stats = manager.get_all_stats()
        assert stats["bot_1"]["runs"] == 1
        mock_cfg.set_config_value.assert_called()

    def test_increment_error(self, mock_config_stats):
        manager, mock_cfg = mock_config_stats
        manager.increment_error("bot_1")

        stats = manager.get_all_stats()
        assert stats["bot_1"]["errors"] == 1
