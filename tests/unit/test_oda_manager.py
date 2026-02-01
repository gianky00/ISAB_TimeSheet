from unittest.mock import patch

from src.core.oda_manager import OdaManager


class TestOdaManager:
    @patch("src.core.oda_manager.db_manager")
    def test_init_db(self, mock_db):
        OdaManager.init_db()
        mock_db.init_db.assert_called_once()

    @patch("src.core.oda_manager.db_manager.execute_query")
    def test_get_all_oda_no_filter(self, mock_query):
        mock_query.return_value = [
            (
                "ORG1",
                "2025-01-15",
                "123",
                "10",
                "APERTO",
                "CAT1",
                "Test desc",
                10,
                "PZ",
                "2025-02-01",
                1000.0,
                500.0,
                1500.0,
                "DIV1",
                "DEST1",
                "Nome Dest",
                "FOR001",
                "Fornitore S.r.l.",
                "EMI01",
                "Emittente",
                "CC01",
                "CONTR001",
                "POS1",
                "GRP1",
                "IND1",
                "STATO1",
                "ATT1",
                "1",
                5,
                "UNI",
                200.0,
                "Testo",
            )
        ]

        result = OdaManager.get_all_oda()

        assert len(result) == 1
        assert result[0][2] == "123"  # oda

    @patch("src.core.oda_manager.db_manager.execute_query")
    def test_get_all_oda_with_search(self, mock_query):
        mock_query.return_value = []

        OdaManager.get_all_oda(search_text="fornitore")

        # Verify LIKE params were added (9 params for search)
        call_args = mock_query.call_args
        params = call_args[0][2]
        assert len(params) == 9
        assert "%fornitore%" in params

    @patch(
        "src.core.oda_manager.DataSynchronizer.sync_storico_oda", return_value=(50, 5)
    )
    @patch("src.core.oda_manager.ExcelImporter.import_storico_oda")
    @patch("src.core.sync_tracker.SyncTracker.update_status")
    def test_import_oda_from_excel_success(self, mock_tracker, mock_import, mock_sync):
        mock_import.return_value = (True, "OK", [{"oda": "123"}])

        success, msg, added, removed = OdaManager.import_oda_from_excel("test.xlsx")

        assert success is True
        assert added == 50
        assert removed == 5
        mock_tracker.assert_called_once()

    @patch("src.core.oda_manager.ExcelImporter.import_storico_oda")
    def test_import_oda_from_excel_failure(self, mock_import):
        mock_import.return_value = (False, "File corrupted", [])

        success, msg, added, removed = OdaManager.import_oda_from_excel("bad.xlsx")

        assert success is False
        assert "corrupted" in msg
        assert added == 0
