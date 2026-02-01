from src.utils.validators import InputValidator


class TestInputValidatorPDL:
    def test_valid_pdl_with_suffix(self):
        result = InputValidator.validate_pdl("123456/C")
        assert result.valid is True
        assert result.sanitized_value == "123456/C"

    def test_valid_pdl_lowercase(self):
        result = InputValidator.validate_pdl("123456/c")
        assert result.valid is True
        assert result.sanitized_value == "123456/C"

    def test_pdl_auto_suffix_c(self):
        # >= 400000 gets /C
        result = InputValidator.validate_pdl("500000")
        assert result.valid is True
        assert result.sanitized_value == "500000/C"

    def test_pdl_auto_suffix_s(self):
        # < 400000 gets /S
        result = InputValidator.validate_pdl("300000")
        assert result.valid is True
        assert result.sanitized_value == "300000/S"

    def test_pdl_empty(self):
        result = InputValidator.validate_pdl("")
        assert result.valid is False
        assert "obbligatorio" in result.error

    def test_pdl_invalid_format(self):
        result = InputValidator.validate_pdl("12345")
        assert result.valid is False

    def test_pdl_strips_whitespace(self):
        result = InputValidator.validate_pdl("  123456/C  ")
        assert result.valid is True
        assert result.sanitized_value == "123456/C"


class TestInputValidatorOdA:
    def test_valid_oda(self):
        result = InputValidator.validate_oda("ABC123")
        assert result.valid is True
        assert result.sanitized_value == "ABC123"

    def test_oda_empty(self):
        result = InputValidator.validate_oda("")
        assert result.valid is False

    def test_oda_too_long(self):
        result = InputValidator.validate_oda("A" * 25)
        assert result.valid is False
        assert "troppo lungo" in result.error

    def test_oda_invalid_chars(self):
        result = InputValidator.validate_oda("ABC-123")
        assert result.valid is False


class TestInputValidatorCodiceFiscale:
    def test_valid_cf(self):
        # Valid Italian fiscal code
        result = InputValidator.validate_codice_fiscale("RSSMRA80A01H501U")
        assert result.valid is True

    def test_cf_empty(self):
        result = InputValidator.validate_codice_fiscale("")
        assert result.valid is False

    def test_cf_wrong_length(self):
        result = InputValidator.validate_codice_fiscale("RSSMRA80A01")
        assert result.valid is False
        assert "16 caratteri" in result.error

    def test_cf_invalid_checksum(self):
        # Valid format but wrong checksum
        result = InputValidator.validate_codice_fiscale("RSSMRA80A01H501A")
        assert result.valid is False
        assert "Checksum" in result.error


class TestInputValidatorDate:
    def test_valid_date(self):
        result = InputValidator.validate_date_italian("15.01.2025")
        assert result.valid is True
        assert result.sanitized_value == "15.01.2025"

    def test_date_with_slashes(self):
        result = InputValidator.validate_date_italian("15/01/2025")
        assert result.valid is True
        assert result.sanitized_value == "15.01.2025"

    def test_date_empty(self):
        result = InputValidator.validate_date_italian("")
        assert result.valid is False

    def test_invalid_date(self):
        result = InputValidator.validate_date_italian("31.02.2025")
        assert result.valid is False
        assert "non esistente" in result.error


class TestSanitizeSQLString:
    def test_removes_control_chars(self):
        result = InputValidator.sanitize_sql_string("Hello\x00World")
        assert "\x00" not in result
        assert "HelloWorld" == result

    def test_keeps_newlines(self):
        result = InputValidator.sanitize_sql_string("Hello\nWorld")
        assert "\n" in result

    def test_empty_string(self):
        result = InputValidator.sanitize_sql_string("")
        assert result == ""
