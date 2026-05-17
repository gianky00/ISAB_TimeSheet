from unittest.mock import MagicMock

import pytest

from src.core.database.repositories.contabilita_repository import ContabilitaRepository
from src.models import (
    AttivitaProgrammataRecord,
    CertificatoCampioneRecord,
    ContabilitaRecord,
    GiornalieraRecord,
)


@pytest.fixture
def mock_db_manager():
    db = MagicMock()
    # Mocking paths
    db.DB_CONTABILITA = MagicMock()
    db.DB_CONTABILITA.exists.return_value = True
    return db


@pytest.fixture
def repo(mock_db_manager):
    return ContabilitaRepository(db_manager_instance=mock_db_manager)


def test_get_available_years_success(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(2026,), (2025,)]

    assert repo.get_available_years() == [2026, 2025]


def test_get_available_years_no_db(repo, mock_db_manager):
    mock_db_manager.DB_CONTABILITA.exists.return_value = False
    assert repo.get_available_years() == []


def test_get_available_years_error(repo, mock_db_manager):
    mock_db_manager.get_connection.side_effect = Exception("DB Error")
    assert repo.get_available_years() == []


def test_get_data_by_year_success_objects(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {
            "id": 1,
            "year": 2026,
            "data_prev": "01/01/2026",
            "mese": "Gen",
            "n_prev": "123",
            "totale_prev": 100.0,
            "attivita": "A",
            "tcl": "T",
            "odc": "O",
            "stato_attivita": "S",
            "tipologia": "T",
            "ore_sp": 8.0,
            "resa": "R",
            "annotazioni": "",
            "indirizzo_consuntivo": "",
            "nome_file": "",
        }
    ]

    results = repo.get_data_by_year(2026, as_objects=True)
    assert len(results) == 1
    assert isinstance(results[0], ContabilitaRecord)
    assert results[0].year == 2026


def test_get_data_by_year_success_tuples(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, 2026)]

    results = repo.get_data_by_year(2026, as_objects=False)
    assert len(results) == 1
    assert isinstance(results[0], tuple)


def test_get_data_by_year_no_db(repo, mock_db_manager):
    mock_db_manager.DB_CONTABILITA.exists.return_value = False
    assert repo.get_data_by_year(2026) == []


def test_get_data_by_year_error(repo, mock_db_manager):
    mock_db_manager.get_connection.side_effect = Exception("DB Error")
    assert repo.get_data_by_year(2026) == []


def test_get_giornaliere_by_year_success_objects(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {
            "id": 1,
            "year": 2026,
            "data": "2026-01-01",
            "personale": "Mario",
            "tcl": "1",
            "descrizione": "Lavoro",
            "n_prev": "1",
            "odc": "1",
            "pdl": "1",
            "inizio": "08:00",
            "fine": "17:00",
            "ore": 8.0,
            "nome_file": "file.xlsx",
        }
    ]

    results = repo.get_giornaliere_by_year(2026, as_objects=True)
    assert len(results) == 1
    assert isinstance(results[0], GiornalieraRecord)


def test_get_giornaliere_by_year_success_tuples(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("2026-01-01", "Mario")]

    results = repo.get_giornaliere_by_year(2026, as_objects=False)
    assert len(results) == 1
    assert isinstance(results[0], tuple)


def test_get_giornaliere_by_year_no_db(repo, mock_db_manager):
    mock_db_manager.DB_CONTABILITA.exists.return_value = False
    assert repo.get_giornaliere_by_year(2026) == []


def test_get_giornaliere_by_year_error(repo, mock_db_manager):
    mock_db_manager.get_connection.side_effect = Exception("DB Error")
    assert repo.get_giornaliere_by_year(2026) == []


def test_get_attivita_programmate_success_objects(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {
            "id": 1,
            "n_prev": "A1",
            "odc": "O",
            "descrizione": "Test",
            "stato": "Mensile",
            "data_inizio": "2026-01-01",
            "data_fine": "2026-01-31",
        }
    ]

    results = repo.get_attivita_programmate(as_objects=True)
    assert len(results) == 1
    assert isinstance(results[0], AttivitaProgrammataRecord)


def test_get_attivita_programmate_success_tuples(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("A1", "Test")]

    results = repo.get_attivita_programmate(as_objects=False)
    assert len(results) == 1
    assert isinstance(results[0], tuple)


def test_get_attivita_programmate_no_db(repo, mock_db_manager):
    mock_db_manager.DB_CONTABILITA.exists.return_value = False
    assert repo.get_attivita_programmate() == []


def test_get_attivita_programmate_error(repo, mock_db_manager):
    mock_db_manager.get_connection.side_effect = Exception("DB Error")
    assert repo.get_attivita_programmate() == []


def test_get_certificati_campione_success_objects(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mocking PRAGMA info and fetchall
    mock_cursor.fetchall.side_effect = [
        [(0, "id_coemi")],  # PRAGMA
        [
            {
                "id_coemi": "123",
                "certificato": "C1",
                "modello": "M1",
                "costruttore": "C1",
                "matricola": "M1",
                "range_strumento": "R1",
                "errore_max": "E1",
                "emissione": "01/01",
                "scadenza": "01/01",
                "stato": "A",
                "annotazioni": "",
                "ubicazione": "U1",
            }
        ],  # SELECT
    ]

    results = repo.get_certificati_campione(as_objects=True)
    assert len(results) == 1
    assert isinstance(results[0], CertificatoCampioneRecord)


def test_get_certificati_campione_success_tuples(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mocking PRAGMA info and fetchall
    mock_cursor.fetchall.side_effect = [
        [(0, "id_strumento")],  # PRAGMA
        [("123", "C1", "M1")],  # SELECT
    ]

    results = repo.get_certificati_campione(as_objects=False)
    assert len(results) == 1
    assert isinstance(results[0], tuple)


def test_get_certificati_campione_no_db(repo, mock_db_manager):
    mock_db_manager.DB_CONTABILITA.exists.return_value = False
    assert repo.get_certificati_campione() == []


def test_get_certificati_campione_error(repo, mock_db_manager):
    mock_db_manager.get_connection.side_effect = Exception("DB Error")
    assert repo.get_certificati_campione() == []


def test_get_scarico_ore_success_objects(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{"id": 1, "test": "val"}]

    results = repo.get_scarico_ore(as_objects=True)
    assert len(results) == 1
    assert isinstance(results[0], dict)  # SQLite row dict representation


def test_get_scarico_ore_success_tuples(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("val1", "val2")]

    results = repo.get_scarico_ore(as_objects=False)
    assert len(results) == 1
    assert isinstance(results[0], tuple)


def test_get_scarico_ore_no_db(repo, mock_db_manager):
    mock_db_manager.DB_CONTABILITA.exists.return_value = False
    assert repo.get_scarico_ore() == []


def test_get_scarico_ore_error(repo, mock_db_manager):
    mock_db_manager.get_connection.side_effect = Exception("DB Error")
    assert repo.get_scarico_ore() == []
