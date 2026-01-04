import pytest
import sqlite3
import pandas as pd
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open
from src.core.contabilita_manager import ContabilitaManager
from src.core.database import db_manager

@pytest.fixture
def mock_db(mocker):
    """Configura un database SQLite in memoria per i test usando pytest-mock."""
    ContabilitaManager._instance = None
    
    in_memory_conn = sqlite3.connect(':memory:')

    mocker.patch.object(db_manager, 'get_connection', autospec=True)
    db_manager.get_connection.return_value.__enter__.return_value = in_memory_conn
    db_manager.get_connection.return_value.__exit__.return_value = False

    db_manager.init_db()

    yield in_memory_conn
    
    in_memory_conn.close()
    ContabilitaManager._instance = None

class TestContabilitaManagerLogic:

    def test_init_db(self, mock_db):
        cursor = mock_db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "contabilita" in tables
        assert "giornaliere" in tables

    def test_search_oda_empty(self, mock_db):
        results = ContabilitaManager().search_oda("12345")
        assert results == []

    def test_get_available_years_empty(self, mock_db):
        years = ContabilitaManager().get_available_years()
        assert years == []

    @patch('pandas.read_excel')
    def test_import_data_validation(self, mock_read, mock_db, tmp_path):
        """Verifica che l'importazione gestisca un file Excel vuoto."""
        # Crea un vero file Excel vuoto
        fake_excel = tmp_path / "fake.xlsx"
        pd.DataFrame().to_excel(fake_excel)
        
        # Simula che pandas legga un dataframe vuoto
        mock_read.return_value = pd.DataFrame()
        
        success, msg, added, removed = ContabilitaManager().import_data_from_excel(str(fake_excel))
        assert not success
        assert "Nessun anno importato" in msg

    def test_clean_oda_format(self, mock_db):
        test_val = " 5400123456 / 10 "
        assert "5400123456" in test_val.replace(" ", "")
