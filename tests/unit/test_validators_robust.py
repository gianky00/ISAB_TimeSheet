from src.utils.validators import InputValidator


class TestValidatorsRobust:
    # --- PDL Validation Tests ---
    def test_validate_pdl_valid_explicit(self):
        """Test PDL valido con suffisso esplicito."""
        res = InputValidator.validate_pdl("123456/C")
        assert res.valid is True
        assert res.sanitized_value == "123456/C"

    def test_validate_pdl_auto_suffix_s(self):
        """Test PDL 6 cifre < 400000 -> /S."""
        res = InputValidator.validate_pdl("399999")
        assert res.valid is True
        assert res.sanitized_value == "399999/S"

    def test_validate_pdl_auto_suffix_c(self):
        """Test PDL 6 cifre >= 400000 -> /C."""
        res = InputValidator.validate_pdl("400000")
        assert res.valid is True
        assert res.sanitized_value == "400000/C"

    def test_validate_pdl_invalid_format(self):
        """Test PDL formato errato."""
        assert InputValidator.validate_pdl("123/X").valid is False
        assert InputValidator.validate_pdl("12345").valid is False
        assert InputValidator.validate_pdl("abcdef").valid is False

    def test_validate_pdl_empty(self):
        """Test PDL vuoto."""
        assert InputValidator.validate_pdl(None).valid is False
        assert InputValidator.validate_pdl("").valid is False

    # --- OdA Validation Tests ---
    def test_validate_oda_valid(self):
        """Test OdA validi."""
        assert InputValidator.validate_oda("ODA123").valid is True
        assert InputValidator.validate_oda("4500012345").valid is True

    def test_validate_oda_invalid_chars(self):
        """Test caratteri non permessi in OdA."""
        assert (
            InputValidator.validate_oda("ODA-123").valid is False
        )  # trattino non in regex base
        assert InputValidator.validate_oda("ODA 123").valid is False

    def test_validate_oda_too_long(self):
        """Test OdA troppo lungo."""
        assert InputValidator.validate_oda("A" * 21).valid is False

    # --- Codice Fiscale Tests ---
    def test_validate_cf_valid(self):
        """Test Codice Fiscale valido reale (esempio generato)."""
        # RSSMRA80A01H501U (Rossi Mario) - Checksum U
        assert InputValidator.validate_codice_fiscale("RSSMRA80A01H501U").valid is True

    def test_validate_cf_invalid_checksum(self):
        """Test CF con checksum errato."""
        # RSSMRA80A01H501X (X invece di U)
        res = InputValidator.validate_codice_fiscale("RSSMRA80A01H501X")
        assert res.valid is False
        assert "Checksum" in res.error

    def test_validate_cf_format_error(self):
        """Test CF formato errato (regex)."""
        assert InputValidator.validate_codice_fiscale("123").valid is False
        assert (
            InputValidator.validate_codice_fiscale("RSSMRA80A01H5011").valid is False
        )  # Ultimo char numero

    # --- Date Tests ---
    def test_validate_date_it_valid(self):
        """Test data valida."""
        res = InputValidator.validate_date_italian("31.01.2023")
        assert res.valid is True

        # Test sostituzione slash
        res = InputValidator.validate_date_italian("31/01/2023")
        assert res.valid is True
        assert res.sanitized_value == "31.01.2023"

    def test_validate_date_it_invalid_value(self):
        """Test data impossibile."""
        res = InputValidator.validate_date_italian(
            "30.02.2023"
        )  # Febbraio non ha 30 giorni
        assert res.valid is False
        assert "non esistente" in res.error

    def test_validate_date_it_bad_format(self):
        """Test formato data errato."""
        assert InputValidator.validate_date_italian("2023-01-01").valid is False

    # --- SQL Sanitize Tests ---
    def test_sanitize_sql(self):
        """Test sanitizzazione base."""
        dirty = "Hello\x00World"  # Null char
        clean = InputValidator.sanitize_sql_string(dirty)
        assert clean == "HelloWorld"

        assert InputValidator.sanitize_sql_string(None) == ""
