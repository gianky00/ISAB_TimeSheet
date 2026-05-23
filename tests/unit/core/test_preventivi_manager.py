import zipfile
from unittest.mock import MagicMock, patch

import pytest

from src.core.preventivi_manager import PreventiviGeneratorManager


class TestPreventiviManager:
    @pytest.fixture
    def manager(self):
        with patch("src.core.preventivi_manager._win32com_found", True):
            return PreventiviGeneratorManager("template.xlsm")

    def test_get_next_progressive(self, manager, fs):
        fs.create_dir("/quotes")
        fs.create_file("/quotes/001-26.xlsm")
        fs.create_file("/quotes/005-26.xlsm")

        res = manager.get_next_progressive("/quotes")
        assert res == "006"

    def test_get_next_progressive_empty(self, manager, fs):
        res = manager.get_next_progressive("/nonexistent")
        assert res == "001"

    @patch("src.core.preventivi_manager.win32com.client.Dispatch")
    @patch("src.core.preventivi_manager.pythoncom.CoInitialize")
    @patch("src.core.preventivi_manager.pythoncom.CoUninitialize")
    def test_read_existing_data(self, mock_uninit, mock_init, mock_dispatch, manager, fs):
        fs.create_file("existing.xlsm")
        mock_app = MagicMock()
        mock_wb = MagicMock()
        mock_sheet = MagicMock()
        mock_dispatch.return_value = mock_app
        mock_app.Workbooks.Open.return_value = mock_wb
        mock_wb.Sheets.side_effect = lambda n: mock_sheet

        # Setup mock data in ranges
        mock_sheet.Range.return_value.Value = "some_value"

        data = manager.read_existing_data("existing.xlsm")
        assert "data" in data
        assert mock_app.Workbooks.Open.called

    def test_sanitize_excel_file(self, manager, fs):
        # Creiamo un file zip (excel) finto
        excel_path = "/test.xlsm"
        with zipfile.ZipFile(excel_path, "w") as z:
            z.writestr(
                "xl/workbook.xml", '<workbook><definedName name="Print_Area">corrupt</definedName></workbook>'
            )

        manager._sanitize_excel_file(excel_path)

        # Verifichiamo che Print_Area sia rimosso
        with zipfile.ZipFile(excel_path, "r") as z:
            xml = z.read("xl/workbook.xml").decode("utf-8")
            assert "Print_Area" not in xml

    @patch("src.core.preventivi_manager.shutil.copy2")
    @patch("src.core.preventivi_manager.PreventiviGeneratorManager._fill_excel_data")
    @patch("src.core.preventivi_manager.PreventiviGeneratorManager._sanitize_excel_file")
    def test_generate_preventivo_success(self, mock_sanitize, mock_fill, mock_copy, manager, fs):
        mock_fill.return_value = (True, "OK")

        data = {"progressivo": "010", "anno_short": "26"}
        success, res = manager.generate_preventivo(data, "/output")

        assert success is True
        assert "010-26.xlsm" in res
        assert mock_copy.called
        assert mock_sanitize.called
