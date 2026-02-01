from datetime import datetime, timedelta
from unittest.mock import patch

from src.core.auth_monitor import (
    _build_access_maps,
    _normalize,
    check_expiring_isab_authorizations,
)


class TestAuthMonitorRobust:
    def test_normalize(self):
        assert _normalize("  Rossi   Mario  ") == "ROSSI MARIO"
        assert _normalize("rossi mario") == "ROSSI MARIO"
        assert _normalize(123) == "123"
        assert _normalize(None) == "NONE"

    def test_build_access_maps_formats(self):
        # Test vari formati data
        today = datetime.now()
        date_10_days_ago = (today - timedelta(days=10)).strftime("%Y-%m-%d")
        date_40_days_ago = (today - timedelta(days=40)).strftime("%d/%m/%Y")

        raw_data = [
            ("Rossi", "Mario", "RSSMRA80A01H501Z", date_10_days_ago),
            ("Bianchi", "Luigi", None, date_40_days_ago),
            ("Verdi", "Anna", "", "invalid-date"),
        ]

        last_by_cf, last_by_name = _build_access_maps(raw_data)

        assert "RSSMRA80A01H501Z" in last_by_cf
        assert last_by_cf["RSSMRA80A01H501Z"][0] == 10

        name_key = ("BIANCHI", "LUIGI")
        assert name_key in last_by_name
        assert last_by_name[name_key][0] == 40

        assert ("VERDI", "ANNA") not in last_by_name

    def test_build_access_maps_priority(self):
        # Verifica che mantenga la data più recente (delta minore)
        today = datetime.now()
        d1 = (today - timedelta(days=50)).strftime("%Y-%m-%d")
        d2 = (today - timedelta(days=5)).strftime("%Y-%m-%d")

        raw_data = [("Rossi", "Mario", "CF1", d1), ("Rossi", "Mario", "CF1", d2)]

        last_by_cf, _ = _build_access_maps(raw_data)
        assert last_by_cf["CF1"][0] == 5

    @patch("src.core.database.db_manager.execute_query")
    def test_check_expiring_authorizations_logic(self, mock_query):
        today = datetime.now()

        # 1. Mock Dipendenti
        mock_query.side_effect = [
            # Risultato query dipendenti
            [
                ("ROSSI", "MARIO", "CF_ROSSI"),  # Scaduto
                ("BIANCHI", "LUIGI", "CF_BIANCHI"),  # In scadenza
                ("VERDI", "ANNA", "CF_VERDI"),  # Attivo
                ("NERI", "PAOLO", None),  # Fallback nome - In scadenza
            ],
            # Risultato query timbrature
            [
                (
                    "ROSSI",
                    "MARIO",
                    "CF_ROSSI",
                    (today - timedelta(days=40)).strftime("%Y-%m-%d"),
                ),
                (
                    "BIANCHI",
                    "LUIGI",
                    "CF_BIANCHI",
                    (today - timedelta(days=25)).strftime("%Y-%m-%d"),
                ),
                (
                    "VERDI",
                    "ANNA",
                    "CF_VERDI",
                    (today - timedelta(days=5)).strftime("%Y-%m-%d"),
                ),
                (
                    "NERI",
                    "PAOLO",
                    "QUALCHE_CF",
                    (today - timedelta(days=22)).strftime("%Y-%m-%d"),
                ),
            ],
        ]

        results = check_expiring_isab_authorizations()

        # Dovrebbe trovare 3 persone (Rossi, Bianchi, Neri)
        assert len(results) == 3

        # Rossi: Scaduta (>30)
        rossi = next(r for r in results if r["cognome"] == "ROSSI")
        assert rossi["stato"] == "SCADUTA"
        assert rossi["giorni_trascorsi"] == 40

        # Bianchi: In scadenza (20-30)
        bianchi = next(r for r in results if r["cognome"] == "BIANCHI")
        assert bianchi["stato"] == "IN SCADENZA"

        # Neri: In scadenza (match per nome, cf_mancante=True)
        neri = next(r for r in results if r["cognome"] == "NERI")
        assert neri["stato"] == "IN SCADENZA"
        assert neri["cf_mancante"] is True

    @patch(
        "src.core.database.db_manager.execute_query", side_effect=Exception("DB Error")
    )
    def test_check_expiring_authorizations_error(self, mock_query):
        # Deve gestire l'eccezione e tornare lista vuota
        results = check_expiring_isab_authorizations()
        assert results == []
