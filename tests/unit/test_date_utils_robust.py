from datetime import date, datetime, timedelta
from unittest.mock import patch

import pytest

from src.utils import date_utils


class TestDateUtilsRobust:
    
    # --- Parsing Tests ---
    def test_parse_date_flexible_formats(self):
        """Test parsing di vari formati."""
        # ISO
        assert date_utils.parse_date_flexible("2024-01-15") == date(2024, 1, 15)
        # Italian
        assert date_utils.parse_date_flexible("15/01/2024") == date(2024, 1, 15)
        # Italian with dot (common in Excel)
        assert date_utils.parse_date_flexible("15.01.2024", formats=["%d.%m.%Y"]) == date(2024, 1, 15)
        
    def test_parse_date_flexible_invalid(self):
        """Test parsing stringhe non valide."""
        assert date_utils.parse_date_flexible(None) is None
        assert date_utils.parse_date_flexible("") is None
        assert date_utils.parse_date_flexible("invalid") is None
        assert date_utils.parse_date_flexible("-") is None

    def test_parse_datetime_flexible(self):
        """Test parsing datetime completo."""
        dt_str = "15/01/2024 14:30:00"
        res = date_utils.parse_datetime_flexible(dt_str)
        assert isinstance(res, datetime)
        assert res.hour == 14
        assert res.minute == 30

    # --- Formatting Tests ---
    def test_format_date_it(self):
        """Test formattazione italiana."""
        d = date(2024, 1, 15)
        assert date_utils.format_date_it(d) == "15/01/2024"
        assert date_utils.format_date_it(None) == "-"
        
        # Datetime with time
        dt = datetime(2024, 1, 15, 10, 30, 0)
        assert date_utils.format_date_it(dt, include_time=True) == "15/01/2024 10:30:00"

    def test_format_date_iso(self):
        """Test formattazione ISO."""
        assert date_utils.format_date_iso(date(2024, 1, 15)) == "2024-01-15"
        assert date_utils.format_date_iso(None) == "-"

    # --- Calculation Tests ---
    def test_calculate_days_diff(self):
        """Test differenza giorni."""
        d_past = date(2024, 1, 1)
        d_ref = date(2024, 1, 10)
        
        # Test con data di riferimento esplicita
        assert date_utils.calculate_days_diff(d_past, from_date=d_ref) == 9
        
        # Test con oggi (mockato)
        with patch("src.utils.date_utils.date") as mock_date:
            mock_date.today.return_value = d_ref
            # Nota: calculate_days_diff usa date.today() internamente
            # Dobbiamo essere sicuri che chiami il mock
            res = date_utils.calculate_days_diff(d_past)
            assert res == 9

    def test_get_status_by_days(self):
        """Test logica soglie (OK, Warning, Expired)."""
        # Thresholds default: (20, 30)
        assert date_utils.get_status_by_days(10) == ("ok", "#198754")
        assert date_utils.get_status_by_days(25) == ("warning", "#fd7e14")
        assert date_utils.get_status_by_days(40) == ("expired", "#dc3545")
        assert date_utils.get_status_by_days(None) == ("unknown", "#6c757d")

    def test_format_days_ago(self):
        """Test stringa giorni fa."""
        assert date_utils.format_days_ago(0) == "Oggi"
        assert date_utils.format_days_ago(1) == "Ieri"
        assert date_utils.format_days_ago(5) == "5 giorni fa"
        assert date_utils.format_days_ago(None) == "-"

    def test_get_date_range(self):
        """Test calcolo range date."""
        ref = date(2024, 1, 10)
        start, end = date_utils.get_date_range(days_back=7, from_date=ref)
        assert end == ref
        assert start == date(2024, 1, 3)

    def test_format_datetime_for_filename(self):
        """Test nome file sicuro."""
        dt = datetime(2024, 1, 15, 14, 30, 0)
        assert date_utils.format_datetime_for_filename(dt) == "15-01-2024_14-30"

    def test_is_same_day(self):
        """Test confronto giorni."""
        dt1 = datetime(2024, 1, 1, 10, 0)
        dt2 = datetime(2024, 1, 1, 23, 59)
        dt3 = datetime(2024, 1, 2, 0, 1)
        
        assert date_utils.is_same_day(dt1, dt2) is True
        assert date_utils.is_same_day(dt1, dt3) is False

    @patch("src.gui.styles.constants.MONTHS_IT", ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"])
    @patch("src.gui.styles.constants.MONTHS_IT_FULL", ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"])
    def test_get_month_name_it(self):
        """Test nomi mesi italiani."""
        assert date_utils.get_month_name_it(1) == "Gen"
        assert date_utils.get_month_name_it(1, full=True) == "Gennaio"
        assert date_utils.get_month_name_it(13) == "" # Out of range
