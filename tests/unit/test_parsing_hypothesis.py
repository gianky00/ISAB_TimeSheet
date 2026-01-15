from hypothesis import given, strategies as st
from src.utils.parsing import parse_currency

def test_parse_currency_basics():
    assert parse_currency("1.234,56") == 1234.56
    assert parse_currency("1,234.56") == 1234.56
    assert parse_currency("508,83") == 508.83
    assert parse_currency(None) == 0.0
    assert parse_currency("nan") == 0.0

@given(st.text())
def test_parse_currency_never_crashes(s):
    # Prova a passare qualsiasi stringa generata casualmente.
    # Non deve MAI sollevare un'eccezione non gestita.
    try:
        parse_currency(s)
    except Exception as e:
        pytest.fail(f"parse_currency crashata con input {s!r}: {e}")

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_parse_currency_with_floats(f):
    # Se passiamo un float direttamente, deve restituire lo stesso valore.
    assert parse_currency(f) == f

@given(st.integers())
def test_parse_currency_with_integers(i):
    # Se passiamo un intero direttamente, deve restituire lo stesso valore come float.
    assert parse_currency(i) == float(i)
