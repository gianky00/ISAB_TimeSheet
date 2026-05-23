import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from src.core.database.manager import DatabaseManager


class TestDatabaseManager:
    @pytest.fixture(autouse=True)
    def setup_db(self, tmp_path):
        DatabaseManager._instance = None
        self.db_path = tmp_path / "test.db"
        self.manager = DatabaseManager()

    def test_get_connection_wal_mode(self):
        with self.manager.get_connection(self.db_path) as conn:
            # Verifica WAL mode
            res = conn.execute("PRAGMA journal_mode").fetchone()
            assert res[0].lower() == "wal"
            # Verifica FK
            res = conn.execute("PRAGMA foreign_keys").fetchone()
            assert res[0] == 1

    def test_get_connection_read_only(self):
        # Crea il DB prima
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE t (id INT)")

        with self.manager.get_connection(self.db_path, read_only=True) as conn:
            with pytest.raises(sqlite3.OperationalError):
                conn.execute("INSERT INTO t VALUES (1)")

    def test_get_write_connection_lock(self):
        with self.manager.get_write_connection(self.db_path) as conn:
            assert DatabaseManager._write_lock.locked()
            conn.execute("CREATE TABLE t (id INT)")
        assert not DatabaseManager._write_lock.locked()

    def test_execute_query_success(self):
        with self.manager.get_connection(self.db_path) as conn:
            conn.execute("CREATE TABLE t (id INT, val TEXT)")
            conn.execute("INSERT INTO t VALUES (1, 'A'), (2, 'B')")

        rows = self.manager.execute_query(self.db_path, "SELECT * FROM t WHERE id = ?", (1,))
        assert len(rows) == 1
        assert rows[0]["val"] == "A"

    def test_execute_query_retry_on_locked(self):
        # Simula blocco DB
        with patch("src.core.database.manager.sqlite3.connect") as mock_conn:
            mock_conn.side_effect = [
                sqlite3.OperationalError("database is locked"),
                sqlite3.OperationalError("database is locked"),
                MagicMock(),  # Terzo tentativo ok
            ]

            # Setup mock cursor for the 3rd attempt
            mock_cursor = mock_conn.return_value.execute.return_value
            mock_cursor.fetchall.return_value = []

            # Ridurre sleep per velocità test
            with patch("src.core.database.manager.time.sleep"):
                self.manager.execute_query(self.db_path, "SELECT 1")

            assert mock_conn.call_count == 3

    def test_migrations_logic(self):
        # Setup finto dizionario migrazioni
        mock_mig = MagicMock()
        migrations = {1: mock_mig}

        # Esegui migrazione
        self.manager._run_migrations(self.db_path, migrations, "TestDB")

        assert mock_mig.called
        # Verifica versione salvata
        with self.manager.get_connection(self.db_path) as conn:
            assert self.manager._get_db_version(conn) == 1

        # Seconda esecuzione non deve chiamare migrazioni già fatte
        mock_mig.reset_mock()
        self.manager._run_migrations(self.db_path, migrations, "TestDB")
        assert not mock_mig.called

    def test_db_version_helpers(self):
        with self.manager.get_connection(self.db_path) as conn:
            self.manager._set_db_version(conn, 5)
            assert self.manager._get_db_version(conn) == 5
