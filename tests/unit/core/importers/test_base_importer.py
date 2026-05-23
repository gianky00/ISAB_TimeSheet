from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

from src.core.importers.base import BaseImporter


class TestBaseImporter:
    def test_get_pd(self):
        assert BaseImporter._get_pd() is pd

    @patch("src.core.importers.base.msoffcrypto")
    @patch("src.core.importers.base.config_manager.load_config")
    def test_decrypt_if_encrypted_with_msoffcrypto(self, mock_load, mock_msoff, fs):
        mock_load.return_value = {"excel_decryption_password": "test"}
        mock_office_file = MagicMock()
        mock_msoff.OfficeFile.return_value = mock_office_file

        test_file = Path("/test.xlsx")
        fs.create_file(str(test_file), contents="encrypted_content")

        _decrypted_obj, was_encrypted = BaseImporter._decrypt_if_encrypted(test_file)

        assert was_encrypted is True
        assert mock_office_file.load_key.called
        assert mock_office_file.decrypt.called

    @patch("src.core.importers.base.msoffcrypto", None)
    def test_decrypt_if_encrypted_no_msoffcrypto(self, fs):
        test_file = Path("/test.xlsx")
        decrypted_obj, was_encrypted = BaseImporter._decrypt_if_encrypted(test_file)

        assert was_encrypted is False
        assert decrypted_obj == test_file

    def test_identify_sheet_year(self):
        # Extract from string
        assert BaseImporter._identify_sheet_year("Dati_2023") == 2023
        assert BaseImporter._identify_sheet_year("2024") == 2024

        # Invalid year range
        assert BaseImporter._identify_sheet_year("1999") is None
        assert BaseImporter._identify_sheet_year("2101") is None

        # Specific names mapping to current year
        curr_year = datetime.now(UTC).year
        assert BaseImporter._identify_sheet_year("Dati") == curr_year
        assert BaseImporter._identify_sheet_year("PREVENTIVI") == curr_year
        assert BaseImporter._identify_sheet_year("Riepilogo") == curr_year

        # Unknown
        assert BaseImporter._identify_sheet_year("Foglio1") is None

    @patch("src.core.importers.base.pd.ExcelFile")
    def test_get_excel_file_engines(self, mock_excel_file):
        file_obj = MagicMock()

        # Test Calamine
        mock_excel_file.return_value = "calamine_engine"
        res = BaseImporter._get_excel_file(file_obj)
        assert res == "calamine_engine"
        mock_excel_file.assert_called_with(file_obj, engine="calamine")

        # Test fallback a standard pd.ExcelFile se calamine fallisce
        mock_excel_file.side_effect = [ValueError("No calamine"), "standard_engine"]
        res = BaseImporter._get_excel_file(file_obj)
        assert res == "standard_engine"

        # Test fallback a openpyxl se anche standard fallisce
        mock_excel_file.side_effect = [
            ValueError("No calamine"),
            ValueError("No standard"),
            "openpyxl_engine",
        ]
        res = BaseImporter._get_excel_file(file_obj)
        assert res == "openpyxl_engine"
        assert mock_excel_file.call_args_list[-1][1]["engine"] == "openpyxl"
