import pytest
import pandas as pd
import os
from unittest.mock import MagicMock, patch
from src.core.contabilita_manager import ContabilitaManager

class TestContabilitaLogic:

    @pytest.fixture
    def mock_db(self):
        with patch('src.core.contabilita_manager.db_manager') as mock:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock.get_connection.return_value.__enter__.return_value = mock_conn
            mock.get_connection.return_value.__exit__.return_value = None
            yield mock

    @patch('src.core.contabilita_manager.pd.read_excel')
    @patch('src.core.contabilita_manager.pd.ExcelFile')
    def test_import_data_success(self, mock_excel_file, mock_read_excel, mock_db):
        # Setup ExcelFile
        mock_xl_instance = MagicMock()
        mock_xl_instance.sheet_names = ['2023'] # Valid year sheet
        mock_excel_file.return_value = mock_xl_instance
        
        # Column names matching COLUMNS_MAPPING
        columns = [
            'DATA PREV.', 'MESE', 'N°PREV.', 'TOTALE PREV.', "ATTIVITA'", 'TCL', 'ODC',
            "STATO ATTIVITA'", 'TIPOLOGIA', 'ORE SP', 'RESA', 'ANNOTAZIONI',
            'INDIRIZZO CONSUNTIVO', 'NOME FILE'
        ]
        
        # 1. Preview DF (read_excel with header=None)
        # We put headers in row 1 (index 1) to match header_row_idx logic
        preview_rows = [
            ["Some Title"], 
            columns, 
            ['2023-01-01', 'Gennaio', '100', 1000.50, 'A', 'T', 'O', 'S', 'T', 10, 100, 'N', 'P', 'F']
        ]
        preview_df = pd.DataFrame(preview_rows)
        
        # 2. Data DF (read_excel with header=1)
        data_df = pd.DataFrame([preview_rows[2]], columns=columns)
        
        # Setup side effect
        mock_read_excel.side_effect = [preview_df, data_df]
        
        with patch('src.core.contabilita_manager.Path.exists', return_value=True):
             # Ensure open() doesn't fail for the dummy path
             with patch('builtins.open', MagicMock()):
                  # Mock msoffcrypto if necessary or just skip decryption branch
                  with patch('src.core.contabilita_manager.msoffcrypto', None):
                       success, msg, added, removed = ContabilitaManager.import_data_from_excel("dummy.xlsx")
        
        if not success:
            print(f"Import failed with: {msg}")
            
        assert success is True
        assert added >= 0

    @patch('src.core.contabilita_manager.pd.read_sql_query')
    @patch('src.core.contabilita_manager.pd.read_excel')
    def test_import_giornaliere(self, mock_read_excel, mock_read_sql, mock_db):
        mock_read_sql.return_value = pd.DataFrame(columns=['n_prev', 'odc'])
        
        # RIASSUNTO sheet data
        cols = ['DATA', 'PERSONALE', "DESCRIZIONE ATTIVITA'", 'TCL', 'ODC', 'N° PDL', 'INIZIO', 'FINE', 'ORE', 'consuntivo']
        row = ['2023-01-01', 'U', 'D', 'T', 'O', 'P', '08', '17', 8, '100']
        mock_read_excel.return_value = pd.DataFrame([row], columns=cols)

        with patch('src.core.contabilita_manager.ContabilitaManager.scan_workload', return_value=(1, 1)):
             with patch('src.core.contabilita_manager.Path') as MockPath:
                 path_inst = MockPath.return_value
                 path_inst.exists.return_value = True
                 
                 year_dir = MagicMock()
                 year_dir.is_dir.return_value = True
                 year_dir.name = "Giornaliere 2023"
                 year_dir.glob.return_value = [MagicMock(name="file.xlsx")]
                 
                 path_inst.iterdir.return_value = [year_dir]
                 
                 success, msg, added, removed = ContabilitaManager.import_giornaliere("dummy_folder")
                 
        assert success is True

    def test_scan_workload(self, tmp_path):
        d = tmp_path / "dummy_dir"
        d.mkdir()
        f = tmp_path / "dummy_file.xlsx"
        f.touch()
        
        with patch('zipfile.ZipFile') as MockZip:
            z = MockZip.return_value
            z.__enter__.return_value = z
            z.namelist.return_value = ['xl/workbook.xml']
            z.read.return_value = b'name="2023"'
            
            sheets, files = ContabilitaManager.scan_workload(str(f), str(d))
            assert sheets == 1