from unittest.mock import ANY, patch

from src.core.contabilita_manager import ContabilitaManager


class TestContabilitaImport:
    """Test facade ContabilitaManager."""

    @patch("src.core.contabilita_manager.ContabilitaImporterService.import_main_data")
    def test_import_data_delegation(self, mock_import):
        # Setup mock
        mock_import.return_value = (True, "Success", 10, 0)

        # Execute
        result, _msg, added, _removed = ContabilitaManager.import_data_from_excel("dummy.xlsx")

        assert result is True
        assert added == 10
        mock_import.assert_called_once_with("dummy.xlsx", ANY)

    @patch("src.core.contabilita_manager.ContabilitaImporterService.import_giornaliere")
    def test_import_giornaliere_delegation(self, mock_import):
        mock_import.return_value = (True, "OK", 5, 1)
        res = ContabilitaManager.import_giornaliere("/root")
        assert res[0] is True
        assert res[2] == 5
