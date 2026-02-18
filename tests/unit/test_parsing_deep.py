from src.utils.parsing import parse_currency


class TestParsingDeep:
    def test_parse_currency_formats(self):
        assert parse_currency("1.234,56") == 1234.56
        assert parse_currency("1,234.56") == 1234.56
        assert parse_currency("1234,56") == 1234.56
        assert parse_currency("1234.56") == 1234.56
        assert parse_currency("€ 1.234,56") == 1234.56
        assert parse_currency("50,00 Euro") == 50.0
        assert parse_currency("-50,00") == -50.0
        assert parse_currency("50,00 -") == -50.0
        assert parse_currency(None) == 0.0
        assert parse_currency("") == 0.0
        assert parse_currency("nan") == 0.0
        assert parse_currency(100) == 100.0
        assert parse_currency(100.5) == 100.5

    def test_parse_currency_ambiguous(self):
        # In formato italiano 1.000 è mille.
        # Il parser privilegia il formato italiano per stringhe ambigue con 3 cifre dopo il punto.
        assert parse_currency("1.000") == 1000.0
        # 1.000.000 -> more than one dot, definitely thousands
        assert parse_currency("1.000.000") == 1000000.0

    def test_parse_currency_invalid(self):
        assert parse_currency("not a number") == 0.0
