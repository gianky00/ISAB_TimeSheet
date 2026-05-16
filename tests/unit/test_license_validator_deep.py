import base64
import json
from unittest.mock import MagicMock, patch

from src.core.license_validator import (
    LicenseStatus,
    get_detailed_license_status,
    get_hardware_id,
    get_license_info,
)


class TestLicenseValidatorDeep:
    @patch("platform.system", return_value="Windows")
    @patch("subprocess.check_output")
    def test_get_hardware_id_windows_wmic(self, mock_sub, mock_platform):
        mock_sub.return_value = b"SerialNumber\nABC-123\n"
        hwid = get_hardware_id()
        assert hwid == "ABC-123"

    @patch("platform.system", return_value="Linux")
    @patch("subprocess.check_output")
    @patch("os.path.exists", return_value=True)
    def test_get_hardware_id_linux_lsblk(self, mock_exists, mock_sub, mock_platform):
        mock_sub.return_value = b"SN-LINUX-456\n"
        hwid = get_hardware_id()
        assert hwid == "SN-LINUX-456"

    @patch("src.core.license_validator.SecretsManager.get_license_key")
    @patch("src.core.license_validator._get_license_paths")
    def test_get_license_info_decryption(self, mock_paths, mock_get_key):
        from pathlib import Path

        config_path = Path("fake.dat")

        mock_paths.return_value = {"config": config_path}

        # 32-byte key for Fernet

        key = b"12345678901234567890123456789012"

        mock_get_key.return_value = key

        from cryptography.fernet import Fernet

        key_b64 = base64.urlsafe_b64encode(key)

        f = Fernet(key_b64)

        payload = {"Cliente": "Test Client", "Hardware ID": "HW1"}

        encrypted = f.encrypt(json.dumps(payload).encode())

        # Mock both exists and read_bytes on the Path object

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_bytes", return_value=encrypted):
                info = get_license_info()

                assert info is not None

                assert info["Cliente"] == "Test Client"

    @patch("src.core.license_validator._get_license_paths")
    def test_detailed_status_integrity_fail(self, mock_paths):
        from pathlib import Path

        mock_paths.return_value = {
            "dir": Path("dir"),
            "config": Path("conf"),
            "manifest": Path("man"),
        }

        manifest_data = {"config.dat": "CORRECT_HASH"}

        # Mock Path methods to satisfy existence checks

        with patch.object(Path, "exists", return_value=True):
            with patch("builtins.open", MagicMock()) as mock_open:
                mock_open.return_value.__enter__.return_value.read.side_effect = [
                    json.dumps(manifest_data).encode(),  # manifest read
                    b"wrong data",  # config.dat read for hashing
                ]

                # Mock hash calculation to return wrong hash

                with patch(
                    "src.core.license_validator._calculate_sha256",
                    return_value="WRONG_HASH",
                ):
                    status, msg = get_detailed_license_status()

                    assert status == LicenseStatus.INVALID

                    assert "Integrità" in msg

    @patch("src.core.license_validator.get_license_info")
    @patch("src.core.license_validator.get_hardware_id", return_value="MY-HW")
    @patch(
        "src.core.license_validator._check_integrity_with_manifest",
        return_value=(LicenseStatus.VALID, ""),
    )
    def test_detailed_status_hardware_mismatch(self, mock_integrity, mock_hwid, mock_info):
        from pathlib import Path

        mock_info.return_value = {"Hardware ID": "OTHER-HW", "Cliente": "C1"}

        with patch.object(Path, "exists", return_value=True):
            status, msg = get_detailed_license_status()

            assert status == LicenseStatus.INVALID

            assert "Hardware ID non valido" in msg

    @patch("src.core.license_validator.get_license_info")
    @patch("src.core.license_validator.get_hardware_id", return_value="MY-HW")
    @patch(
        "src.core.license_validator._check_integrity_with_manifest",
        return_value=(LicenseStatus.VALID, ""),
    )
    @patch("src.core.license_validator.get_trusted_time")
    def test_detailed_status_expired(self, mock_trusted_time, mock_integrity, mock_hwid, mock_info):
        from datetime import datetime
        from pathlib import Path

        mock_info.return_value = {
            "Hardware ID": "MY-HW",
            "Scadenza Licenza": "01/01/2023",
        }

        # Trusted time is in 2024

        mock_trusted_time.return_value = (datetime(2024, 1, 1), True)

        with patch.object(Path, "exists", return_value=True):
            status, msg = get_detailed_license_status()

            assert status == LicenseStatus.EXPIRED

            assert "SCADUTA" in msg

    @patch("platform.system", return_value="Linux")
    @patch("builtins.open", MagicMock())
    def test_get_hardware_id_linux_machine_id(self, mock_platform):
        from pathlib import Path

        # Fail lsblk, fallback to machine-id

        with patch("subprocess.check_output", side_effect=Exception("no lsblk")):
            with patch.object(
                Path, "exists", side_effect=lambda *args: str(args[0]).replace("\\", "/") == "/etc/machine-id"
            ):
                with patch.object(Path, "read_text", return_value="MACHINE-ID-123"):
                    hwid = get_hardware_id()

                    assert hwid == "MACHINE-ID-123"
