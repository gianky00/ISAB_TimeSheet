from src.utils.parsing import parse_currency


class TestParsingSuite:
    def test_parse_currency_it_standard(self):
        """Verifica formato italiano standard."""
        assert parse_currency("1.234,56") == 1234.56  # noqa: PLR2004
        assert parse_currency("1234,56") == 1234.56  # noqa: PLR2004
        assert parse_currency("€ 50,00") == 50.0  # noqa: PLR2004

    def test_parse_currency_us_standard(self):
        """Verifica formato US standard."""
        assert parse_currency("1,234.56") == 1234.56  # noqa: PLR2004
        assert parse_currency("1234.56") == 1234.56  # noqa: PLR2004

    def test_parse_currency_ambiguous_dot(self):
        """Verifica gestione del punto ambiguo."""
        # Un punto solo con 3 cifre dopo viene trattato come migliaia (formato IT)
        assert parse_currency("1.000") == 1000.0  # noqa: PLR2004
        # Più di un punto -> migliaia sicure
        assert parse_currency("1.234.567") == 1234567.0  # noqa: PLR2004

    def test_parse_currency_negative_variations(self):
        """Verifica gestione del segno meno in varie posizioni."""
        assert parse_currency("-10,50") == -10.5  # noqa: PLR2004
        assert parse_currency("10,50-") == -10.5  # noqa: PLR2004
        assert parse_currency(" - 10,50 ") == -10.5  # noqa: PLR2004

    def test_parse_currency_cleaning(self):
        """Verifica rimozione testo e caratteri sporchi."""
        assert parse_currency("50 Euro") == 50.0  # noqa: PLR2004
        assert parse_currency(" 100 \n ") == 100.0  # noqa: PLR2004
        assert parse_currency("NaN") == 0.0
        assert parse_currency(None) == 0.0

    def test_parse_currency_numeric_inputs(self):
        """Verifica input già numerici."""
        assert parse_currency(1234.5) == 1234.5  # noqa: PLR2004
        assert parse_currency(100) == 100.0  # noqa: PLR2004

    def test_parse_currency_extreme_cases(self):
        """Verifica casi estremi di stringhe non numeriche."""
        assert parse_currency("ABC") == 0.0
        assert parse_currency("") == 0.0
