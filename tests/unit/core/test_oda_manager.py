from unittest.mock import patch

from src.core.oda_manager import OdaManager


class TestOdaManager:
    @patch("src.core.database.repositories.OdaRepository.get_all")
    def test_get_all_oda_search_date_conversion(self, mock_get_all):
        """Verifica la delega al repository per la ricerca OdA."""
        mock_get_all.return_value = []

        # Caso 1: Ricerca testuale semplice
        OdaManager.get_all_oda("12345")
        mock_get_all.assert_called_with("12345", as_objects=False)

        # Caso 2: Ricerca per data
        OdaManager.get_all_oda("21/03/2026")
        mock_get_all.assert_called_with("21/03/2026", as_objects=False)

    @patch("src.core.oda_manager.Pipeline.run")
    def test_import_oda_from_excel_failure(self, mock_pipeline_run):
        """Verifica gestione errore se l'importer Excel fallisce."""
        mock_pipeline_run.return_value = {
            "success": False,
            "message": "File Corrotto",
            "total_added": 0,
            "total_removed": 0,
        }

        success, msg, added, _removed = OdaManager.import_oda_from_excel("fake.xlsx")

        assert success is False
        assert msg == "File Corrotto"
        assert added == 0
