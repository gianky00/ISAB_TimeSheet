from unittest.mock import MagicMock, patch

import pytest

from src.core.database.repositories.pdl_repository import PdlRepository
from src.models import PdlProgrammazioneRecord, PdlRecord


@pytest.fixture
def mock_db_manager():
    db = MagicMock()
    db.DB_PDL = "test_db"
    return db


@pytest.fixture
def repo(mock_db_manager):
    return PdlRepository(db_manager_instance=mock_db_manager)


def test_get_filtered_success(repo, mock_db_manager):
    mock_db_manager.execute_query.return_value = [
        {
            "id": 1,
            "n_pdl": "123",
            "data_creazione": "01/01/2026",
            "area": "A1",
            "unita": "U1",
            "ditta": "D1",
            "descrizione_lavoro": "Test",
            "tipologia": "T1",
            "stato": "Aperto",
            "apparecchiatura": "App1",
            "richiedente": "Req1",
            "data_richiesta": "01/01/2026",
            "emittente": "Em1",
            "data_emissione": "01/01/2026",
            "aprente": "Ap1",
            "data_apertura": "01/01/2026",
            "priorita": "P1",
            "contratto": "C1",
            "ordine": "O1",
            "sito": "S1",
            "importato_il": "2026-01-01",
        }
    ]

    filters = {"search": "Test", "site": "S1", "group": "G1", "area": "A1", "unit": "U1"}
    results = repo.get_filtered(filters=filters, as_objects=True)
    assert len(results) == 1
    assert isinstance(results[0], PdlRecord)

    # Test sort_col_name logic branches
    repo.get_filtered(filters={}, sort_col_name="n_pdl")
    repo.get_filtered(filters={}, sort_col_name="data_creazione")


def test_get_filtered_as_tuples(repo, mock_db_manager):
    mock_db_manager.execute_query.return_value = [
        (
            1,
            "123",
            "01/01/2026",
            "A1",
            "U1",
            "D1",
            "Test",
            "T1",
            "Aperto",
            "App1",
            "Req1",
            "01/01/2026",
            "Em1",
            "01/01/2026",
            "Ap1",
            "01/01/2026",
            "P1",
            "C1",
            "O1",
            "S1",
            "2026-01-01",
        )
    ]

    filters = {}
    results = repo.get_filtered(filters=filters, as_objects=False)
    assert len(results) == 1
    assert isinstance(results[0], tuple)


def test_get_filtered_error(repo, mock_db_manager):
    mock_db_manager.execute_query.side_effect = Exception("DB Error")
    results = repo.get_filtered(filters={})
    assert results == []


def test_get_unique_requesters_success(repo, mock_db_manager):
    mock_db_manager.execute_query.return_value = [("mario rossi",), ("luigi bianchi",), ("",), (None,)]
    results = repo.get_unique_requesters()
    assert results == ["Luigi Bianchi", "Mario Rossi"]


def test_get_unique_requesters_error(repo, mock_db_manager):
    mock_db_manager.execute_query.side_effect = Exception("DB Error")
    results = repo.get_unique_requesters()
    assert results == []


def test_get_programming_by_week_success(repo, mock_db_manager):
    mock_db_manager.execute_query.return_value = [
        {
            "id": 1,
            "richiedente": "Req1",
            "n_pdl": "123",
            "area": "A1",
            "unita": "U1",
            "descrizione": "Desc",
            "lun_tcl": 1,
            "lun_tgo": 0,
            "mar_tcl": 1,
            "mar_tgo": 0,
            "mer_tcl": 1,
            "mer_tgo": 0,
            "gio_tcl": 1,
            "gio_tgo": 0,
            "ven_tcl": 1,
            "ven_tgo": 0,
            "sab_tcl": 1,
            "sab_tgo": 0,
            "dom_tcl": 1,
            "dom_tgo": 0,
            "settimana_start": "2026-01-01",
            "settimana_end": "2026-01-07",
        }
    ]
    results = repo.get_programming_by_week("2026-01-01", "2026-01-07")
    assert len(results) == 1
    assert isinstance(results[0], PdlProgrammazioneRecord)


def test_get_programming_by_week_error(repo, mock_db_manager):
    mock_db_manager.execute_query.side_effect = Exception("DB Error")
    results = repo.get_programming_by_week("2026-01-01", "2026-01-07")
    assert results == []


def test_save_programming_success_empty(repo, mock_db_manager):
    assert repo.save_programming([], "2026-01-01", "2026-01-07") is True
    assert mock_db_manager.execute_query.call_count == 1


def test_save_programming_success_with_records(repo, mock_db_manager):
    records = [
        PdlProgrammazioneRecord(
            id=1,
            richiedente="Req1",
            n_pdl="123",
            area="A1",
            unita="U1",
            descrizione="Desc",
            settimana_start="2026-01-01",
            settimana_end="2026-01-07",
            lun_tcl=1,
            lun_tgo=0,
            mar_tcl=1,
            mar_tgo=0,
            mer_tcl=1,
            mer_tgo=0,
            gio_tcl=1,
            gio_tgo=0,
            ven_tcl=1,
            ven_tgo=0,
            sab_tcl=1,
            sab_tgo=0,
            dom_tcl=1,
            dom_tgo=0,
        )
    ]

    mock_conn = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn

    assert repo.save_programming(records, "2026-01-01", "2026-01-07") is True
    assert mock_conn.executemany.call_count == 1


def test_save_programming_error(repo, mock_db_manager):
    mock_db_manager.execute_query.side_effect = Exception("DB Error")
    assert repo.save_programming([], "2026-01-01", "2026-01-07") is False


def test_get_interventions_success(repo):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {
            "fonte": "Report",
            "data": "2026-01-01",
            "tecnico": "Mario",
            "team": "",
            "ore_lavoro": "",
            "descrizione": "Test",
        }
    ]

    with patch("sqlite3.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_conn
        results = repo.get_interventions("123", "dummy.db")

    assert len(results) == 1
    assert results[0]["tecnico"] == "Mario"


def test_get_interventions_error(repo):
    with patch("sqlite3.connect", side_effect=Exception("Connect Error")):
        results = repo.get_interventions("123", "dummy.db")
    assert results == []
