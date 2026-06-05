from unittest.mock import MagicMock, patch

import pytest

from src.application.services.importers.pdl_sync_manager import ProgrammingSyncManager


class TestPdlSyncManager:
    @pytest.fixture
    def manager(self, fs):
        fs.create_file("master.xlsm")
        return ProgrammingSyncManager("master.xlsm")

    @patch("src.application.services.importers.pdl_sync_manager.win32com.client", create=True)
    def test_get_excel_workbook_new_instance(self, mock_win32, manager):
        mock_app = MagicMock()
        mock_win32.DispatchEx.return_value = mock_app
        mock_app.Workbooks.Open.return_value = MagicMock(Name="master.xlsm")
        mock_win32.GetActiveObject.side_effect = Exception("No active Excel")

        with patch("src.application.services.importers.pdl_sync_manager._win32com_found", True):
            assert manager._get_excel_workbook() is True
            assert manager.excel_app == mock_app

    def test_map_master_pdls(self, manager):
        manager.wb_master = MagicMock()

        def get_sheet(name):
            sh = MagicMock()
            sh.Name = name
            sh.Cells.return_value.End.return_value.Row = 4
            if name == "A1":
                sh.Range.return_value.Value = (
                    ("A", "B", "C", "D", "PDL1", "F", "G", "H", "I", "J", "K", "L", "EMESSO"),
                )
            else:
                sh.Range.return_value.Value = None
            return sh

        manager.wb_master.Sheets.side_effect = get_sheet
        mappa = manager._map_master_pdls()
        assert "PDL1" in mappa

    @patch("src.application.services.importers.pdl_sync_manager.openpyxl.load_workbook")
    def test_analyze_downloaded_file_mocked(self, mock_load, manager):
        mock_wb = MagicMock()
        mock_ws = MagicMock()
        mock_load.return_value = mock_wb
        mock_wb.active = mock_ws
        row = [""] * 21
        row[0] = "PDL1"
        row[3] = "si"
        row[14] = "Richiesto"
        mock_ws.iter_rows.return_value = [row]
        mappa_master = {"PDL1": {"stato": "EMESSO", "foglio": "A1", "riga": 4}}
        _nuovi, modif_x, _modif_stato = manager._analyze_downloaded_file("dummy.xlsx", mappa_master)
        assert "PDL1" in modif_x

    def test_run_sync_macros(self, manager):
        manager.excel_app = MagicMock()
        manager.wb_master = MagicMock(Name="master.xlsm")
        manager.run_sync_macros()
        assert manager.excel_app.Run.called

    def test_prepare_excel_state(self, manager):
        manager.excel_app = MagicMock()
        manager.excel_app.Calculation = 1

        manager._prepare_excel_state(True)
        assert manager.excel_app.ScreenUpdating is False

        manager._prepare_excel_state(False)
        assert manager.excel_app.ScreenUpdating is True

    @patch(
        "src.application.services.importers.pdl_sync_manager.ProgrammingSyncManager._get_excel_workbook",
        return_value=True,
    )
    @patch("src.application.services.importers.pdl_sync_manager.ProgrammingSyncManager._map_master_pdls")
    @patch(
        "src.application.services.importers.pdl_sync_manager.ProgrammingSyncManager._analyze_downloaded_file"
    )
    @patch(
        "src.application.services.importers.pdl_sync_manager.ProgrammingSyncManager._apply_modifications_to_master"
    )
    @patch("src.application.services.importers.pdl_sync_manager.ProgrammingSyncManager._insert_new_pdls")
    def test_process_downloaded_report_full(self, m_ins, m_app, m_ana, m_map, m_get, manager):  # noqa: PLR0913
        manager.excel_app = MagicMock()
        manager.wb_master = MagicMock()
        m_map.return_value = {}
        m_ana.return_value = ({"NEW": []}, {}, {})

        manager.process_downloaded_report("path.xlsx")

        assert m_map.called
        assert m_ana.called
        assert m_ins.called
        assert manager.wb_master.Save.called

    def test_cleanup(self, manager):
        mock_app = MagicMock()
        manager.excel_app = mock_app
        manager.wb_master = MagicMock()
        manager._is_already_open = False

        manager.cleanup()
        assert mock_app.Quit.called
        assert manager.excel_app is None

    @patch("src.application.services.importers.pdl_sync_manager.win32com.client", create=True)
    def test_get_excel_workbook_already_open(self, mock_win32, manager):
        mock_app = MagicMock()
        mock_win32.GetActiveObject.return_value = mock_app
        mock_wb = MagicMock(Name="master.xlsm")
        mock_app.Workbooks = [mock_wb]

        with patch("src.application.services.importers.pdl_sync_manager._win32com_found", True):
            assert manager._get_excel_workbook() is True
            assert manager.wb_master == mock_wb
            assert manager._is_already_open is True
