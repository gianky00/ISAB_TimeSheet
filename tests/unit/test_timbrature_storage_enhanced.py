"""
Tests for Timbrature Storage Enhanced logic using config.json for mappings.
"""
import pytest
import sqlite3
from pathlib import Path
from src.bots.timbrature.storage import TimbratureStorage
from unittest.mock import patch, MagicMock

@pytest.fixture
def temp_db(tmp_path):
    """Fixture per creare un DB temporaneo."""
    db_file = tmp_path / "data" / "timbrature_Isab.db"
    return db_file

@pytest.fixture
def mock_config():
    """Fixture per mockare config_manager."""
    with patch("src.bots.timbrature.storage.config_manager") as mock:
        # Configurazione iniziale vuota
        mock.load_config.return_value = {
            "reparti": ["STRUMENTALE", "ELETTRICO"],
            "cantieri": [],
            "employee_mappings": {}
        }
        
        # Simulazione salvataggio (aggiorna il mock di load_config)
        def mock_set(key, value):
            mock.load_config.return_value[key] = value
            
        mock.set_config_value.side_effect = mock_set
        yield mock

@pytest.fixture
def storage(temp_db, mock_config):
    """Fixture per creare uno storage con DB temporaneo e config mockato."""
    storage = TimbratureStorage(temp_db)
    return storage

def test_schema_basic(temp_db, storage):
    """Verifica che la tabella timbrature esista (dipendenti non deve esistere)."""
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='timbrature'")
        assert cursor.fetchone() is not None
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dipendenti'")
        assert cursor.fetchone() is None

def test_update_employee_details_in_config(storage, mock_config):
    """Test aggiornamento dettagli dipendente salvati nel mock config."""
    # Setup: timbratura necessaria per get_employees
    with sqlite3.connect(storage.db_path) as conn:
        conn.execute("INSERT INTO timbrature (nome, cognome) VALUES ('Mario', 'Rossi')")
        conn.commit()

    storage.update_employee_details("Mario", "Rossi", reparto="Rep1", cantiere="CantA")
    
    # Verifica tramite mock
    mappings = mock_config.load_config().get("employee_mappings")
    assert "Mario|Rossi" in mappings
    assert mappings["Mario|Rossi"]["reparto"] == "Rep1"
    
    # Verifica tramite storage
    emps = storage.get_employees()
    assert len(emps) == 1
    assert emps[0]['reparto'] == "Rep1"
    assert emps[0]['cantiere'] == "CantA"

def test_get_timbrature_with_config_filters(storage, mock_config):
    """Test filtri cantiere e reparto usando dati da config."""
    # Setup data
    with sqlite3.connect(storage.db_path) as conn:
        conn.execute("INSERT INTO timbrature (data, nome, cognome) VALUES ('2025-01-01', 'Mario', 'Rossi')")
        conn.execute("INSERT INTO timbrature (data, nome, cognome) VALUES ('2025-01-01', 'Luigi', 'Verdi')")
        conn.commit()
    
    # Setup Mappings in mock
    storage.update_employee_details("Mario", "Rossi", reparto="RepA", cantiere="CantA")
    storage.update_employee_details("Luigi", "Verdi", reparto="RepB", cantiere="CantB")
    
    # Test Filter Cantiere
    rows = storage.get_timbrature_with_reparto(filter_cantiere="CantA")
    assert len(rows) == 1
    assert rows[0][3] == "Mario"
    
    # Test Filter Reparto
    rows = storage.get_timbrature_with_reparto(filter_reparto="RepB")
    assert len(rows) == 1
    assert rows[0][3] == "Luigi"

def test_list_management_in_config(storage, mock_config):
    """Test gestione liste Reparti/Cantieri tramite config."""
    # Verifica caricamento
    lists = storage.get_lists()
    assert "STRUMENTALE" in lists["reparti"]
    
    # Verifica salvataggio
    new_data = {"reparti": ["R1"], "cantieri": ["C1"]}
    storage.save_lists(new_data)
    
    assert mock_config.set_config_value.called
    assert mock_config.load_config()["reparti"] == ["R1"]