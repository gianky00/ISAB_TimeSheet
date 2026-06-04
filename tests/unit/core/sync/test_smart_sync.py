import sqlite3
from pathlib import Path
from unittest.mock import patch

import pytest

from src.application.services.sync.base import SyncTarget
from src.application.services.sync.smart_sync import SmartSyncEngine


class TestSmartSyncEngine:
    @pytest.fixture
    def target(self):
        return SyncTarget(db_path=Path(":memory:"), table_name="my_table", columns=["id", "val"])

    def _setup_db(self, db_path):
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE my_table (id TEXT PRIMARY KEY, val TEXT, note TEXT)")
        conn.executemany(
            "INSERT INTO my_table VALUES (?, ?, ?)",
            [
                ("1", "A", "n1"),
                ("2", "B", "n2"),
            ],
        )
        return conn

    @patch("src.application.services.sync.smart_sync.db_manager.get_connection")
    def test_sync_upsert_smart_no_conflict_cols(self, mock_conn, target):
        conn = self._setup_db(":memory:")
        mock_conn.return_value.__enter__.return_value = conn

        # New data: update id=1, add id=3
        new_data = [("1", "X"), ("3", "Y")]

        added_updated, deleted = SmartSyncEngine.sync_upsert_smart(
            target, new_data, conflict_cols=None, mirror=False
        )

        assert added_updated == 2
        assert deleted == 0

        cursor = conn.cursor()
        cursor.execute("SELECT id, val FROM my_table ORDER BY id")
        res = cursor.fetchall()
        assert res == [("1", "X"), ("2", "B"), ("3", "Y")]

    @patch("src.application.services.sync.smart_sync.db_manager.get_connection")
    def test_sync_upsert_smart_with_conflict_and_mirror(self, mock_conn, target):
        conn = self._setup_db(":memory:")
        mock_conn.return_value.__enter__.return_value = conn

        # New data: update id=1, drop id=2 (mirror)
        new_data = [("1", "X")]

        added_updated, deleted = SmartSyncEngine.sync_upsert_smart(
            target, new_data, conflict_cols=["id"], mirror=True
        )

        assert added_updated == 1
        assert deleted == 1

        cursor = conn.cursor()
        cursor.execute("SELECT id, val FROM my_table ORDER BY id")
        res = cursor.fetchall()
        assert res == [("1", "X")]

    @patch("src.application.services.sync.smart_sync.db_manager.get_connection")
    def test_sync_upsert_smart_empty(self, mock_conn, target):
        added, deleted = SmartSyncEngine.sync_upsert_smart(target, [])
        assert added == 0
        assert deleted == 0
        assert not mock_conn.called

    @patch("src.application.services.sync.smart_sync.db_manager.get_connection")
    def test_sync_full_replace_with_metadata(self, mock_conn, target):
        conn = self._setup_db(":memory:")
        mock_conn.return_value.__enter__.return_value = conn

        # Sostituiamo tutto, ma manteniamo la nota
        new_data = [("1", "NEW_A"), ("3", "NEW_C")]

        added, removed = SmartSyncEngine.sync_full_replace_with_metadata(
            target, new_data, key_cols=["id"], metadata_cols=["note"]
        )

        assert added == 2
        assert removed == 0

        cursor = conn.cursor()
        cursor.execute("SELECT id, val, note FROM my_table ORDER BY id")
        res = cursor.fetchall()
        assert res == [("1", "NEW_A", "n1"), ("3", "NEW_C", "")]
