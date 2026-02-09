from unittest.mock import patch

from src.core.contabilita_manager import ContabilitaManager


class TestContabilitaManager:
    @patch("src.core.contabilita_manager.db_manager")
    def test_init_db(self, mock_db):
        ContabilitaManager.init_db()
        mock_db.init_db.assert_called_once()

    @patch(
        "src.core.contabilita_manager.ExcelImporter.scan_scarico_ore_rows",
        return_value=500,
    )
    def test_scan_scarico_ore_rows(self, mock_scan):
        result = ContabilitaManager.scan_scarico_ore_rows("test.xlsx")
        assert result == 500

    @patch("src.core.contabilita_manager.ExcelImporter.scan_workload", return_value=(10, 5))
    def test_scan_workload(self, mock_scan):
        sheets, files = ContabilitaManager.scan_workload("dati.xlsx", "giornaliere/")
        assert sheets == 10
        assert files == 5

    @patch(
        "src.core.contabilita_manager.DataSynchronizer.sync_contabilita_dati",
        return_value=(100, 5),
    )
    @patch("src.core.contabilita_manager.ExcelImporter.import_contabilita_dati")
    def test_import_data_from_excel_success(self, mock_import, mock_sync):
        mock_import.return_value = (True, "OK", [{"row": 1}], [2024])

        success, _msg, added, removed = ContabilitaManager.import_data_from_excel("test.xlsx")

        assert success is True
        assert added == 100
        assert removed == 5

    @patch("src.core.contabilita_manager.ExcelImporter.import_contabilita_dati")
    def test_import_data_from_excel_failure(self, mock_import):
        mock_import.return_value = (False, "File not found", [], [])

        success, msg, added, _removed = ContabilitaManager.import_data_from_excel("missing.xlsx")

        assert success is False
        assert "File not found" in msg
        assert added == 0

    @patch(
        "src.core.contabilita_manager.DataSynchronizer.sync_scarico_ore",
        return_value=(50, 10),
    )
    @patch("src.core.contabilita_manager.ExcelImporter.import_scarico_ore")
    def test_import_scarico_ore_success(self, mock_import, mock_sync):
        mock_import.return_value = (True, "OK", [{"data": "test"}])

        success, _msg, added, _removed = ContabilitaManager.import_scarico_ore("ore.xlsx")

        assert success is True
        assert added == 50

    @patch(
        "src.core.contabilita_manager.ContabilitaQueries.get_available_years",
        return_value=[2024, 2025],
    )
    def test_get_available_years(self, mock_query):
        years = ContabilitaManager.get_available_years()
        assert 2024 in years
        assert 2025 in years

    @patch(
        "src.core.contabilita_manager.ContabilitaQueries.get_data_by_year",
        return_value=[(1, "Test")],
    )
    def test_get_data_by_year(self, mock_query):
        data = ContabilitaManager.get_data_by_year(2024)
        assert len(data) == 1

    @patch(
        "src.core.contabilita_manager.ContabilitaSearch.search_oda",
        return_value=[{"codice_oda": "123"}],
    )
    def test_search_oda(self, mock_search):
        results = ContabilitaManager.search_oda("123")
        assert len(results) == 1
        assert results[0]["codice_oda"] == "123"

    @patch("src.core.contabilita_manager.ContabilitaStats.get_year_stats")
    def test_get_year_stats(self, mock_stats):
        mock_stats.return_value = {"total_prev": 100000, "total_ore": 500}

        stats = ContabilitaManager.get_year_stats(2024)

        assert stats["total_prev"] == 100000
