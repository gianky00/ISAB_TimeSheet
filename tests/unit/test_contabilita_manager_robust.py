from unittest.mock import patch

import pytest

from src.application.services.contabilita_manager import ContabilitaManager


class TestContabilitaManagerRobust:
    @pytest.fixture
    def mock_db_mgr(self, tmp_path):
        path = tmp_path / "contabilita.db"
        with patch("src.application.services.contabilita_manager.db_manager") as mock:
            mock.DB_CONTABILITA = path
            yield mock

    @patch("src.application.services.contabilita.importer_service.ContabilitaImporterService.import_main_data")
    def test_import_data_from_excel_success(self, mock_import):
        """Test importazione dati contabilità successo."""
        mock_import.return_value = (True, "OK", 10, 0)
        success, _msg, added, _removed = ContabilitaManager.import_data_from_excel("file.xlsx")
        assert success is True
        assert added == 10
        mock_import.assert_called_with("file.xlsx", None)

    @patch("src.application.services.contabilita.importer_service.ContabilitaImporterService.import_main_data")
    def test_import_data_from_excel_failure(self, mock_import):
        """Test importazione dati contabilità fallimento."""
        mock_import.return_value = (False, "Error", 0, 0)
        success, msg, _added, _removed = ContabilitaManager.import_data_from_excel("file.xlsx")
        assert success is False
        assert msg == "Error"

    @patch("src.application.services.contabilita.importer_service.ContabilitaImporterService.import_giornaliere")
    def test_import_giornaliere_flow(self, mock_import):
        """Test flusso complesso importazione giornaliere."""
        mock_import.return_value = (True, "OK", 5, 2)
        success, _msg, added, removed = ContabilitaManager.import_giornaliere("root")
        assert success is True
        assert added == 5
        assert removed == 2
        mock_import.assert_called_with("root", None)

    def test_import_giornaliere_root_not_found(self):
        """Test directory giornaliere inesistente."""
        # Non mockiamo il servizio per testare la validazione del path nel manager/servizio
        # ContabilitaManager delega al servizio, il servizio controlla l'esistenza del path
        success, msg, _, _ = ContabilitaManager.import_giornaliere("non_existent_path")
        assert success is False
        assert "non trovata" in msg

    @patch("src.application.services.contabilita.importer_service.ContabilitaImporterService.import_scarico_ore")
    def test_import_scarico_ore(self, mock_import):
        """Test importazione scarico ore."""
        mock_import.return_value = (True, "OK", 100, 0)
        success, _msg, added, _removed = ContabilitaManager.import_scarico_ore("file.xlsx")
        assert success is True
        assert added == 100
        mock_import.assert_called_with("file.xlsx", None)

    def test_getters_delegation(self, mocker):
        """Test delega ai metodi del repository."""
        mock_repo = mocker.patch("src.application.services.contabilita_manager.ContabilitaManager._repo")

        ContabilitaManager.get_available_years()
        mock_repo.get_available_years.assert_called_once()

        ContabilitaManager.get_data_by_year(2024)
        mock_repo.get_data_by_year.assert_called_with(2024, as_objects=False)

    @patch("src.application.services.contabilita_manager.ContabilitaSearch")
    @patch("src.application.services.contabilita_manager.db_manager")
    def test_search_delegation(self, mock_db_mgr, mock_search):
        """Test delega ricerca."""
        ContabilitaManager.search_oda("test")
        mock_search.search_oda.assert_called_with(mock_db_mgr.DB_CONTABILITA, "test")

    @patch("src.application.services.contabilita_manager.ContabilitaStats")
    @patch("src.application.services.contabilita_manager.db_manager")
    def test_stats_delegation(self, mock_db_mgr, mock_stats):
        """Test delega statistiche."""
        ContabilitaManager.get_year_stats(2024)
        mock_stats.get_year_stats.assert_called_with(mock_db_mgr.DB_CONTABILITA, 2024)
