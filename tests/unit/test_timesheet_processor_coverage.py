from pathlib import Path

import pandas as pd
import pytest

from src.core.timesheet_processor import TimesheetProcessor


class TestTimesheetProcessorCoverage:
    """Test suite for src/core/timesheet_processor.py"""

    @pytest.fixture
    def sample_df(self):
        """Dataframe sample for testing."""
        return pd.DataFrame({
            "POS": ["POS1", "POS2", "POS1"],
            "Ore": [8, 4, 4]
        })

    def test_process_file_not_found(self):
        """Test elaborazione file non esistente."""
        path = Path("non_existent_file.xlsx")
        success, msg = TimesheetProcessor.process_file(path)
        assert success is False
        assert "non trovato" in msg

    def test_process_file_no_sheet(self, tmp_path):
        """Test file senza foglio Timesheet."""
        file_path = tmp_path / "test_no_sheet.xlsx"
        # Crea un excel con un foglio diverso
        df = pd.DataFrame({"A": [1]})
        with pd.ExcelWriter(file_path) as writer:
            df.to_excel(writer, sheet_name="Altro", index=False)

        success, msg = TimesheetProcessor.process_file(file_path)
        assert success is False
        assert "Foglio 'Timesheet' non trovato" in msg

    def test_process_file_with_pos(self, tmp_path, sample_df):
        """Test elaborazione corretta con colonna POS."""
        file_path = tmp_path / "test_ok.xlsx"
        # header=1 significa che la prima riga è skippata, quindi mettiamo dati dummy nella prima riga
        # Per simulare correttamente, scriviamo header manuale.
        # In pandas to_excel, startrow=1 scrive header a riga 2 (index 1).
        with pd.ExcelWriter(file_path) as writer:
            sample_df.to_excel(writer, sheet_name="Timesheet", index=False, startrow=1)

        success, msg = TimesheetProcessor.process_file(file_path)
        assert success is True
        assert "Trovati 2 POS univoci" in msg

    def test_process_file_no_pos_column(self, tmp_path):
        """Test file con Timesheet ma senza colonna POS."""
        file_path = tmp_path / "test_no_pos.xlsx"
        df = pd.DataFrame({"Altro": [1, 2]})
        with pd.ExcelWriter(file_path) as writer:
            df.to_excel(writer, sheet_name="Timesheet", index=False, startrow=1)

        success, msg = TimesheetProcessor.process_file(file_path)
        assert success is True
        assert "Nessuna colonna POS trovata" in msg

    def test_process_file_exception(self, tmp_path):
        """Test gestione eccezioni (es. file corrotto o non leggibile)."""
        file_path = tmp_path / "corrupted.xlsx"
        file_path.write_text("Not an excel file") # Scrive testo, pd.ExcelFile fallirà

        success, msg = TimesheetProcessor.process_file(file_path)
        assert success is False
        # msg conterrà l'errore di pandas/zipfile
        assert msg is not None
