from src.infrastructure.utils.validators import InputValidator


def test_validate_pdl():
    # Caso corretto automatico (senza suffisso)
    res = InputValidator.validate_pdl("123456")
    assert res.valid is True
    assert res.sanitized_value == "123456/S"  # num < 400000

    # Caso corretto automatico (suffisso /C)
    res = InputValidator.validate_pdl("500000")
    assert res.valid is True
    assert res.sanitized_value == "500000/C"

    # Caso errore formato
    res = InputValidator.validate_pdl("abc/C")
    assert res.valid is False


def test_validate_oda():
    res = InputValidator.validate_oda("ODA123")
    assert res.valid is True
    assert res.sanitized_value == "ODA123"

    res = InputValidator.validate_oda("")
    assert res.valid is False


def test_validate_codice_fiscale():
    # CF valido di test
    cf = "RSSMRA80A01H501U"
    res = InputValidator.validate_codice_fiscale(cf)
    assert res.valid is True

    # CF non valido (checksum errato)
    res = InputValidator.validate_codice_fiscale("RSSMRA80A01H501A")
    assert res.valid is False


def test_validate_date_italian():
    res = InputValidator.validate_date_italian("17.05.2026")
    assert res.valid is True
    assert res.sanitized_value == "17.05.2026"

    # Formato errato
    res = InputValidator.validate_date_italian("17/05/2026")
    assert res.valid is True  # sanitizer lo converte in .
    assert res.sanitized_value == "17.05.2026"

    # Data inesistente
    res = InputValidator.validate_date_italian("32.05.2026")
    assert res.valid is False
