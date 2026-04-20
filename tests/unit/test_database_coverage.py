import sqlite3
from unittest.mock import patch

import pytest

from src.core.database import DatabaseManager


class TestDatabaseManager:
    @pytest.fixture
    def manager(self, tmp_path, mocker):
        # Mock DB_DIR in src.core.database.manager to use tmp_path
        mocker.patch("src.core.database.manager.DB_DIR", tmp_path)

        # Reset singleton
        DatabaseManager._instance = None
        mgr = DatabaseManager()
        yield mgr
        DatabaseManager._instance = None

    def test_init_db_and_migrations(self, manager):
        """Verifica che init_db crei le tabelle tramite il sistema di migrazione."""
        manager.init_db()

        # Verify tables in contabilita.db
        with manager.get_connection(manager.DB_CONTABILITA) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cursor.fetchall()]
            assert "contabilita" in tables
            assert "giornaliere" in tables

    def test_execute_query_select(self, manager):
        """Verifica esecuzione query SELECT."""
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

    def test_execute_query_retry_on_busy(self, manager):
        """Verifica logica di retry in caso di DB locked."""
        manager.init_db()

        # Simuliamo un fallimento temporaneo
        # Nota: usiamo un helper per la connessione reale
        real_conn = sqlite3.connect(manager.DB_CONTABILITA)

        with patch(
            "src.core.database.manager.sqlite3.connect",
            side_effect=[
                sqlite3.OperationalError("database is locked"),
                real_conn,
            ],
        ):
            res = manager.execute_query(manager.DB_CONTABILITA, "SELECT 1")
            assert res == [(1,)]

    def test_connection_error_rollback(self, manager):
        """Verifica rollback in caso di errore durante la transazione."""
        # SQLite autocommits DDL, quindi testiamo con DML
        with manager.get_connection(manager.DB_CONTABILITA) as conn:
            conn.execute("CREATE TABLE test_rollback (id INT)")

        with pytest.raises(sqlite3.OperationalError):
            with manager.get_connection(manager.DB_CONTABILITA) as conn:
                conn.execute("INSERT INTO test_rollback VALUES (1)")
                conn.execute("INVALID SQL")  # Fallimento qui

        # La riga non deve essere presente (rollback)
        res = manager.execute_query(manager.DB_CONTABILITA, "SELECT * FROM test_rollback")
        assert len(res) == 0
