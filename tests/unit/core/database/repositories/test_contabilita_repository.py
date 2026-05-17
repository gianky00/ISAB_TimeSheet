from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.database.repositories.contabilita_repository import ContabilitaRepository


@pytest.fixture
def repo():
    # Mocking semplice e robusto
    db_mgr = MagicMock()
    # Mocking file path esistente
    db_mgr.DB_CONTABILITA = Path("fake.db")
    return ContabilitaRepository(db_manager_instance=db_mgr)

def test_get_available_years(repo):
    # Mock del cursore per restituire anni
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    repo.db.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(2026,), (2025,)]

    with patch("pathlib.Path.exists", return_value=True):
        years = repo.get_available_years()
        assert 2026 in years
        assert 2025 in years

def test_get_data_by_year_legacy(repo):
    # Mock del cursore per il flusso legacy (as_objects=False)
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    repo.db.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    # Mocka il ritorno di 1 record (tupla)
    mock_cursor.fetchall.return_value = [("P1", "Desc", "2026-05-17", 100.0, "T1", "O1")]

    with patch("pathlib.Path.exists", return_value=True):
        # Patch dell'importo per evitare problemi di importazione
        with patch("src.core.excel_importer.ExcelImporter.COLUMNS_MAPPING", {"n": "n_prev"}):
            data = repo.get_data_by_year(2026, as_objects=False)
            assert len(data) == 1
            assert data[0][0] == "P1"
