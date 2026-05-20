from unittest.mock import patch

from src.core.contabilita_manager import ContabilitaManager


class TestContabilitaManager:
    @patch("src.core.contabilita_manager.ContabilitaImporterService")
    def test_import_data_from_excel_success(self, mock_importer):
        """Verifica la delega corretta per l'importazione dei dati contabili."""
        mock_importer.import_main_data.return_value = (True, "OK", 1, 0)

        success, _msg, added, _removed = ContabilitaManager.import_data_from_excel("file.xlsx")

        assert success is True
        assert added == 1
        mock_importer.import_main_data.assert_called_once_with("file.xlsx", None)

    @patch("src.core.contabilita_manager.db_manager")
    @patch("src.core.contabilita_manager.ContabilitaImporterService")
    def test_import_giornaliere_full_workflow(self, mock_importer, mock_db, tmp_path):
        """Testa il ciclo completo di import giornaliere."""
        root = tmp_path / "Giornaliere"
        root.mkdir()

        # 3. Mock Importer
        mock_importer.import_giornaliere.return_value = (True, "Imported", 5, 0)

        success, msg, added, _removed = ContabilitaManager.import_giornaliere(str(root))

        assert success is True
        assert added == 5
        assert "Imported" in msg
        mock_importer.import_giornaliere.assert_called_once_with(str(root), None)

    @patch("src.core.contabilita_manager.db_manager")
    def test_update_certificato_field_logic(self, mock_db):
        """Verifica la validazione e l'esecuzione dell'update certificato."""
        # Caso valido
        res = ContabilitaManager.update_certificato_field(1, "annotazioni", "Nuova Nota")
        assert res is True
        # Verifica chiamata SQL
        args = mock_db.execute_query.call_args[0]
        assert "SET annotazioni =" in args[1]
        assert args[2] == ("Nuova Nota", 1)

        # Caso non valido (campo non ammesso)
        res_invalid = ContabilitaManager.update_certificato_field(1, "id", "999")
        assert res_invalid is False

    @patch("src.core.contabilita_manager.ContabilitaSearch")
    def test_search_oda_delegation(self, mock_search):
        mock_search.search_oda.return_value = []
        ContabilitaManager.search_oda("query")
        mock_search.search_oda.assert_called_once()
