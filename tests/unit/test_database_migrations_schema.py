import sqlite3

import pytest

from src.core.database.migrations.contabilita import (
    mig_contabilita_v1,
    mig_contabilita_v2,
    mig_contabilita_v3,
)


class TestDatabaseMigrations:
    @pytest.fixture
    def db_conn(self):
        conn = sqlite3.connect(":memory:")
        yield conn
        conn.close()

    def test_migration_v1_tables(self, db_conn):  # noqa: ANN001
        mig_contabilita_v1(db_conn)

        cursor = db_conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cursor.fetchall()]

        expected = [
            "contabilita",
            "giornaliere",
            "scarico_ore",
            "attivita_programmate",
            "certificati_campione",
        ]
        for t in expected:
            assert t in tables

    def test_migration_v2_indexes(self, db_conn):  # noqa: ANN001
        mig_contabilita_v1(db_conn)
        mig_contabilita_v2(db_conn)

        cursor = db_conn.cursor()
        cursor.execute("PRAGMA index_list('contabilita')")
        indexes = [r[1] for r in cursor.fetchall()]

        assert "idx_cont_n_prev" in indexes
        assert "idx_cont_odc" in indexes

    def test_migration_v3_fts(self, db_conn):  # noqa: ANN001
        mig_contabilita_v1(db_conn)
        mig_contabilita_v3(db_conn)

        # Check FTS table
        cursor = db_conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contabilita_fts'")
        assert cursor.fetchone() is not None

        # Check Triggers
        cursor.execute(
            "INSERT INTO contabilita (n_prev, attivita, odc, year) VALUES ('P1', 'Att1', 'ODC1', 2024)"
        )
        db_conn.commit()

        # Verify FTS is populated via trigger
        cursor.execute("SELECT * FROM contabilita_fts WHERE contabilita_fts MATCH 'Att1'")
        assert cursor.fetchone() is not None

    def test_basic_crud_operations(self, db_conn):  # noqa: ANN001
        mig_contabilita_v1(db_conn)
        cursor = db_conn.cursor()

        # INSERT
        cursor.execute("INSERT INTO giornaliere (year, data, personale) VALUES (2024, '2024-01-01', 'Mario')")
        last_id = cursor.lastrowid
        assert last_id == 1

        # SELECT
        cursor.execute("SELECT personale FROM giornaliere WHERE id=?", (last_id,))
        assert cursor.fetchone()[0] == "Mario"

        # UPDATE
        cursor.execute("UPDATE giornaliere SET personale='Luigi' WHERE id=?", (last_id,))
        cursor.execute("SELECT personale FROM giornaliere WHERE id=?", (last_id,))
        assert cursor.fetchone()[0] == "Luigi"

        # DELETE
        cursor.execute("DELETE FROM giornaliere WHERE id=?", (last_id,))
        cursor.execute("SELECT count(*) FROM giornaliere")
        assert cursor.fetchone()[0] == 0
