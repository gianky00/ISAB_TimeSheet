"""
Tests for Timbrature Storage Enhanced logic (Reparti, Cantieri, Lists).
"""
import pytest
import sqlite3
import json
from pathlib import Path
from src.bots.timbrature.storage import TimbratureStorage

@pytest.fixture
def temp_db(tmp_path):
    """Fixture per creare un DB temporaneo."""
    db_file = tmp_path / "data" / "timbrature_Isab.db"
    return db_file

@pytest.fixture
def storage(temp_db):
    """Fixture per creare uno storage con DB temporaneo."""
    storage = TimbratureStorage(temp_db)
    return storage

def test_schema_enhanced(temp_db, storage):
    """Test che lo schema includa la colonna cantiere."""
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(dipendenti)")
        columns = [info[1] for info in cursor.fetchall()]
        assert "reparto" in columns
        assert "cantiere" in columns

def test_update_employee_details(storage):
    """Test aggiornamento dettagli dipendente."""
    # Insert initial data implicitly via update
    storage.update_employee_details("Mario", "Rossi", reparto="Rep1", cantiere="CantA")
    
    # Verify
    emps = storage.get_employees()
    # Note: get_employees gets FROM timbrature usually, but here we don't have timbrature yet.
    # The method get_employees joins or selects distinctive from timbrature.
    # Let's check the code of get_employees... it does SELECT DISTINCT FROM timbrature.
    # So we need to insert a timbratura first.
    
    with sqlite3.connect(storage.db_path) as conn:
        conn.execute("INSERT INTO timbrature (data, nome, cognome) VALUES ('2025-01-01', 'Mario', 'Rossi')")
        conn.commit()
        
    emps = storage.get_employees()
    assert len(emps) == 1
    assert emps[0]['nome'] == "Mario"
    assert emps[0]['reparto'] == "Rep1"
    assert emps[0]['cantiere'] == "CantA"
    
    # Update only one field
    storage.update_employee_details("Mario", "Rossi", cantiere="CantB")
    emps = storage.get_employees()
    assert emps[0]['reparto'] == "Rep1" # Should remain
    assert emps[0]['cantiere'] == "CantB" # Should change

def test_get_timbrature_with_reparto_filters(storage):
    """Test filtri cantiere e reparto."""
    # Setup data
    with sqlite3.connect(storage.db_path) as conn:
        # Timbrature
        conn.execute("INSERT INTO timbrature (data, nome, cognome, sito_timbratura) VALUES ('2025-01-01', 'Mario', 'Rossi', 'Sito1')")
        conn.execute("INSERT INTO timbrature (data, nome, cognome, sito_timbratura) VALUES ('2025-01-01', 'Luigi', 'Verdi', 'Sito1')")
        conn.commit()
    
    # Setup Details
    storage.update_employee_details("Mario", "Rossi", reparto="RepA", cantiere="CantA")
    storage.update_employee_details("Luigi", "Verdi", reparto="RepB", cantiere="CantB")
    
    # Test Filter Cantiere
    rows = storage.get_timbrature_with_reparto(filter_cantiere="CantA")
    assert len(rows) == 1
    assert rows[0][3] == "Mario" # Nome
    
    # Test Filter Reparto
    rows = storage.get_timbrature_with_reparto(filter_reparto="RepB")
    assert len(rows) == 1
    assert rows[0][3] == "Luigi"

    # Test Filter Mixed
    rows = storage.get_timbrature_with_reparto(filter_cantiere="CantB", filter_reparto="RepA")
    assert len(rows) == 0

def test_list_management(storage, temp_db):
    """Test gestione liste JSON."""
    defaults = storage.get_lists()
    assert "reparti" in defaults
    assert "cantieri" in defaults
    
    new_data = {
        "reparti": ["R1", "R2"],
        "cantieri": ["C1"]
    }
    storage.save_lists(new_data)
    
    loaded = storage.get_lists()
    assert loaded["reparti"] == ["R1", "R2"]
    assert loaded["cantieri"] == ["C1"]
    
    # Check file existence
    json_path = temp_db.parent / "timbrature_lists.json"
    assert json_path.exists()
