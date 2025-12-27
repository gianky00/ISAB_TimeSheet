
import unittest
from unittest.mock import MagicMock, patch, ANY
import pandas as pd
from src.core.contabilita_manager import ContabilitaManager

class TestContabilitaImport(unittest.TestCase):

    @patch('src.core.contabilita_manager.db_manager')
    @patch('src.core.contabilita_manager.pd.ExcelFile')
    @patch('src.core.contabilita_manager.pd.read_excel')
    @patch('src.core.contabilita_manager.Path.exists')
    def test_import_preventivi_dynamic_header(self, mock_exists, mock_read_excel, mock_excel_file, mock_db_manager):
        # Setup mocks
        mock_exists.return_value = True

        # Mock ExcelFile and sheet names
        mock_xls_instance = MagicMock()
        mock_xls_instance.sheet_names = ["2025"]
        mock_excel_file.return_value = mock_xls_instance

        # Mock DB connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock fetchall for existing rows (return empty)
        mock_cursor.fetchall.return_value = []

        # 1. Preview DataFrame (simulate header at row 1, i.e., index 1)
        # Row 0: Garbage
        # Row 1: Valid Headers: DATA PREV., MESE, N°PREV., TOTALE PREV., ATTIVITA', ...
        preview_data = [
            ["Info", "Misc", "", "", ""], # Row 0
            ["DATA PREV.", "MESE", "N°PREV.", "TOTALE PREV.", "ATTIVITA'", "ODC"] # Row 1 (Target)
        ]
        preview_df = pd.DataFrame(preview_data)

        # 2. Real Data DataFrame (read with header=1)
        # We need at least 2 rows because the logic drops the last one (Total row)
        data_rows = [
            ["2025-01-01", "Gennaio", "P2025/001", "1000", "Test Activity", "5400123"], # Row to keep
            ["", "", "Totale", "1000", "", ""] # Row to drop
        ]
        real_df = pd.DataFrame(data_rows, columns=["DATA PREV.", "MESE", "N°PREV.", "TOTALE PREV.", "ATTIVITA'", "ODC"])

        # Configure side_effect for read_excel
        # First call: Preview (nrows=10)
        # Second call: Real read (header=1)
        def read_excel_side_effect(*args, **kwargs):
            if kwargs.get('nrows') == 10:
                return preview_df
            return real_df

        mock_read_excel.side_effect = read_excel_side_effect

        # Execute
        result, msg, added, removed = ContabilitaManager.import_data_from_excel("dummy.xlsx")

        # Assertions
        self.assertTrue(result, f"Import failed: {msg}")
        self.assertEqual(added, 1) # Should import 1 row (the first one)

        # Check if executemany was called with correct data mapping
        # We expect normalization:
        # 'DATA PREV.' -> 'data_prev'
        # 'N°PREV.' -> 'n_prev'
        # 'ATTIVITA'' -> 'attivita'

        # Verify the SQL Insert contains the normalized column names
        args, _ = mock_cursor.executemany.call_args
        sql_query = args[0]

        self.assertIn("data_prev", sql_query)
        self.assertIn("n_prev", sql_query)
        self.assertIn("attivita", sql_query)

        print(f"\nImport Result: {msg}")

if __name__ == '__main__':
    unittest.main()
