import pytest
from src.utils.parsing import parse_currency

class TestParsingCoverage:
    """Test suite per src/utils/parsing.py"""

    def test_parse_currency_basics(self):
        assert parse_currency(None) == 0.0
        assert parse_currency(123.45) == 123.45
        assert parse_currency(100) == 100.0
        assert parse_currency("") == 0.0
        assert parse_currency("  ") == 0.0

    def test_parse_currency_it_format(self):
        """Test formato italiano con punti per migliaia e virgola per decimali."""
        assert parse_currency("1.234,56") == 1234.56
        assert parse_currency("508,83") == 508.83

    def test_parse_currency_us_format(self):
        """Test formato US con virgole per migliaia e punto per decimali."""
        assert parse_currency("1,234.56") == 1234.56
        assert parse_currency("508.83") == 508.83

    def test_parse_currency_symbols(self):
        """Test con simboli valuta e testo."""
        assert parse_currency("€ 1.234,56") == 1234.56
        assert parse_currency("1234,56 Euro") == 1234.56
        assert parse_currency("EURO 100") == 100.0

    def test_parse_currency_negative(self):
        """Test numeri negativi."""
        assert parse_currency("-100,50") == -100.5
        assert parse_currency("100,50-") == -100.5
        assert parse_currency(" - 100,50 ") == -100.5

    def test_parse_currency_special_cases(self):
        """Test casi speciali come nan e caratteri invisibili."""
        assert parse_currency("nan") == 0.0
        assert parse_currency("NaN") == 0.0
        # Carattere non printable (null byte rimosso da join c.isprintable())
        assert parse_currency("100\0.50") == 100.5

    def test_parse_currency_dots_and_commas(self):
        """Test logica complessa punti/virgole."""
        # Solo virgola
        assert parse_currency("1234,56") == 1234.56
        
        # Più punti (migliaia)
        assert parse_currency("1.234.567") == 1234567.0
        
        # Solo un punto - ambiguo
        # "1.234" -> 3 cifre dopo punto. Attualmente il codice lascia il punto se == 3.
        # float("1.234") -> 1.234
        assert parse_currency("1.234") == 1.234
        
        # "1.23" -> < 3 cifre -> Decimale
        assert parse_currency("1.23") == 1.23
        
        # "1.2345" -> > 3 cifre -> Decimale
        assert parse_currency("1.2345") == 1.2345

    def test_parse_currency_errors(self):
        """Test gestione errori di parsing."""
        assert parse_currency("abc") == 0.0
        assert parse_currency("€ ---") == 0.0