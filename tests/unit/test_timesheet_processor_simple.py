from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.core.timesheet_processor import TimesheetProcessor


class TestTimesheetProcessorSimple:
    def test_process_file_logic(self):
        # Mocking everything to avoid disk access
        data = {
            "POS": [1, 1, 2, 2, 3],
            "Descrizione": ["A", "A", "B", "B", "C"]
        }
        df = pd.DataFrame(data)

        with patch("src.core.timesheet_processor.Path.exists", return_value=True), \
             patch("src.core.timesheet_processor.pd.ExcelFile") as mock_excel_file, \
             patch("src.core.timesheet_processor.pd.read_excel", return_value=df):

            mock_xls = mock_excel_file.return_value
            mock_xls.sheet_names = ["Timesheet"]

            success, msg = TimesheetProcessor.process_file(Path("fake.xlsx"))
            assert success is True
            assert "3 POS univoci" in msg
