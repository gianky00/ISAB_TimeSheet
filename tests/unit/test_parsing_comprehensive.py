"""
SafeWork - Parsing Comprehensive Test Suite (100% Coverage)
==========================================================
Test suite definitiva per garantire l'assenza di regressioni nel parsing
di valute, numeri e stringhe sporche.

Matches source code: src/utils/parsing.py
"""

from src.utils.parsing import parse_currency


class TestParsingComprehensive:
    # ========================================================================
    # 1. BASIC INPUT TYPES
    # ========================================================================

    def test_parse_currency_none_and_empty(self):
        """Verifica la gestione di input nulli o vuoti."""
        assert parse_currency(None) == 0.0
        assert parse_currency("") == 0.0
        assert parse_currency("   ") == 0.0
        assert parse_currency("\t\n") == 0.0

    def test_parse_currency_numeric_types(self):
        """Verifica che gli input già numerici vengano passati correttamente."""
        assert parse_currency(100) == 100.0
        assert parse_currency(123.45) == 123.45
        assert isinstance(parse_currency(50), float)
        # Stringa numerica senza separatori
        assert parse_currency("100") == 100.0

    def test_parse_currency_nan(self):
        """Verifica la gestione del valore NaN (stringa)."""
        assert parse_currency("NaN") == 0.0
        assert parse_currency("nan") == 0.0
        assert parse_currency("  nAn  ") == 0.0

    # ========================================================================
    # 2. NORMALIZATION & CLEANING
    # ========================================================================

    def test_parse_currency_symbols(self):
        """Verifica la rimozione di simboli valuta."""
        assert parse_currency("€ 123,45") == 123.45
        assert parse_currency("$ 100.00") == 100.00
        assert parse_currency("£ 50,00") == 50.0
        assert parse_currency("10,50 Euro") == 10.5
        assert parse_currency("20,00 EURO") == 20.0
        assert parse_currency("30,00 eUrO") == 30.0
        # Simboli multipli
        assert parse_currency("€ $ £ 100") == 100.0

    def test_parse_currency_unprintable_chars(self):
        """Verifica la rimozione di caratteri invisibili/non stampabili."""
        # \x00 è null, \x07 è bell, etc.
        assert parse_currency("123\x00,45") == 123.45
        assert parse_currency("\x01 50,00 \x02") == 50.0

    # ========================================================================
    # 3. SIGN HANDLING
    # ========================================================================

    def test_parse_currency_negative_positions(self):
        """Verifica la gestione del segno meno in varie posizioni."""
        assert parse_currency("-123,45") == -123.45
        assert parse_currency("123,45-") == -123.45
        assert parse_currency(" - 123,45 ") == -123.45
        assert parse_currency("123,45 - ") == -123.45
        assert parse_currency(" -123,45 ") == -123.45

    # ========================================================================
    # 4. SEPARATOR LOGIC (THE CORE)
    # ========================================================================

    def test_parse_currency_italian_format(self):
        """Verifica il formato italiano: punto migliaia, virgola decimale."""
        assert parse_currency("1.234,56") == 1234.56
        assert parse_currency("1.000.000,00") == 1000000.0
        assert parse_currency("508,83") == 508.83

    def test_parse_currency_international_format(self):
        """Verifica il formato internazionale: virgola migliaia, punto decimale."""
        assert parse_currency("1,234.56") == 1234.56
        assert parse_currency("1,000,000.00") == 1000000.0
        assert parse_currency("508.83") == 508.83

    def test_parse_currency_single_separators(self):
        """Verifica l'uso di un solo tipo di separatore."""
        # Solo virgola -> interpretata come punto decimale
        assert parse_currency("123,45") == 123.45
        # Solo punto (non ambiguo) -> decimale
        assert parse_currency("123.45") == 123.45
        assert parse_currency("1.2") == 1.2

    def test_parse_currency_multiple_dots(self):
        """Verifica punti multipli (migliaia senza decimali)."""
        assert parse_currency("1.234.567") == 1234567.0
        assert parse_currency("1.000.000") == 1000000.0
        # Punti multipli "sporchi"
        assert parse_currency("1.2.3.4") == 1234.0

    def test_parse_currency_ambiguous_dot(self):
        """
        Verifica il caso ambiguo: un solo punto seguito da 3 cifre.
        In questo progetto, lo trattiamo come separatore delle migliaia (IT).
        """
        assert parse_currency("1.000") == 1000.0
        assert parse_currency("1.234") == 1234.0

    # ========================================================================
    # 5. EDGE CASES & ERRORS
    # ========================================================================

    def test_parse_currency_not_a_number(self):
        """Verifica che stringhe non numeriche restituiscano 0.0 senza crashare."""
        assert parse_currency("abc") == 0.0
        assert parse_currency("12.34.ab") == 0.0
        assert parse_currency("Euro") == 0.0
        assert parse_currency("€") == 0.0
        # Solo "rumore" che viene pulito
        assert parse_currency(" € Euro ") == 0.0

    def test_parse_currency_mixed_garbage(self):
        """Verifica il parsing di stringhe molto sporche."""
        assert parse_currency(" - € 1.234,56 Euro ") == -1234.56
        assert parse_currency(" \x00 50.83 $ ") == 50.83

    def test_parse_currency_consecutive_separators(self):
        """Test con separatori consecutivi o malformati."""
        assert parse_currency("1,,23") == 1.23
        assert parse_currency("1..234") == 1234.0
        assert parse_currency(",,50") == 0.5
        assert parse_currency("..50") == 0.5
