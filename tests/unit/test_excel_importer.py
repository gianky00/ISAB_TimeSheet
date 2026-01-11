import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.core.excel_importer import ExcelImporter

class TestExcelImporter:
    @patch("src.core.excel_importer.pd.ExcelFile")
    @patch("src.core.excel_importer.pd.read_excel")
    @patch("src.core.excel_importer.Path.exists", return_value=True)
    def test_import_contabilita_dati_success(self, mock_exists, mock_read_excel, mock_excel_file):
        # Mock ExcelFile
        mock_xls = MagicMock()
        mock_xls.sheet_names = ["2024"]
        mock_excel_file.return_value = mock_xls
        
        # Mock preview_df for header detection
        preview_data = [
            ["Row 1", "Garbage"],
            ["DATA PREV.", "MESE", "N° PREV.", "TOTALE PREV.", "ATTIVITA'", "ODC"]
        ]
        preview_df = pd.DataFrame(preview_data)
        
        # Mock main df (must have at least 2 rows because code does iloc[:-1])
        main_df = pd.DataFrame({
            "DATA PREV.": ["01/01/2024", "TOTAL"],
            "MESE": ["Gennaio", ""],
            "N° PREV.": ["123", ""],
            "TOTALE PREV.": ["1000", "1000"],
            "ATTIVITA'": ["Test", ""],
            "ODC": ["5400123", ""]
        })
        
        mock_read_excel.side_effect = [preview_df, main_df]
        
        success, msg, rows, years = ExcelImporter.import_contabilita_dati("dummy.xlsx")
        
        assert success is True, f"Import failed: {msg}"
        assert 2024 in years
        assert len(rows) == 1
        assert rows[0][0] == 2024

    def test_process_single_giornaliera_cleaning(self):
        # Mock df for RIASSUNTO (must have 2 rows)
        df = pd.DataFrame({
            "DATA": ["2024-01-01", "TOTAL"],
            "PERSONALE": ["Mario Rossi", ""],
            "ODC": ["5400123 ", ""],
            "N° PDL": ["999", ""],
            "ORE": [8.0, 8.0],
            "consuntivo": ["123", ""]
        })
        
        with patch("src.core.excel_importer.pd.read_excel", return_value=df):
            year, rows, err = ExcelImporter._process_single_giornaliera((2024, Path("file.xlsx"), dict()))
            
            assert err is None
            assert len(rows) == 1
            assert rows[0][5] == "5400123"

    @patch("src.core.excel_importer.ProcessPoolExecutor")
    @patch("src.core.excel_importer.Path")
    def test_import_giornaliere_parallel_mock(self, mock_path, mock_executor):
        # Mock directory structure
        mock_root = MagicMock()
        mock_folder = MagicMock()
        mock_folder.is_dir.return_value = True
        mock_folder.name = "Giornaliere 2024"
        
        mock_file = MagicMock()
        mock_file.name = "giorn.xlsx"
        mock_file.startswith.return_value = False
        
        mock_folder.glob.return_value = [mock_file]
        mock_root.iterdir.return_value = [mock_folder]
        mock_root.exists.return_value = True
        mock_path.return_value = mock_root
        
        # Mock executor behavior
        mock_exec_instance = mock_executor.return_value.__enter__.return_value
        mock_exec_instance.map.return_value = [(2024, [("row",)], None)]
        
        success, msg, rows, years = ExcelImporter.import_giornaliere("path", dict())
        
        assert success is True
        assert 2024 in years
        assert len(rows) == 1

    @patch("src.core.excel_importer.pd.read_excel")
    @patch("src.core.excel_importer.pd.ExcelFile")
    @patch("src.core.excel_importer.Path.exists", return_value=True)
    def test_import_certificati_campione(self, mock_exists, mock_excel_file, mock_read_excel):
        mock_xls = MagicMock()
        mock_xls.sheet_names = ["Strumenti Campione"]
        mock_excel_file.return_value = mock_xls
        
        # Header detection mock
        preview_df = pd.DataFrame([
            ["Modello / Tipo", "Costruttore", "Matricola", "ID-COEMI"]
        ])
        
        main_df = pd.DataFrame({
            "Modello / Tipo": ["M1"],
            "Costruttore": ["C1"],
            "Matricola": ["SN1"],
            "ID-COEMI": ["ID1"],
            "Scadenza Certificato": ["2025-01-01"]
        })
        
        mock_read_excel.side_effect = [preview_df, main_df]
        
        success, msg, rows = ExcelImporter.import_certificati_campione("c.xlsx")
        assert success is True
        assert len(rows) == 1

    @patch("src.core.excel_importer.msoffcrypto", None)
    @patch("src.core.excel_importer.openpyxl.load_workbook")
    @patch("src.core.excel_importer.Path.exists", return_value=True)
    def test_import_scarico_ore_mock(self, mock_exists, mock_load_wb):
        mock_file_handle = MagicMock()
        mock_file_handle.__enter__.return_value = mock_file_handle
        mock_file_handle.read.return_value = b"fake excel bytes"
        
        with patch("builtins.open", return_value=mock_file_handle):
            mock_wb = MagicMock()
            mock_wb.sheetnames = ["SCARICO ORE"]
            mock_ws = MagicMock()
            mock_wb.__getitem__.return_value = mock_ws
            mock_load_wb.return_value = mock_wb
            
            # Helper to create a complex cell mock
            def create_mock_cell(value):
                cell = MagicMock()
                cell.value = value
                cell.font.color = None
                cell.fill.patternType = None
                return cell
    
            # mock_cells must match col_keys length (11)
            mock_cells = [
                create_mock_cell("2024-01-01"), # data
                create_mock_cell("P1"),         # pers1
                create_mock_cell("P2"),         # pers2
                create_mock_cell("54001"),      # odc
                create_mock_cell("10"),         # pos
                create_mock_cell("08:00"),      # dalle
                create_mock_cell("17:00"),      # alle
                create_mock_cell("8.0"),        # totale_ore
                create_mock_cell("Desc"),       # descrizione
                create_mock_cell("SI"),         # finito
                create_mock_cell("COMM")        # commessa
            ]
            
            mock_ws.iter_rows.return_value = [mock_cells]
            mock_ws.max_row = 10
            
            success, msg, rows = ExcelImporter.import_scarico_ore("s.xlsx")
            assert success is True, f"Failed: {msg}"
            assert len(rows) == 1

    @patch("src.core.excel_importer.pd.read_excel")
    @patch("src.core.excel_importer.Path.exists", return_value=True)
    def test_import_attivita_programmate(self, mock_exists, mock_read_excel):
        df = pd.DataFrame({
            "PS": ["P1"],
            "AREA": ["A1"],
            "DESCRIZIONE\nATTIVITA'": ["D1"]
        })
        mock_read_excel.return_value = df
        
        success, msg, rows = ExcelImporter.import_attivita_programmate("p.xlsx")
        assert success is True
        assert len(rows) == 1

    @patch("src.core.excel_importer.zipfile.ZipFile")
    @patch("src.core.excel_importer.Path.exists", return_value=True)
    def test_scan_workload(self, mock_exists, mock_zip):
        mock_zip_instance = mock_zip.return_value.__enter__.return_value
        mock_zip_instance.namelist.return_value = ["xl/workbook.xml"]
        mock_zip_instance.read.return_value = b'name="2024" name="2025"'
        
        sheets, files = ExcelImporter.scan_workload("dummy.xlsx", "")
        assert sheets == 2
        assert files == 0