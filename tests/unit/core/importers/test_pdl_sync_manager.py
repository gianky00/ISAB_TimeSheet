from unittest.mock import MagicMock, patch

from src.core.importers.pdl_sync_manager import ProgrammingSyncManager


class TestProgrammingSyncManager:
    @patch("src.core.importers.pdl_sync_manager.win32com.client")
    @patch("src.core.importers.pdl_sync_manager._win32com_found", True)
    def test_get_excel_workbook_new_instance(self, mock_win32, tmp_path):
        """Testa l'apertura di una nuova istanza Excel."""
        master_file = tmp_path / "master.xlsx"
        master_file.touch()

        manager = ProgrammingSyncManager(str(master_file))

        # Simula fallimento GetActiveObject e successo DispatchEx
        mock_win32.GetActiveObject.side_effect = Exception("Not found")
        mock_app = mock_win32.DispatchEx.return_value

        success = manager._get_excel_workbook()

        assert success is True
        assert mock_win32.DispatchEx.called
        assert manager.excel_app == mock_app
        assert not manager._is_already_open

    @patch("src.core.importers.pdl_sync_manager._win32com_found", True)
    def test_run_sync_macros(self):
        """Testa l'esecuzione delle macro."""
        manager = ProgrammingSyncManager("fake.xlsx")
        manager.excel_app = MagicMock()
        manager.wb_master = MagicMock()
        manager.wb_master.Name = "Master"

        manager.run_sync_macros()

        assert manager.excel_app.Run.call_count == 3
        manager.excel_app.Run.assert_any_call("'Master'!PulisciNomiDefiniti")

    @patch("src.core.importers.pdl_sync_manager._win32com_found", True)
    def test_prepare_excel_state(self):
        """Testa l'impostazione dello stato di ottimizzazione Excel."""
        manager = ProgrammingSyncManager("fake.xlsx")
        manager.excel_app = MagicMock()
        manager.excel_app.Calculation = 1  # xlCalculationAutomatic

        manager._prepare_excel_state(True)
        assert manager.excel_app.Calculation == -4135  # xlCalculationManual
        assert manager.excel_app.ScreenUpdating is False

        manager._prepare_excel_state(False)
        assert manager.excel_app.Calculation == 1
        assert manager.excel_app.ScreenUpdating is True

    @patch("src.core.importers.pdl_sync_manager._win32com_found", True)
    def test_cleanup(self):
        """Testa la chiusura di Excel."""
        manager = ProgrammingSyncManager("fake.xlsx")
        mock_app = MagicMock()
        manager.excel_app = mock_app
        manager.wb_master = MagicMock()
        manager._is_already_open = False

        manager.cleanup()
        assert manager.wb_master.Close.called
        assert mock_app.Quit.called
        assert manager.excel_app is None

    @patch("src.core.importers.pdl_sync_manager.openpyxl")
    @patch("src.core.importers.pdl_sync_manager._win32com_found", True)
    def test_analyze_downloaded_file_empty(self, mock_openpyxl):
        """Testa l'analisi di un file scaricato vuoto."""
        manager = ProgrammingSyncManager("fake.xlsx")
        mock_wb = mock_openpyxl.load_workbook.return_value
        mock_wb.active = None

        nuovi, mod_x, mod_st = manager._analyze_downloaded_file("report.xlsx", {})
        assert nuovi == {}
        assert mod_x == {}
        assert mod_st == {}
