from src.utils.parsing import parse_currency


class TestParsing:
    def test_parse_currency_basics(self):
        assert parse_currency(None) == 0.0
        assert parse_currency(123) == 123.0
        assert parse_currency(123.45) == 123.45
        assert parse_currency("  ") == 0.0
        assert parse_currency("NaN") == 0.0

    def test_parse_currency_formats(self):
        # Italian format
        assert parse_currency("1.234,56") == 1234.56
        assert parse_currency("508,83") == 508.83

        # International format
        assert parse_currency("1,234.56") == 1234.56
        assert parse_currency("508.83") == 508.83

        # Currency symbols
        assert parse_currency("€ 123,45") == 123.45
        assert parse_currency("123,45 Euro") == 123.45
        assert parse_currency("123,45 EURO") == 123.45

    def test_parse_currency_negative(self):
        assert parse_currency("-123,45") == -123.45
        assert parse_currency("123,45 -") == -123.45
        assert parse_currency(" - 123,45 ") == -123.45

    def test_parse_currency_ambiguous_single_dot(self):
        # 1.234 -> if treated as float: 1.234. if treated as IT thousands: 1234.
        # Implementation says: if it has 3 digits after dot, it stays as is (float).
        assert parse_currency("1.234") == 1.234
        assert parse_currency("1.2") == 1.2
        assert parse_currency("1.234.567") == 1234567.0  # Multiple dots -> thousands

    def test_parse_currency_error_fallback(self):
        assert parse_currency("not_a_number") == 0.0

    def test_parse_currency_unprintable(self):
        # Should remove unprintable chars
        assert parse_currency("123\x00,45") == 123.45
