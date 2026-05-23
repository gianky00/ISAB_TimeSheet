import sqlite3

import pytest

from src.core.database.migrations.storico_oda import mig_storico_oda_v1, mig_storico_oda_v2


class TestOdaMigrations:
    @pytest.fixture
    def conn(self):
        conn = sqlite3.connect(":memory:")
        yield conn
        conn.close()

    def test_full_migration_chain(self, conn):
        mig_storico_oda_v1(conn)
        mig_storico_oda_v2(conn)

        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(storico_oda)")
        cols = [r[1] for r in cursor.fetchall()]

        assert "oda" in cols
        assert "valore_netto_oda" in cols

        # Verifica indici
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indices = [r[0] for r in cursor.fetchall()]
        assert "idx_oda_data_oda" in indices

    def test_mig_v2_recreates(self, conn):
        mig_storico_oda_v1(conn)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO storico_oda (oda, pos_oda, num_riga) VALUES ('1', '10', '1')")
        conn.commit()

        mig_storico_oda_v2(conn)

        # Deve essere vuota dopo DROP + CREATE
        cursor.execute("SELECT count(*) FROM storico_oda")
        assert cursor.fetchone()[0] == 0
