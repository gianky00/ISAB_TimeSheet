
import unittest
from unittest.mock import MagicMock, patch, ANY
import pandas as pd
from src.core.contabilita_manager import ContabilitaManager

class TestCertificatiImport(unittest.TestCase):

    @patch('src.core.contabilita_manager.db_manager')
    @patch('src.core.contabilita_manager.pd.ExcelFile')
    @patch('src.core.contabilita_manager.pd.read_excel')
    @patch('src.core.contabilita_manager.Path.exists')
    def test_import_certificati_dynamic_header(self, mock_exists, mock_read_excel, mock_excel_file, mock_db_manager):
        # Setup mocks
        mock_exists.return_value = True

        # Mock ExcelFile and sheet names
        mock_xls_instance = MagicMock()
        mock_xls_instance.sheet_names = ["Strumenti Campione ISAB SUD", "Other Sheet"]
        mock_excel_file.return_value = mock_xls_instance

        # Mock DB connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock read_sql for existing rows (return empty)
        with patch('src.core.contabilita_manager.pd.read_sql') as mock_read_sql:
            mock_read_sql.return_value = pd.DataFrame()

            # 1. Preview DataFrame (simulate header at row 5)
            # Row 0-4: Garbage
            # Row 5: Valid Headers: Modello / Tipo, Costruttore, Matricola...
            preview_data = [
                ["Garbage"] * 5,
                ["Garbage"] * 5,
                ["Garbage"] * 5,
                ["Garbage"] * 5,
                ["Garbage"] * 5,
                ["Modello / Tipo", "Costruttore", "Matricola", "Range Strumento", "Errore max %"] # Row 5
            ]
            preview_df = pd.DataFrame(preview_data)

            # 2. Real Data DataFrame (read with header=5)
            data_rows = [
                ["Modello A", "Costruttore B", "12345", "0-100", "1%"],
            ]
            real_df = pd.DataFrame(data_rows, columns=["Modello / Tipo", "Costruttore", "Matricola", "Range Strumento", "Errore max %"])
            real_df["Scadenza Certificato"] = "2025-12-31" # Add other cols to satisfy mapping if strictly needed or if they are just optional
            real_df["Emissione Certificato"] = "2025-01-01"
            real_df["ID-COEMI"] = "ID001"
            real_df["Stato Certificato"] = "Valido"
            real_df["Certificato Taratura"] = "CERT-001"

            # Configure side_effect for read_excel
            # First call: Preview (nrows=20)
            # Second call: Real read (header=5)
            def read_excel_side_effect(*args, **kwargs):
                if kwargs.get('nrows') == 20:
                    return preview_df
                return real_df

            mock_read_excel.side_effect = read_excel_side_effect

            # Execute
            result, msg, added, removed = ContabilitaManager.import_certificati_campione("dummy.xlsx")

            # Assertions
            self.assertTrue(result, f"Import failed: {msg}")
            self.assertEqual(added, 1) # Should import 1 row

            # Verify that it picked the correct sheet
            # mock_read_excel.call_args_list[0] is preview
            # mock_read_excel.call_args_list[1] is real read
            args, kwargs = mock_read_excel.call_args_list[1]
            self.assertEqual(kwargs['sheet_name'], "Strumenti Campione ISAB SUD")
            self.assertEqual(kwargs['header'], 5)

if __name__ == '__main__':
    unittest.main()
