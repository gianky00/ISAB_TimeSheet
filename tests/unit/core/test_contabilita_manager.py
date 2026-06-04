from unittest.mock import MagicMock, patch

import pytest

from src.application.services.contabilita_manager import ContabilitaManager


class TestContabilitaManager:
    @pytest.fixture
    def mock_repo(self):
        with patch("src.application.services.contabilita_manager.ContabilitaRepository") as mock:
            # Injecting mock repo into class property
            ContabilitaManager._repo = mock.return_value
            yield mock.return_value

    def test_get_available_years(self, mock_repo):
        mock_repo.get_available_years.return_value = [2022, 2023]
        assert ContabilitaManager.get_available_years() == [2022, 2023]

    @patch("src.application.services.contabilita_manager.db_manager.execute_query")
    def test_update_certificato_field_allowed(self, mock_query, mock_repo):
        # Annotazioni è un campo permesso
        success = ContabilitaManager.update_certificato_field(1, "annotazioni", "Nuova nota")
        assert success is True
        assert mock_query.called
        assert "annotazioni = ?" in mock_query.call_args[0][1]

    def test_update_certificato_field_forbidden(self, mock_repo):
        # 'n_oda' non è permesso via questo metodo specifico
        success = ContabilitaManager.update_certificato_field(1, "n_oda", "123")
        assert success is False

    @patch("src.application.services.contabilita_manager.ContabilitaSearch.search_oda")
    def test_search_oda_delegate(self, mock_search, mock_repo):
        mock_search.return_value = [{"n_oda": "123"}]
        res = ContabilitaManager.search_oda("123")
        assert res[0]["n_oda"] == "123"
        assert mock_search.called

    @patch("src.application.services.contabilita_manager.ContabilitaStats.get_year_stats")
    def test_get_year_stats_delegate(self, mock_stats, mock_repo):
        mock_year_stats = MagicMock()
        mock_stats.return_value = mock_year_stats

        res = ContabilitaManager.get_year_stats(2023)
        assert res == mock_year_stats
        assert mock_stats.called

    @patch("src.application.services.contabilita_manager.ContabilitaImporterService.import_main_data")
    def test_import_data_from_excel_delegate(self, mock_import, mock_repo):
        mock_import.return_value = (True, "OK", 100, 0)
        success, _msg, added, _rem = ContabilitaManager.import_data_from_excel("file.xlsx")
        assert success is True
        assert added == 100

    @patch("src.application.services.contabilita_manager.db_manager.execute_query")
    def test_update_certificati_ubicazione_cumulativa(self, mock_query, mock_repo):
        success = ContabilitaManager.update_certificati_ubicazione_by_id_coemi("COE1", "OFFICINA")
        assert success is True
        args = mock_query.call_args[0]
        assert "UPDATE certificati_campione SET ubicazione = ?" in args[1]
        assert args[2] == ("OFFICINA", "COE1")
