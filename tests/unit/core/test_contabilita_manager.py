from unittest.mock import MagicMock, patch

from src.core.contabilita_manager import ContabilitaManager


class TestContabilitaManager:
    @patch("src.core.contabilita_manager.ContabilitaImporterService.import_main_data")
    def test_import_data_from_excel(self, mock_import):
        mock_import.return_value = (True, "OK", 100, 0)
        res = ContabilitaManager.import_data_from_excel("path.xlsx")
        assert res[0] is True
        assert mock_import.called

    @patch("src.core.contabilita_manager.ContabilitaImporterService.import_giornaliere")
    def test_import_giornaliere(self, mock_import):
        mock_import.return_value = (True, "OK", 50, 0)
        res = ContabilitaManager.import_giornaliere("/root")
        assert res[0] is True
        assert mock_import.called

    @patch("src.core.contabilita_manager.ContabilitaSearch.search_oda")
    def test_search_oda(self, mock_search):
        mock_search.return_value = [{"oda": "123"}]
        res = ContabilitaManager.search_oda("123")
        assert len(res) == 1
        assert res[0]["oda"] == "123"

    @patch("src.core.contabilita_manager.ContabilitaStats.get_year_stats")
    def test_get_year_stats(self, mock_stats):
        mock_stats.return_value = MagicMock()
        res = ContabilitaManager.get_year_stats(2023)
        assert res is not None
        assert mock_stats.called

    @patch("src.core.contabilita_manager.db_manager.execute_query")
    def test_update_certificato_field_success(self, mock_query):
        res = ContabilitaManager.update_certificato_field(1, "annotazioni", "test")
        assert res is True
        assert mock_query.called

    def test_update_certificato_field_invalid(self):
        res = ContabilitaManager.update_certificato_field(1, "invalid_field", "test")
        assert res is False

    @patch("src.core.contabilita_manager.db_manager.execute_query")
    def test_update_certificati_ubicazione(self, mock_query):
        res = ContabilitaManager.update_certificati_ubicazione_by_id_coemi("COE123", "LAB")
        assert res is True
        assert mock_query.called

    @patch("src.core.contabilita_manager.ContabilitaRepository.get_available_years")
    def test_get_available_years(self, mock_repo):
        mock_repo.return_value = [2022, 2023]
        assert ContabilitaManager.get_available_years() == [2022, 2023]
