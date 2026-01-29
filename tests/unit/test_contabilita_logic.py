from unittest.mock import ANY, MagicMock, patch

import pandas as pd
import pytest

from src.core.contabilita_manager import ContabilitaManager


class TestContabilitaLogic:
    @pytest.fixture(autouse=True)
    def mock_db(self):
        with (
            patch("src.core.contabilita_manager.db_manager") as mock1,
            patch("src.core.data_synchronizer.db_manager") as mock2,
        ):
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor

            mock1.get_connection.return_value.__enter__.return_value = mock_conn
            mock1.get_connection.return_value.__exit__.return_value = None
            mock2.get_connection.return_value.__enter__.return_value = mock_conn
            mock2.get_connection.return_value.__exit__.return_value = None

            # Ensure SELECT returns an empty list for existence checks
            mock_cursor.fetchall.return_value = []
            yield mock1

    @patch("src.core.contabilita_manager.DataSynchronizer.sync_contabilita_dati")
    @patch("src.core.excel_importer.pd.read_sql")
    @patch("src.core.excel_importer.pd.read_excel")
    @patch("src.core.excel_importer.pd.ExcelFile")
    def test_import_data_success(self, mock_excel_file, mock_read_excel, mock_read_sql, mock_sync, mock_db):
        """Test importazione contabilità con successo."""
        # 1. Mock Excel File structure
        mock_file_instance = MagicMock()
        mock_file_instance.sheet_names = ["Dati 2024"]
        # Fix: The code uses ExcelFile as a constructor, not context manager
        mock_excel_file.return_value = mock_file_instance

        # 2. Mock DataFrame content
        cols = [
            "Data Prev",
            "Mese",
            "N° Prev",
            "Totale Prev",
            "Descrizione Attività",
            "TCL",
            "ODC",
            "Stato Attività",
            "Tipologia",
            "Ore SP",
            "Resa",
            "Annotazioni",
            "Indirizzo Consuntivo",
        ]
        # Create valid rows (Need at least 2 rows because logic drops last row as Total)
        data = {c: ["val", "val_total"] for c in cols}
        data["Data Prev"] = ["2024-01-01", "Totale"]
        data["N° Prev"] = ["100/2024", ""]
        df = pd.DataFrame(data)

        mock_read_excel.return_value = df

        # 3. Mock SQL return (Empty existing data)
        db_cols = ["year"] + [
            "data_prev",
            "mese",
            "n_prev",
            "totale_prev",
            "attivita",
            "tcl",
            "odc",
            "stato_attivita",
            "tipologia",
            "ore_sp",
            "resa",
            "annotazioni",
            "indirizzo_consuntivo",
            "nome_file",
        ]
        mock_read_sql.return_value = pd.DataFrame(columns=db_cols)
        mock_sync.return_value = (1, 0)

        # 4. Call import
        with patch("pathlib.Path.exists", return_value=True):
            success, msg, added, removed = ContabilitaManager.import_data_from_excel(
                "C:/Fake/Contabilita_2024.xlsx"
            )

        assert success is True
        assert "importati" in msg.lower()
        assert "2024" in msg

    @patch("src.core.contabilita_manager.DataSynchronizer")
    @patch("src.core.contabilita_manager.ExcelImporter")
    def test_import_giornaliere(self, mock_excel_importer, mock_data_synchronizer, mock_db):
        # Mock ExcelImporter.import_giornaliere
        imported_rows = [
            (
                2023,
                "2023-01-01",
                "U",
                "D",
                "T",
                "O",
                "P",
                "08",
                "17",
                8,
                "100",
                "file.xlsx",
            ),
        ]
        imported_years = [2023]
        mock_excel_importer.import_giornaliere.return_value = (
            True,
            "Import successful",
            imported_rows,
            imported_years,
        )

        # Mock DataSynchronizer.sync_giornaliere
        mock_data_synchronizer.sync_giornaliere.return_value = (1, 0)

        with patch("src.core.contabilita_manager.Path") as MockPath:
            path_inst = MockPath.return_value
            path_inst.exists.return_value = True

            success, msg, added, removed = ContabilitaManager.import_giornaliere("dummy_folder")

        assert success is True
        assert added == 1
        assert removed == 0
        mock_excel_importer.import_giornaliere.assert_called_once_with("dummy_folder", ANY, ANY)
        mock_data_synchronizer.sync_giornaliere.assert_called_once_with(
            ContabilitaManager.DB_PATH, imported_rows, imported_years
        )

    def test_scan_workload(self, tmp_path):
        d = tmp_path / "dummy_dir"
        d.mkdir()
        f = tmp_path / "dummy_file.xlsx"
        f.touch()

        with patch("zipfile.ZipFile") as MockZip:
            z = MockZip.return_value
            z.__enter__.return_value = z
            z.namelist.return_value = ["xl/workbook.xml"]
            z.read.return_value = b'name="2023"'

            sheets, files = ContabilitaManager.scan_workload(str(f), str(d))
            assert sheets == 1
