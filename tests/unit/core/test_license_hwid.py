import subprocess
from unittest.mock import patch

from src.core.license_hwid import _get_linux_hardware_id, _get_windows_hardware_id, get_hardware_id


class TestLicenseHWID:
    @patch("src.core.license_hwid.platform.system", return_value="Windows")
    @patch("src.core.license_hwid._get_windows_hardware_id")
    def test_get_hardware_id_windows(self, mock_win_id, mock_system):
        mock_win_id.return_value = "WIN_HWID"
        assert get_hardware_id() == "WIN_HWID"

    @patch("src.core.license_hwid.platform.system", return_value="Linux")
    @patch("src.core.license_hwid._get_linux_hardware_id")
    def test_get_hardware_id_linux(self, mock_lin_id, mock_system):
        mock_lin_id.return_value = "LINUX_HWID"
        assert get_hardware_id() == "LINUX_HWID"

    @patch("src.core.license_hwid.platform.system", return_value="Darwin")
    @patch("src.core.license_hwid.uuid.getnode", return_value=123456789)
    def test_get_hardware_id_fallback(self, mock_uuid, mock_system):
        assert get_hardware_id() == "123456789"

    @patch("src.core.license_hwid.platform.system", return_value="Darwin")
    @patch("src.core.license_hwid.uuid.getnode", side_effect=Exception("Error"))
    def test_get_hardware_id_fallback_error(self, mock_uuid, mock_system):
        assert get_hardware_id() == "ERROR_GETTING_ID"

    @patch("src.core.license_hwid.subprocess.check_output")
    def test_get_windows_hardware_id_wmic(self, mock_sub):
        mock_sub.return_value = b"SerialNumber \n  WIN_SERIAL_123 \n"
        hwid = _get_windows_hardware_id()
        assert hwid == "WIN_SERIAL_123"

    @patch("src.core.license_hwid.subprocess.check_output")
    def test_get_windows_hardware_id_powershell_disk(self, mock_sub):
        # Fallisce WMIC, passa al primo PS
        mock_sub.side_effect = [
            subprocess.CalledProcessError(1, "cmd"),
            b"PS_SERIAL_456\n",
        ]
        hwid = _get_windows_hardware_id()
        assert hwid == "PS_SERIAL_456"

    @patch("src.core.license_hwid.subprocess.check_output")
    def test_get_windows_hardware_id_powershell_uuid(self, mock_sub):
        # Fallisce WMIC e PS disk, passa a PS uuid
        mock_sub.side_effect = [
            subprocess.CalledProcessError(1, "cmd"),
            subprocess.CalledProcessError(1, "cmd"),
            b"PS_UUID_789\n",
        ]
        hwid = _get_windows_hardware_id()
        assert hwid == "PS_UUID_789"

    @patch("src.core.license_hwid.subprocess.check_output")
    def test_get_linux_hardware_id_lsblk(self, mock_sub):
        mock_sub.return_value = b"LINUX_BLK_123\n"
        hwid = _get_linux_hardware_id()
        assert hwid == "LINUX_BLK_123"

    @patch("src.core.license_hwid.subprocess.check_output", side_effect=Exception("Err"))
    def test_get_linux_hardware_id_machine_id(self, mock_sub, fs):
        fs.create_file("/etc/machine-id", contents="MACHINE_ID_456\n")
        hwid = _get_linux_hardware_id()
        assert hwid == "MACHINE_ID_456"

    @patch("src.core.license_hwid.subprocess.check_output", side_effect=Exception("Err"))
    def test_get_linux_hardware_id_fail(self, mock_sub, fs):
        # Nessun file e subprocess fallisce
        hwid = _get_linux_hardware_id()
        assert hwid is None
