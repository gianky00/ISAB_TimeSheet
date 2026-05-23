from src.utils.parsing import parse_currency


class TestParsingUtils:
    def test_parse_currency_basics(self):
        assert parse_currency(None) == 0.0
        assert parse_currency("") == 0.0
        assert parse_currency(10) == 10.0
        assert parse_currency(12.5) == 12.5

    def test_parse_currency_it_format(self):
        # Virgola come decimale
        assert parse_currency("12,50") == 12.5
        # Punto come migliaia
        assert parse_currency("1.200") == 1200.0
        # Misto
        assert parse_currency("1.234,56") == 1234.56

    def test_parse_currency_en_format(self):
        # Virgola come migliaia
        assert parse_currency("1,234.56") == 1234.56
        # Punto come decimale
        assert parse_currency("12.50") == 12.5

    def test_parse_currency_negative(self):
        # Dash
        assert parse_currency("-10,50") == -10.5
        # Parenthesis (standard contabile)
        assert parse_currency("(100,00)") == -100.0

    def test_parse_currency_scientific(self):
        assert parse_currency("1.2e2") == 120.0
        assert parse_currency("1,2E-1") == 0.12

    def test_parse_currency_noise_and_whitelist(self):
        assert parse_currency("Euro 1.000,00") == 1000.0
        assert parse_currency("1.000,00 EUR") == 1000.0
        assert parse_currency("Importo: 50,00") == 50.0

        # Test noise non in whitelist (torna 0.0 se non valida integrità)
        # Nota: La logica attuale in _validate_currency_integrity ritorna False
        # se c'è rumore alfabetico NON in whitelist.
        assert parse_currency("Qualcosa di strano 10,00") == 0.0

    def test_smart_convert_edge_cases(self):
        # 1.234 -> migliaia perché 3 cifre dopo
        assert parse_currency("1.234") == 1234.0
        # 1.23 -> decimale perché < 3 cifre
        assert parse_currency("1.23") == 1.23
        # 1.234.567 -> migliaia
        assert parse_currency("1.234.567") == 1234567.0

    def test_corrupted_separators(self):
        # Separatori consecutivi
        assert parse_currency("1,,50") == 1.5
        assert parse_currency("1..50") == 1.5
        # Nessun numero
        assert parse_currency("Euro") == 0.0
