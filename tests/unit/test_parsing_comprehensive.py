from src.utils.parsing import parse_currency


class TestParsingComprehensive:
    def test_parse_currency_none_and_empty(self):
        assert parse_currency(None) == 0.0
        assert parse_currency("") == 0.0
        assert parse_currency("   ") == 0.0

    def test_parse_currency_numeric_types(self):
        assert parse_currency(1234) == 1234.0
        assert parse_currency(1234.56) == 1234.56

    def test_parse_currency_nan(self):
        assert parse_currency("nan") == 0.0
        assert parse_currency("NaN") == 0.0

    def test_parse_currency_symbols(self):
        # Supporta simboli e parole valuta separate da spazio
        assert parse_currency("10,50 Euro") == 10.5
        assert parse_currency("€ 1.234,56") == 1234.56
        assert parse_currency("$ 100.00") == 100.0
        assert parse_currency("100 £") == 100.0

    def test_parse_currency_unprintable_chars(self):
        # Rimuove caratteri nulli
        assert parse_currency("123\x00.45") == 123.45

    def test_parse_currency_negative_positions(self):
        assert parse_currency("-123,45") == -123.45
        assert parse_currency("123,45-") == -123.45
        assert parse_currency("(123,45)") == -123.45

    def test_parse_currency_italian_format(self):
        assert parse_currency("1.234.567,89") == 1234567.89
        assert parse_currency("1.234") == 1234.0  # Rilevato come migliaia

    def test_parse_currency_international_format(self):
        assert parse_currency("1,234,567.89") == 1234567.89
        assert parse_currency("1,234") == 1.234  # Virgola singola = decimale

    def test_parse_currency_single_separators(self):
        assert parse_currency("1234,56") == 1234.56
        assert parse_currency("1234.56") == 1234.56

    def test_parse_currency_consecutive_separators(self):
        # Pulisce separatori duplicati
        assert parse_currency("1,,23") == 1.23
        assert parse_currency("1..23") == 1.23

    def test_parse_currency_not_a_number(self):
        # Stringhe ambigue con lettere mescolate devono restituire 0.0
        assert parse_currency("12.34.ab") == 0.0
        assert parse_currency("12a34") == 0.0
        assert parse_currency("abc") == 0.0

    def test_parse_currency_mixed_garbage(self):
        # Test con testo descrittivo (deve passare se separato)
        assert parse_currency("Prezzo: 1.234,56 €") == 1234.56
        # Ma fallisce se il testo è mescolato alle cifre
        assert parse_currency("12Euro34") == 0.0

    def test_parse_currency_scientific(self):
        assert parse_currency("1.23e2") == 123.0
        assert parse_currency("1.23E-2") == 0.0123
