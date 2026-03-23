import unittest
from unittest.mock import ANY, patch

from src.core.contabilita_manager import ContabilitaManager


class TestContabilitaImport(unittest.TestCase):
    @patch("src.core.contabilita_manager.DataSynchronizer")
    @patch("src.core.contabilita_manager.ExcelImporter")
    @patch("src.core.contabilita_manager.Path.exists")
    def test_import_preventivi_dynamic_header(self, mock_exists, mock_excel_importer, mock_data_synchronizer):  # noqa: ANN001
        # Setup mocks
        mock_exists.return_value = True

        # Mock ExcelImporter.import_contabilita_dati per restituire dati fittizi
        imported_rows = [
            (
                2025,
                "2025-01-01",
                "Gennaio",
                "P2025/001",
                "1000",
                "Test Activity",
                "",
                "5400123",
                "Attiva",
                "Tipo",
                "10",
                "Resa",
                "Note",
                "file.xlsx",
            ),
        ]
        imported_years = [2025]
        mock_excel_importer.import_contabilita_dati.return_value = (
            True,
            "Import successful",
            imported_rows,
            imported_years,
        )

        # Mock DataSynchronizer.sync_contabilita_dati
        mock_data_synchronizer.sync_contabilita_dati.return_value = (
            1,
            0,
        )  # 1 aggiunto, 0 rimosso

        # Execute
        result, msg, added, removed = ContabilitaManager.import_data_from_excel("dummy.xlsx")

        # Assertions
        self.assertTrue(result, f"Import failed: {msg}")
        self.assertEqual(added, 1)  # Dovrebbe importare 1 riga
        self.assertEqual(removed, 0)

        # Verifica che ExcelImporter.import_contabilita_dati sia stato chiamato
        mock_excel_importer.import_contabilita_dati.assert_called_once_with("dummy.xlsx", ANY)

        # Verifica che DataSynchronizer.sync_contabilita_dati sia stato chiamato con i dati corretti
        mock_data_synchronizer.sync_contabilita_dati.assert_called_once_with(
            ContabilitaManager.DB_PATH, imported_rows, imported_years
        )

        print(f"\nImport Result: {msg}")


if __name__ == "__main__":
    unittest.main()
