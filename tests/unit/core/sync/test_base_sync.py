import sqlite3

import pytest

from src.application.services.exceptions import ValidationError
from src.application.services.sync.base import BaseSyncEngine, PartitionConfig


class TestBaseSyncEngine:
    def test_validate_identifier_valid(self):
        assert BaseSyncEngine._validate_identifier("table_name") == "table_name"
        assert BaseSyncEngine._validate_identifier("col_123") == "col_123"

    def test_validate_identifier_invalid(self):
        with pytest.raises(ValidationError):
            BaseSyncEngine._validate_identifier("table; DROP TABLE users")
        with pytest.raises(ValidationError):
            BaseSyncEngine._validate_identifier("col-name")
        with pytest.raises(ValidationError):
            BaseSyncEngine._validate_identifier("col name")

    def test_clean_value(self):
        assert BaseSyncEngine._clean_value(" test ") == "test"
        assert BaseSyncEngine._clean_value(None) == ""
        assert BaseSyncEngine._clean_value(123) == "123"
        assert BaseSyncEngine._clean_value(12.5) == "12.5"

    def test_create_temp_table(self):
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        temp_name = BaseSyncEngine._create_temp_table(cursor, "my_table", ["col1", "col2"])
        assert temp_name == "temp_my_table"

        # Verify table exists and has correct columns
        cursor.execute(f"PRAGMA table_info({temp_name})")
        cols = cursor.fetchall()
        assert len(cols) == 2
        assert cols[0][1] == "col1"
        assert cols[1][1] == "col2"

    def test_sync_partitioned_data(self):
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        # Setup initial table
        cursor.execute("CREATE TABLE my_table (id TEXT, val TEXT, year TEXT)")
        cursor.executemany(
            "INSERT INTO my_table VALUES (?, ?, ?)",
            [
                ("1", "A", "2023"),
                ("2", "B", "2023"),
                ("3", "C", "2024"),  # This should be untouched if partition is 2023
            ],
        )

        # New data for 2023:
        # "1" unchanged (in terms of str rep)
        # "2" is missing (should be removed)
        # "4" is new (should be added)
        # "5" is new (should be added)
        new_data = [("1", "A", "2023"), ("4", "D", "2023"), ("5", "E", "2023")]

        partition = PartitionConfig(column="year", values=["2023"])
        added, removed = BaseSyncEngine.sync_partitioned_data(
            cursor, "my_table", ["id", "val", "year"], new_data, partition
        )

        assert added == 2
        assert removed == 1

        # Verify final state
        cursor.execute("SELECT id FROM my_table ORDER BY id")
        final_ids = [r[0] for r in cursor.fetchall()]
        assert final_ids == ["1", "3", "4", "5"]
