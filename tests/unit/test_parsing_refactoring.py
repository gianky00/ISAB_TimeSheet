"""
Tests for parse_currency refactoring.
Aims for 100% coverage and functional parity.
"""

from src.utils.parsing import parse_currency


def test_parse_currency_basics():
    assert parse_currency(None) == 0.0
    assert parse_currency(123) == 123.0
    assert parse_currency(123.45) == 123.45
    assert parse_currency("") == 0.0
    assert parse_currency("   ") == 0.0
    assert parse_currency("nan") == 0.0
    assert parse_currency("NAN") == 0.0


def test_parse_currency_symbols():
    assert parse_currency("€ 1.234,56") == 1234.56
    assert parse_currency("1.234,56 €") == 1234.56
    assert parse_currency("1234,56 Euro") == 1234.56
    assert parse_currency("EURO 1234,56") == 1234.56


def test_parse_currency_negative():
    assert parse_currency("-100,50") == -100.5
    assert parse_currency("100,50-") == -100.5
    assert parse_currency("100,50 - ") == -100.5
    assert parse_currency(" - 100,50") == -100.5


def test_parse_currency_formats():
    # IT Format
    assert parse_currency("1.234,56") == 1234.56
    # US Format
    assert parse_currency("1,234.56") == 1234.56

    # Only comma
    assert parse_currency("1234,56") == 1234.56
    assert parse_currency("1,234") == 1.234  # Current logic converts , to .

    # Only dot
    assert parse_currency("1234.56") == 1234.56
    assert parse_currency("1.234.567") == 1234567.0
    assert (
        parse_currency("1.234") == 1.234
    )  # Current logic: if len == 3, does nothing -> 1.234
    assert parse_currency("10.5") == 10.5
    assert parse_currency("10.50") == 10.5


def test_parse_currency_non_printable():
    # Character \u200b is zero-width space, not printable in some contexts
    # But s = "".join(c for c in s if c.isprintable()) removes it.
    assert parse_currency("1234\u200b,56") == 1234.56


def test_parse_currency_errors():
    assert parse_currency("not a number") == 0.0
    assert parse_currency("€ ---") == 0.0


def test_parse_currency_scientific_like():
    # Current code mentions scientific or huge numbers but doesn't do special scaling yet
    assert parse_currency("1.23e2") == 123.0
