from unittest.mock import patch

from src.core.oda_manager import OdaManager


class TestOdaManager:
    @patch("src.core.oda_manager.db_manager")
    def test_get_all_oda_search_date_conversion(self, mock_db):
        """Verifica la conversione smart delle date nella ricerca OdA."""
        mock_db.execute_query.return_value = []

        # Caso 1: Ricerca testuale semplice
        OdaManager.get_all_oda("12345")
        params = mock_db.execute_query.call_args[0][2]
        assert "%12345%" in params

        # Caso 2: Ricerca per data italiana (DD/MM/YYYY)
        OdaManager.get_all_oda("21/03/2026")
        query_params = mock_db.execute_query.call_args[0][2]
        # Deve essere convertita in formato ISO per il DB SQLite
        assert "%2026-03-21%" in query_params

    @patch("src.core.oda_manager.StoricoOdaImporter")
    @patch("src.core.oda_manager.DataSynchronizer")
    @patch("src.core.sync_tracker.SyncTracker.update_status")
    def test_import_oda_from_excel_failure(self, mock_tracker, mock_sync, mock_importer):
        """Verifica gestione errore se l'importer Excel fallisce."""
        mock_importer.import_storico_oda.return_value = (False, "File Corrotto", [])

        success, msg, added, _removed = OdaManager.import_oda_from_excel("fake.xlsx")

        assert success is False
        assert msg == "File Corrotto"
        assert added == 0
        mock_sync.sync_storico_oda.assert_not_called()
