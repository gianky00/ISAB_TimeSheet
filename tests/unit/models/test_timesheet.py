import pytest

from src.models.timesheet import TimesheetMetadata, TimesheetRecord


class TestTimesheetModels:
    def test_timesheet_record_creation(self):
        """Testa la creazione di TimesheetRecord."""
        record = TimesheetRecord(
            pos="10",
            data="2026-05-17",
            ingresso="08:00",
            uscita="17:00",
            totale="08:00",
            presenza="Si",
            ore_c="8",
            ore_m="0",
            ore_st_not="0",
            ore_st_diu="0",
            ore_fest_not="0",
            ore_fest_diu="0",
            odc="ODC-123",
            tecnico="Mario Rossi",
        )

        assert record.pos == "10"
        assert record.data == "2026-05-17"
        assert record.odc == "ODC-123"
        assert record.tecnico == "Mario Rossi"

    def test_timesheet_record_defaults(self):
        """Testa la creazione di TimesheetRecord omettendo argomenti opzionali."""
        record = TimesheetRecord(
            pos="10",
            data="2026-05-17",
            ingresso="08:00",
            uscita="17:00",
            totale="08:00",
            presenza="Si",
            ore_c="8",
            ore_m="0",
            ore_st_not="0",
            ore_st_diu="0",
            ore_fest_not="0",
            ore_fest_diu="0",
        )

        assert record.odc is None
        assert record.tecnico is None

    def test_timesheet_metadata_creation(self):
        """Testa la creazione di TimesheetMetadata."""
        meta = TimesheetMetadata(odc="ODC-123", pos_values={"10", "20", "30"}, first_pos_cleaned="10")

        assert meta.odc == "ODC-123"
        assert "20" in meta.pos_values
        assert meta.first_pos_cleaned == "10"

    def test_frozen_instances(self):
        """Verifica che le istanze siano immutabili (frozen=True)."""
        record = TimesheetRecord(
            pos="10",
            data="2026-05-17",
            ingresso="08:00",
            uscita="17:00",
            totale="08:00",
            presenza="Si",
            ore_c="8",
            ore_m="0",
            ore_st_not="0",
            ore_st_diu="0",
            ore_fest_not="0",
            ore_fest_diu="0",
        )

        with pytest.raises(Exception):  # dataclasses.FrozenInstanceError inherits from Exception
            record.pos = "20"

        meta = TimesheetMetadata(odc="ODC-123", pos_values={"10"}, first_pos_cleaned="10")
        with pytest.raises(Exception):
            meta.odc = "ODC-456"
