from src.utils.validators import InputValidator


class TestInputValidator:
    def test_validate_pdl(self):
        res = InputValidator.validate_pdl("123456/C")
        assert res.valid
        assert res.sanitized_value == "123456/C"

        res = InputValidator.validate_pdl("123456")
        assert res.valid
        assert res.sanitized_value == "123456/S"

        res = InputValidator.validate_pdl("500000")
        assert res.valid
        assert res.sanitized_value == "500000/C"

        res = InputValidator.validate_pdl("")
        assert not res.valid
        assert res.error == "Numero PDL obbligatorio"

        res = InputValidator.validate_pdl("12345")
        assert not res.valid

        res = InputValidator.validate_pdl("123456/X")
        assert not res.valid

    def test_validate_oda(self):
        res = InputValidator.validate_oda("ODA123")
        assert res.valid
        assert res.sanitized_value == "ODA123"

        res = InputValidator.validate_oda("")
        assert not res.valid
        assert res.error == "Numero OdA obbligatorio"

        res = InputValidator.validate_oda("A" * 21)
        assert not res.valid

        res = InputValidator.validate_oda("ODA-123!")
        assert not res.valid

    def test_validate_codice_fiscale(self):
        valid_cf = "RSSMRA80A01H501U"

        res = InputValidator.validate_codice_fiscale(valid_cf)
        assert res.valid
        assert res.sanitized_value == valid_cf

        res = InputValidator.validate_codice_fiscale("RSSMRA")
        assert not res.valid

        res = InputValidator.validate_codice_fiscale("1234567890123456")
        assert not res.valid

        res = InputValidator.validate_codice_fiscale("RSSMRA80A01H501Z")
        assert not res.valid

        res = InputValidator.validate_codice_fiscale("")
        assert not res.valid

    def test_validate_date_italian(self):
        res = InputValidator.validate_date_italian("15.10.2023")
        assert res.valid
        assert res.sanitized_value == "15.10.2023"

        res = InputValidator.validate_date_italian("15/10/2023")
        assert res.valid
        assert res.sanitized_value == "15.10.2023"

        res = InputValidator.validate_date_italian("")
        assert not res.valid

        res = InputValidator.validate_date_italian("32.10.2023")
        assert not res.valid

        res = InputValidator.validate_date_italian("abc")
        assert not res.valid

    def test_sanitize_sql_string(self):
        assert InputValidator.sanitize_sql_string("hello world") == "hello world"
        assert InputValidator.sanitize_sql_string("hello\nworld") == "hello\nworld"
        assert InputValidator.sanitize_sql_string(None) == ""
        assert InputValidator.sanitize_sql_string("") == ""
        assert InputValidator.sanitize_sql_string("hello\x00world") == "helloworld"
