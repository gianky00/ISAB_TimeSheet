import sqlite3

import pytest

from src.application.services.database.migrations.timbrature import (
    mig_timbrature_v1,
    mig_timbrature_v2,
    mig_timbrature_v3,
    mig_timbrature_v4,
)


class TestTimbratureMigrations:
    @pytest.fixture
    def conn(self):
        conn = sqlite3.connect(":memory:")
        yield conn
        conn.close()

    def test_full_migration_chain(self, conn):
        mig_timbrature_v1(conn)
        mig_timbrature_v2(conn)
        mig_timbrature_v3(conn)
        mig_timbrature_v4(conn)

        cursor = conn.cursor()

        # Verifica tabelle
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cursor.fetchall()]
        assert "timbrature" in tables
        assert "dipendenti" in tables

        # Verifica colonne aggiunte in v3 e v4
        cursor.execute("PRAGMA table_info(timbrature)")
        cols = [r[1] for r in cursor.fetchall()]
        assert "codice_fiscale" in cols
        assert "id_dipendente" in cols
        assert "numero_badge" in cols

        # Verifica indici
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indices = [r[0] for r in cursor.fetchall()]
        assert "idx_timb_cf" in indices

    def test_mig_v3_v4_idempotent(self, conn):
        mig_timbrature_v1(conn)
        # Esegui due volte
        mig_timbrature_v3(conn)
        mig_timbrature_v3(conn)
        mig_timbrature_v4(conn)
        mig_timbrature_v4(conn)

        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(timbrature)")
        cols = [r[1] for r in cursor.fetchall()]
        assert cols.count("codice_fiscale") == 1
        assert cols.count("id_dipendente") == 1
