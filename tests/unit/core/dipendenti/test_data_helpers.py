from datetime import UTC, datetime, timedelta

from src.application.services.dipendenti.data_helpers import (
    build_timbrature_maps,
    compute_employee_status,
    format_db_date,
    normalize_name,
)


class TestDataHelpers:
    def test_normalize_name(self):
        assert normalize_name("  mario  rossi  ") == "MARIO ROSSI"
        assert normalize_name(None) == ""
        assert normalize_name("") == ""
        assert normalize_name(123) == "123"

    def test_build_timbrature_maps(self):
        today = datetime.now(UTC)
        date1 = (today - timedelta(days=5)).strftime("%Y-%m-%d")
        date2 = (today - timedelta(days=10)).strftime("%d/%m/%Y")

        accessi = [
            ("Rossi", "Mario", "CF1", f"{date1} 10:00:00"),
            ("Verdi", "Luigi", None, f"{date2} 09:00:00"),
            ("Rossi", "Mario", "CF1", f"{today.strftime('%Y-%m-%d')} 08:00:00"),  # Newer
        ]

        last_by_cf, last_by_name, normalize = build_timbrature_maps(accessi)

        assert "CF1" in last_by_cf
        assert last_by_cf["CF1"][0] == 0  # Most recent (today)

        name_key = (normalize("Rossi"), normalize("Mario"))
        assert name_key in last_by_name
        assert last_by_name[name_key][0] == 0

        verdi_key = (normalize("Verdi"), normalize("Luigi"))
        assert last_by_name[verdi_key][0] == 10
        assert last_by_name[verdi_key][1] == (today - timedelta(days=10)).strftime("%d/%m/%Y")

    def test_build_timbrature_maps_invalid_date(self):
        accessi = [("A", "B", "C", "invalid-date")]
        l_cf, l_name, _ = build_timbrature_maps(accessi)
        assert len(l_cf) == 0
        assert len(l_name) == 0

    def test_compute_employee_status(self):
        normalize = normalize_name
        l_cf = {"CF1": (5, "20/05/2026")}
        l_name = {("VERDI", "LUIGI"): (10, "15/05/2026")}

        # Case 1: Match by CF
        row1 = [None, "Rossi", "Mario", None, None, None, None, "CF1"]
        diff, warn, last, _, _, cf = compute_employee_status(row1, l_cf, l_name, normalize)
        assert diff == 5
        assert warn is False
        assert last == "20/05/2026"
        assert cf == "CF1"

        # Case 2: Match by Name (CF missing in row)
        row2 = [None, "Verdi", "Luigi", None, None, None, None, ""]
        diff, warn, last, _, _, cf = compute_employee_status(row2, l_cf, l_name, normalize)
        assert diff == 10
        assert warn is True  # CF missing but name found
        assert last == "15/05/2026"

        # Case 3: No match
        row3 = [None, "Neri", "Paolo", None, None, None, None, "CF3"]
        diff, warn, last, _, _, cf = compute_employee_status(row3, l_cf, l_name, normalize)
        assert diff is None
        assert warn is False

    def test_format_db_date(self):
        assert format_db_date("2024-05-24 10:30:00") == "24/05/2024 10:30:00"
        assert format_db_date(None) == "-"
        assert format_db_date("None") == "-"
        assert format_db_date("invalid") == "invalid"
