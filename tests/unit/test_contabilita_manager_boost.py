import pytest
from src.core.contabilita_manager import ContabilitaManager
from unittest.mock import MagicMock, patch
from pathlib import Path

class TestContabilitaManagerDeep:
    def test_scan_scarico_ore_rows_proxy(self):
        with patch("src.core.excel_importer.ExcelImporter.scan_scarico_ore_rows", return_value=50):
            res = ContabilitaManager.scan_scarico_ore_rows("fake.xlsx")
            assert res == 50

    def test_scan_workload_proxy(self):
        with patch("src.core.excel_importer.ExcelImporter.scan_workload", return_value=(10, 5)):
            res = ContabilitaManager.scan_workload("f1.xlsx", "dir")
            assert res == (10, 5)

    def test_import_giornaliere_path_not_exists(self, tmp_path):
        res = ContabilitaManager.import_giornaliere(str(tmp_path / "missing"))
        assert res[0] is False
        assert "non trovata" in res[1]

    @patch("src.core.contabilita_manager.db_manager.get_connection")
    def test_import_data_fail_flow(self, mock_conn):
        # Test failure in excel import step
        with patch("src.core.excel_importer.ExcelImporter.import_contabilita_dati", return_value=(False, "Err", [], [])):
            res = ContabilitaManager.import_data_from_excel("fake.xlsx")
            assert res[0] is False
            assert res[1] == "Err"
