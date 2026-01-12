
import pytest
import pandas as pd
from pathlib import Path
from src.core.timesheet_processor import TimesheetProcessor

class TestTimesheetProcessorDeep:
    @pytest.fixture
    def mock_excel(self, tmp_path):
        """Crea un file Excel finto per i test."""
        file_path = tmp_path / "timesheet.xlsx"
        # Crea un DataFrame con colonna POS
        df = pd.DataFrame({
            "POS": ["10", "20", "10", "30"],
            "Descrizione": ["A", "B", "C", "D"]
        })
        # Scrivi su foglio 'Timesheet' con header alla riga 2 (index 1)
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Riga vuota in alto per simulare header=1
            empty_df = pd.DataFrame()
            empty_df.to_excel(writer, sheet_name='Timesheet', index=False)
            df.to_excel(writer, sheet_name='Timesheet', startrow=1, index=False)
        return file_path

    def test_process_file_success(self, mock_excel):
        """Verifica elaborazione corretta con conteggio POS."""
        success, msg = TimesheetProcessor.process_file(mock_excel)
        assert success is True
        assert "3 POS univoci" in msg

    def test_process_file_missing_sheet(self, tmp_path):
        """Verifica errore se il foglio 'Timesheet' manca."""
        file_path = tmp_path / "wrong.xlsx"
        df = pd.DataFrame({"A": [1]})
        df.to_excel(file_path, sheet_name="Sheet1")
        
        success, msg = TimesheetProcessor.process_file(file_path)
        assert success is False
        assert "non trovato" in msg

    def test_process_file_no_pos_column(self, tmp_path):
        """Verifica comportamento se la colonna POS manca."""
        file_path = tmp_path / "no_pos.xlsx"
        df = pd.DataFrame({"Data": ["2024"]})
        with pd.ExcelWriter(file_path) as writer:
            df.to_excel(writer, sheet_name='Timesheet', startrow=1, index=False)
            
        success, msg = TimesheetProcessor.process_file(file_path)
        assert success is True
        assert "Nessuna colonna POS" in msg

    def test_process_file_not_found(self):
        """Verifica errore se il file non esiste."""
        success, msg = TimesheetProcessor.process_file(Path("ghost.xlsx"))
        assert success is False
        assert "non trovato" in msg
