"""
Tests for Lyra AI Client.
Mocks external API calls to Gemini and local DB interaction.
"""
import pytest
import requests
from unittest.mock import MagicMock, patch, ANY
from src.core.lyra_client import LyraClient

@pytest.fixture
def mock_contabilita_manager():
    with patch("src.core.lyra_client.ContabilitaManager") as mock_cm:
        # Mock default return for available years
        mock_cm.get_available_years.return_value = [2025]
        # Mock default stats
        mock_cm.get_year_stats.return_value = {
            'total_prev': 100000.0,
            'total_ore': 1000.0,
            'count_total': 50,
            'status_counts': {'COMPLETED': 40, 'WIP': 10},
            'top_commesse': [("Project A", 50000.0)]
        }
        yield mock_cm

@pytest.fixture
def mock_timbrature_db(tmp_path):
    # Mock file system path for db
    db_path = tmp_path / "timbrature_Isab.db"
    
    # We won't actually create the DB file here unless we patch sqlite3.connect too,
    # or we can just mock pathlib.Path.exists inside the class logic.
    # Since LyraClient imports sqlite3, let's patch sqlite3.
    
    with patch("src.core.lyra_client.sqlite3") as mock_sqlite, \
         patch("src.core.lyra_client.CONFIG_DIR", tmp_path):
         
        # Mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Setup cursor responses
        # 1. Total count
        # 2. Last entries
        # 3. Anomalies
        mock_cursor.fetchone.side_effect = [
            (100,), # Total
            (5,),   # Anomalies (missing out)
        ]
        
        mock_cursor.fetchall.return_value = [
            ("2025-01-01", "Mario", "Rossi", "08:00", "17:00")
        ]
        
        yield db_path

def test_system_context_generation(mock_contabilita_manager, mock_timbrature_db):
    client = LyraClient()
    
    # Need to ensure the check for db.exists() passes
    # We patched CONFIG_DIR to tmp_path. So client will look at tmp_path / data / db.
    # Let's create the dummy file.
    (mock_timbrature_db.parent / "data").mkdir(parents=True, exist_ok=True)
    (mock_timbrature_db.parent / "data" / "timbrature_Isab.db").touch()
    
    context = client._get_system_context()
    
    assert "REPORT CONTABILITÀ (2025)" in context
    assert "Valore Totale Preventivato: € 100,000.00" in context
    assert "REPORT TIMBRATURE" in context
    assert "Rilevate 5 timbrature con uscita mancante" in context

@patch("src.core.lyra_client.requests.post")
def test_ask_success(mock_post, mock_contabilita_manager):
    # Setup success response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'candidates': [{'content': {'parts': [{'text': 'Risposta AI'}]}}]
    }
    mock_post.return_value = mock_response
    
    client = LyraClient()
    # Mock getting context to avoid FS ops
    with patch.object(client, '_get_system_context', return_value="[System Data]"):
        answer = client.ask("Ciao")
        
    assert answer == "Risposta AI"
    mock_post.assert_called_once()

@patch("src.core.lyra_client.requests.post")
def test_ask_fail_retry(mock_post, mock_contabilita_manager):
    # Setup fail sequence: 429, then 500, then 200 (on 3rd model)
    # Models list has 3 entries.
    
    r1 = MagicMock(); r1.status_code = 429; r1.text = "Quota"
    r2 = MagicMock(); r2.status_code = 500; r2.text = "Error"
    r3 = MagicMock(); r3.status_code = 200
    r3.json.return_value = {'candidates': [{'content': {'parts': [{'text': 'Ok Third'}]}}]}
    
    mock_post.side_effect = [r1, r2, r3]
    
    client = LyraClient()
    with patch.object(client, '_get_system_context', return_value=""):
        answer = client.ask("Ciao")
        
    assert answer == "Ok Third"
    assert mock_post.call_count == 3

@patch("src.core.lyra_client.requests.post")
def test_ask_all_fail(mock_post, mock_contabilita_manager):
    # All fail
    mock_fail = MagicMock()
    mock_fail.status_code = 500
    mock_fail.text = "Error"
    mock_post.return_value = mock_fail
    
    client = LyraClient()
    with patch.object(client, '_get_system_context', return_value=""):
        answer = client.ask("Ciao")
        
    assert "Tutti i modelli AI hanno fallito" in answer
