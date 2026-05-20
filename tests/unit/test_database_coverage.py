import sqlite3
from unittest.mock import patch

import pytest

from src.core.database import DatabaseManager


class TestDatabaseManager:
    @pytest.fixture
    def manager(self, tmp_path):
        # Reset singleton
        DatabaseManager._instance = None
        mgr = DatabaseManager()

        # Override class variables dynamically to point to tmp_path
        mgr.DB_CONTABILITA = tmp_path / "contabilita.db"
        mgr.DB_TIMBRATURE = tmp_path / "timbrature.db"
        mgr.DB_PDL = tmp_path / "pdl.db"
        mgr.DB_STORICO_ODA = tmp_path / "storico_oda.db"
        mgr.DB_DIPENDENTI = tmp_path / "dipendenti.db"
        mgr.DB_CERTIFICATI = tmp_path / "certificati.db"
        mgr.DB_SCARICO_ORE = tmp_path / "scarico_ore.db"
        mgr.DB_GIORNALIERE = tmp_path / "giornaliere.db"
        mgr.DB_AUDIT = tmp_path / "audit_log.db"

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
        # Insert test data using get_connection so it commits
        with manager.get_connection(manager.DB_CONTABILITA) as conn:
            conn.execute(
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
        real_conn.row_factory = sqlite3.Row

        with patch(
            "src.core.database.manager.sqlite3.connect",
            side_effect=[
                sqlite3.OperationalError("database is locked"),
                real_conn,
            ],
        ):
            res = manager.execute_query(manager.DB_CONTABILITA, "SELECT 1")
            assert res[0][0] == 1

    def test_connection_error_rollback(self, manager):
        """Verifica rollback in caso di errore durante la transazione."""
        manager.init_db()
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
