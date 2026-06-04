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
from src.application.services.database.migrations.dipendenti import (
    mig_dipendenti_v1,
    mig_dipendenti_v2,
    mig_dipendenti_v3,
)
from src.application.services.database.migrations.pdl import (
    mig_pdl_v1,
    mig_pdl_v2,
    mig_pdl_v3,
    mig_pdl_v4,
    mig_pdl_v5,
)
from src.application.services.database.migrations.storico_oda import mig_storico_oda_v1, mig_storico_oda_v2
from src.application.services.database.migrations.timbrature import (
    mig_timbrature_v1,
    mig_timbrature_v2,
    mig_timbrature_v3,
    mig_timbrature_v4,
)


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    yield connection
    connection.close()


def test_dipendenti_migrations(conn):
    mig_dipendenti_v1(conn)
    mig_dipendenti_v2(conn)
    # Call v3 twice to hit the condition where column already exists
    mig_dipendenti_v3(conn)
    mig_dipendenti_v3(conn)

    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(dipendenti)")
    cols = [r[1] for r in cursor.fetchall()]
    assert "codice_fiscale" in cols
    assert "monitoraggio_attivo" in cols


def test_pdl_migrations(conn):
    mig_pdl_v1(conn)
    mig_pdl_v2(conn)
    mig_pdl_v3(conn)
    mig_pdl_v4(conn)
    mig_pdl_v5(conn)

    # Hit suppress blocks
    mig_pdl_v4(conn)
    mig_pdl_v5(conn)

    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(pdl)")
    cols = [r[1] for r in cursor.fetchall()]
    assert "n_pdl" in cols

    cursor.execute("PRAGMA table_info(pdl_programmazione)")
    prog_cols = [r[1] for r in cursor.fetchall()]
    assert "settimana_start" in prog_cols
    assert "unita" in prog_cols


def test_timbrature_migrations(conn):
    mig_timbrature_v1(conn)
    mig_timbrature_v2(conn)
    mig_timbrature_v3(conn)
    # Second time for v3
    mig_timbrature_v3(conn)

    mig_timbrature_v4(conn)
    # Second time for v4
    mig_timbrature_v4(conn)

    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(timbrature)")
    cols = [r[1] for r in cursor.fetchall()]
    assert "codice_fiscale" in cols
    assert "ore_effettive" in cols
    assert "id_dipendente" in cols


def test_storico_oda_migrations(conn):
    mig_storico_oda_v1(conn)
    mig_storico_oda_v2(conn)

    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(storico_oda)")
    cols = [r[1] for r in cursor.fetchall()]
    assert "oda" in cols


def test_contabilita_migrations(conn):
    mig_contabilita_v1(conn)
    mig_contabilita_v2(conn)

    # Needs dummy data to test triggers
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contabilita (year, n_prev) VALUES (2026, '1')")

    mig_contabilita_v3(conn)

    cursor.execute("INSERT INTO certificati_campione (matricola, certificato) VALUES ('1', '1')")
    cursor.execute("INSERT INTO certificati_campione (matricola, certificato) VALUES ('1', '1')")

    mig_contabilita_v4(conn)
    mig_contabilita_v5(conn)
    # Call v5 again to test suppress
    mig_contabilita_v5(conn)

    mig_contabilita_v6(conn)

    mig_contabilita_v7(conn)

    cursor.execute("PRAGMA table_info(certificati_campione)")
    cols = [r[1] for r in cursor.fetchall()]
    assert "annotazioni" in cols
    assert "ubicazione" in cols
