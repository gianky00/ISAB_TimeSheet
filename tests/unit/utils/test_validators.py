from src.utils.validators import InputValidator


def test_validate_pdl():
    assert InputValidator.validate_pdl("123456").sanitized_value == "123456/S"
    assert InputValidator.validate_pdl("400001").sanitized_value == "400001/C"
    assert InputValidator.validate_pdl("123456/C").valid is True
    assert InputValidator.validate_pdl("abc").valid is False


def test_validate_oda():
    assert InputValidator.validate_oda("ODA123").sanitized_value == "ODA123"
    assert InputValidator.validate_oda("").valid is False
    assert InputValidator.validate_oda("A" * 21).valid is False


def test_validate_codice_fiscale():
    # Example valid CF
    assert InputValidator.validate_codice_fiscale("RSSMRA80A01H501U").valid is True
    assert InputValidator.validate_codice_fiscale("INVALID").valid is False


def test_validate_date_italian():
    assert InputValidator.validate_date_italian("17.05.2024").sanitized_value == "17.05.2024"
    assert InputValidator.validate_date_italian("17/05/2024").sanitized_value == "17.05.2024"
    assert InputValidator.validate_date_italian("32.01.2024").valid is False
