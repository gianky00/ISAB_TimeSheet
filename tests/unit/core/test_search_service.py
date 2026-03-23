from unittest.mock import MagicMock, patch

from src.core.search.search_service import SearchService


class TestSearchService:
    @patch("src.core.search.search_service.ContabilitaManager")
    @patch("src.core.search.search_service.TimbratureStorage")
    @patch("src.core.search.search_service.AuditManager")
    @patch("src.core.search.search_service.db_manager")
    @patch("src.core.search.search_service.CONFIG_DIR")
    def test_search_all_success(self, mock_config, mock_db, mock_audit, mock_timbrature, mock_contabilita):  # noqa: ANN001
        """Test di successo su tutte le categorie di ricerca."""
        # Setup Mocks
        mock_contabilita.search_oda.return_value = [{"codice_oda": "123", "descrizione": "test"}]
        mock_contabilita.search_extended.return_value = {"GIORNALIERE": []}

        mock_timbrature_instance = mock_timbrature.return_value
        mock_timbrature_instance.search_employees.return_value = [{"cognome": "Rossi", "nome": "Mario"}]

        mock_audit_instance = mock_audit.instance.return_value
        mock_audit_instance.get_logs.return_value = [{"action": "Login", "entity": "Admin"}]

        # Mock SQLite connections for local DBs
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.fetchall.return_value = []

        # Ensure path exists for local DB searches
        mock_config.__truediv__.return_value.__truediv__.return_value.exists.return_value = True

        # Execute
        results = SearchService.search_all("login")

        # Assert
        assert len(results["oda"]) == 1
        assert results["employees"][0]["cognome"] == "Rossi"
        assert len(results["audit"]) == 1
        assert "extended" in results

    def test_search_oda_error_handling(self):
        """Verifica che un errore in una categoria non blocchi le altre."""
        with patch(
            "src.core.search.search_service.ContabilitaManager.search_oda", side_effect=Exception("DB Crash")
        ):
            results = SearchService._search_oda("query", 10)
            assert results == []

    @patch("src.core.search.search_service.db_manager")
    @patch("src.core.search.search_service.CONFIG_DIR")
    def test_search_storico_oda_no_file(self, mock_config, mock_db):  # noqa: ANN001
        """Verifica comportamento se il file database non esiste."""
        mock_config.__truediv__.return_value.__truediv__.return_value.exists.return_value = False
        results = SearchService._search_storico_oda("query", 10)
        assert results == []
        mock_db.get_connection.assert_not_called()

    @patch("src.core.search.search_service.db_manager")
    @patch("src.core.search.search_service.CONFIG_DIR")
    def test_search_pdl_query_logic(self, mock_config, mock_db):  # noqa: ANN001
        """Verifica la costruzione della query SQL per PDL."""
        mock_config.__truediv__.return_value.__truediv__.return_value.exists.return_value = True
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value

        # Simula una riga restituita
        mock_cursor.fetchall.return_value = [(123, "Descrizione PDL", "U.T. Nord")]
        # In sqlite3.Row simulation, we need a list of dicts or similar if row_factory is used
        # But SearchService does [dict(row) for row in fetchall()] which requires sqlite3.Row objects.
        # We'll mock the row factory behavior.
        mock_row = {"odl": 123, "descrizione": "Descrizione PDL", "unita_tecnica": "U.T. Nord"}
        mock_cursor.fetchall.return_value = [mock_row]

        results = SearchService._search_pdl("123", 5)

        assert len(results) == 1
        assert results[0]["odl"] == 123  # noqa: PLR2004
        assert mock_cursor.execute.called
        # Verifica che il pattern LIKE sia stato passato correttamente
        query_args = mock_cursor.execute.call_args[0][1]
        assert "%123%" in query_args
