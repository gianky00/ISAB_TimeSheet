import sqlite3

import pytest

from src.core.database.migrations.pdl import mig_pdl_v1, mig_pdl_v2, mig_pdl_v3, mig_pdl_v4, mig_pdl_v5


class TestPdlMigrations:
    @pytest.fixture
    def conn(self):
        conn = sqlite3.connect(":memory:")
        yield conn
        conn.close()

    def test_full_migration_chain(self, conn):
        mig_pdl_v1(conn)
        mig_pdl_v2(conn)
        mig_pdl_v3(conn)
        mig_pdl_v4(conn)
        mig_pdl_v5(conn)

        cursor = conn.cursor()

        # Verifica pdl
        cursor.execute("PRAGMA table_info(pdl)")
        cols = [r[1] for r in cursor.fetchall()]
        assert "n_pdl" in cols

        # Verifica programmazione
        cursor.execute("PRAGMA table_info(pdl_programmazione)")
        prog_cols = [r[1] for r in cursor.fetchall()]
        assert "settimana_start" in prog_cols
        assert "unita" in prog_cols

    def test_mig_v2_uniqueness_and_cleanup(self, conn):
        mig_pdl_v1(conn)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pdl (n_pdl, area) VALUES ('123', 'A'), ('123', 'B'), ('456', 'C')")
        conn.commit()

        mig_pdl_v2(conn)

        cursor.execute("SELECT count(*) FROM pdl")
        assert cursor.fetchone()[0] == 2

        # Verifica vincolo UNIQUE
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO pdl (n_pdl) VALUES ('456')")

    def test_mig_v4_v5_idempotent(self, conn):
        mig_pdl_v3(conn)
        # Esegui due volte
        mig_pdl_v4(conn)
        mig_pdl_v4(conn)
        mig_pdl_v5(conn)
        mig_pdl_v5(conn)

        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(pdl_programmazione)")
        cols = [r[1] for r in cursor.fetchall()]
        assert cols.count("settimana_start") == 1
        assert cols.count("unita") == 1
