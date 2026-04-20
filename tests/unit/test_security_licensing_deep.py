import base64
from unittest.mock import MagicMock, patch

from src.core.license_validator import (
    LicenseStatus,
    _calculate_sha256,
    _get_windows_hardware_id,
    get_detailed_license_status,
    get_hardware_id,
)
from src.core.secrets_manager import SecretsManager


class TestSecretsManagerDeep:
    def test_get_license_key_priority_env(self):
        val = base64.urlsafe_b64encode(b"env_key").decode()
        with patch.dict("os.environ", {"SYNCROJOB_LICENSE_KEY": val}):
            res = SecretsManager.get_license_key()
            assert res == val.encode("utf-8")

    @patch("src.core.secrets_manager.keyring.get_password")
    def test_get_license_key_priority_keyring(self, mock_keyring):
        val = base64.urlsafe_b64encode(b"keyring_key").decode()
        # Env empty, check keyring
        with patch.dict("os.environ", {}, clear=True):
            mock_keyring.return_value = val
            res = SecretsManager.get_license_key()
            assert res == val.encode("utf-8")
            # Verify correct service name and key
            mock_keyring.assert_called_with(SecretsManager.APP_NAME, "license_key")

    def test_derive_key_robustness(self):
        # Test HMAC key derivation (PBKDF2)
        pwd = "test_password"
        salt = b"test_salt"
        key1 = SecretsManager.derive_key(pwd, salt)
        key2 = SecretsManager.derive_key(pwd, salt)
        assert key1 == key2
        assert len(base64.urlsafe_b64decode(key1)) == 32  # 256 bits

    @patch("src.core.secrets_manager.keyring.set_password")
    def test_store_credential(self, mock_set):
        SecretsManager.store_credential("isab", "admin", "secret")
        mock_set.assert_called_with(f"{SecretsManager.APP_NAME}_isab", "admin", "secret")


class TestHardwareFingerprinting:
    @patch("platform.system", return_value="Windows")
    @patch(
        "src.core.license_validator._get_windows_hardware_id",
        return_value="WIN-SERIAL-123",
    )
    def test_get_hardware_id_windows(self, mock_win, mock_sys):
        assert get_hardware_id() == "WIN-SERIAL-123"

    @patch("subprocess.check_output")
    def test_windows_hardware_id_powershell_fallback(self, mock_output):
        # First call fails, second (powershell) succeeds
        mock_output.side_effect = [
            Exception("WMIC fail"),
            b"PS-DISK-ID\n",
        ]
        res = _get_windows_hardware_id()
        assert res == "PS-DISK-ID"


class TestLicenseIntegrity:
    def test_calculate_sha256(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello integrity")
        h = _calculate_sha256(f)
        assert len(h) == 64  # Hex SHA256 len

    @patch("src.core.license_validator._get_license_paths")
    @patch("src.core.license_validator._calculate_sha256")
    def test_detailed_status_invalid_integrity(self, mock_sha, mock_paths, tmp_path):
        config = tmp_path / "config.dat"
        manifest = tmp_path / "manifest.json"
        config.write_text("data")
        manifest.write_text('{"config.dat": "valid_hash"}')

        mock_paths.return_value = {
            "dir": tmp_path,
            "config": config,
            "manifest": manifest,
        }
        mock_sha.return_value = "mismatch_hash"

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.INVALID
        assert "Integrità" in msg

    @patch("src.core.license_validator._get_license_paths")
    @patch("src.core.license_validator.get_license_info")
    @patch("src.core.license_validator.get_hardware_id")
    @patch("src.core.license_validator._check_integrity_with_manifest")
    def test_detailed_status_hw_mismatch(self, mock_integrity, mock_hw, mock_info, mock_paths):
        mock_paths.return_value = {
            "config": MagicMock(exists=lambda: True),
            "manifest": MagicMock(exists=lambda: True),
            "dir": MagicMock(exists=lambda: True),
        }
        mock_integrity.return_value = (LicenseStatus.VALID, "")
        mock_hw.return_value = "MY-HW-123"
        mock_info.return_value = {"Hardware ID": "WRONG-HW-456", "Cliente": "Test"}

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.INVALID
        assert "Hardware ID non valido" in msg
