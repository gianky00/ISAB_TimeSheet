from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from src.core.auth_monitor import (
    _build_access_maps,
    _normalize,
    _parse_date,
    _process_employee_match,
    check_expiring_isab_authorizations,
)


class TestAuthMonitor:
    def test_normalize(self):
        assert _normalize("  mario  rossi  ") == "MARIO ROSSI"
        assert _normalize("MARIO ROSSI") == "MARIO ROSSI"

    def test_parse_date(self):
        assert _parse_date("2023-05-23").year == 2023
        assert _parse_date("23/05/2023").day == 23
        assert _parse_date("invalid") is None

    def test_build_access_maps(self):
        today = datetime.now(UTC)
        date_10_days_ago = (today - timedelta(days=10)).strftime("%Y-%m-%d")
        date_50_days_ago = (today - timedelta(days=50)).strftime("%Y-%m-%d")

        accessi = [
            ("Rossi", "Mario", "CF1", date_10_days_ago),
            ("Bianchi", "Luigi", "CF2", date_50_days_ago),
            ("Rossi", "Mario", "CF1", date_50_days_ago),  # Più vecchio, deve prevalere il 10
        ]

        last_by_cf, last_by_name = _build_access_maps(accessi)

        assert "CF1" in last_by_cf
        assert last_by_cf["CF1"][0] == 10
        assert "CF2" in last_by_cf
        assert last_by_cf["CF2"][0] == 50
        assert last_by_name[("ROSSI", "MARIO")][0] == 10

    def test_process_employee_match_valid(self):
        last_by_cf = {"CF1": (10, "01/01/2023")}
        last_by_name = {("ROSSI", "MARIO"): (10, "01/01/2023")}

        # Sotto la soglia warning (20) -> None
        res = _process_employee_match("Rossi", "Mario", "CF1", last_by_cf, last_by_name)
        assert res is None

    def test_process_employee_match_warning(self):
        # Soglia warning = 20, expired = 30. Usiamo 25.
        last_by_cf = {"CF1": (25, "01/01/2023")}
        last_by_name = {("ROSSI", "MARIO"): (25, "01/01/2023")}

        res = _process_employee_match("Rossi", "Mario", "CF1", last_by_cf, last_by_name)
        assert res is not None
        assert res["stato"] == "IN SCADENZA"
        assert res["cf_mancante"] is False

    def test_process_employee_match_expired(self):
        # Usiamo 40 (> 30)
        last_by_cf = {"CF1": (40, "01/01/2023")}
        last_by_name = {("ROSSI", "MARIO"): (40, "01/01/2023")}

        res = _process_employee_match("Rossi", "Mario", "CF1", last_by_cf, last_by_name)
        assert res is not None
        assert res["stato"] == "SCADUTA"

    def test_process_employee_match_fallback_name(self):
        last_by_cf = {}
        last_by_name = {("ROSSI", "MARIO"): (25, "01/01/2023")}

        res = _process_employee_match("Rossi", "Mario", None, last_by_cf, last_by_name)
        assert res is not None
        assert res["cf_mancante"] is True

    @patch("src.core.auth_monitor.db_manager.execute_query")
    def test_check_expiring_authorizations_integration(self, mock_query):
        # Mock dipendenti
        mock_query.side_effect = [
            [("Rossi", "Mario", "CF1")],  # Risultato query dipendenti
            [("Rossi", "Mario", "CF1", "2020-01-01")],  # Risultato query timbrature (vecchia)
        ]

        with patch("src.core.auth_monitor.get_logger"):
            results = check_expiring_isab_authorizations()
            assert len(results) == 1
            assert results[0]["cognome"] == "ROSSI"
            assert results[0]["stato"] == "SCADUTA"

    @patch("src.core.auth_monitor.db_manager.execute_query", side_effect=Exception("DB down"))
    def test_check_expiring_authorizations_error(self, mock_query):
        results = check_expiring_isab_authorizations()
        assert results == []
