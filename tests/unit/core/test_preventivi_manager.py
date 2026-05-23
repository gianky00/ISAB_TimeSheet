import zipfile
from unittest.mock import patch

import pytest

from src.core.preventivi_manager import GeneratoreWorker, PreventiviGeneratorManager


class TestPreventiviManager:
    @pytest.fixture
    def manager(self):
        return PreventiviGeneratorManager("master.xlsm")

    def test_get_next_progressive_empty_dir(self, manager, fs):
        fs.create_dir("/preventivi")
        assert manager.get_next_progressive("/preventivi") == "001"

    def test_get_next_progressive_with_files(self, manager, fs):
        fs.create_dir("/preventivi")
        fs.create_file("/preventivi/001-23.xlsm")
        fs.create_file("/preventivi/005-23.xlsm")
        fs.create_file("/preventivi/note.txt")

        assert manager.get_next_progressive("/preventivi") == "006"

    def test_sanitize_excel_file_logic(self, manager, fs):
        # Simuliamo un file .xlsm (che è uno ZIP)
        xlsm_path = "/tmp/test.xlsm"
        fs.create_dir("/tmp")

        # Crea uno zip con workbook.xml corrotto (contenente Print_Area)
        content = '<workbook><definedName name="_xlnm.Print_Area">A1:B10</definedName><other>Data</other></workbook>'

        with zipfile.ZipFile(xlsm_path, "w") as z:
            z.writestr("xl/workbook.xml", content)
            z.writestr("other.xml", "data")

        manager._sanitize_excel_file(xlsm_path)

        # Verifica che Print_Area sia stato rimosso
        with zipfile.ZipFile(xlsm_path, "r") as z:
            xml = z.read("xl/workbook.xml").decode("utf-8")
            assert "Print_Area" not in xml
            assert "<other>Data</other>" in xml

    @patch("src.core.preventivi_manager.win32com.client.Dispatch")
    @patch("src.core.preventivi_manager.pythoncom.CoInitialize")
    @patch("src.core.preventivi_manager.pythoncom.CoUninitialize")
    @patch("src.core.preventivi_manager._win32com_found", True)
    def test_fill_excel_data_mock(self, mock_uninit, mock_init, mock_dispatch, manager, fs):
        fs.create_file("test.xlsm")
        mock_app = mock_dispatch.return_value
        mock_wb = mock_app.Workbooks.Open.return_value
        mock_sheet = mock_wb.Sheets.return_value

        data = {"data": "2023-01-01", "odc": "ODC123", "descrizione_lavoro": "Riga1\nRiga2"}

        success, _msg = manager._fill_excel_data("test.xlsm", data)

        assert success is True
        # Verifica iniezioni principali
        mock_sheet.Range.assert_any_call("A5")
        mock_sheet.Range.assert_any_call("B5")
        mock_sheet.Range.assert_any_call("A11")  # Prima riga descrizione
        mock_sheet.Range.assert_any_call("A12")  # Seconda riga descrizione

    @patch("src.core.preventivi_manager.PreventiviGeneratorManager.generate_preventivo")
    def test_generatore_worker_signals(self, mock_gen, qtbot):
        mock_gen.return_value = (True, "path/to/file.xlsm")

        worker = GeneratoreWorker("master.xlsm", {}, "out/")

        with qtbot.wait_signal(worker.finished_signal) as blocker:
            worker.start()

        assert blocker.args == [True, "path/to/file.xlsm"]
