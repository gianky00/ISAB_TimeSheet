from unittest.mock import patch

from src.core.license_hwid import _get_linux_hardware_id, _get_windows_hardware_id, get_hardware_id


class TestLicenseHWID:
    @patch("src.core.license_hwid.platform.system")
    def test_get_hardware_id_windows(self, mock_system):
        mock_system.return_value = "Windows"
        with patch("src.core.license_hwid._get_windows_hardware_id", return_value="WIN-HWID"):
            assert get_hardware_id() == "WIN-HWID"

    @patch("src.core.license_hwid.platform.system")
    def test_get_hardware_id_linux(self, mock_system):
        mock_system.return_value = "Linux"
        with patch("src.core.license_hwid._get_linux_hardware_id", return_value="LIN-HWID"):
            assert get_hardware_id() == "LIN-HWID"

    @patch("src.core.license_hwid.platform.system")
    @patch("src.core.license_hwid.uuid.getnode", return_value=123456789)
    def test_get_hardware_id_fallback(self, mock_uuid, mock_system):
        mock_system.return_value = "Darwin"
        assert get_hardware_id() == "123456789"

    @patch("src.core.license_hwid.subprocess.check_output")
    def test_get_windows_hardware_id_wmic(self, mock_sub):
        # Simula output WMIC
        mock_sub.return_value = b"SerialNumber\nSER123\n"
        res = _get_windows_hardware_id()
        assert res == "SER123"

    @patch("src.core.license_hwid.subprocess.check_output")
    def test_get_windows_hardware_id_powershell(self, mock_sub):
        # Fallback se WMIC fallisce
        mock_sub.side_effect = [Exception("WMIC fail"), b"PS-SER456\n"]
        res = _get_windows_hardware_id()
        assert res == "PS-SER456"

    @patch("src.core.license_hwid.subprocess.check_output")
    def test_get_linux_hardware_id_lsblk(self, mock_sub):
        mock_sub.return_value = b"LNX-SER789\n"
        res = _get_linux_hardware_id()
        assert res == "LNX-SER789"

    def test_get_linux_hardware_id_machine_id(self, fs):
        with patch("src.core.license_hwid.subprocess.check_output", side_effect=Exception()):
            fs.create_file("/etc/machine-id", contents="mid123")
            res = _get_linux_hardware_id()
            assert res == "mid123"

    @patch("src.core.license_hwid.platform.system", return_value="Windows")
    @patch("src.core.license_hwid._get_windows_hardware_id", return_value=None)
    def test_get_hardware_id_error(self, mock_win, mock_sys):
        assert get_hardware_id() == "ERROR_GETTING_ID"
