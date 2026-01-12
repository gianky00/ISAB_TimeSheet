import sqlite3
from unittest.mock import patch

import pytest

from src.core.database import DatabaseManager


class TestDatabaseCoverage:
    """
    Test suite per src/core/database.py.
    Utilizza database temporanei su file per evitare collisioni col DB reale.
    """

    @pytest.fixture(autouse=True)
    def setup_database(self, tmp_path):
        """Setup e Teardown automatico per ogni test."""
        # Crea path temporanei per i DB
        self.temp_dir = tmp_path / "data"
        self.temp_dir.mkdir()

        self.db_contabilita = self.temp_dir / "test_contabilita.db"
        self.db_timbrature = self.temp_dir / "test_timbrature.db"

        # Patch delle costanti nel DatabaseManager
        # Dato che è un Singleton, dobbiamo stare attenti.
        # Patchiamo le proprietà dell'istanza.
        self.db_manager = DatabaseManager()

        # Salviamo i valori originali
        self.orig_cont = self.db_manager.DB_CONTABILITA
        self.orig_timb = self.db_manager.DB_TIMBRATURE

        # Sovrascriviamo
        self.db_manager.DB_CONTABILITA = self.db_contabilita
        self.db_manager.DB_TIMBRATURE = self.db_timbrature

        # Inizializza i DB (crea tabelle)
        self.db_manager.init_db()

        yield

        # Ripristino
        self.db_manager.DB_CONTABILITA = self.orig_cont
        self.db_manager.DB_TIMBRATURE = self.orig_timb

    def test_singleton(self):
        """Verifica che DatabaseManager sia un Singleton."""
        db1 = DatabaseManager()
        db2 = DatabaseManager()
        assert db1 is db2

    def test_init_creates_tables_contabilita(self):
        """Verifica che init_db crei le tabelle di contabilità."""
        # Controlliamo se la tabella 'contabilita' esiste
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='contabilita';"
        res = self.db_manager.execute_query(self.db_contabilita, query)
        assert len(res) == 1
        assert res[0][0] == 'contabilita'

        # Verifica versione DB
        with self.db_manager.get_connection(self.db_contabilita) as conn:
            ver = self.db_manager._get_db_version(conn)
            assert ver == 3 # Ci sono 3 migrazioni

    def test_init_creates_tables_timbrature(self):
        """Verifica che init_db crei le tabelle di timbrature."""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='timbrature';"
        res = self.db_manager.execute_query(self.db_timbrature, query)
        assert len(res) == 1

        with self.db_manager.get_connection(self.db_timbrature) as conn:
            ver = self.db_manager._get_db_version(conn)
            assert ver == 2 # Ci sono 2 migrazioni

    def test_execute_query_insert_select(self):
        """Testa inserimento e selezione dati."""
        # Insert
        insert_sql = "INSERT INTO contabilita (year, n_prev) VALUES (?, ?)"
        self.db_manager.execute_query(self.db_contabilita, insert_sql, (2024, "P-001"))

        # Select
        select_sql = "SELECT year, n_prev FROM contabilita WHERE n_prev = ?"
        rows = self.db_manager.execute_query(self.db_contabilita, select_sql, ("P-001",))

        assert len(rows) == 1
        assert rows[0][0] == 2024
        assert rows[0][1] == "P-001"

    def test_write_lock_concurrency_simulation(self):
        """Simula uso del lock (basic check)."""
        # Verifica che possiamo scrivere senza errori
        # Il lock è interno, difficile testare la concorrenza reale in unit test veloce,
        # ma verifichiamo che non blocchi il thread corrente.
        self.db_manager.execute_query(self.db_contabilita, "INSERT INTO contabilita (year) VALUES (2025)")
        res = self.db_manager.execute_query(self.db_contabilita, "SELECT year FROM contabilita WHERE year=2025")
        assert len(res) == 1

    def test_operational_error_retry(self):
        """Verifica che il retry system intercetti errori di lock (mocked)."""
        with patch.object(sqlite3.Cursor, 'execute', side_effect=sqlite3.OperationalError("database is locked")) as mock_exec:
            with pytest.raises(sqlite3.OperationalError) as excinfo:
                self.db_manager.execute_query(self.db_contabilita, "SELECT * FROM contabilita", retry_count=2)

            assert "locked" in str(excinfo.value)
            # Deve aver riprovato retry_count volte (range(2) -> 0, 1)
            assert mock_exec.call_count == 2

    def test_migrations_logic(self):
        """Testa logica migrazioni manuale."""
        # Creiamo un DB vuoto e forziamo versione 0
        tmp_db = self.temp_dir / "migration_test.db"

        # Definizione migrazione fake
        def mig_v1(conn):
            conn.execute("CREATE TABLE test (id INT)")

        migrations = {1: mig_v1}

        self.db_manager._run_migrations(tmp_db, migrations, "TestDB")

        # Verifica
        with self.db_manager.get_connection(tmp_db) as conn:
            ver = self.db_manager._get_db_version(conn)
            assert ver == 1
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test'")
            assert cursor.fetchone() is not None

