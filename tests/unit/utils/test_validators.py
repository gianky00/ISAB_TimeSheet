from src.utils.validators import InputValidator


class TestInputValidator:
    def test_validate_pdl_with_suffix(self):
        # Sotto soglia 400k -> /S
        res = InputValidator.validate_pdl("123456")
        assert res.valid is True
        assert res.sanitized_value == "123456/S"

        # Sopra soglia 400k -> /C
        res = InputValidator.validate_pdl("540000")
        assert res.valid is True
        assert res.sanitized_value == "540000/C"

    def test_validate_pdl_already_suffixed(self):
        res = InputValidator.validate_pdl("123456/S")
        assert res.valid is True
        assert res.sanitized_value == "123456/S"

        res = InputValidator.validate_pdl("540000/C")
        assert res.valid is True
        assert res.sanitized_value == "540000/C"

    def test_validate_pdl_invalid(self):
        assert InputValidator.validate_pdl("").valid is False
        assert InputValidator.validate_pdl("12345").valid is False  # Troppo corto
        assert InputValidator.validate_pdl("1234567").valid is False  # Troppo lungo
        assert InputValidator.validate_pdl("ABCDEF").valid is False

    def test_validate_oda(self):
        assert InputValidator.validate_oda("ODA123").valid is True
        assert InputValidator.validate_oda("A" * 21).valid is False  # Troppo lungo
        assert InputValidator.validate_oda("").valid is False

    def test_validate_codice_fiscale_valid(self):
        # Mario Rossi, nato il 01/01/1980 a Roma (H501)
        # Checksum calcolato: U
        res = InputValidator.validate_codice_fiscale("RSSMRA80A01H501U")
        assert res.valid is True
        assert res.sanitized_value == "RSSMRA80A01H501U"

    def test_validate_codice_fiscale_invalid(self):
        assert InputValidator.validate_codice_fiscale("INVALID").valid is False
        assert InputValidator.validate_codice_fiscale("RSSMRA80A01H501X").valid is False  # Checksum sbagliato

    def test_validate_date_italian(self):
        # Valido con .
        res = InputValidator.validate_date_italian("23.05.2026")
        assert res.valid is True
        assert res.sanitized_value == "23.05.2026"

        # Valido con / (convertito)
        res = InputValidator.validate_date_italian("23/05/2026")
        assert res.valid is True
        assert res.sanitized_value == "23.05.2026"

        # Invalido Formato Errato
        assert InputValidator.validate_date_italian("2026-05-23").valid is False

        # Invalido (data inesistente)
        assert InputValidator.validate_date_italian("31.02.2023").valid is False

    def test_sanitize_sql_string(self):
        # Rimuove null bytes e caratteri strani ma tiene \n
        bad_str = "Clean\x00String\nWith\tFormatting"
        sanitized = InputValidator.sanitize_sql_string(bad_str)
        assert "\x00" not in sanitized
        assert "\n" in sanitized
        assert "\t" in sanitized
        assert "CleanString" in sanitized
