from datetime import date

from src.utils.date_utils import calculate_days_diff, format_date_it, get_month_name_it, parse_date_flexible


def test_parse_date_flexible():
    assert parse_date_flexible("2024-05-17") == date(2024, 5, 17)
    assert parse_date_flexible("17/05/2024") == date(2024, 5, 17)
    assert parse_date_flexible("invalid") is None


def test_format_date_it():
    assert format_date_it(date(2024, 5, 17)) == "17/05/2024"
    assert format_date_it(None) == "-"


def test_calculate_days_diff():
    # Mocking current date for consistent testing could be complex,
    # but we can test the logic with explicit arguments
    d1 = date(2024, 5, 10)
    d2 = date(2024, 5, 17)
    assert calculate_days_diff(d1, from_date=d2) == 7


def test_get_month_name_it():
    assert get_month_name_it(1) == "Gen"
    assert get_month_name_it(1, full=True) == "Gennaio"
    assert get_month_name_it(13) == ""
