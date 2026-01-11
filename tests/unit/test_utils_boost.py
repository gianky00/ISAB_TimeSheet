from src.utils.parsing import parse_currency
from src.utils.validators import InputValidator


class TestValidatorsAndParsingDeep:
    def test_input_validator_pdl_auto_suffix(self):
        # Test 6 digits auto-completion
        res1 = InputValidator.validate_pdl("123456")
        assert res1.sanitized_value == "123456/S"
        res2 = InputValidator.validate_pdl("456789")
        assert res2.sanitized_value == "456789/C"

    def test_input_validator_cf_invalid(self):
        # Test invalid checksum
        res = InputValidator.validate_codice_fiscale("RSSMRA80A01L219Z") # Checksum wrong
        assert res.valid is False

    def test_parse_currency_edge_cases(self):
        assert parse_currency("1.234,56 €") == 1234.56
        # Fixed logic supports detached negative signs
        assert parse_currency("  - 10,00 ") == -10.0
        assert parse_currency("10,00 -") == -10.0
        assert parse_currency(None) == 0.0
        assert parse_currency("invalid") == 0.0

    def test_validate_date_it_invalid(self):
        assert InputValidator.validate_date_italian("32.01.2024").valid is False
        assert InputValidator.validate_date_italian("01/01/24").valid is False
