import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.core.excel_importer import ExcelImporter

class TestExcelImporterComprehensive:
    @pytest.fixture
    def sample_df(self):
        # Create a dataframe where Row 0 contains key columns for detection
        data = {
            0: ["DATA PREV.", "MESE", "N° PREV.", "TOTALE PREV.", "ATTIVITA'", "ODC"],
            1: ["2024-01-01", "Gennaio", "100/24", "1.000", "Lavoro A", "O1"]
        }
        df = pd.DataFrame.from_dict(data, orient='index')
        return df

    def test_import_contabilita_dati_logic(self, sample_df, tmp_path):
        file_path = tmp_path / "test_2024.xlsx"
        file_path.touch()
        
        with patch("src.core.excel_importer.Path.exists", return_value=True), \
             patch("src.core.excel_importer.ExcelImporter._decrypt_if_encrypted", return_value=(str(file_path), False)), \
             patch("src.core.excel_importer.pd.ExcelFile") as mock_xls, \
             patch("src.core.excel_importer.pd.read_excel") as mock_read:
            
            mock_xls_inst = MagicMock()
            mock_xls_inst.sheet_names = ["2024"]
            mock_xls.return_value = mock_xls_inst
            
            # Preview call (header=None)
            # Second call: real data
            mock_read.side_effect = [sample_df, sample_df]
            
            success, msg, rows, years = ExcelImporter.import_contabilita_dati(str(file_path))
            assert success is True

    def test_import_giornaliere_parsing(self, tmp_path):
        file1 = tmp_path / "file1.xlsx"
        file1.touch()
        
        cols = ["DATA", "PERSONALE", "DESCRIZIONE ATTIVITA'", "TCL", "ODC", "N° PDL", "INIZIO", "FINE", "ORE", "consuntivo"]
        # Add 3 rows: Data, Total (which is dropped), and one extra
        data = [
            ["01/01/2024", "Mario Rossi", "Desc", "T1", "O1", "P1", "08:00", "17:00", 8, "100/24"],
            ["02/01/2024", "Luigi Verdi", "Desc", "T1", "O1", "P1", "08:00", "17:00", 8, "100/24"],
            ["Totale", "", "", "", "", "", "", "", 16, ""]
        ]
        df = pd.DataFrame(data, columns=cols)
        
        with patch("src.core.excel_importer.pd.read_excel", return_value=df):
            year, rows, err = ExcelImporter._process_single_giornaliera((2024, file1, {{}}))
            assert year == 2024
            # iloc[:-1] removes Totale, so we should have 2 rows
            assert len(rows) == 2