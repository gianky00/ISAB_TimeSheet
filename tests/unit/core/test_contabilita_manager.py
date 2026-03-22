from unittest.mock import MagicMock, patch

from src.core.contabilita_manager import ContabilitaManager


class TestContabilitaManager:
    @patch("src.core.contabilita_manager.ExcelImporter")
    @patch("src.core.contabilita_manager.DataSynchronizer")
    def test_import_data_from_excel_success(self, mock_sync, mock_importer):
        """Verifica la delega corretta per l'importazione dei dati contabili."""
        mock_importer.import_contabilita_dati.return_value = (True, "OK", [("row",)], [2024])
        mock_sync.sync_contabilita_dati.return_value = (1, 0)

        success, _msg, added, _removed = ContabilitaManager.import_data_from_excel("file.xlsx")

        assert success is True
        assert added == 1
        mock_sync.sync_contabilita_dati.assert_called_once()

    @patch("src.core.contabilita_manager.db_manager")
    @patch("src.core.contabilita_manager.ExcelImporter")
    @patch("src.core.contabilita_manager.DataSynchronizer")
    def test_import_giornaliere_full_workflow(self, mock_sync, mock_importer, mock_db, tmp_path):
        """Testa il ciclo completo di import giornaliere con preparazione lookup map."""
        # 1. Setup root path
        root = tmp_path / "Giornaliere"
        root.mkdir()

        # 2. Mock DB lookup
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.fetchall.return_value = [("P1", "ODC1")]

        # 3. Mock Importer and Sync
        mock_importer.import_giornaliere.return_value = (True, "Imported", [("row",)], [2025])
        mock_sync.sync_giornaliere.return_value = (5, 0)

        success, msg, added, _removed = ContabilitaManager.import_giornaliere(str(root))

        assert success is True
        assert added == 5
        assert "2025" in msg
        # Verifica che il lookup_map sia stato passato all'importer
        args = mock_importer.import_giornaliere.call_args[0]
        assert args[1] == {"P1": "ODC1"}

    @patch("src.core.contabilita_manager.db_manager")
    def test_update_certificato_field_logic(self, mock_db):
        """Verifica la validazione e l'esecuzione dell'update certificato."""
        # Caso valido
        res = ContabilitaManager.update_certificato_field(1, "annotazioni", "Nuova Nota")
        assert res is True
        assert "SET annotazioni =" in mock_db.execute_query.call_args[0][1]

        # Caso non valido (campo non ammesso)
        res_invalid = ContabilitaManager.update_certificato_field(1, "id", "999")
        assert res_invalid is False

    @patch("src.core.contabilita_manager.ContabilitaSearch")
    def test_search_oda_delegation(self, mock_search):
        mock_search.search_oda.return_value = []
        ContabilitaManager.search_oda("query")
        mock_search.search_oda.assert_called_once()
