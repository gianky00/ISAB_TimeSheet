from unittest.mock import MagicMock, patch

from src.core.initialization.license_verifier import LicenseVerifier
from src.core.license_validator import LicenseStatus


class TestLicenseVerifier:
    @patch("src.core.initialization.license_verifier.get_detailed_license_status")
    @patch("src.core.initialization.license_verifier.get_hardware_id")
    @patch("src.core.initialization.license_verifier.run_update")
    def test_verify_license_valid(self, mock_update, mock_hwid, mock_status):
        mock_status.return_value = (LicenseStatus.VALID, "")
        step = MagicMock()

        LicenseVerifier.verify_license(step)
        assert mock_hwid.called
        assert mock_status.called
        assert step.call_count == 3
