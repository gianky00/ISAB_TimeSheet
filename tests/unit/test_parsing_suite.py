import pytest
from src.utils.parsing import parse_currency

class TestParsingUtils:

    @pytest.mark.parametrize("input_val, expected", [
        ("1.234,56", 1234.56),      # IT format
        ("1,234.56", 1234.56),      # US format
        ("1234.56", 1234.56),       # Simple US
        ("1234,56", 1234.56),       # Simple IT
        ("€ 1.234,56", 1234.56),    # Currency symbol
        ("  500,00  ", 500.0),      # Spacing
        (123.45, 123.45),           # Float input
        (None, 0.0),                # None
        ("", 0.0),                  # Empty
        ("nan", 0.0),               # Textual NaN
    ])
    def test_parse_currency_standard(self, input_val, expected):
        assert parse_currency(input_val) == expected

    def test_parse_currency_ambiguous_thousands(self):
        # 1.000 is usually 1000 in IT, but ambiguous.
        # The logic says: if only one dot and not 3 digits after -> decimal.
        # But "1.000" HAS 3 digits. Logic implies it might try float parsing.
        # Let's verify behavior.
        # If passed as string "1.000" -> logic check dots_count=1. parts[1] len=3.
        # It falls through to float conversion of "1.000" -> 1.0.
        # This is often correct for data coming from systems that serialize floats as 1.000.
        assert parse_currency("1.000") == 1.0 

    def test_parse_currency_dirty_input(self):
        assert parse_currency("Euro 1.200,50") == 1200.50
        assert parse_currency("1.200,50 \u20ac") == 1200.50 # Euro symbol