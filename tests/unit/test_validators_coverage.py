import pytest
from src.utils.validators import InputValidator

class TestValidatorsCoverage:
    """Test suite per src/utils/validators.py"""

    # --- Test validate_pdl ---
    def test_validate_pdl_valid(self):
        """Test PDL valido."""
        res = InputValidator.validate_pdl("123456/C")
        assert res.valid is True
        assert res.sanitized_value == "123456/C"

    def test_validate_pdl_auto_suffix_s(self):
        """Test PDL 6 cifre < 400000 -> /S"""
        res = InputValidator.validate_pdl("100000")
        assert res.valid is True
        assert res.sanitized_value == "100000/S"

    def test_validate_pdl_auto_suffix_c(self):
        """Test PDL 6 cifre >= 400000 -> /C"""
        res = InputValidator.validate_pdl("500000")
        assert res.valid is True
        assert res.sanitized_value == "500000/C"

    def test_validate_pdl_invalid_format(self):
        """Test PDL formato errato."""
        assert InputValidator.validate_pdl("ABC").valid is False
        assert InputValidator.validate_pdl("1234567").valid is False
        assert InputValidator.validate_pdl("").valid is False

    # --- Test validate_oda ---
    def test_validate_oda_valid(self):
        """Test OdA valido."""
        res = InputValidator.validate_oda("ODA123")
        assert res.valid is True
        assert res.sanitized_value == "ODA123"

    def test_validate_oda_too_long(self):
        """Test OdA troppo lungo."""
        long_oda = "A" * 21
        assert InputValidator.validate_oda(long_oda).valid is False

    def test_validate_oda_invalid_chars(self):
        """Test OdA caratteri non validi."""
        assert InputValidator.validate_oda("ODA#123").valid is False

    def test_validate_oda_empty(self):
        """Test OdA vuoto."""
        assert InputValidator.validate_oda("").valid is False

    # --- Test validate_codice_fiscale ---
    def test_validate_cf_valid(self):
        """Test Codice Fiscale valido."""
        # Esempio CF calcolato correttamente: RSSMRA80A01H501U (Rossi Mario)
        cf = "RSSMRA80A01H501U"
        res = InputValidator.validate_codice_fiscale(cf)
        assert res.valid is True
        assert res.sanitized_value == cf

    def test_validate_cf_wrong_length(self):
        """Test CF lunghezza errata."""
        assert InputValidator.validate_codice_fiscale("RSS").valid is False

    def test_validate_cf_invalid_format(self):
        """Test CF formato regex errato (es. numeri al posto di lettere iniziali)."""
        # Primi 6 char devono essere lettere
        assert InputValidator.validate_codice_fiscale("12345680A01H501U").valid is False

    def test_validate_cf_wrong_checksum(self):
        """Test CF checksum errato."""
        # RSSMRA80A01H501U corretto. Cambio ultima lettera in 'A'.
        cf = "RSSMRA80A01H501A"
        res = InputValidator.validate_codice_fiscale(cf)
        assert res.valid is False
        assert "Checksum" in res.error

    def test_validate_cf_empty(self):
        assert InputValidator.validate_codice_fiscale("").valid is False

    # --- Test validate_date_italian ---
    def test_validate_date_valid(self):
        """Test data valida."""
        res = InputValidator.validate_date_italian("25.12.2023")
        assert res.valid is True
        assert res.sanitized_value == "25.12.2023"

    def test_validate_date_slash_conversion(self):
        """Test conversione slash in punto."""
        res = InputValidator.validate_date_italian("25/12/2023")
        assert res.valid is True
        assert res.sanitized_value == "25.12.2023"

    def test_validate_date_invalid_format(self):
        """Test formato data errato."""
        assert InputValidator.validate_date_italian("2023-12-25").valid is False

    def test_validate_date_not_exist(self):
        """Test data non esistente (es. 30 Febbraio)."""
        assert InputValidator.validate_date_italian("30.02.2023").valid is False

    def test_validate_date_empty(self):
        assert InputValidator.validate_date_italian("").valid is False

    # --- Test sanitize_sql_string ---
    def test_sanitize_sql(self):
        """Test sanitizzazione SQL base."""
        assert InputValidator.sanitize_sql_string("SELECT *") == "SELECT *"
        assert InputValidator.sanitize_sql_string("Test\nLine") == "Test\nLine" # Printable
        # Test caratteri non printable se necessario (es. null byte)
        assert InputValidator.sanitize_sql_string(None) == ""