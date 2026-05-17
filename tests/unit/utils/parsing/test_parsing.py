from src.utils.parsing import parse_currency


def test_parse_currency_basics():
    assert parse_currency("100") == 100.0
    assert parse_currency(100) == 100.0
    assert parse_currency(None) == 0.0
    assert parse_currency("nan") == 0.0


def test_parse_currency_formats():
    assert parse_currency("1.234,56") == 1234.56
    assert parse_currency("1234,56") == 1234.56
    assert parse_currency("1234.56") == 1234.56
    assert parse_currency("1,234.56") == 1234.56


def test_parse_currency_noise():
    assert parse_currency("100 Euro") == 100.0
    assert parse_currency("Prezzo 50.50") == 50.50
    assert parse_currency("1.000 EUR") == 1000.0


def test_parse_currency_scientific():
    assert parse_currency("1.5e2") == 150.0
    assert parse_currency("1,5E+2") == 150.0


def test_parse_currency_negatives():
    assert parse_currency("-100") == -100.0
    assert parse_currency("(100)") == -100.0


def test_is_value_negative_extended():
    from src.utils.parsing import _is_value_negative

    assert _is_value_negative("100") is False
    assert _is_value_negative("-100") is True
    assert _is_value_negative("(100)") is True
    assert _is_value_negative("1e-1") is False


def test_parse_currency_invalid():
    # Test per coprire i rami di errore nel parsing
    assert parse_currency("invalid") == 0.0
    assert parse_currency("1.234.567.890.123.456.789") == 1234567890123456789.0
