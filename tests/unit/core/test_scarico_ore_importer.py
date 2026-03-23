from unittest.mock import MagicMock

from src.core.importers.scarico_ore import ScaricoOreImporter


class TestScaricoOreImporter:
    def test_validate_scarico_row_logic(self):
        """Verifica i criteri di validazione per una riga di scarico ore."""
        # Riga valida (data, p1, p2, odc, pos, dalle, alle, tot, desc, fin, comm)
        valid_vals = ["2024-01-01", "Mario", "", "123", "10", "08:00", "17:00", "8.0", "Lavoro", "NO", "C1"]
        assert ScaricoOreImporter._validate_scarico_row(valid_vals) is True

        # Mancano ODC e POS
        invalid_vals = ["2024-01-01", "Mario", "", "", "", "08:00", "17:00", "8.0", "Lavoro", "NO", "C1"]
        assert ScaricoOreImporter._validate_scarico_row(invalid_vals) is False

        # Manca Personale
        invalid_vals_no_pers = [
            "2024-01-01",
            "",
            "",
            "123",
            "10",
            "08:00",
            "17:00",
            "8.0",
            "Lavoro",
            "NO",
            "C1",
        ]
        assert ScaricoOreImporter._validate_scarico_row(invalid_vals_no_pers) is False

    def test_extract_row_values_formatting(self):
        """Verifica che i valori estratti dalle celle siano formattati correttamente."""

        # Creiamo dei mock per le celle
        def mock_cell(val):  # noqa: ANN001, ANN202
            m = MagicMock()
            m.value = val
            return m

        # Mock di una riga Excel (lista di celle)
        row = [mock_cell(None) for _ in range(11)]
        row[0].value = MagicMock()  # Data
        row[0].value.strftime.return_value = "2024-01-01"
        row[1].value = " Mario \n Rossi "  # P1
        row[3].value = 123.0  # ODC (float da Excel)
        row[4].value = "0"  # POS (stringa "0" da ignorare)
        row[7].value = 8.5  # Totale Ore

        vals = ScaricoOreImporter._extract_row_values(row)

        assert vals is not None
        assert vals[0] == "2024-01-01"
        assert vals[1] == "Mario Rossi"  # \n rimosso e trim
        assert vals[3] == "123"  # Convertito in stringa intera se possibile
        assert vals[4] == ""  # "0" convertito in vuoto
        assert vals[7] == "8.5"
