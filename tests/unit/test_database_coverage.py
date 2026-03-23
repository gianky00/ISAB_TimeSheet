import sqlite3
from unittest.mock import patch

import pytest

from src.core.database import DatabaseManager


class TestDatabaseManager:
    @pytest.fixture
    def manager(self, tmp_path, mocker):  # noqa: ANN001
        # Mock class-level DB paths to use tmp_path
        mocker.patch(
            "src.core.database.DatabaseManager.DB_CONTABILITA",
            tmp_path / "contabilita.db",
        )
        mocker.patch(
            "src.core.database.DatabaseManager.DB_TIMBRATURE",
            tmp_path / "timbrature.db",
        )
        mocker.patch("src.core.database.manager.CONFIG_DIR", tmp_path)

        # Reset singleton
        DatabaseManager._instance = None
        return DatabaseManager()

    def test_init_db_and_migrations(self, manager):  # noqa: ANN001
        # Mock migration dicts if they exist in the class (checked in code)
        # Actually, let's just run it and see if it creates the tables.
        manager.init_db()

        # Verify tables in contabilita.db
        with manager.get_connection(manager.DB_CONTABILITA) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cursor.fetchall()]
            assert "contabilita" in tables
            assert "giornaliere" in tables

    def test_execute_query_select(self, manager):  # noqa: ANN001
        manager.init_db()
        # Insert test data
        manager.execute_query(
            manager.DB_CONTABILITA,
            "INSERT INTO contabilita (year, attivita) VALUES (?, ?)",
            (2026, "Test"),
        )

        res = manager.execute_query(manager.DB_CONTABILITA, "SELECT attivita FROM contabilita")
        assert len(res) == 1
        assert res[0][0] == "Test"

    def test_execute_query_retry_on_busy(self, manager):  # noqa: ANN001
        manager.init_db()
        # Mock sqlite3.connect to raise busy error first then succeed
        with patch(
            "sqlite3.connect",
            side_effect=[
                sqlite3.OperationalError("database is locked"),
                sqlite3.connect(f"file:{manager.DB_CONTABILITA.absolute()}?mode=rw", uri=True),
            ],
        ):
            res = manager.execute_query(manager.DB_CONTABILITA, "SELECT 1")
            assert res == [(1,)]

    def test_connection_error_rollback(self, manager):  # noqa: ANN001
        with pytest.raises(sqlite3.OperationalError):
            with manager.get_connection(manager.DB_CONTABILITA) as conn:
                conn.execute("CREATE TABLE test (id INT)")
                # Force an error
                conn.execute("INVALID SQL")

        # Verify table was NOT created (or rolled back if it was in transaction)
        # SQLite autocommits DDL, so let's test with DML
        with manager.get_connection(manager.DB_CONTABILITA) as conn:
            conn.execute("CREATE TABLE test2 (id INT)")

        with pytest.raises(sqlite3.OperationalError):
            with manager.get_connection(manager.DB_CONTABILITA) as conn:
                conn.execute("INSERT INTO test2 VALUES (1)")
                conn.execute("INVALID SQL")

        res = manager.execute_query(manager.DB_CONTABILITA, "SELECT * FROM test2")
        assert len(res) == 0
