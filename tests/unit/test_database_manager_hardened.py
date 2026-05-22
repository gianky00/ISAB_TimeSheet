"""Hardened tests for DatabaseManager.
Verifies thread safety, WAL mode, and migration logic.
"""

import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from src.core.database.manager import DatabaseManager


class TestDatabaseManagerHardened:
    @pytest.fixture
    def db_path(self, tmp_path):
        return tmp_path / "test.db"

    @pytest.fixture
    def manager(self):
        # Reset singleton state if possible or just use the global one but with tmp paths
        DatabaseManager._instance = None
        return DatabaseManager()

    def test_wal_mode_enabled(self, manager, db_path):
        """Verifica che la connessione attivi la modalità WAL."""
        with manager.get_connection(db_path) as conn:
            mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
            assert mode.lower() == "wal"

    def test_write_serialization(self, manager, db_path):
        """Verifica che get_write_connection usi il lock per le scritture."""
        # Simula l'acquisizione del lock
        with patch.object(manager, "_write_lock") as mock_lock:
            with manager.get_write_connection(db_path) as conn:
                conn.execute("CREATE TABLE test (val TEXT)")
            assert mock_lock.__enter__.called
            assert mock_lock.__exit__.called

    def test_retry_logic_on_locked(self, manager, db_path):
        """Verifica che il manager riprovi se il database è occupato."""
        # Patchiamo get_connection in modo che sollevi OperationalError
        with patch.object(
            manager, "get_connection", side_effect=sqlite3.OperationalError("database is locked")
        ):
            # Patchiamo anche sleep per non aspettare davvero
            with patch("src.core.database.manager.time.sleep") as mock_sleep:
                with pytest.raises(sqlite3.OperationalError):
                    manager.execute_query(db_path, "INSERT INTO test VALUES (1)", retry_count=2)

                # Deve aver dormito 2 volte (i=0 e i=1)
                assert mock_sleep.call_count == 2

    def test_migration_sequence(self, manager, db_path):
        """Verifica l'esecuzione sequenziale delle migrazioni."""
        # Mock delle funzioni di migrazione
        m1 = MagicMock()
        m2 = MagicMock()
        migrations = {1: m1, 2: m2}

        # Esegui migrazione
        manager._run_migrations(db_path, migrations, "TestDB")

        assert m1.called
        assert m2.called

        # Verifica versione nel DB
        with manager.get_connection(db_path) as conn:
            ver = conn.execute("PRAGMA user_version").fetchone()[0]
            assert ver == 2

    def test_migration_skips_if_up_to_date(self, manager, db_path):
        """Verifica che le migrazioni già fatte non vengano rieseguite."""
        # Setup versione a 1
        with manager.get_connection(db_path) as conn:
            conn.execute("PRAGMA user_version = 1")

        m1 = MagicMock()
        m2 = MagicMock()
        migrations = {1: m1, 2: m2}

        manager._run_migrations(db_path, migrations, "TestDB")

        assert not m1.called  # Gia' a v1
        assert m2.called  # Manca v2
