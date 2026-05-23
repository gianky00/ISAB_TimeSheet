import sqlite3

import pytest

from src.core.database.migrations.dipendenti import mig_dipendenti_v1, mig_dipendenti_v2, mig_dipendenti_v3


class TestDipendentiMigrations:
    @pytest.fixture
    def conn(self):
        conn = sqlite3.connect(":memory:")
        yield conn
        conn.close()

    def test_full_migration_chain(self, conn):
        mig_dipendenti_v1(conn)
        mig_dipendenti_v2(conn)
        mig_dipendenti_v3(conn)

        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(dipendenti)")
        cols = [r[1] for r in cursor.fetchall()]

        assert "id_risorsa" in cols
        assert "codice_fiscale" in cols
        assert "monitoraggio_attivo" in cols

        # Verifica indici
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indices = [r[0] for r in cursor.fetchall()]
        assert "idx_dip_cf" in indices
        assert "idx_dip_monitoraggio" in indices

    def test_mig_v3_idempotent(self, conn):
        mig_dipendenti_v1(conn)
        # Esegui v3 due volte
        mig_dipendenti_v3(conn)
        mig_dipendenti_v3(conn)

        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(dipendenti)")
        cols = [r[1] for r in cursor.fetchall()]
        assert cols.count("monitoraggio_attivo") == 1
