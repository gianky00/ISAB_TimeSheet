import sqlite3
from unittest.mock import MagicMock

import pytest

from src.application.services.database.repositories.pdl_repository import PdlRepository


@pytest.fixture
def repo(tmp_path):
    db_path = tmp_path / "pdl.db"
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE pdl (
            id TEXT, n_pdl TEXT, data_creazione TEXT, area TEXT, unita TEXT,
            ditta TEXT, descrizione_lavoro TEXT, tipologia TEXT, stato TEXT,
            apparecchiatura TEXT, richiedente TEXT, data_richiesta TEXT,
            emittente TEXT, data_emissione TEXT, aprente TEXT, data_apertura TEXT,
            priorita TEXT, contratto TEXT, ordine TEXT, sito TEXT, importato_il TEXT
        )
    """)
    conn.execute(
        "INSERT INTO pdl (id, n_pdl, sito, area, unita) VALUES ('1', '123/A', 'ISAB-SUD', 'Area1', 'Unita1')"
    )
    conn.commit()
    conn.close()

    db_mgr = MagicMock()
    db_mgr.DB_PDL = db_path

    # Mock per usare connessione reale
    def execute_query(db_path, query, params=()):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    db_mgr.execute_query = execute_query
    return PdlRepository(db_manager_instance=db_mgr)


def test_get_filtered_by_site(repo):
    filters = {"site": "ISAB-SUD"}
    # Il repository ritorna una lista di tuple quando as_objects=False
    pdl = repo.get_filtered(filters=filters, as_objects=False)
    assert len(pdl) > 0
    # Verifica per indice (tuple index)
    # L'indice 19 è 'sito' basato sullo schema SQL
    assert pdl[0][19] == "ISAB-SUD"


def test_get_filtered_by_area(repo):
    filters = {"area": "Area1"}
    pdl = repo.get_filtered(filters=filters, as_objects=False)
    assert len(pdl) > 0
    # L'indice 3 è 'area'
    assert pdl[0][3] == "Area1"
