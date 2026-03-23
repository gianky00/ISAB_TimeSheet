from src.utils.parsing import parse_currency


class TestParsing:
    def test_parse_currency_basic(self):
        """Verifica il parsing di numeri semplici e tipi diretti."""
        assert parse_currency(100) == 100.0
        assert parse_currency(100.5) == 100.5
        assert parse_currency(None) == 0.0
        assert parse_currency("") == 0.0
        assert parse_currency("nan") == 0.0

    def test_parse_currency_it_format(self):
        """Verifica il parsing del formato italiano (punto migliaia, virgola decimale)."""
        assert parse_currency("1.234,56") == 1234.56
        assert parse_currency("1.234") == 1234.0
        assert parse_currency("12,34") == 12.34
        assert parse_currency("€ 1.500") == 1500.0

    def test_parse_currency_us_format(self):
        """Verifica il parsing del formato internazionale/US."""
        assert parse_currency("1,234.56") == 1234.56
        assert parse_currency("1,234") == 1.234  # Virgola trattata come decimale se sola
        assert parse_currency("12.34") == 12.34

    def test_parse_currency_negative(self):
        """Verifica la gestione corretta del segno meno in varie posizioni."""
        assert parse_currency("-100") == -100.0
        assert parse_currency("100 -") == -100.0
        assert parse_currency("- 50,20") == -50.20

    def test_parse_currency_dirty_strings(self):
        """Verifica la pulizia di stringhe con testo extra o caratteri non stampabili."""
        assert parse_currency("Circa 100 Euro") == 100.0
        assert parse_currency("100\u200b.50") == 100.50  # Zero-width space
        assert parse_currency("Prezzo: 1.200,00 €") == 1200.0
        assert parse_currency("invalid") == 0.0
