"""
Hardened tests for DatabaseManager.
Verifies thread safety, WAL mode, and migration logic.
"""

import sqlite3
import time
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
        """Verifica che execute_query usi il lock per le scritture."""
        # Creiamo la tabella
        manager.execute_query(db_path, "CREATE TABLE test (val TEXT)")

        # Simula una scrittura lenta per testare il lock (patchando _write_lock)
        with patch.object(manager, "_write_lock") as mock_lock:
            manager.execute_query(db_path, "INSERT INTO test VALUES ('a')")
            assert mock_lock.acquire.called
            assert mock_lock.release.called

    def test_retry_logic_on_locked(self, manager, db_path):
        """Verifica che il manager riprovi se il database è occupato."""
        # 1. Blocca il DB con una connessione esterna
        conn_ext = sqlite3.connect(db_path)
        conn_ext.execute("CREATE TABLE test (id INTEGER)")
        conn_ext.execute("BEGIN EXCLUSIVE TRANSACTION")

        # 2. Tenta di scrivere tramite manager
        # Usiamo un timeout brevissimo per get_connection altrimenti attende 30s per ogni tentativo
        original_get_conn = manager.get_connection
        
        def mock_get_conn(path, read_only=False, timeout=0.1):
            return original_get_conn(path, read_only=read_only, timeout=timeout)

        with patch.object(manager, "get_connection", side_effect=mock_get_conn):
            start_time = time.time()
            with pytest.raises(sqlite3.OperationalError):
                manager.execute_query(db_path, "INSERT INTO test VALUES (1)", retry_count=2)
            end_time = time.time()

            # Verifica che abbia fatto i retry (almeno due tentativi con sleep crescenti)
            # Tentativo 0: fail -> sleep 0.1
            # Tentativo 1: fail -> sleep 0.2
            # Totale attesa minima ~0.3s
            assert end_time - start_time >= 0.3

        conn_ext.rollback()
        conn_ext.close()

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
