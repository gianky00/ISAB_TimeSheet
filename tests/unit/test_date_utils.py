from datetime import UTC, date, datetime

from src.utils.date_utils import (
    calculate_days_diff,
    format_date_iso,
    format_date_it,
    format_datetime_for_filename,
    format_days_ago,
    get_date_range,
    get_status_by_days,
    is_same_day,
    parse_date_flexible,
    parse_datetime_flexible,
)


class TestDateUtils:
    def test_parse_date_flexible(self):
        # Success cases
        assert parse_date_flexible("2024-01-15") == date(2024, 1, 15)
        assert parse_date_flexible("15/01/2024") == date(2024, 1, 15)
        assert parse_date_flexible(r"15\01\2024") == date(2024, 1, 15)

        # None cases
        assert parse_date_flexible(None) is None
        assert parse_date_flexible("None") is None
        assert parse_date_flexible("-") is None
        assert parse_date_flexible("") is None
        assert parse_date_flexible("invalid") is None

    def test_parse_datetime_flexible(self):
        assert parse_datetime_flexible("2024-01-15 14:30:00") == datetime(2024, 1, 15, 14, 30, 0, tzinfo=UTC)
        assert parse_datetime_flexible("15/01/2024 14:30:00") == datetime(2024, 1, 15, 14, 30, 0, tzinfo=UTC)
        assert parse_datetime_flexible("invalid") is None

    def test_format_date_it(self):
        d = date(2024, 1, 15)
        dt = datetime(2024, 1, 15, 14, 30, 0)

        assert format_date_it(d) == "15/01/2024"
        assert format_date_it(dt) == "15/01/2024"
        assert format_date_it(dt, include_time=True) == "15/01/2024 14:30:00"
        assert format_date_it(None) == "-"

    def test_format_date_iso(self):
        assert format_date_iso(date(2024, 1, 15)) == "2024-01-15"
        assert format_date_iso(None) == "-"

    def test_calculate_days_diff(self):
        d1 = date(2024, 1, 15)
        d2 = date(2024, 1, 10)

        # Diff is from_date - date_obj
        assert calculate_days_diff(d2, from_date=d1) == 5
        assert calculate_days_diff(d1, from_date=d2) == -5
        assert calculate_days_diff(None) is None

    def test_get_status_by_days(self):
        # thresholds default: (20, 30)
        assert get_status_by_days(None) == ("unknown", "#6c757d")
        assert get_status_by_days(10) == ("ok", "#198754")
        assert get_status_by_days(25) == ("warning", "#fd7e14")
        assert get_status_by_days(35) == ("expired", "#dc3545")

    def test_format_days_ago(self):
        assert format_days_ago(None) == "-"
        assert format_days_ago(0) == "Oggi"
        assert format_days_ago(1) == "Ieri"
        assert format_days_ago(5) == "5 giorni fa"

    def test_get_date_range(self):
        end = date(2024, 1, 15)
        start, end_res = get_date_range(10, from_date=end)
        assert end_res == end
        assert start == date(2024, 1, 5)

    def test_format_datetime_for_filename(self):
        dt = datetime(2024, 1, 15, 14, 30, 0)
        assert format_datetime_for_filename(dt) == "15-01-2024_14-30"

    def test_is_same_day(self):
        dt1 = datetime(2024, 1, 15, 10, 0)
        dt2 = datetime(2024, 1, 15, 20, 0)
        dt3 = datetime(2024, 1, 16, 10, 0)

        assert is_same_day(dt1, dt2) is True
        assert is_same_day(dt1, dt3) is False
