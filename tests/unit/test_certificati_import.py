import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.core.contabilita_manager import ContabilitaManager


class TestCertificatiImport(unittest.TestCase):
    @patch("src.core.excel_importer.pd.read_sql")
    @patch("src.core.excel_importer.pd.ExcelFile")
    @patch("src.core.excel_importer.pd.read_excel")
    @patch("src.core.excel_importer.Path.exists")
    def test_import_certificati_dynamic_header(
        self, mock_exists, mock_read_excel, mock_excel_file, mock_read_sql
    ):
        # Setup mocks
        mock_exists.return_value = True

        # Mock ExcelFile and sheet names
        mock_xls_instance = MagicMock()
        mock_xls_instance.sheet_names = ["Strumenti Campione ISAB SUD", "Other Sheet"]
        mock_excel_file.return_value = mock_xls_instance

        # Mock read_sql for existing rows (return empty)
        mock_read_sql.return_value = pd.DataFrame()

        with patch(
            "src.core.data_synchronizer.DataSynchronizer.sync_certificati_campione"
        ) as mock_sync:
            mock_sync.return_value = (1, 0)

            # 1. Preview DataFrame (simulate header at row 5)
            # Row 0-4: Garbage
            # Row 5: Valid Headers: Modello / Tipo, Costruttore, Matricola...
            preview_data = [
                ["Garbage"] * 5,
                ["Garbage"] * 5,
                ["Garbage"] * 5,
                ["Garbage"] * 5,
                ["Garbage"] * 5,
                [
                    "Modello / Tipo",
                    "Costruttore",
                    "Matricola",
                    "Range Strumento",
                    "Errore max %",
                ],  # Row 5
            ]
            preview_df = pd.DataFrame(preview_data)

            # 2. Real Data DataFrame (read with header=5)
            data_rows = [
                ["Modello A", "Costruttore B", "12345", "0-100", "1%"],
            ]
            real_df = pd.DataFrame(
                data_rows,
                columns=[
                    "Modello / Tipo",
                    "Costruttore",
                    "Matricola",
                    "Range Strumento",
                    "Errore max %",
                ],
            )
            real_df["Scadenza Certificato"] = (
                "2025-12-31"  # Add other cols to satisfy mapping if strictly needed or if they are just optional
            )
            real_df["Emissione Certificato"] = "2025-01-01"
            real_df["ID-COEMI"] = "ID001"
            real_df["Stato Certificato"] = "Valido"
            real_df["Certificato Taratura"] = "CERT-001"

            # Configure side_effect for read_excel
            # First call: Preview (nrows=20)
            # Second call: Real read (header=5)
            def read_excel_side_effect(*args, **kwargs):
                if kwargs.get("nrows") == 20:
                    return preview_df
                return real_df

            mock_read_excel.side_effect = read_excel_side_effect

            # Execute
            (
                result,
                msg,
                added,
                removed,
            ) = ContabilitaManager.import_certificati_campione("dummy.xlsx")

            # Assertions
            self.assertTrue(result, f"Import failed: {msg}")
            self.assertEqual(added, 1)  # Should import 1 row

            # Verify that it picked the correct sheet
            # mock_read_excel.call_args_list[0] is preview
            # mock_read_excel.call_args_list[1] is real read
            args, kwargs = mock_read_excel.call_args_list[1]
            self.assertEqual(kwargs["sheet_name"], "Strumenti Campione ISAB SUD")
            self.assertEqual(kwargs["header"], 5)


if __name__ == "__main__":
    unittest.main()
