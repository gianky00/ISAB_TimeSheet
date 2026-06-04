import sqlite3

import pytest

from src.application.services.database.migrations.contabilita import (
    mig_contabilita_v1,
    mig_contabilita_v2,
    mig_contabilita_v3,
    mig_contabilita_v4,
    mig_contabilita_v5,
    mig_contabilita_v6,
    mig_contabilita_v7,
)


class TestContabilitaMigrations:
    @pytest.fixture
    def conn(self):
        conn = sqlite3.connect(":memory:")
        yield conn
        conn.close()

    def test_full_migration_chain(self, conn):
        # Eseguiamo tutta la catena e verifichiamo la struttura finale
        mig_contabilita_v1(conn)
        mig_contabilita_v2(conn)
        mig_contabilita_v3(conn)
        mig_contabilita_v4(conn)
        mig_contabilita_v5(conn)
        mig_contabilita_v6(conn)
        mig_contabilita_v7(conn)

        cursor = conn.cursor()

        # Verifica tabelle principali
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cursor.fetchall()]
        assert "contabilita" in tables
        assert "giornaliere" in tables
        assert "certificati_campione" in tables
        assert "contabilita_fts" in tables

        # Verifica ridenominazione v7
        cursor.execute("PRAGMA table_info(certificati_campione)")
        cols = [r[1] for r in cursor.fetchall()]
        assert "id_coemi" in cols
        assert "id_strumento" not in cols
        assert "annotazioni" in cols
        assert "ubicazione" in cols

    def test_mig_v4_cleanup(self, conn):
        mig_contabilita_v1(conn)
        cursor = conn.cursor()
        # Inseriamo duplicati (matricola + certificato)
        cursor.execute(
            "INSERT INTO certificati_campione (matricola, certificato) VALUES ('M1', 'C1'), ('M1', 'C1'), ('M2', 'C2')"
        )
        conn.commit()

        mig_contabilita_v4(conn)

        cursor.execute("SELECT count(*) FROM certificati_campione")
        assert cursor.fetchone()[0] == 2

    def test_mig_v7_legacy_handling(self, conn):
        # Setup tabella manuale con vecchi nomi per testare v7 isolatamente
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE certificati_campione (id_strumento TEXT, range TEXT, errore TEXT)")

        mig_contabilita_v7(conn)

        cursor.execute("PRAGMA table_info(certificati_campione)")
        cols = [r[1] for r in cursor.fetchall()]
        assert "id_coemi" in cols
        assert "range_strumento" in cols
        assert "errore_max" in cols
