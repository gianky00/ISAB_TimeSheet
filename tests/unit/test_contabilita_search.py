from unittest.mock import MagicMock, patch

import pytest

from src.core.contabilita_search import ContabilitaSearch


class TestContabilitaSearch:
    @pytest.fixture
    def mock_db_path(self, tmp_path):
        db_file = tmp_path / "contabilita.db"
        db_file.touch()
        return db_file

    def test_search_oda_query_too_short(self, mock_db_path):
        results = ContabilitaSearch.search_oda(mock_db_path, "a")
        assert results == []

    @patch("src.core.contabilita_search.db_manager.get_connection")
    def test_search_oda_fts5_success(self, mock_conn, mock_db_path):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("ODA001", "Manutenzione", "ODC001")]
        mock_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        results = ContabilitaSearch.search_oda(mock_db_path, "manutenzione")

        assert len(results) == 1
        assert results[0]["type"] == "ODA"
        assert results[0]["codice_oda"] == "ODA001"

    @patch("src.core.contabilita_search.db_manager.get_connection")
    def test_search_oda_fts5_fallback_to_like(self, mock_conn, mock_db_path):
        mock_cursor = MagicMock()
        # FTS5 returns empty, LIKE succeeds
        mock_cursor.fetchall.side_effect = [
            [],  # FTS5 empty
            [("ODA002", "Altro Servizio", "ODC002")],  # LIKE success
        ]
        mock_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        results = ContabilitaSearch.search_oda(mock_db_path, "servizio")

        assert len(results) == 1
        assert results[0]["codice_oda"] == "ODA002"

    def test_search_oda_db_not_exists(self, tmp_path):
        fake_path = tmp_path / "nonexistent.db"
        results = ContabilitaSearch.search_oda(fake_path, "test")
        assert results == []

    @patch("src.core.contabilita_search.db_manager.get_connection")
    def test_search_extended(self, mock_conn, mock_db_path):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = [
            [("2025-01-15", "Mario Rossi", "Lavoro X")],  # Giornaliere
            [("2025-01-16", "Luigi Verdi", "Desc Y", "COM01", 8.0)],  # Scarico Ore
            [("Mod01", "Brand", "MAT001")],  # Certificati
        ]
        mock_conn.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        results = ContabilitaSearch.search_extended(mock_db_path, "test", year=2025)

        assert "GIORNALIERE" in results
        assert "CANTIERE" in results
        assert "CERTIFICATI" in results
        assert len(results["GIORNALIERE"]) == 1
        assert len(results["CANTIERE"]) == 1

    def test_search_extended_query_too_short(self, mock_db_path):
        results = ContabilitaSearch.search_extended(mock_db_path, "a")
        assert results == {}

    def test_fmt_date_valid(self):
        result = ContabilitaSearch._fmt_date("2025-01-15")
        assert result == "15/01/2025"

    def test_fmt_date_invalid(self):
        result = ContabilitaSearch._fmt_date("not-a-date")
        assert result == "not-a-date"

    def test_fmt_date_empty(self):
        result = ContabilitaSearch._fmt_date("")
        assert result == ""
