import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.core.timesheet_processor import TimesheetProcessor

class TestTimesheetProcessorSimple:
    def test_process_file_not_found(self):
        # Path non esistente deve restituire False
        success, msg = TimesheetProcessor.process_file(Path("nonexistent.xlsx"))
        assert success is False
        assert "non trovato" in msg

    def test_process_file_logic(self):
        # Mocking everything to avoid disk access
        data = {
            "POS": [1, 1, 2, 2, 3],
            "Descrizione": ["A", "A", "B", "B", "C"]
        }
        df = pd.DataFrame(data)
        
        with patch("src.core.timesheet_processor.Path.exists", return_value=True), \
             patch("src.core.timesheet_processor.pd.read_excel", return_value=df), \
             patch("src.core.timesheet_processor.pd.ExcelWriter") as mock_writer:
            
            # Setup mock writer to act as context manager
            mock_writer.return_value.__enter__.return_value = MagicMock()
            
            success, msg = TimesheetProcessor.process_file(Path("fake.xlsx"))
            assert success is True
            assert "3 POS" in msg
