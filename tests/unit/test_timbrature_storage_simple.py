import pytest
import os
import pandas as pd
from unittest.mock import MagicMock, patch
from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage

class TestTimbratureStorageSimple:
    def test_storage_init_and_import(self, tmp_path):
        db_file = tmp_path / "timbrature.db"
        storage = TimbratureStorage(db_file) # Pass as Path object
        
        # Test importing excel
        excel_file = tmp_path / "data.xlsx"
        excel_file.touch()
        
        data = {
            "Data Timbratura": ["2024-01-01"],
            "Ora Ingresso": ["08:00"],
            "Ora Uscita": ["17:00"],
            "Nome Risorsa": ["Mario"],
            "Cognome Risorsa": ["Rossi"],
            "Presente Nei Timesheet": ["Sì"],
            "Sito Timbratura": ["ISAB"]
        }
        df = pd.DataFrame(data)
        
        with patch("src.bots.portale_fornitori.timbrature.storage.pd.read_excel", return_value=df):
            success = storage.import_excel(str(excel_file))
            assert success is True
            
        # Verify search
        results = storage.search_employees("Rossi")
        assert len(results) == 1
        assert results[0]["nome"] == "Mario"

    def test_get_lists_default(self, tmp_path):
        db_file = tmp_path / "timbrature.db"
        storage = TimbratureStorage(db_file)
        lists = storage.get_lists()
        assert "STRUMENTALE" in lists["reparti"]