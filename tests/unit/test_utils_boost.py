from src.utils.parsing import parse_currency
from src.utils.validators import InputValidator


class TestValidatorsAndParsingDeep:
    def test_input_validator_pdl_auto_suffix(self):
        """Test: Auto-completamento PDL con soglia 400.000 (S vs C)."""
        # Test 6 digits auto-completion
        # Inferiore a 400.000 -> /S
        assert InputValidator.validate_pdl("123456").sanitized_value == "123456/S"
        assert InputValidator.validate_pdl("399999").sanitized_value == "399999/S"

        # Uguale o superiore a 400.000 -> /C
        assert InputValidator.validate_pdl("400000").sanitized_value == "400000/C"
        assert InputValidator.validate_pdl("456789").sanitized_value == "456789/C"
        assert InputValidator.validate_pdl("999999").sanitized_value == "999999/C"

    def test_input_validator_cf_invalid(self):
        """Test: Validazione Codice Fiscale con checksum errato."""
        res = InputValidator.validate_codice_fiscale("RSSMRA80A01L219Z")  # Checksum wrong
        assert res.valid is False

    def test_parse_currency_comprehensive(self):
        """Test: Parsing valuta con vari separatori e simboli (IT, US, Misto)."""
        # Standard IT
        assert parse_currency("1.234,56 €") == 1234.56  # noqa: PLR2004
        assert parse_currency("50,00") == 50.0  # noqa: PLR2004

        # Standard US/International
        assert parse_currency("1,234.56 $") == 1234.56  # noqa: PLR2004
        assert parse_currency("50.00") == 50.0  # noqa: PLR2004

        # Segni negativi (anche staccati)
        assert parse_currency("  - 10,00 ") == -10.0  # noqa: PLR2004
        assert parse_currency("10,00 -") == -10.0  # noqa: PLR2004

        # Separatori multipli (migliaia)
        assert parse_currency("1.234.567,89") == 1234567.89  # noqa: PLR2004
        assert parse_currency("1,234,567.89") == 1234567.89  # noqa: PLR2004

        # Casi ambigui (punto singolo)
        # Se ha esattamente 3 cifre dopo, la logica italiana lo tratta come migliaia (1.234 -> 1234.0)
        assert parse_currency("1.234") == 1234.0  # noqa: PLR2004
        assert parse_currency("1.23") == 1.23  # noqa: PLR2004

        # Null/Invalid
        assert parse_currency(None) == 0.0
        assert parse_currency("") == 0.0
        assert parse_currency("NaN") == 0.0
        assert parse_currency("invalid") == 0.0

    def test_validate_date_it_invalid(self):
        """Test: Validazione date in formato italiano non valide."""
        assert InputValidator.validate_date_italian("32.01.2024").valid is False
        assert InputValidator.validate_date_italian("01/01/24").valid is False
        assert InputValidator.validate_date_italian("").valid is False
