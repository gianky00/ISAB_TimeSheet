import pytest
from src.utils.parsing import parse_currency

@pytest.mark.parametrize("input_val, expected", [
    # Basic cases
    (None, 0.0),
    (100, 100.0),
    (100.50, 100.50),
    ("50", 50.0),
    ("nan", 0.0),
    ("NaN", 0.0),
    ("", 0.0),
    ("   ", 0.0),

    # Italian format (Comma decimal, Dot thousands)
    ("1.234,56", 1234.56),
    ("1.000,00", 1000.00),
    ("508,83", 508.83),
    ("0,50", 0.50),

    # US/International format (Dot decimal, Comma thousands)
    ("1,234.56", 1234.56),
    ("1,000.00", 1000.00),
    ("508.83", 508.83),

    # Symbols and Text
    ("€ 50,00", 50.0),
    ("50,00 €", 50.0),
    ("Euro 100", 100.0),
    ("100 euro", 100.0),

    # Negative numbers
    ("-50", -50.0),
    ("- 50,00", -50.0),
    ("50,00 -", -50.0),
    ("€ -10", -10.0),

    # Edge cases (Ambiguous dots)
    ("1.234.567", 1234567.0), # Multiple dots = thousands
    ("1.000", 1.0), # Single dot with 3 digits = standard float logic (ambiguous but defined behavior)
    ("1.5", 1.5),   # Single dot normal

    # Invalid
    ("abc", 0.0),
    ("12.34.56,78", 123456.78), # Messy but parsable
])
def test_parse_currency(input_val, expected):
    assert parse_currency(input_val) == expected