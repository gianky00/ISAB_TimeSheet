from unittest.mock import MagicMock, patch

import pandas as pd

from src.core.importers.contabilita import ContabilitaImporter


class TestContabilitaImporter:
    def test_scan_sheets_not_exists(self):
        assert ContabilitaImporter.scan_sheets("/non/existent.xlsx") == 0

    @patch("src.core.importers.contabilita.zipfile.is_zipfile", return_value=True)
    @patch("src.core.importers.contabilita.zipfile.ZipFile")
    def test_scan_sheets_success(self, mock_zip, mock_iszip, fs):
        fs.create_file("test.xlsx")
        # Simula workbook.xml con nomi fogli YYYY
        mock_z = MagicMock()
        mock_z.namelist.return_value = ["xl/workbook.xml"]
        xml_content = b'<workbook><sheets><sheet name="2022" /><sheet name="2023" /><sheet name="Other" /></sheets></workbook>'
        mock_z.read.return_value = xml_content
        mock_zip.return_value.__enter__.return_value = mock_z

        assert ContabilitaImporter.scan_sheets("test.xlsx") == 2

    @patch("src.core.importers.contabilita.ContabilitaImporter._get_excel_file")
    def test_import_contabilita_dati_success(self, mock_get_xls, fs):
        fs.create_file("test.xlsx")
        mock_xls = MagicMock()
        mock_xls.sheet_names = ["2023"]
        mock_get_xls.return_value = mock_xls

        # Mock single sheet processing
        rows = [
            (
                2023,
                "2023-01-01",
                "GEN",
                "1",
                1000.0,
                "ACT",
                "TCL",
                "ODC",
                "OK",
                "T1",
                8,
                "1.0",
                "NOTE",
                "URL",
                "FILE",
            )
        ]
        with patch.object(ContabilitaImporter, "_process_single_sheet", return_value=rows):
            success, _msg, all_rows, years = ContabilitaImporter.import_contabilita_dati("test.xlsx")
            assert success is True
            assert 2023 in years
            assert len(all_rows) == 1

    def test_clean_numeric(self):
        assert ContabilitaImporter._clean_numeric("1.234,56") == 1234.56
        assert ContabilitaImporter._clean_numeric("1234.56") == 1234.56
        assert ContabilitaImporter._clean_numeric("1234,56") == 1234.56
        assert ContabilitaImporter._clean_numeric("") == 0.0
        assert ContabilitaImporter._clean_numeric(None) == 0.0

    def test_clean_resa_value(self):
        assert ContabilitaImporter._clean_resa_value("1,5") == "1.5"
        assert ContabilitaImporter._clean_resa_value("95%") == "95%"
        assert ContabilitaImporter._clean_resa_value("") == ""

    def test_find_header_row(self):
        xls = MagicMock()
        # Mock dataframe preview
        data = [
            ["Title", None, None],
            ["DATA PREV.", "MESE", "N PREV."],  # Header
            ["2023-01-01", "GEN", "1"],
        ]
        df_preview = pd.DataFrame(data)

        with patch("src.core.importers.contabilita.pd.read_excel", return_value=df_preview):
            idx = ContabilitaImporter._find_header_row(xls, "Sheet1")
            assert idx == 1

    def test_normalize_columns(self):
        df = pd.DataFrame(columns=["DATA PREV.", "ALTRO"])
        df = ContabilitaImporter._normalize_columns(df)
        assert "data_prev" in df.columns

    def test_ensure_required_columns(self):
        df = pd.DataFrame(columns=["data_prev"])
        df = ContabilitaImporter._ensure_required_columns(df)
        assert "tcl" in df.columns
        assert df["tcl"].iloc[0] == "" if not df.empty else True
