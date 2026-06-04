from datetime import datetime, timedelta
from unittest.mock import patch

from src.application.services.auth_monitor import (
    _build_access_maps,
    _normalize,
    check_expiring_isab_authorizations,
)


class TestAuthMonitor:
    def test_normalize_spaces_and_case(self):
        assert _normalize("  rossi   mario  ") == "ROSSI MARIO"
        assert _normalize("MARIO") == "MARIO"

    def test_build_access_maps_logic(self, mocker):
        # Format: cog, nom, cf, last_date_str
        from datetime import UTC

        fixed_now = datetime(2026, 3, 21, 12, 0, 0, tzinfo=UTC)
        mock_dt = mocker.patch("src.application.services.auth_monitor.datetime")
        mock_dt.now.return_value = fixed_now
        mock_dt.strptime = datetime.strptime

        today = fixed_now
        d30 = (today - timedelta(days=30)).strftime("%d/%m/%Y")
        d10 = (today - timedelta(days=10)).strftime("%d/%m/%Y")

        accessi = [
            ("ROSSI", "MARIO", "RSSMRA80", d30),
            ("BIANCHI", "LUIGI", None, d10),
            ("VERDI", "ANNA", "VRDNNA90", "invalid_date"),
        ]

        last_by_cf, last_by_name = _build_access_maps(accessi)

        assert "RSSMRA80" in last_by_cf
        assert last_by_cf["RSSMRA80"][0] == 30
        assert ("ROSSI", "MARIO") in last_by_name
        assert last_by_name[("ROSSI", "MARIO")][0] == 30

        # BIANCHI only in by_name
        assert ("BIANCHI", "LUIGI") in last_by_name
        assert last_by_name[("BIANCHI", "LUIGI")][0] == 10

        # VERDI should be ignored due to invalid date
        assert "VRDNNA90" not in last_by_cf

    @patch("src.application.services.auth_monitor.db_manager")
    def test_check_expiring_authorizations(self, mock_db, mocker):
        from datetime import UTC

        # Mocking datetime.now(UTC)
        fixed_now = datetime(2026, 3, 21, 12, 0, 0, tzinfo=UTC)
        mock_dt = mocker.patch("src.application.services.auth_monitor.datetime")
        mock_dt.now.return_value = fixed_now
        mock_dt.strptime = datetime.strptime  # Preserve strptime

        today = fixed_now
        d35 = (today - timedelta(days=35)).strftime("%Y-%m-%d")  # Expired
        d25 = (today - timedelta(days=25)).strftime("%Y-%m-%d")  # Expiring
        d5 = (today - timedelta(days=5)).strftime("%Y-%m-%d")  # Active

        # Mock Dipendenti: cog, nom, cf
        mock_db.execute_query.side_effect = [
            # Dipendenti
            [
                ("ROSSI", "MARIO", "RSSMRA80"),  # Expired
                ("BIANCHI", "LUIGI", "BNCLGU70"),  # Expiring
                ("VERDI", "ANNA", "VRDNNA90"),  # Active
                ("NERI", "PAOLO", ""),  # No CF, Expired by Name
            ],
            # Timbrature: cog, nom, cf, data
            [
                ("ROSSI", "MARIO", "RSSMRA80", d35),
                ("BIANCHI", "LUIGI", "BNCLGU70", d25),
                ("VERDI", "ANNA", "VRDNNA90", d5),
                ("NERI", "PAOLO", "", d35),
            ],
        ]
        mock_db.DB_DIPENDENTI = "dip.db"
        mock_db.DB_TIMBRATURE = "timb.db"

        results = check_expiring_isab_authorizations()

        # Should contain ROSSI, BIANCHI, and NERI. VERDI is active (5 days).
        assert len(results) == 3

        # Check ROSSI (Expired)
        rossi = next(r for r in results if r["cognome"] == "ROSSI")
        assert rossi["stato"] == "SCADUTA"
        assert rossi["giorni_trascorsi"] == 35

        # Check BIANCHI (Expiring)
        bianchi = next(r for r in results if r["cognome"] == "BIANCHI")
        assert bianchi["stato"] == "IN SCADENZA"
        assert bianchi["giorni_trascorsi"] == 25

        # Check NERI (No CF, matched by name)
        neri = next(r for r in results if r["cognome"] == "NERI")
        assert neri["cf_mancante"] is True
        assert neri["stato"] == "SCADUTA"

    @patch("src.application.services.auth_monitor.db_manager")
    def test_check_expiring_error_handling(self, mock_db):
        mock_db.execute_query.side_effect = Exception("DB Error")
        results = check_expiring_isab_authorizations()
        assert results == []
