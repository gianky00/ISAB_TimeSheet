from src.utils.parsing import _normalize_string, _process_separators, parse_currency


class TestParseCurrency:
    def test_none_returns_zero(self):
        assert parse_currency(None) == 0.0

    def test_int_input(self):
        assert parse_currency(50) == 50.0

    def test_float_input(self):
        assert parse_currency(123.45) == 123.45

    def test_empty_string(self):
        assert parse_currency("") == 0.0

    def test_nan_string(self):
        assert parse_currency("nan") == 0.0
        assert parse_currency("NaN") == 0.0

    def test_italian_format_comma_decimal(self):
        assert parse_currency("508,83") == 508.83

    def test_italian_format_full(self):
        assert parse_currency("1.234,56") == 1234.56

    def test_us_format_full(self):
        assert parse_currency("1,234.56") == 1234.56

    def test_us_format_dot_decimal(self):
        assert parse_currency("508.83") == 508.83

    def test_euro_symbol_removal(self):
        assert parse_currency("€ 50,00") == 50.0
        assert parse_currency("€50.00") == 50.0

    def test_euro_word_removal(self):
        assert parse_currency("100 Euro") == 100.0
        assert parse_currency("100euro") == 100.0

    def test_negative_values(self):
        assert parse_currency("-100,50") == -100.5
        assert parse_currency("100,50-") == -100.5

    def test_multiple_dots_thousands(self):
        assert parse_currency("1.234.567") == 1234567.0

    def test_invalid_string(self):
        assert parse_currency("not a number") == 0.0


class TestNormalizeString:
    def test_removes_euro_symbol(self):
        result, _ = _normalize_string("€100")
        assert "€" not in result

    def test_removes_euro_word(self):
        result, _ = _normalize_string("100 Euro")
        assert "euro" not in result.lower()

    def test_detects_negative_prefix(self):
        _, is_neg = _normalize_string("-100")
        assert is_neg is True

    def test_detects_negative_suffix(self):
        _, is_neg = _normalize_string("100-")
        assert is_neg is True


class TestProcessSeparators:
    def test_comma_only_becomes_decimal(self):
        assert _process_separators("100,50") == "100.50"

    def test_dot_only_stays(self):
        assert _process_separators("100.50") == "100.50"

    def test_italian_mixed(self):
        # Italian: dot=thousands, comma=decimal
        assert _process_separators("1.234,56") == "1234.56"

    def test_us_mixed(self):
        # US: comma=thousands, dot=decimal
        assert _process_separators("1,234.56") == "1234.56"
