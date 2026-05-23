from datetime import UTC, date, datetime

from src.utils.date_utils import (
    calculate_days_diff,
    format_date_iso,
    format_date_it,
    format_datetime_for_filename,
    format_days_ago,
    get_date_range,
    get_month_name_it,
    get_status_by_days,
    is_same_day,
    parse_date_flexible,
    parse_datetime_flexible,
)


class TestDateUtils:
    def test_parse_date_flexible(self):
        assert parse_date_flexible("2023-05-23") == date(2023, 5, 23)
        assert parse_date_flexible("23/05/2023") == date(2023, 5, 23)
        assert parse_date_flexible("23\\05\\2023") == date(2023, 5, 23)
        assert parse_date_flexible(None) is None
        assert parse_date_flexible("invalid") is None

    def test_parse_datetime_flexible(self):
        dt = parse_datetime_flexible("23/05/2023 10:30:00")
        assert dt.day == 23 and dt.hour == 10
        assert dt.tzinfo == UTC

    def test_format_date_it(self):
        d = date(2023, 5, 23)
        assert format_date_it(d) == "23/05/2023"
        assert format_date_it(None) == "-"

        dt = datetime(2023, 5, 23, 10, 30, 0)
        assert format_date_it(dt, include_time=True) == "23/05/2023 10:30:00"

    def test_format_date_iso(self):
        assert format_date_iso(date(2023, 5, 23)) == "2023-05-23"
        assert format_date_iso(None) == "-"

    def test_calculate_days_diff(self):
        d1 = date(2023, 5, 20)
        d2 = date(2023, 5, 23)
        assert calculate_days_diff(d1, from_date=d2) == 3
        assert calculate_days_diff(None) is None

    def test_get_status_by_days(self):
        # Usando thresholds custom per non dipendere da costanti esterne in questo test
        status, _color = get_status_by_days(5, thresholds=(10, 20))
        assert status == "ok"

        status, _color = get_status_by_days(15, thresholds=(10, 20))
        assert status == "warning"

        status, _color = get_status_by_days(25, thresholds=(10, 20))
        assert status == "expired"

        assert get_status_by_days(None)[0] == "unknown"

    def test_format_days_ago(self):
        assert format_days_ago(0) == "Oggi"
        assert format_days_ago(1) == "Ieri"
        assert format_days_ago(5) == "5 giorni fa"
        assert format_days_ago(None) == "-"

    def test_get_date_range(self):
        end = date(2023, 5, 23)
        start, end_res = get_date_range(10, from_date=end)
        assert end_res == end
        assert start == date(2023, 5, 13)

    def test_format_datetime_for_filename(self):
        dt = datetime(2023, 5, 23, 10, 30)
        assert format_datetime_for_filename(dt) == "23-05-2023_10-30"

    def test_is_same_day(self):
        dt1 = datetime(2023, 5, 23, 10, 0)
        dt2 = datetime(2023, 5, 23, 20, 0)
        dt3 = datetime(2023, 5, 24, 10, 0)
        assert is_same_day(dt1, dt2) is True
        assert is_same_day(dt1, dt3) is False

    def test_get_month_name_it(self):
        assert get_month_name_it(1) == "Gen"
        assert get_month_name_it(1, full=True) == "Gennaio"
        assert get_month_name_it(12, full=True) == "Dicembre"
        assert get_month_name_it(13) == ""
