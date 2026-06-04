from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from src.application.services.auth_monitor import (
    _build_access_maps,
    _normalize,
    _parse_date,
    _process_employee_match,
    check_expiring_isab_authorizations,
)
from src.application.services.constants import THRESHOLD_DAYS


class TestAuthMonitor:
    def test_normalize(self):
        assert _normalize("  rossi  mario  ") == "ROSSI MARIO"
        assert _normalize("MARIO") == "MARIO"
        assert _normalize(123) == "123"

    def test_parse_date(self):
        assert _parse_date("2023-05-23").day == 23
        assert _parse_date("23/05/2023").day == 23
        assert _parse_date("invalid") is None
        assert _parse_date(None) is None

    def test_build_access_maps(self):
        today = datetime.now(UTC)
        date1 = (today - timedelta(days=10)).strftime("%Y-%m-%d")
        date2 = (today - timedelta(days=40)).strftime("%Y-%m-%d")

        raw_data = [
            ("ROSSI", "MARIO", "CF1", date1),
            ("VERDI", "LUIGI", "", date2),
            ("ROSSI", "MARIO", "CF1", date2),  # Più vecchio, deve preferire date1
        ]

        last_by_cf, last_by_name = _build_access_maps(raw_data)

        assert last_by_cf["CF1"] == (10, (today - timedelta(days=10)).strftime("%d/%m/%Y"))
        assert last_by_name[("VERDI", "LUIGI")] == (40, (today - timedelta(days=40)).strftime("%d/%m/%Y"))

    def test_process_employee_match_ok(self):
        # Sotto soglia warning
        last_by_cf = {"CF1": (5, "20/05/2026")}
        res = _process_employee_match("ROSSI", "MARIO", "CF1", last_by_cf, {})
        assert res is None

    def test_process_employee_match_warning(self):
        # Tra warning e expired
        days = THRESHOLD_DAYS["warning"] + 1
        last_by_cf = {"CF1": (days, "01/05/2026")}
        res = _process_employee_match("ROSSI", "MARIO", "CF1", last_by_cf, {})
        assert res["stato"] == "IN SCADENZA"
        assert res["giorni_trascorsi"] == days

    def test_process_employee_match_expired(self):
        # Oltre expired
        days = THRESHOLD_DAYS["expired"] + 1
        last_by_cf = {"CF1": (days, "01/01/2026")}
        res = _process_employee_match("ROSSI", "MARIO", "CF1", last_by_cf, {})
        assert res["stato"] == "SCADUTA"

    def test_process_employee_match_fallback_name(self):
        days = THRESHOLD_DAYS["expired"] + 5
        last_by_name = {("ROSSI", "MARIO"): (days, "01/01/2026")}

        # Match per nome perché CF manca in anagrafica o non coincide
        res = _process_employee_match("ROSSI", "MARIO", "", {}, last_by_name)
        assert res["stato"] == "SCADUTA"
        assert res["cf_mancante"] is True

    @patch("src.application.services.auth_monitor.db_manager.execute_query")
    def test_check_expiring_isab_authorizations_integration(self, mock_query):
        # Mock 1: Dipendenti
        # Mock 2: Timbrature
        today = datetime.now(UTC)
        date_exp = (today - timedelta(days=40)).strftime("%Y-%m-%d")

        mock_query.side_effect = [
            [("ROSSI", "MARIO", "CF1")],  # Dipendenti
            [("ROSSI", "MARIO", "CF1", date_exp)],  # Timbrature
        ]

        results = check_expiring_isab_authorizations()
        assert len(results) == 1
        assert results[0]["cognome"] == "ROSSI"
        assert results[0]["stato"] == "SCADUTA"
