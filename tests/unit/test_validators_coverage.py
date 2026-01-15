
import pytest
from src.utils.validators import InputValidator, ValidationResult

class TestValidators:
    def test_validate_pdl(self):
        # Valid PDL
        res = InputValidator.validate_pdl("123456/C")
        assert res.valid is True
        assert res.sanitized_value == "123456/C"
        
        # Valid PDL lowercase
        res = InputValidator.validate_pdl("123456/s")
        assert res.valid is True
        assert res.sanitized_value == "123456/S"
        
        # Auto-suffix S
        res = InputValidator.validate_pdl("123456")
        assert res.valid is True
        assert res.sanitized_value == "123456/S"
        
        # Auto-suffix C
        res = InputValidator.validate_pdl("456789")
        assert res.valid is True
        assert res.sanitized_value == "456789/C"
        
        # Invalid
        res = InputValidator.validate_pdl("abc")
        assert res.valid is False
        assert "non valido" in res.error

    def test_validate_oda(self):
        res = InputValidator.validate_oda("ODA123")
        assert res.valid is True
        assert res.sanitized_value == "ODA123"
        
        res = InputValidator.validate_oda("")
        assert res.valid is False
        
        res = InputValidator.validate_oda("A" * 21)
        assert res.valid is False
        assert "troppo lungo" in res.error

    def test_validate_codice_fiscale(self):
        # Valid CF (Mario Rossi, Roma)
        valid_cf = "RSSMRA80A01H501U"
        res = InputValidator.validate_codice_fiscale(valid_cf)
        assert res.valid is True
        
        # Invalid length
        assert InputValidator.validate_codice_fiscale("ABC").valid is False
        
        # Invalid checksum
        assert InputValidator.validate_codice_fiscale("GNCALR80A01H501A").valid is False

    def test_validate_date_italian(self):
        assert InputValidator.validate_date_italian("15.01.2026").valid is True
        assert InputValidator.validate_date_italian("15/01/2026").valid is True
        assert InputValidator.validate_date_italian("32.01.2026").valid is False
        assert InputValidator.validate_date_italian("invalid").valid is False

    def test_sanitize_sql_string(self):
        dirty = "some' OR 1=1; --\x00\x01"
        clean = InputValidator.sanitize_sql_string(dirty)
        assert "\x00" not in clean
        assert "\x01" not in clean
        assert "some' OR 1=1; --" in clean
