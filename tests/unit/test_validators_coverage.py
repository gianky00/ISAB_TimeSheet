import pytest
from src.utils.validators import InputValidator

class TestInputValidator:
    """Test coverage for src/utils/validators.py"""

    @pytest.mark.parametrize("pdl, expected_valid, expected_val", [
        ("123456", True, "123456/S"),  # Auto suffix /S (< 400000)
        ("500000", True, "500000/C"),  # Auto suffix /C (>= 400000)
        ("123456/C", True, "123456/C"), # Explicit /C
        ("123456/S", True, "123456/S"), # Explicit /S
        ("  123456  ", True, "123456/C"), # Trimming
        ("", False, None), # Empty
        ("123", False, None), # Too short
        ("1234567", False, None), # Too long
        ("12345X", False, None), # Invalid chars
        ("123456/X", False, None), # Invalid suffix
    ])
    def test_validate_pdl(self, pdl, expected_valid, expected_val):
        res = InputValidator.validate_pdl(pdl)
        assert res.valid == expected_valid
        if expected_valid:
            assert res.sanitized_value == expected_val
        else:
            assert res.error is not None

    @pytest.mark.parametrize("oda, expected_valid", [
        ("ODA123", True),
        ("  ODA123  ", True),
        ("", False),
        ("A" * 21, False), # Too long
        ("ODA$123", False), # Invalid chars
    ])
    def test_validate_oda(self, oda, expected_valid):
        res = InputValidator.validate_oda(oda)
        assert res.valid == expected_valid
        if expected_valid:
            assert res.sanitized_value == oda.strip().upper()

    @pytest.mark.parametrize("cf, expected_valid", [
        ("RSSMRA85T10A562S", True), # Valid (Mario Rossi check)
        ("rssmra85t10a562s", True), # Lowercase
        ("", False),
        ("RSSMRA85T10A562", False), # Too short
        ("RSSMRA85T10A562SS", False), # Too long
        ("RSSMRA85T10A562X", False), # Invalid checksum (S expected)
        ("1234567890123456", False), # Invalid format pattern
    ])
    def test_validate_codice_fiscale(self, cf, expected_valid):
        res = InputValidator.validate_codice_fiscale(cf)
        assert res.valid == expected_valid
        if expected_valid:
            assert res.sanitized_value == cf.upper()

    @pytest.mark.parametrize("date_str, expected_valid, expected_val", [
        ("15.01.2026", True, "15.01.2026"),
        ("15/01/2026", True, "15.01.2026"),
        ("  15/01/2026  ", True, "15.01.2026"),
        ("", False, None),
        ("32.01.2026", False, None), # Invalid day
        ("15.13.2026", False, None), # Invalid month
        ("15.01.26", False, None), # Short year (regex requires 4 digits)
        ("abc", False, None),
    ])
    def test_validate_date_italian(self, date_str, expected_valid, expected_val):
        res = InputValidator.validate_date_italian(date_str)
        assert res.valid == expected_valid
        if expected_valid:
            assert res.sanitized_value == expected_val

    def test_sanitize_sql_string(self):
        dirty = "SELECT * FROM users;\n"
        clean = InputValidator.sanitize_sql_string(dirty)
        assert clean == "SELECT * FROM users;\n"
        
        # Non-printable check
        dirty_np = "User\x00Name"
        clean_np = InputValidator.sanitize_sql_string(dirty_np)
        assert clean_np == "UserName" # Null char removed

        assert InputValidator.sanitize_sql_string(None) == ""