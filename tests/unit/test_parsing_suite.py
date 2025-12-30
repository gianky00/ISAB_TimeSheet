"""
Tests for src.utils.parsing module.
"""
import pytest
from src.utils import parsing

def test_parse_currency():
    assert parsing.parse_currency("1.000,50") == 1000.50
    assert parsing.parse_currency("1,50 €") == 1.50
    assert parsing.parse_currency("-10,00") == -10.00
    assert parsing.parse_currency(None) == 0.0
    assert parsing.parse_currency(123) == 123.0
    
    # Ambiguous cases handled by heuristic
    # "1.000" -> 1000? or 1.0? 
    # Logic says: if 3 digits after dot, it's risky. But standard float conversion takes precedence if no comma.
    # Let's verify behavior with existing code: 
    # "1.000". split('.')[1] is '000' len 3. Logic -> pass (leaves dot). float("1.000") is 1.0.
    assert parsing.parse_currency("1.000") == 1.0