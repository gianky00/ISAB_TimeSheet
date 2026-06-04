import json
from unittest.mock import MagicMock, patch

from src.application.services.processing.scarico_ore.steps import (
    LoadScaricoOreStep,
    ProcessScaricoOreRowsStep,
    SyncScaricoOreStep,
)


class TestScaricoOreProcessingSteps:
    @patch("src.application.services.processing.scarico_ore.steps.openpyxl.load_workbook")
    def test_load_scarico_ore_step_success(self, mock_load, fs):
        fs.create_file("scarico.xlsx")
        mock_wb = MagicMock()
        mock_wb.sheetnames = ["SCARICO ORE"]
        mock_load.return_value = mock_wb

        step = LoadScaricoOreStep()
        ctx = {"file_path": "scarico.xlsx"}
        step.execute(ctx)

        assert ctx["success"] is True
        assert ctx["ws"] == mock_wb["SCARICO ORE"]

    def test_process_scarico_ore_rows_step(self):
        mock_ws = MagicMock()
        mock_ws.max_row = 7

        # Setup riga mock (row index 6)
        # c_data, c_p1, c_p2, c_odc, c_pos, c_dalle, c_alle, c_tot, c_desc, c_fin, c_comm
        mock_row = []
        values = ["2023-01-01", "P1", "", "ODC1", "10", "08:00", "17:00", "8", "DESC", "SI", "123"]
        for v in values:
            c = MagicMock()
            c.value = v
            c.font = None
            c.fill = None
            mock_row.append(c)

        mock_ws.iter_rows.return_value = [mock_row]

        step = ProcessScaricoOreRowsStep()
        ctx = {"ws": mock_ws, "success": True}
        step.execute(ctx)

        assert ctx["success"] is True
        assert len(ctx["rows"]) == 1
        assert ctx["rows"][0][3] == "ODC1"

    def test_extract_row_styles(self):
        step = ProcessScaricoOreRowsStep()

        mock_cell = MagicMock()
        # Mock font color
        mock_cell.font.color.type = "rgb"
        mock_cell.font.color.rgb = "FFFF0000"  # Red
        # Mock fill color
        mock_cell.fill.patternType = "solid"
        mock_cell.fill.start_color.type = "rgb"
        mock_cell.fill.start_color.rgb = "FF00FF00"  # Green

        row = [mock_cell] * 11
        vals = ["V"] * 11

        res = step._extract_row_styles(row, vals)
        style_data = json.loads(res)
        assert style_data["data"]["fg"] == "#FF0000"
        assert style_data["data"]["bg"] == "#00FF00"

    def test_validate_scarico_row(self):
        step = ProcessScaricoOreRowsStep()
        # Valid: p1 or p2 present, odc present, pos present, tot present
        assert step._validate_scarico_row(["D", "P1", "", "O", "P", "8", "17", "8", "D", "S", "C"]) is True
        # Invalid: missing ODC
        assert step._validate_scarico_row(["D", "P1", "", "", "P", "8", "17", "8", "D", "S", "C"]) is False
        # Invalid: missing both P1 and P2
        assert step._validate_scarico_row(["D", "", "", "O", "P", "8", "17", "8", "D", "S", "C"]) is False

    @patch("src.application.services.data_synchronizer.DataSynchronizer.sync_scarico_ore")
    def test_sync_scarico_ore_step(self, mock_sync):
        mock_sync.return_value = (50, 10)
        step = SyncScaricoOreStep()
        ctx = {"success": True, "rows": [("row",)]}

        step.execute(ctx)
        assert ctx["total_added"] == 50
        assert ctx["total_removed"] == 10
