from src.utils.validators import InputValidator


class TestValidatorsExtended:
    def test_validate_pdl_auto_suffix(self):
        """Verifica l'aggiunta automatica del suffisso /S o /C."""
        # < 400000 -> /S
        res_s = InputValidator.validate_pdl("123456")
        assert res_s.valid is True
        assert res_s.sanitized_value == "123456/S"

        # >= 400000 -> /C
        res_c = InputValidator.validate_pdl("400001")
        assert res_c.valid is True
        assert res_c.sanitized_value == "400001/C"

        # Già presente -> mantiene
        res_existing = InputValidator.validate_pdl("123456/C")
        assert res_existing.sanitized_value == "123456/C"

    def test_validate_pdl_invalid(self):
        """Verifica blocchi su PDL malformati."""
        assert InputValidator.validate_pdl("12345").valid is False  # Troppo corto
        assert InputValidator.validate_pdl("1234567").valid is False  # Troppo lungo
        assert InputValidator.validate_pdl("ABCDEF").valid is False  # Non numerico
        assert InputValidator.validate_pdl("").valid is False  # Vuoto

    def test_validate_codice_fiscale_checksum(self):
        """Verifica l'algoritmo di checksum del Codice Fiscale."""
        # CF Valido (esempio reale/strutturato correttamente)
        valid_cf = "RSSMRA80A01H501U"
        res = InputValidator.validate_codice_fiscale(valid_cf)
        assert res.valid is True

        # Checksum errato (cambio l'ultima lettera)
        invalid_cf = "RSSMRA80A01H501Z"
        res_inv = InputValidator.validate_codice_fiscale(invalid_cf)
        assert res_inv.valid is False
        assert "Checksum" in res_inv.error

    def test_validate_date_italian_logical_check(self):
        """Verifica che date inesistenti siano bloccate."""
        assert InputValidator.validate_date_italian("31.02.2024").valid is False  # Febbraio corto
        assert InputValidator.validate_date_italian("01/01/2024").valid is True
        assert InputValidator.validate_date_italian("01/01/2024").sanitized_value == "01.01.2024"

    def test_validate_oda_constraints(self):
        """Verifica vincoli lunghezza e caratteri OdA."""
        # 20 caratteri (limite max)
        assert InputValidator.validate_oda("ODA12345678901234567").valid is True
        assert InputValidator.validate_oda("ODA-123").valid is False  # Carattere non ammesso dal pattern
        assert InputValidator.validate_oda("A" * 21).valid is False  # Troppo lungo

    def test_sanitize_sql_string(self):
        """Verifica rimozione caratteri non stampabili."""
        dirty = "Hello\x00World\nTest"
        clean = InputValidator.sanitize_sql_string(dirty)
        assert "\x00" not in clean
        assert "\n" in clean
        assert clean == "HelloWorld\nTest"
