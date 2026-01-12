import pytest
from src.utils.parsing import parse_currency

class TestParsingSuite:
    """Test approfonditi per src/utils/parsing.py."""

    def test_parse_none_empty(self):
        """Test valori nulli o vuoti."""
        assert parse_currency(None) == 0.0
        assert parse_currency("") == 0.0
        assert parse_currency("   ") == 0.0

    def test_parse_numeric_types(self):
        """Test tipi già numerici."""
        assert parse_currency(100) == 100.0
        assert parse_currency(100.50) == 100.50

    def test_parse_currency_clean_symbols(self):
        """Test rimozione simboli valuta."""
        assert parse_currency("€ 50,00") == 50.0
        assert parse_currency("50,00 €") == 50.0
        assert parse_currency("Euro 50") == 50.0
        assert parse_currency("EURO 50") == 50.0

    def test_parse_negative(self):
        """Test numeri negativi."""
        assert parse_currency("-50,00") == -50.0
        assert parse_currency("50,00-") == -50.0
        assert parse_currency("- 50,00") == -50.0

    def test_format_italian_standard(self):
        """Test formato 1.234,56 (IT)."""
        assert parse_currency("1.234,56") == 1234.56
        assert parse_currency("10.000,00") == 10000.00
        assert parse_currency("1234,56") == 1234.56 # Senza migliaia

    def test_format_us_standard(self):
        """Test formato 1,234.56 (US)."""
        assert parse_currency("1,234.56") == 1234.56
        assert parse_currency("10,000.00") == 10000.00
        assert parse_currency("1234.56") == 1234.56 # Senza migliaia

    def test_ambiguous_single_dot(self):
        """
        Test casi ambigui con un solo punto.
        La logica corrente: se parti decimali != 3 char -> float standard.
        """
        assert parse_currency("10.50") == 10.50
        assert parse_currency("10.5") == 10.5
        # "1.234" è ambiguo. Codice dice: se 3 cifre, potrebbe essere migliaia o float.
        # Al momento 'parse_currency' fallisce nel decidere e prova float(s).
        # Quindi "1.234" -> float("1.234") -> 1.234
        assert parse_currency("1.234") == 1.234 

    def test_nan_handling(self):
        """Test gestione stringa 'nan'."""
        assert parse_currency("nan") == 0.0
        assert parse_currency("NAN") == 0.0

    def test_cleanup_garbage(self):
        """Test pulizia caratteri strani."""
        # Il codice non rimuove lettere arbitrarie, quindi float("12a34") fallisce -> return 0.0
        assert parse_currency("12a34") == 0.0