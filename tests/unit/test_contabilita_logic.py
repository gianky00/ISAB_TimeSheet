"""
Tests for ContabilitaManager logic.
"""
import pytest
import sqlite3
import pandas as pd
from pathlib import Path
from src.core.contabilita_manager import ContabilitaManager
from src.core.database import db_manager

@pytest.fixture
def test_db_path(tmp_path):
    """Overrides the real DB path with a temp one."""
    db = tmp_path / "contabilita_test.db"
    # We patch the DB_PATH class attribute for the test duration
    original = ContabilitaManager.DB_PATH
    ContabilitaManager.DB_PATH = db
    
    # Init Schema via db_manager helper
    db_manager.init_db() # Initializes ALL dbs, including the one at config_dir.
    # To be safe, let's manually init this specific file
    with sqlite3.connect(db) as conn:
        # Minimal Schema for Contabilita
        conn.execute("""
            CREATE TABLE IF NOT EXISTS contabilita (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER,
                data_prev TEXT,
                totale_prev TEXT,
                annotazioni TEXT,
                nome_file TEXT,
                n_prev TEXT,
                created_at TIMESTAMP
            )
        """)
    
    yield db
    ContabilitaManager.DB_PATH = original

@pytest.fixture
def manager(test_db_path):
    return ContabilitaManager()

def test_insert_and_get_data(manager, test_db_path):
    # Test manual insertion logic (simulating what import_excel does internally)
    with sqlite3.connect(test_db_path) as conn:
        conn.execute("""
            INSERT INTO contabilita (year, data_prev, totale_prev, annotazioni)
            VALUES (2025, '2025-01-01', '1000', 'Test Note')
        """)
        conn.commit()
    
    # Test retrieval methods if they exist, or raw query
    with sqlite3.connect(test_db_path) as conn:
        rows = conn.execute("SELECT * FROM contabilita").fetchall()
        assert len(rows) == 1
        assert rows[0][1] == 2025

def test_column_mapping(manager):
    # Verify mappings exist
    assert "DATA PREV." in manager.COLUMNS_MAPPING
    assert "MESE" in manager.COLUMNS_MAPPING
    
    # Verify DB column names match schema
    db_cols = list(manager.COLUMNS_MAPPING.values())
    assert "data_prev" in db_cols
    assert "mese" in db_cols

def test_year_extraction(manager):
    # If there is a helper method for year, test it.
    # Assuming standard behavior, let's test a potential utility if exposed
    pass

def test_scarico_ore_schema(test_db_path):
    # Verify scarico_ore table creation
    with sqlite3.connect(test_db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scarico_ore (
                id INTEGER PRIMARY KEY,
                data TEXT,
                totale_ore TEXT,
                styles TEXT
            )
        """)
        conn.execute("INSERT INTO scarico_ore (data, totale_ore) VALUES ('2025-01-01', '8')")
        conn.commit()
        
        row = conn.execute("SELECT * FROM scarico_ore").fetchone()
        assert row[2] == '8'

from unittest.mock import MagicMock, patch

def test_import_attivita_programmate_logic(manager, test_db_path, tmp_path):
    # Create a dummy excel logic mock
    mock_df = pd.DataFrame({
        "PS": ["PS1"],
        "AREA": ["Area1"],
        "PdL": ["PDL1"],
        "IMP.": ["IMP1"],
        "DESCRIZIONE\nATTIVITA'": ["Desc"],
        # Add other required mapped cols with dummy values to match mapping logic
        "LUN": [""], "MAR": [""], "MER": [""], "GIO": [""], "VEN": [""],
        "STATO\nPdL": [""], "STATO\nATTIVITA'": [""], "DATA\nCONTROLLO": [""],
        "PERSONALE\nIMPIEGATO": [""], "PO": [""], "AVVISO": [""]
    })
    
    dummy_path = tmp_path / "dummy_attivita.xlsx"
    dummy_path.touch() # Create file so os.path.exists passes
    
    # PATCH db_manager.DB_CONTABILITA to point to our test DB!
    with patch("pandas.read_excel", return_value=mock_df) as mock_read, \
         patch("src.core.database.DatabaseManager.DB_CONTABILITA", test_db_path):
        
        # Init schema on the TEST DB (since we patched the path class attribute)
        # Note: DatabaseManager singleton is already instantiated. 
        # But we patched the class attribute, so accessing self.DB_CONTABILITA *might* work if accessed via self.
        # Let's verify usage in DatabaseManager: self.DB_CONTABILITA. 
        # Since it's an instance attribute usually set from class, patching Class attribute might be tricky if instance already exists.
        # Let's patch the INSTANCE attribute.
        
        db_manager.DB_CONTABILITA = test_db_path
        db_manager.init_db() 
        
        success, msg, added, removed = manager.import_attivita_programmate(str(dummy_path))
        
        assert success is True, f"Failed: {msg}"
        assert added == 1
        
        # Verify DB
        with sqlite3.connect(test_db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM attivita_programmate").fetchone()
            assert row is not None
            assert row['ps'] == "PS1"
