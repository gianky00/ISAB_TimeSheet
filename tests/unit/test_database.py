import sqlite3
from unittest.mock import patch

import pytest

from src.core.database import DatabaseManager


class TestDatabaseManager:
    @pytest.fixture
    def db_path(self, tmp_path):
        return tmp_path / "test.db"

    @pytest.fixture
    def manager(self):
        # Reset singleton logic?
        # Actually DatabaseManager is a singleton, so we need to be careful.
        # But we can create a fresh instance by bypassing __new__ logic or just
        # testing the methods on a specific path.
        return DatabaseManager()

    def test_singleton(self):
        m1 = DatabaseManager()
        m2 = DatabaseManager()
        assert m1 is m2

    def test_init_db(self, manager, tmp_path):
        # Patch DB_DIR nel modulo manager per usare tmp_path
        with patch("src.core.database.manager.DB_DIR", tmp_path):
            test_db_cont = manager.DB_CONTABILITA
            test_db_timb = manager.DB_TIMBRATURE

            manager.init_db()
            assert test_db_cont.exists()
            assert test_db_timb.exists()

            # Verify schema
            with sqlite3.connect(test_db_cont) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                assert "contabilita" in tables
                assert "giornaliere" in tables
                assert "scarico_ore" in tables

    def test_execute_query(self, manager, db_path):
        # Create table
        manager.execute_query(db_path, "CREATE TABLE test (id INTEGER PRIMARY KEY, val TEXT)")

        # Insert
        manager.execute_query(db_path, "INSERT INTO test (val) VALUES (?)", ("foo",))

        # Select
        rows = manager.execute_query(db_path, "SELECT * FROM test")
        assert len(rows) == 1
        assert rows[0][1] == "foo"
