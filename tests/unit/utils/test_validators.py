from src.utils.validators import InputValidator


class TestInputValidator:
    def test_validate_pdl(self):
        # Valido con suffisso
        res = InputValidator.validate_pdl("123456/S")
        assert res.valid is True
        assert res.sanitized_value == "123456/S"

        # Solo cifre < 400000 -> /S
        res = InputValidator.validate_pdl("100000")
        assert res.sanitized_value == "100000/S"

        # Solo cifre >= 400000 -> /C
        res = InputValidator.validate_pdl("500000")
        assert res.sanitized_value == "500000/C"

        # Invalido
        assert InputValidator.validate_pdl("123").valid is False

    def test_validate_oda(self):
        assert InputValidator.validate_oda("123456ABC").valid is True
        # La regex attuale ^[A-Za-z0-9]{1,20}$ non ammette trattini
        assert InputValidator.validate_oda("ODA123").valid is True
        assert InputValidator.validate_oda("X" * 21).valid is False
        assert InputValidator.validate_oda("").valid is False

    def test_validate_codice_fiscale(self):
        # CF Valido (Checksum corretto: RSSMRA80A01H501 -> U)
        cf_valido = "RSSMRA80A01H501U"
        res = InputValidator.validate_codice_fiscale(cf_valido)
        assert res.valid is True

        assert InputValidator.validate_codice_fiscale("INVALID").valid is False
        assert InputValidator.validate_codice_fiscale("A" * 16).valid is False

    def test_validate_date_italian(self):
        assert InputValidator.validate_date_italian("23.05.2023").valid is True
        assert InputValidator.validate_date_italian("23/05/2023").valid is True
        assert InputValidator.validate_date_italian("23/05/2023").sanitized_value == "23.05.2023"

        assert InputValidator.validate_date_italian("32.01.2023").valid is False
        assert InputValidator.validate_date_italian("2023-05-23").valid is False

    def test_sanitize_sql_string(self):
        assert InputValidator.sanitize_sql_string("Hello\x00World") == "HelloWorld"
        assert InputValidator.sanitize_sql_string("Line1\nLine2") == "Line1\nLine2"
        assert InputValidator.sanitize_sql_string(None) == ""

    def test_validate_cf_checksum_logic(self):
        # RSSMRA80A01H501U è valido
        assert InputValidator._validate_cf_checksum("RSSMRA80A01H501U") is True
        assert InputValidator._validate_cf_checksum("RSSMRA80A01H501A") is False
