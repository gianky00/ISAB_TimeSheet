from datetime import UTC, datetime
from unittest.mock import patch

from src.core.auth_monitor import _normalize, _parse_date, check_expiring_isab_authorizations


class TestAuthMonitor:
    def test_normalize(self):
        assert _normalize("  rossi  mario  ") == "ROSSI MARIO"
        assert _normalize("MARIO") == "MARIO"

    def test_parse_date(self):
        assert _parse_date("2024-01-15").day == 15
        assert _parse_date("15/01/2024").month == 1
        assert _parse_date("invalid") is None

    @patch("src.core.database.db_manager.execute_query")
    def test_check_expiring_isab_authorizations_logic(self, mock_query):
        # Setup THRESHOLD_DAYS: warning=45, expired=60 (presumibilmente)
        # Mocking today as 2024-05-17
        with patch("src.core.auth_monitor.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 5, 17, tzinfo=UTC)
            mock_dt.strptime = datetime.strptime

            # Dipendenti:
            # 1. Rossi Mario (CF: RSSMRA) - Ultimo 10 giorni fa (OK)
            # 2. Bianchi Luigi (CF: BNCLGU) - Ultimo 50 giorni fa (WARNING)
            # 3. Verdi Giovanni (CF: VRDGVN) - Ultimo 100 giorni fa (EXPIRED)
            # 4. Neri Paolo (No CF in anagrafica) - Match per Nome (WARNING)

            mock_query.side_effect = [
                # query_dip
                [
                    ("Rossi", "Mario", "RSSMRA"),
                    ("Bianchi", "Luigi", "BNCLGU"),
                    ("Verdi", "Giovanni", "VRDGVN"),
                    ("Neri", "Paolo", ""),
                ],
                # query_timb
                [
                    ("Rossi", "Mario", "RSSMRA", "2024-05-07"),
                    ("Bianchi", "Luigi", "BNCLGU", "2024-03-28"),  # 50 days ago
                    ("Verdi", "Giovanni", "VRDGVN", "2024-02-07"),  # 100 days ago
                    ("Neri", "Paolo", "NRIPLO", "2024-03-28"),  # 50 days ago (Match via name)
                ],
            ]

            results = check_expiring_isab_authorizations()

            # Verify results
            assert len(results) == 3

            res_bianchi = next(r for r in results if r["cognome"] == "BIANCHI")
            assert res_bianchi["stato"] == "SCADUTA"
            assert res_bianchi["giorni_trascorsi"] == 50

            res_verdi = next(r for r in results if r["cognome"] == "VERDI")
            assert res_verdi["stato"] == "SCADUTA"

            res_neri = next(r for r in results if r["cognome"] == "NERI")
            assert res_neri["cf_mancante"] is True
            assert res_neri["stato"] == "SCADUTA"

    @patch("src.core.database.db_manager.execute_query")
    def test_check_expiring_isab_authorizations_error(self, mock_query):
        mock_query.side_effect = Exception("DB Fail")
        assert check_expiring_isab_authorizations() == []
