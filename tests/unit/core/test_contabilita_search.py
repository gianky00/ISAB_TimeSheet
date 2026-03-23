import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from src.core.contabilita_search import ContabilitaSearch


class TestContabilitaSearch:
    @pytest.fixture
    def db_path(self, tmp_path):
        p = tmp_path / "test_search.db"
        p.touch()
        return p

    @patch("src.core.database.db_manager.get_connection")
    def test_search_oda_fts5_fallback_to_like(self, mock_get_conn, db_path):
        """Verifica il fallback su LIKE se FTS5 fallisce (es. tabella non esistente)."""
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value

        # 1. Simula errore FTS5
        mock_cursor.execute.side_effect = [sqlite3.OperationalError("no such table"), None]
        # 2. Simula risultato da LIKE
        mock_cursor.fetchall.return_value = [("ODA1", "Desc", "ODC1")]

        results = ContabilitaSearch.search_oda(db_path, "query")

        assert len(results) == 1
        assert results[0]["codice_oda"] == "ODA1"
        # Verifica che siano state tentate entrambe le query
        assert mock_cursor.execute.call_count == 2

    @patch("src.core.database.db_manager.get_connection")
    def test_search_extended_with_year_filter(self, mock_get_conn, db_path):
        """Verifica che il filtro anno venga applicato correttamente nelle query estese."""
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = []

        results = ContabilitaSearch.search_extended(db_path, "rossi", year=2025)

        assert "GIORNALIERE" in results
        # Verifica che l'anno sia presente nei parametri SQL delle sub-query
        calls = mock_cursor.execute.call_args_list
        # Almeno una query (Giornaliere o Scarico Ore) deve contenere il filtro anno
        year_param_found = any("2025-%" in str(c) for c in calls)
        assert year_param_found is True

    def test_fmt_date_robustness(self):
        """Testa la conversione date ISO -> IT con vari input."""
        assert ContabilitaSearch._fmt_date("2026-03-21") == "21/03/2026"
        assert ContabilitaSearch._fmt_date("2026-03-21 14:00:00") == "21/03/2026"
        assert ContabilitaSearch._fmt_date("invalid-date") == "invalid-date"
        assert ContabilitaSearch._fmt_date(None) == ""
        assert ContabilitaSearch._fmt_date("") == ""
