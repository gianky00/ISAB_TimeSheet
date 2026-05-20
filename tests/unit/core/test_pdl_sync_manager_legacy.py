from unittest.mock import MagicMock, patch

import pytest

from src.core.importers.pdl_sync_manager import ProgrammingSyncManager


class TestProgrammingSyncManager:
    @pytest.fixture
    def manager(self):
        return ProgrammingSyncManager("master.xlsx")

    @patch("src.core.importers.pdl_sync_manager.win32com.client")
    def test_get_excel_workbook_already_open(self, mock_win32, manager):
        """Verifica l'aggancio a un'istanza Excel già aperta."""
        mock_app = mock_win32.GetActiveObject.return_value
        mock_wb = MagicMock()
        mock_wb.Name = "master.xlsx"
        mock_app.Workbooks = [mock_wb]

        success = manager._get_excel_workbook()

        assert success is True
        assert manager._is_already_open is True
        assert manager.wb_master == mock_wb

    def test_map_master_pdls_logic(self, manager):
        """Verifica la mappatura dei PDL esistenti dai fogli Excel."""
        manager.excel_app = MagicMock()
        manager.wb_master = MagicMock()

        # Mocking di un foglio
        mock_sheet = MagicMock()
        manager.wb_master.Sheets.return_value = mock_sheet
        # Simula last row
        mock_sheet.Cells.return_value.End.return_value.Row = 5
        # Simula dati (Col E è l'indice 4, Col M è l'indice 12)
        # Nota: Range.Value ritorna una tupla di tuple
        mock_sheet.Range.return_value.Value = (
            ("A", "B", "C", "D", "PDL_1", "F", "G", "H", "I", "J", "K", "L", "EMESSO"),
            ("A", "B", "C", "D", "PDL_2", "F", "G", "H", "I", "J", "K", "L", "RICHIESTO"),
        )

        mappa = manager._map_master_pdls()

        assert "PDL_1" in mappa
        assert mappa["PDL_1"]["stato"] == "EMESSO"
        assert mappa["PDL_1"]["riga"] == 4
        assert mappa["PDL_2"]["riga"] == 5

    @patch("openpyxl.load_workbook")
    def test_analyze_downloaded_file_diff(self, mock_load_wb, manager):
        """Verifica il rilevamento delle differenze tra report e master."""
        # Setup Master Map
        mappa_pdl = {
            "PDL_STALE": {"foglio": "A1", "riga": 4, "stato": "EMESSO"},
            "PDL_UPDATING": {"foglio": "A1", "riga": 5, "stato": "EMESSO"},
        }

        # Setup Downloaded Workbook Mock
        mock_wb = MagicMock()
        mock_load_wb.return_value = mock_wb
        mock_ws = mock_wb.active

        # Righe report: [PDL, Altro, ..., X_Giorno, ..., Stato]
        # Mappa giorni report indices: {8: 3, 9: 5, 10: 7, 11: 9, 12: 11}
        # Riga 1: PDL Esistente con Stato cambiato
        row1 = ["PDL_UPDATING"] + [""] * 13 + ["Richiesto"] + [""] * 10
        # Riga 2: Nuovo PDL
        row2 = ["PDL_NEW"] + ["Val"] * 20

        mock_ws.iter_rows.return_value = [row1, row2]

        nuovi, _modif_x, modif_stato = manager._analyze_downloaded_file("report.xlsx", mappa_pdl)

        assert "PDL_NEW" in nuovi
        assert "PDL_UPDATING" in modif_stato
        assert modif_stato["PDL_UPDATING"] == "RICHIESTO"

    def test_cleanup_closes_excel(self, manager):
        """Verifica la chiusura dell'app Excel se aperta dal manager."""
        mock_app = MagicMock()
        mock_wb = MagicMock()
        manager.excel_app = mock_app
        manager.wb_master = mock_wb
        manager._is_already_open = False

        manager.cleanup()

        mock_wb.Close.assert_called_with(SaveChanges=True)
        mock_app.Quit.assert_called_once()
        assert manager.excel_app is None
