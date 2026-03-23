import openpyxl
import pytest

from src.core.timesheet_processor import TimesheetProcessor


class TestTimesheetProcessor:
    @pytest.fixture
    def sample_xlsx(self, tmp_path):
        """Crea un file Excel di test con la struttura attesa."""
        path = tmp_path / "source.xlsx"
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Timesheet"

        # Metadata
        ws["A2"] = "5400123"  # ODC

        # Headers
        ws["B1"] = "OLD_B"
        ws["C1"] = "OLD_C"

        # Dati POS
        ws["B2"] = "10.0"
        ws["B3"] = "10.0"

        wb.save(path)
        return path

    def test_process_and_move_success(self, sample_xlsx, tmp_path):
        """Verifica il ciclo completo di elaborazione e rinomina."""
        dest_dir = tmp_path / "processed"

        success, _msg = TimesheetProcessor.process_and_move(sample_xlsx, dest_dir)

        assert success is True
        # Nome file atteso: ODC_POS_TS.xlsx (perché c'è solo un POS '10')
        expected_name = "5400123_10_TS.xlsx"
        dest_path = dest_dir / expected_name
        assert dest_path.exists()
        assert not sample_xlsx.exists(), "Il sorgente deve essere rimosso"

        # Verifica trasformazioni
        wb = openpyxl.load_workbook(dest_path)
        ws = wb["Timesheet"]
        assert ws["B1"].value == "Data"  # Colonna C originale spostata in B dopo eliminazione A
        assert ws["A1"].value == "POS"  # Colonna B originale spostata in A dopo eliminazione A
        # Nota: l'eliminazione colonne cambia gli indici. Testiamo i valori finali.

    def test_analyze_pos_column_logic(self):
        """Verifica il conteggio dei POS univoci."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws["B2"] = "10"
        ws["B3"] = "20"
        ws["B4"] = "10.0"

        pos_values, first_cleaned = TimesheetProcessor._analyze_pos_column(ws)

        # 10, 20, 10.0 (stringhe) -> 3 valori univoci se non normalizzati prima del set
        # Ma nel codice: val = str(row[0].value).strip()
        assert len(pos_values) == 3
        assert first_cleaned == "10"

    def test_clean_pos_value(self):
        assert TimesheetProcessor._clean_pos_value("10.0") == "10"
        assert TimesheetProcessor._clean_pos_value("5") == "5"
        assert TimesheetProcessor._clean_pos_value("abc") == "abc"

    def test_get_destination_path_conflict(self, tmp_path):
        """Verifica la gestione del conflitto se il file esiste già."""
        dest_dir = tmp_path
        odc = "5400123"
        (dest_dir / f"{odc}_TS.xlsx").touch()

        path = TimesheetProcessor._get_destination_path(dest_dir, odc, {"10", "20"}, "10")

        assert path.name.startswith(f"{odc}_TS_")
        assert path.suffix == ".xlsx"
