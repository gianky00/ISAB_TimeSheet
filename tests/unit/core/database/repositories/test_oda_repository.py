from unittest.mock import MagicMock

import pytest

from src.core.database.repositories.oda_repository import OdaRepository
from src.models import OdaRecord


@pytest.fixture
def mock_db_manager():
    db = MagicMock()
    # Mocking paths
    db.DB_STORICO_ODA = MagicMock()
    db.DB_STORICO_ODA.exists.return_value = True
    return db


@pytest.fixture
def repo(mock_db_manager):
    return OdaRepository(db_manager_instance=mock_db_manager)


def test_get_all_success_objects(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {
            "org_acq": "A",
            "data_oda": "2026-01-01",
            "oda": "1",
            "pos_oda": "1",
            "stato": "A",
            "cat_contab": "C",
            "descrizione": "Desc",
            "qta": 1.0,
            "uom": "U",
            "data_consegna": "2026-01-01",
            "valore_netto_pos": 1.0,
            "valore_residuo": 1.0,
            "valore_netto_oda": 1.0,
            "divisione": "D",
            "destinatario": "De",
            "nome_destinatario": "Nd",
            "codice_fornitore": "Cf",
            "descrizione_fornitore": "Df",
            "emittente_fattura": "Ef",
            "desc_emittente_fattura": "Def",
            "contract_card": "Cc",
            "contratto": "C",
            "posizione_contratto": "Pc",
            "gruppo_acquisti": "Ga",
            "indicatore_rilascio": "Ir",
            "stato_rilascio": "Sr",
            "attivita": "A",
            "num_riga": "1",
            "quantita": 1.0,
            "unita_mis": "U",
            "prezzo_lordo": 1.0,
            "testo_breve": "Tb",
        }
    ]

    results = repo.get_all(as_objects=True)
    assert len(results) == 1
    assert isinstance(results[0], OdaRecord)


def test_get_all_success_tuples(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("A", "2026-01-01")]

    results = repo.get_all(as_objects=False)
    assert len(results) == 1
    assert isinstance(results[0], tuple)


def test_get_all_with_search_text(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {
            "org_acq": "A",
            "data_oda": "2026-01-01",
            "oda": "1",
            "pos_oda": "1",
            "stato": "A",
            "cat_contab": "C",
            "descrizione": "Desc",
            "qta": 1.0,
            "uom": "U",
            "data_consegna": "2026-01-01",
            "valore_netto_pos": 1.0,
            "valore_residuo": 1.0,
            "valore_netto_oda": 1.0,
            "divisione": "D",
            "destinatario": "De",
            "nome_destinatario": "Nd",
            "codice_fornitore": "Cf",
            "descrizione_fornitore": "Df",
            "emittente_fattura": "Ef",
            "desc_emittente_fattura": "Def",
            "contract_card": "Cc",
            "contratto": "C",
            "posizione_contratto": "Pc",
            "gruppo_acquisti": "Ga",
            "indicatore_rilascio": "Ir",
            "stato_rilascio": "Sr",
            "attivita": "A",
            "num_riga": "1",
            "quantita": 1.0,
            "unita_mis": "U",
            "prezzo_lordo": 1.0,
            "testo_breve": "Tb",
        }
    ]

    # Text search
    results = repo.get_all(search_text="test")
    assert len(results) == 1

    # Date search format change
    results_date = repo.get_all(search_text="01/01/2026")
    assert len(results_date) == 1


def test_get_all_no_db(repo, mock_db_manager):
    mock_db_manager.DB_STORICO_ODA.exists.return_value = False
    assert repo.get_all() == []


def test_get_all_with_date_search(repo, mock_db_manager):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    # Esegui ricerca con formato data
    repo.get_all(search_text="01/01/2026")

    # Verifica che la query sia stata chiamata (indirettamente verificando i params)
    assert mock_cursor.execute.called
    _query, params = mock_cursor.execute.call_args[0]
    assert "2026-01-01" in params[0]
