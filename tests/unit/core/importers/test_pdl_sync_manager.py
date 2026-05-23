from unittest.mock import MagicMock, patch

import pytest

from src.core.importers.pdl_sync_manager import ProgrammingSyncManager


class TestProgrammingSyncManager:
    @pytest.fixture
    def manager(self):
        with patch("src.core.importers.pdl_sync_manager._win32com_found", True):
            return ProgrammingSyncManager("C:\\Master.xlsm")

    @patch("win32com.client.GetActiveObject")
    @patch("win32com.client.DispatchEx")
    def test_get_excel_workbook_active(self, mock_dispatch, mock_get, manager):
        mock_app = MagicMock()
        mock_wb = MagicMock()
        mock_wb.Name = "Master.xlsm"
        mock_app.Workbooks = [mock_wb]
        mock_get.return_value = mock_app
        res = manager._get_excel_workbook()
        assert res is True
        assert manager.wb_master == mock_wb
        assert manager._is_already_open is True

    @patch("win32com.client.GetActiveObject", side_effect=Exception("No excel"))
    @patch("win32com.client.DispatchEx")
    def test_get_excel_workbook_new(self, mock_dispatch, mock_get, manager):
        mock_app = MagicMock()
        mock_wb = MagicMock()
        mock_app.Workbooks.Open.return_value = mock_wb
        mock_dispatch.return_value = mock_app
        res = manager._get_excel_workbook()
        assert res is True
        assert manager.wb_master == mock_wb
        assert manager._is_already_open is False

    def test_run_sync_macros(self, manager):
        manager.excel_app = MagicMock()
        manager.wb_master = MagicMock()
        manager.wb_master.Name = "Master.xlsm"
        manager.run_sync_macros()
        assert manager.excel_app.Run.called

    @patch("openpyxl.load_workbook")
    def test_analyze_downloaded_file(self, mock_load, manager):
        mock_wb = MagicMock()
        mock_ws = MagicMock()
        mock_wb.active = mock_ws
        mock_load.return_value = mock_wb
        row_new = ["PDL_NEW"] + [None] * 20
        row_new[14] = "Richiesto"
        row_old = ["PDL_OLD"] + [None] * 20
        row_old[3] = "SI"
        row_old[14] = "Eseguito"
        mock_ws.iter_rows.return_value = [row_new, row_old]
        mappa_pdl = {"PDL_OLD": {"foglio": "A1", "riga": 10, "stato": "RICHIESTO"}}
        nuovi, modif_x, modif_stato = manager._analyze_downloaded_file("report.xlsx", mappa_pdl)
        assert "PDL_NEW" in nuovi
        assert "PDL_OLD" in modif_x
        assert modif_x["PDL_OLD"][8] == "X"
        assert modif_stato["PDL_OLD"] == "EMESSO"

    def test_prepare_excel_state(self, manager):
        manager.excel_app = MagicMock()
        manager.excel_app.Calculation = 1
        manager._prepare_excel_state(True)
        assert manager.excel_app.ScreenUpdating is False
        manager._prepare_excel_state(False)
        assert manager.excel_app.ScreenUpdating is True

    def test_cleanup(self, manager):
        mock_app = MagicMock()
        mock_wb = MagicMock()
        manager.excel_app = mock_app
        manager.wb_master = mock_wb
        manager._is_already_open = False

        manager.cleanup()

        assert mock_wb.Close.called
        assert mock_app.Quit.called
        assert manager.excel_app is None
