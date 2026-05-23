from pathlib import Path
from unittest.mock import MagicMock, patch

from src.core.processing.timesheet.steps import (
    ExtractMetadataStep,
    LoadWorkbookStep,
    SaveWorkbookStep,
    TransformSheetStep,
)
from src.models.timesheet import TimesheetMetadata


class TestTimesheetProcessingSteps:
    @patch("src.core.processing.timesheet.steps.openpyxl.load_workbook")
    def test_load_workbook_step(self, mock_load, fs):
        fs.create_file("test.xlsx")
        mock_wb = MagicMock()
        mock_wb.sheetnames = ["Timesheet"]
        mock_load.return_value = mock_wb

        step = LoadWorkbookStep()
        ctx = {"file_path": "test.xlsx"}
        step.execute(ctx)

        assert ctx["workbook"] == mock_wb
        assert "worksheet" in ctx

    def test_extract_metadata_step(self):
        mock_ws = MagicMock()
        # ODC in A2
        mock_ws["A2"].value = "ODC123"
        # POS in col 2, riga 2
        mock_cell = MagicMock()
        mock_cell.value = "10"
        mock_ws.iter_rows.return_value = [[mock_cell]]
        # Not empty
        mock_ws.max_row = 2
        mock_ws.cell.return_value.value = "some data"

        step = ExtractMetadataStep()
        ctx = {"worksheet": mock_ws, "file_path": "any.xlsx"}
        step.execute(ctx)

        assert ctx["metadata"].odc == "ODC123"
        assert "10" in ctx["metadata"].pos_values
        assert ctx["is_empty"] is False

    def test_extract_metadata_deduce_odc(self):
        mock_ws = MagicMock()
        mock_ws["A2"].value = None
        mock_ws.max_row = 2
        mock_ws.cell.return_value.value = "data"

        step = ExtractMetadataStep()
        ctx = {"worksheet": mock_ws, "file_path": "Export_ODC456-10_test.xlsx"}
        step.execute(ctx)

        assert ctx["metadata"].odc == "ODC456"

    def test_transform_sheet_step(self):
        # Usiamo un dizionario per simulare le celle ed evitare che il mock ritorni lo stesso oggetto
        cells = {}

        def get_cell(coord):
            if coord not in cells:
                cells[coord] = MagicMock()
            return cells[coord]

        mock_ws = MagicMock()
        mock_ws.__getitem__.side_effect = get_cell
        mock_ws.max_row = 2
        mock_col = [MagicMock(value="Val", column=1)]
        mock_ws.columns = [mock_col]

        step = TransformSheetStep()
        ctx = {"worksheet": mock_ws, "is_empty": False}
        step.execute(ctx)

        assert cells["B1"].value == "POS"
        assert cells["W1"].value == "ORE_FEST_DIU"
        assert mock_ws.delete_cols.called

    def test_save_workbook_step(self, fs):
        mock_wb = MagicMock()
        mock_dir = Path("/output")
        fs.create_dir(str(mock_dir))

        metadata = TimesheetMetadata(odc="ODC1", pos_values={"10"}, first_pos_cleaned="10")
        ctx = {
            "workbook": mock_wb,
            "dest_dir": mock_dir,
            "metadata": metadata,
            "is_empty": False,
            "file_path": "src.xlsx",
        }

        step = SaveWorkbookStep()
        step.execute(ctx)

        assert ctx["dest_path"] == mock_dir / "ODC1_10_TS.xlsx"
        assert mock_wb.save.called

    def test_save_workbook_step_empty(self, fs):
        fs.create_file("src.xlsx")
        mock_wb = MagicMock()
        # Serve metadata anche se empty per via dell'accesso immediato in SaveWorkbookStep.execute
        metadata = TimesheetMetadata(odc="DUMMY", pos_values=set(), first_pos_cleaned="")
        ctx = {
            "workbook": mock_wb,
            "is_empty": True,
            "file_path": "src.xlsx",
            "dest_dir": "/",
            "metadata": metadata,
        }

        step = SaveWorkbookStep()
        step.execute(ctx)

        assert ctx["dest_path"] is None
        assert not Path("src.xlsx").exists()
