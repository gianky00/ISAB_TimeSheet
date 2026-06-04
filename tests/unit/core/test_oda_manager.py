from unittest.mock import MagicMock, patch

from src.application.services.oda_manager import OdaManager


class TestOdaManager:
    @patch("src.application.services.oda_manager.OdaRepository.get_all")
    def test_get_all_oda(self, mock_get):
        mock_get.return_value = [("1", "2023-01-01")]
        res = OdaManager.get_all_oda(search_text="test")
        assert len(res) == 1
        mock_get.assert_called_with("test", as_objects=False)

    @patch("src.application.services.oda_manager.Pipeline")
    @patch("src.application.services.oda_manager.SyncTracker.update_status")
    def test_import_oda_from_excel_success(self, mock_sync, mock_pipeline):
        mock_p = MagicMock()
        mock_p.run.return_value = {
            "success": True,
            "total_added": 10,
            "total_removed": 2,
            "message": "Import OK",
        }
        mock_pipeline.return_value = mock_p

        success, _msg, added, removed = OdaManager.import_oda_from_excel("oda.xlsx")

        assert success is True
        assert added == 10
        assert removed == 2
        assert mock_sync.called

    @patch("src.application.services.oda_manager.Pipeline")
    def test_import_oda_from_excel_failure(self, mock_pipeline):
        mock_p = MagicMock()
        mock_p.run.return_value = {"success": False, "message": "File error"}
        mock_pipeline.return_value = mock_p

        success, msg, _added, _removed = OdaManager.import_oda_from_excel("oda.xlsx")
        assert success is False
        assert msg == "File error"

    @patch("src.application.services.oda_manager.db_manager.init_db")
    def test_init_db(self, mock_init):
        OdaManager.init_db()
        assert mock_init.called
