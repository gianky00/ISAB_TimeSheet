import sqlite3
import threading

import pytest

from src.core.database import DatabaseManager


class TestDatabaseAdvanced:
    @pytest.fixture
    def db_dir(self, tmp_path):
        d = tmp_path / "data"
        d.mkdir()
        return d

    @pytest.fixture
    def manager(self, db_dir, mocker):
        # Override predefined paths for testing
        mocker.patch.object(DatabaseManager, "DB_CONTABILITA", db_dir / "contabilita.db")
        mocker.patch.object(DatabaseManager, "DB_TIMBRATURE", db_dir / "timbrature.db")
        return DatabaseManager()

    def test_wal_mode_and_foreign_keys(self, manager, db_dir):
        """Verifica che la connessione attivi WAL mode e foreign keys."""
        db_path = db_dir / "test_wal.db"
        with manager.get_connection(db_path) as conn:
            # Check WAL
            mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
            assert mode.lower() == "wal"

            # Check Foreign Keys
            fk = conn.execute("PRAGMA foreign_keys").fetchone()[0]
            assert fk == 1

    def test_migration_sequence(self, manager, db_dir):
        """Verifica l'applicazione sequenziale delle migrazioni."""
        db_path = db_dir / "test_mig.db"

        # Definiamo migrazioni dummy per il test
        def m1(conn):
            conn.execute("CREATE TABLE t1 (id INTEGER)")

        def m2(conn):
            conn.execute("ALTER TABLE t1 ADD COLUMN val TEXT")

        test_migrations = {1: m1, 2: m2}

        # Esegui migrazioni
        manager._run_migrations(db_path, test_migrations, "TestDB")

        # Verifica versione finale
        with manager.get_connection(db_path) as conn:
            ver = conn.execute("PRAGMA user_version").fetchone()[0]
            assert ver == 2

            # Verifica struttura
            cols = [row[1] for row in conn.execute("PRAGMA table_info(t1)").fetchall()]
            assert "id" in cols
            assert "val" in cols

    def test_rollback_on_exception(self, manager, db_dir):
        """Verifica che un'eccezione causi il rollback della transazione."""
        db_path = db_dir / "test_rollback.db"

        # Setup table
        with manager.get_connection(db_path) as conn:
            conn.execute("CREATE TABLE test (id INTEGER)")

        try:
            with manager.get_connection(db_path) as conn:
                conn.execute("INSERT INTO test (id) VALUES (1)")

                def _raise():
                    raise ValueError("Forced error")  # noqa: TRY301

                _raise()
        except ValueError:
            pass

        # Verifica che il dato non sia stato inserito
        with manager.get_connection(db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM test").fetchone()[0]
            assert count == 0

    def test_write_lock_concurrency(self, manager, db_dir):
        """Verifica che il write lock funzioni tra thread diversi."""
        db_path = db_dir / "test_lock.db"
        with manager.get_connection(db_path) as conn:
            conn.execute("CREATE TABLE counter (val INTEGER)")
            conn.execute("INSERT INTO counter VALUES (0)")

        def increment_slowly():
            # Questo thread acquisisce il lock, aspetta, e poi scrive
            query = "UPDATE counter SET val = val + 1"
            # execute_query gestisce il lock internamente
            manager.execute_query(db_path, query)

        threads = []
        for _ in range(5):
            t = threading.Thread(target=increment_slowly)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Risultato deve essere 5
        results = manager.execute_query(db_path, "SELECT val FROM counter")
        assert results[0][0] == 5

    def test_fts5_triggers_sync(self, manager, db_dir):
        """Verifica che i trigger mantengano sincronizzato l'indice FTS5."""
        db_path = db_dir / "contabilita.db"
        manager._run_migrations(db_path, manager.MIGRATIONS_CONTABILITA, "Contabilita")

        # Insert
        manager.execute_query(
            db_path,
            "INSERT INTO contabilita (year, n_prev, attivita) VALUES (2024, 'P123', 'Manutenzione Impianti')",
        )

        # Search via FTS
        res = manager.execute_query(
            db_path,
            "SELECT rowid FROM contabilita_fts WHERE contabilita_fts MATCH 'Manutenzione'",
        )
        assert len(res) == 1

        # Update
        manager.execute_query(
            db_path,
            "UPDATE contabilita SET attivita = 'Riparazione' WHERE n_prev = 'P123'",
        )

        # Search old (should be empty)
        res_old = manager.execute_query(
            db_path,
            "SELECT rowid FROM contabilita_fts WHERE contabilita_fts MATCH 'Manutenzione'",
        )
        assert len(res_old) == 0

        # Search new
        res_new = manager.execute_query(
            db_path,
            "SELECT rowid FROM contabilita_fts WHERE contabilita_fts MATCH 'Riparazione'",
        )
        assert len(res_new) == 1

    def test_execute_query_retries_on_lock(self, manager, db_dir, mocker):
        """Verifica che execute_query riprovi in caso di database locked."""
        db_path = db_dir / "test_retry.db"

        # Simula un errore 'database is locked' alla prima chiamata, successo alla seconda
        # Dobbiamo assicurarci che l'eccezione sia sollevata DENTRO il context manager
        # o durante la sua acquisizione. In DatabaseManager.execute_query l'eccezione
        # sqlite3.OperationalError viene catturata se sollevata dal blocco 'with self.get_connection'

        mock_conn = mocker.MagicMock(spec=sqlite3.Connection)

        # La prima esecuzione fallisce, la seconda passa
        mock_conn.execute.side_effect = [
            sqlite3.OperationalError("database is locked"),
            mocker.MagicMock(),  # Successo
        ]

        # Mocking get_connection che è un context manager
        # Usiamo side_effect per restituire lo stesso mock_conn ogni volta che viene chiamato
        mock_get_conn = mocker.patch.object(manager, "get_connection")
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mocker.patch("time.sleep")  # Non aspettare davvero

        # Esecuzione
        manager.execute_query(db_path, "INSERT INTO x VALUES (1)")

        # Verifica: deve aver chiamato get_connection 2 volte a causa del retry
        assert mock_get_conn.call_count == 2
        assert mock_conn.execute.call_count == 2
