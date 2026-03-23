from unittest.mock import MagicMock, patch

from src.core.timesheet_processor import TimesheetProcessor


class TestTimesheetProcessorSimple:
    """Test suite per TimesheetProcessor (logica di base senza dipendenze complesse)."""

    def test_process_file_logic(self, tmp_path):
        """Verifica la logica di process_file mockando le operazioni su file."""
        # Create a real file on disk so .exists() passes
        file_path = tmp_path / "fake.xlsx"
        file_path.write_text("dummy")

        # Mock openpyxl
        with patch("src.core.timesheet_processor.openpyxl.load_workbook") as mock_load_workbook:
            # Setup mock workbook and worksheet
            mock_wb = MagicMock()
            mock_ws = MagicMock()
            mock_wb.sheetnames = ["Timesheet"]

            # Important: __getitem__ should return different mocks for different cells
            def get_cell_mock(key):
                cell = MagicMock()
                if key == "A2":
                    cell.value = "ODC123"
                else:
                    cell.value = "HEADER"
                return cell

            mock_ws.__getitem__.side_effect = get_cell_mock
            mock_wb.__getitem__.return_value = mock_ws
            mock_load_workbook.return_value = mock_wb

            # Mock iter_rows for analyze_pos_column
            cell1 = MagicMock()
            cell1.value = "10"
            cell2 = MagicMock()
            cell2.value = "20"

            mock_ws.iter_rows.return_value = iter([(cell1,), (cell2,)])

            # Setup for _apply_transformations
            mock_ws.columns = []

            # Execution
            success, msg = TimesheetProcessor.process_and_move(file_path, dest_dir=tmp_path)

            # Verification
            assert success is True, f"Processing failed: {msg}"
            assert "Salvato in" in msg
            mock_load_workbook.assert_called_once_with(file_path)
            mock_wb.save.assert_called_once()
            mock_wb.close.assert_called_once()
