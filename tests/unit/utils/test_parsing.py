from src.utils.parsing import parse_currency


class TestParsing:
    def test_parse_currency_basics(self):
        assert parse_currency(None) == 0.0
        assert parse_currency(100) == 100.0
        assert parse_currency(100.5) == 100.5
        assert parse_currency("") == 0.0
        assert parse_currency("  ") == 0.0
        assert parse_currency("NaN") == 0.0

    def test_parse_currency_it_format(self):
        assert parse_currency("1.234,56") == 1234.56
        assert parse_currency("1.234.567,89") == 1234567.89
        assert parse_currency("1234,56") == 1234.56

    def test_parse_currency_int_format(self):
        assert parse_currency("1,234.56") == 1234.56
        assert parse_currency("10.50") == 10.50

    def test_parse_currency_negative(self):
        assert parse_currency("-100,50") == -100.50
        assert parse_currency("(100,50)") == -100.50
        assert parse_currency("  - 10.00  ") == -10.0

    def test_parse_currency_noise(self):
        assert parse_currency("Euro 1.000,00") == 1000.0
        assert parse_currency("Importo: 50.00 EUR") == 50.0
        assert parse_currency("Prezzo: circa 10.50") == 10.5

    def test_parse_currency_scientific(self):
        assert parse_currency("1.23e-4") == 0.000123
        assert parse_currency("1,23e2") == 123.0

    def test_parse_currency_complex_thousands(self):
        # 1.234 -> Interpretato come 1234 (punto migliaia IT)
        assert parse_currency("1.234") == 1234.0
        # 1.23 -> Interpretato come 1.23 (punto decimale)
        assert parse_currency("1.23") == 1.23

    def test_parse_currency_invalid_integrity(self):
        # Test con testo non in whitelist
        assert parse_currency("Attacco Hacker 100.00") == 0.0

    def test_parse_currency_separators_consecutive(self):
        assert parse_currency("100,,50") == 100.50
        assert parse_currency("1...000") == 1000.0
