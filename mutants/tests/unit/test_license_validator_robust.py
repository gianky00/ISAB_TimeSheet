from datetime import datetime
from unittest.mock import MagicMock, patch

from src.core.license_validator import (
    LicenseStatus,
    get_detailed_license_status,
    get_hardware_id,
)


class TestLicenseValidatorRobust:
    @patch("platform.system", return_value="Windows")
    @patch(
        "src.core.license_validator._get_windows_hardware_id", return_value="MOCK_HWID"
    )
    def test_get_hardware_id_windows(self, mock_win, mock_plat):
        assert get_hardware_id() == "MOCK_HWID"

    @patch("src.core.license_validator._get_license_paths")
    @patch("src.core.license_validator.get_license_info")
    @patch("src.core.license_validator._calculate_sha256", return_value="FAKE_HASH")
    @patch("src.core.license_validator.get_hardware_id", return_value="VALID_HWID")
    @patch("src.core.time_manager.get_trusted_time")
    def test_verify_license_full_logic(
        self, mock_time, mock_hwid, mock_sha, mock_info, mock_paths
    ):
        # Setup percorsi mock
        paths = {"dir": MagicMock(), "config": MagicMock(), "manifest": MagicMock()}
        for p in paths.values():
            p.exists.return_value = True
        mock_paths.return_value = paths

        # Setup manifest
        with patch("builtins.open", MagicMock()):
            with patch("json.load", return_value={"config.dat": "FAKE_HASH"}):
                # Caso 1: Valida
                mock_info.return_value = {
                    "Hardware ID": "VALID_HWID",
                    "Scadenza Licenza": "31/12/2026",
                    "Cliente": "Test User",
                }
                mock_time.return_value = (datetime(2026, 2, 1), True)

                status, msg = get_detailed_license_status()
                assert status == LicenseStatus.VALID
                assert "Test User" in msg

                # Caso 2: Scaduta
                mock_info.return_value["Scadenza Licenza"] = "01/01/2026"
                status, msg = get_detailed_license_status()
                assert status == LicenseStatus.EXPIRED

                # Caso 3: HWID Errato
                mock_info.return_value["Scadenza Licenza"] = "31/12/2026"
                mock_info.return_value["Hardware ID"] = "WRONG_HWID"
                status, msg = get_detailed_license_status()
                assert status == LicenseStatus.INVALID
                assert "Hardware ID" in msg

    @patch("src.core.license_validator._get_license_paths")
    def test_verify_license_missing(self, mock_paths):
        paths = {"dir": MagicMock(), "config": MagicMock(), "manifest": MagicMock()}
        paths["dir"].exists.return_value = True
        paths["config"].exists.return_value = False  # Manca file config
        mock_paths.return_value = paths

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.MISSING

    @patch("src.core.license_validator.get_license_info", return_value=None)
    @patch("src.core.license_validator._get_license_paths")
    @patch(
        "src.core.license_validator._check_integrity_with_manifest",
        return_value=(LicenseStatus.VALID, ""),
    )
    def test_verify_license_info_error(self, mock_integrity, mock_paths, mock_info):
        paths = {"dir": MagicMock(), "config": MagicMock(), "manifest": MagicMock()}
        for p in paths.values():
            p.exists.return_value = True
        mock_paths.return_value = paths

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.INVALID
        assert "leggere i dati" in msg
