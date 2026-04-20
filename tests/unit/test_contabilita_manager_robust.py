from unittest.mock import MagicMock, patch

import pytest

from src.core.contabilita_manager import ContabilitaManager


class TestContabilitaManagerRobust:
    @pytest.fixture
    def mock_db_mgr(self, tmp_path):
        path = tmp_path / "contabilita.db"
        with patch("src.core.contabilita_manager.db_manager") as mock:
            mock.DB_CONTABILITA = path
            yield mock

    @patch("src.core.contabilita_manager.ExcelImporter")
    @patch("src.core.contabilita_manager.DataSynchronizer")
    def test_import_data_from_excel_success(self, mock_sync, mock_importer, mock_db_mgr):
        """Test importazione dati contabilità successo."""
        mock_importer.import_contabilita_dati.return_value = (
            True,
            "OK",
            [("row",)],
            [2024],
        )
        mock_sync.sync_contabilita_dati.return_value = (10, 0)

        success, _msg, added, _removed = ContabilitaManager.import_data_from_excel("file.xlsx")

        assert success is True
        assert added == 10
        mock_importer.import_contabilita_dati.assert_called_with("file.xlsx", None)
        # Verifica che sia stato usato il database corretto dal manager
        mock_sync.sync_contabilita_dati.assert_called_with(mock_db_mgr.DB_CONTABILITA, [("row",)], [2024])

    @patch("src.core.contabilita_manager.ExcelImporter")
    @patch("src.core.contabilita_manager.DataSynchronizer")
    def test_import_data_from_excel_failure(self, mock_sync, mock_importer, mock_db_mgr):
        """Test importazione dati contabilità fallimento."""
        mock_importer.import_contabilita_dati.return_value = (False, "Error", [], [])

        success, msg, _added, _removed = ContabilitaManager.import_data_from_excel("file.xlsx")

        assert success is False
        assert msg == "Error"
        mock_sync.sync_contabilita_dati.assert_not_called()

    @patch("src.core.contabilita_manager.ExcelImporter")
    @patch("src.core.contabilita_manager.DataSynchronizer")
    def test_import_giornaliere_flow(self, mock_sync, mock_importer, mock_db_mgr, tmp_path):
        """Test flusso complesso importazione giornaliere."""
        # 1. Setup Mock DB per Lookup Map
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_mgr.get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        # Risultato query lookup: n_prev -> odc
        mock_cursor.fetchall.return_value = [("5400123", "ODC_A")]

        # 2. Setup Mock Excel Importer
        mock_importer.import_giornaliere.return_value = (
            True,
            "OK",
            [("new_row",)],
            [2024],
        )

        # 3. Setup Mock Sync
        mock_sync.sync_giornaliere.return_value = (5, 2)

        root_path = tmp_path / "Giornaliere"
        root_path.mkdir()

        success, _msg, added, removed = ContabilitaManager.import_giornaliere(str(root_path))

        assert success is True
        assert added == 5
        assert removed == 2

        # Verifica che sia stato passato il lookup map corretto
        args = mock_importer.import_giornaliere.call_args
        assert args[0][1] == {"5400123": "ODC_A"}

        # Verifica uso DB corretto nel sync
        mock_sync.sync_giornaliere.assert_called_with(mock_db_mgr.DB_CONTABILITA, [("new_row",)], [2024])

    def test_import_giornaliere_root_not_found(self):
        """Test directory giornaliere inesistente."""
        success, msg, _, _ = ContabilitaManager.import_giornaliere("non_existent_path")
        assert success is False
        assert "non trovata" in msg

    @patch("src.core.contabilita_manager.ExcelImporter")
    @patch("src.core.contabilita_manager.DataSynchronizer")
    @patch("src.core.contabilita_manager.db_manager")
    def test_import_scarico_ore(self, mock_db_mgr, mock_sync, mock_importer):
        """Test importazione scarico ore."""
        mock_importer.import_scarico_ore.return_value = (True, "OK", [("row",)])
        mock_sync.sync_scarico_ore.return_value = (100, 0)

        success, _msg, added, _removed = ContabilitaManager.import_scarico_ore("file.xlsx")

        assert success is True
        assert added == 100
        mock_sync.sync_scarico_ore.assert_called_with(mock_db_mgr.DB_CONTABILITA, [("row",)])

    @patch("src.core.contabilita_manager.ContabilitaQueries")
    @patch("src.core.contabilita_manager.db_manager")
    def test_getters_delegation(self, mock_db_mgr, mock_queries):
        """Test delega ai metodi di query."""
        ContabilitaManager.get_available_years()
        mock_queries.get_available_years.assert_called_with(mock_db_mgr.DB_CONTABILITA)

        ContabilitaManager.get_data_by_year(2024)
        mock_queries.get_data_by_year.assert_called_with(mock_db_mgr.DB_CONTABILITA, 2024)

    @patch("src.core.contabilita_manager.ContabilitaSearch")
    @patch("src.core.contabilita_manager.db_manager")
    def test_search_delegation(self, mock_db_mgr, mock_search):
        """Test delega ricerca."""
        ContabilitaManager.search_oda("test")
        mock_search.search_oda.assert_called_with(mock_db_mgr.DB_CONTABILITA, "test")

        ContabilitaManager.search_extended("query")
        mock_search.search_extended.assert_called_with(mock_db_mgr.DB_CONTABILITA, "query", None, 100)

    @patch("src.core.contabilita_manager.ContabilitaStats")
    @patch("src.core.contabilita_manager.db_manager")
    def test_stats_delegation(self, mock_db_mgr, mock_stats):
        """Test delega statistiche."""
        ContabilitaManager.get_year_stats(2024)
        mock_stats.get_year_stats.assert_called_with(mock_db_mgr.DB_CONTABILITA, 2024)
