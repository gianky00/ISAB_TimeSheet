
import pytest
from src.utils.parsing import parse_currency

class TestParsing:
    def test_parse_currency_basics(self):
        assert parse_currency(None) == 0.0
        assert parse_currency(123.45) == 123.45
        assert parse_currency("123.45") == 123.45
        assert parse_currency("123,45") == 123.45
        assert parse_currency("  ") == 0.0
        assert parse_currency("nan") == 0.0

    def test_parse_currency_italian(self):
        assert parse_currency("1.234,56") == 1234.56
        assert parse_currency("€ 50,00") == 50.0
        assert parse_currency("50,83 Euro") == 50.83

    def test_parse_currency_international(self):
        assert parse_currency("1,234.56") == 1234.56
        assert parse_currency("508.83") == 508.83

    def test_parse_currency_negative(self):
        assert parse_currency("-1.234,56") == -1234.56
        assert parse_currency("1.234,56 -") == -1234.56
        assert parse_currency(" - 50,00") == -50.0

    def test_parse_currency_multiple_dots(self):
        assert parse_currency("1.234.567,89") == 1234567.89
        assert parse_currency("1.000.000") == 1000000.0

    def test_parse_currency_invalid(self):
        assert parse_currency("invalid") == 0.0
        assert parse_currency("abc 123 def") == 0.0
