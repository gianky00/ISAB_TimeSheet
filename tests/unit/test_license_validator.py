import json
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest
from cryptography.fernet import Fernet

from src.core.license_validator import (
    LicenseStatus,
    _calculate_sha256,
    get_detailed_license_status,
    verify_license,
)


class TestLicenseValidator:
    @pytest.fixture(autouse=True)
    def setup_license_env(self, fs):
        """Setup virtual filesystem for license tests."""
        from src.core.paths import get_data_path

        self.license_dir = Path(get_data_path()) / "Licenza"
        fs.create_dir(self.license_dir)
        self.config_path = self.license_dir / "config.dat"
        self.manifest_path = self.license_dir / "manifest.json"

    def test_verify_license_missing(self, fs):
        valid, msg = verify_license()
        assert valid is False
        assert "mancanti" in msg

    @patch("src.core.secrets_manager.SecretsManager.get_license_key")
    @patch("src.core.license_validator.get_hardware_id")
    @patch("src.core.license_validator.get_trusted_time")
    def test_verify_license_valid_flow(self, mock_time, mock_hwid, mock_key, fs):
        # 1. Setup Key
        key = Fernet.generate_key()
        mock_key.return_value = key

        # 2. Setup Payload
        payload = {"Cliente": "Test Client", "Hardware ID": "TEST-HWID", "Scadenza Licenza": "31/12/2099"}
        cipher = Fernet(key)
        encrypted_payload = cipher.encrypt(json.dumps(payload).encode())
        fs.create_file(self.config_path, contents=encrypted_payload)

        # 3. Setup Manifest
        config_hash = hashlib_sha256_mock_safe(encrypted_payload)
        manifest = {"config.dat": config_hash}
        fs.create_file(self.manifest_path, contents=json.dumps(manifest))

        # 4. Mock System
        mock_hwid.return_value = "TEST-HWID"
        mock_time.return_value = (datetime(2024, 1, 1), True)

        # Test
        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.VALID
        assert "Test Client" in msg

        valid, _ = verify_license()
        assert valid is True

    @patch("src.core.secrets_manager.SecretsManager.get_license_key")
    @patch("src.core.license_validator.get_hardware_id")
    def test_verify_license_hwid_mismatch(self, mock_hwid, mock_key, fs):
        key = Fernet.generate_key()
        mock_key.return_value = key
        payload = {"Hardware ID": "EXPECTED-HWID", "Cliente": "X"}
        encrypted = Fernet(key).encrypt(json.dumps(payload).encode())
        fs.create_file(self.config_path, contents=encrypted)

        manifest = {"config.dat": _calculate_sha256_bytes(encrypted)}
        fs.create_file(self.manifest_path, contents=json.dumps(manifest))

        mock_hwid.return_value = "WRONG-HWID"

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.INVALID
        assert "Hardware ID non valido" in msg

    @patch("src.core.secrets_manager.SecretsManager.get_license_key")
    @patch("src.core.license_validator.get_hardware_id")
    @patch("src.core.license_validator.get_trusted_time")
    def test_verify_license_expired(self, mock_time, mock_hwid, mock_key, fs):
        key = Fernet.generate_key()
        mock_key.return_value = key
        payload = {"Hardware ID": "HWID", "Scadenza Licenza": "01/01/2020"}
        encrypted = Fernet(key).encrypt(json.dumps(payload).encode())
        fs.create_file(self.config_path, contents=encrypted)
        manifest = {"config.dat": _calculate_sha256_bytes(encrypted)}
        fs.create_file(self.manifest_path, contents=json.dumps(manifest))

        mock_hwid.return_value = "HWID"
        mock_time.return_value = (datetime(2024, 1, 1), True)

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.EXPIRED
        assert "SCADUTA" in msg

    def test_calculate_sha256(self, fs):
        path = Path("test.txt")
        fs.create_file(path, contents=b"hello world")
        expected = hashlib_sha256_mock_safe(b"hello world")
        assert _calculate_sha256(path) == expected


def _calculate_sha256_bytes(data: bytes) -> str:
    import hashlib

    return hashlib.sha256(data).hexdigest()


def hashlib_sha256_mock_safe(data: bytes) -> str:
    import hashlib

    return hashlib.sha256(data).hexdigest()
