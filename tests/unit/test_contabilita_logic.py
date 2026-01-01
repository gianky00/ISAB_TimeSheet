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
        mock_xl_instance.sheet_names = ['2023']
        mock_excel_file.return_value = mock_xl_instance
        
        # Prepare Data
        columns = [
            'DATA PREV.', 'MESE', 'N°PREV.', 'TOTALE PREV.', "ATTIVITA'", 'TCL', 'ODC',
            "STATO ATTIVITA'", 'TIPOLOGIA', 'ORE SP', 'RESA', 'ANNOTAZIONI',
            'INDIRIZZO CONSUNTIVO', 'NOME FILE'
        ]
        row_data = [
            '2023-01-01', 'Gennaio', '100', 1000.50, 'Activity', 'TCL1', 'ODC1',
            'Aperta', 'Tipo1', 10.0, 100.0, 'Note', 'path', 'file.pdf'
        ]
        
        # 1. Preview DF (header detection)
        # Needs to contain the headers in the body to be detected by iterrows
        preview_data = [columns] + [row_data]
        preview_df = pd.DataFrame(preview_data)
        
        # 2. Full DF (actual data)
        full_df = pd.DataFrame([row_data], columns=columns)
        
        # Side effect for read_excel calls
        mock_read_excel.side_effect = [preview_df, full_df]
        
        with patch('src.core.contabilita_manager.Path.exists', return_value=True):
             success, msg, added, removed = ContabilitaManager.import_data_from_excel("dummy.xlsx")
        
        if not success:
            print(f"Import failed with: {msg}")
            
        assert success is True
        assert added == 1

    @patch('src.core.contabilita_manager.pd.read_sql_query') # Patch read_sql_query for lookup
    @patch('src.core.contabilita_manager.pd.read_excel')
    def test_import_giornaliere(self, mock_read_excel, mock_read_sql, mock_db):
        # Mock Lookup DF (prevents DB error)
        mock_read_sql.return_value = pd.DataFrame(columns=['n_prev', 'odc'])

        # Mock DataFrame
        data = {
            'DATA': ['2023-01-01'],
            'PERSONALE': ['Mario Rossi'],
            "DESCRIZIONE ATTIVITA'": ['Lavoro'],
            'TCL': ['TCL1'],
            'ODC': ['ODC1'],
            'N° PDL': ['PDL1'],
            'INIZIO': ['08:00'],
            'FINE': ['17:00'],
            'ORE': [8],
            'consuntivo': ['100']
        }
        df = pd.DataFrame(data)
        mock_read_excel.return_value = df

        # Mock scan_workload
        with patch('src.core.contabilita_manager.ContabilitaManager.scan_workload', return_value=(1, 1)):
             # Mock Path.iterdir by creating real temp structure or strict mocking
             # Let's use strict mocking of Path
             with patch('src.core.contabilita_manager.Path') as MockPath:
                 # Instance for giornaliere_path
                 mock_path_inst = MockPath.return_value
                 mock_path_inst.exists.return_value = True
                 
                 # Mock Year Dir
                 mock_year_dir = MagicMock()
                 mock_year_dir.is_dir.return_value = True
                 mock_year_dir.name = "Giornaliere 2023"
                 
                 # Mock File
                 mock_file = MagicMock()
                 mock_file.name = "file.xlsx"
                 
                 mock_year_dir.glob.return_value = [mock_file]
                 
                 mock_path_inst.iterdir.return_value = [mock_year_dir]
                 
                 success, msg, added, removed = ContabilitaManager.import_giornaliere("dummy_folder")
                 
        assert success is True
        assert added == 1

    def test_scan_workload(self, tmp_path):
        # Use real temporary directory
        d = tmp_path / "dummy_dir"
        d.mkdir()
        
        f = tmp_path / "dummy_file.xlsx"
        f.touch()
        
        with patch('zipfile.ZipFile') as MockZip:
            z = MockZip.return_value
            z.__enter__.return_value = z
            z.namelist.return_value = ['xl/workbook.xml']
            z.read.return_value = b'name="Sheet1" name="2023" name="Dati"'
            
            sheets, files = ContabilitaManager.scan_workload(str(f), str(d))
            
            assert sheets == 1
            assert files == 0 # No files in empty dir
