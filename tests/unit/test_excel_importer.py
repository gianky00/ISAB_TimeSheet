import pytest
import pandas as pd
from src.core.excel_importer import ExcelImporter
import os

class TestExcelImporter:

    @pytest.fixture
    def sample_excel_file(self, tmp_path):
        """Create a temporary valid Excel file for testing."""
        file_path = tmp_path / "test_dati.xlsx"
        
        # Create a DataFrame that mimics "Dati" structure
        data = {
            "DATAPREV": ["2023-01-01", "2023-01-02", "Total Row"],
            "MESE": ["Gennaio", "Gennaio", ""],
            "NPREV": ["100", "101", ""],
            "TOTALE PREV.": [1000, 2000, 3000],
            "ATTIVITA'": ["Test A", "Test B", ""],
            "TCL": ["T1", "T2", ""],
            "ODC": ["ODC1", "ODC2", ""],
            "STATO ATTIVITA'": ["Open", "Closed", ""],
            "TIPOLOGIA": ["A", "B", ""],
            "ORE SP": [8, 4, 0],
            "RESA": [100, 100, 0],
            "ANNOTAZIONI": ["", "", ""],
            "INDIRIZZO CONSUNTIVO": ["", "", ""],
            "NOME FILE": ["", "", ""]
        }
        df = pd.DataFrame(data)
        
        # Write to Excel with a specific sheet name (e.g., year 2023)
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="2023", index=False)
            
        return str(file_path)

    def test_import_contabilita_dati_success(self, sample_excel_file):
        success, msg, rows, years = ExcelImporter.import_contabilita_dati(sample_excel_file)
        
        assert success is True
        assert len(rows) == 2
        assert 2023 in years
        
        # Verify content of first row
        # Structure depends on COLUMNS_MAPPING order + year at start
        # COLUMNS_MAPPING: DATA PREV, MESE, N° PREV, TOTALE PREV, ATTIVITA', TCL, ODC, STATO, TIPOLOGIA, ORE SP, RESA, ANNOTAZIONI, INDIRIZZO, NOME FILE
        # Year is prepended.
        
        first_row = rows[0]
        assert first_row[0] == 2023 # Year
        # Check ODC (index 7 in mapping values list, plus year -> 8? No, let's check mapping)
        # MAPPING values: data_prev, mese, n_prev, totale_prev, attivita, tcl, odc, ...
        # index 0: year
        # index 7: odc
        assert first_row[7] == "ODC1"

    def test_import_not_existing_file(self):
        success, msg, _, _ = ExcelImporter.import_contabilita_dati("non_existent.xlsx")
        assert success is False
        assert "File non trovato" in msg

    def test_import_invalid_sheet_name(self, tmp_path):
        file_path = tmp_path / "invalid_sheets.xlsx"
        df = pd.DataFrame({"A": [1]})
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="InvalidName", index=False)
            
        success, msg, rows, _ = ExcelImporter.import_contabilita_dati(str(file_path))
        # Depending on logic, it might return False if no valid sheets found
        assert success is False
        assert "Nessun anno importato" in msg
