import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from cryptography.fernet import Fernet

from src.core.license_validator import (
    LicenseStatus,
    _calculate_sha256,
    get_detailed_license_status,
    get_license_client,
    get_license_expiry,
    get_license_info,
    verify_license,
)


class TestLicenseValidator:
    @pytest.fixture
    def mock_paths(self):
        with patch("src.core.license_validator._get_license_paths") as mock:
            mock.return_value = {
                "dir": Path("/fake/Licenza"),
                "config": Path("/fake/Licenza/config.dat"),
                "manifest": Path("/fake/Licenza/manifest.json"),
            }
            yield mock.return_value

    def test_calculate_sha256(self, fs):
        file_path = "/test.txt"
        fs.create_file(file_path, contents=b"hello world")
        expected = hashlib.sha256(b"hello world").hexdigest()
        assert _calculate_sha256(file_path) == expected

    @patch("src.core.license_validator.SecretsManager.get_license_key")
    def test_get_license_info_success(self, mock_key, mock_paths, fs):
        # Setup fake key
        key = Fernet.generate_key()
        mock_key.return_value = key

        # Setup fake encrypted data
        payload = {"Cliente": "Test Client", "Hardware ID": "HW123", "Scadenza Licenza": "01/01/2099"}
        encrypted = Fernet(key).encrypt(json.dumps(payload).encode())

        fs.create_dir(str(mock_paths["dir"]))
        fs.create_file(str(mock_paths["config"]), contents=encrypted)

        info = get_license_info()
        assert info == payload

    @patch("src.core.license_validator.SecretsManager.get_license_key")
    def test_get_license_info_missing_file(self, mock_key, mock_paths, fs):
        mock_key.return_value = b"somekey"
        assert get_license_info() is None

    @patch("src.core.license_validator.get_detailed_license_status")
    def test_verify_license_bool(self, mock_status):
        mock_status.return_value = (LicenseStatus.VALID, "OK")
        success, msg = verify_license()
        assert success is True
        assert msg == "OK"

    @patch("src.core.license_validator._check_integrity_with_manifest")
    @patch("src.core.license_validator._validate_license_data")
    @patch("src.core.license_validator._check_and_migrate_local_license")
    def test_get_detailed_license_status_missing(self, mock_migrate, mock_val, mock_integ, mock_paths, fs):
        # Se i file mancano e la migrazione fallisce -> MISSING
        mock_migrate.return_value = False
        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.MISSING
        assert "mancanti" in msg

    @patch("src.core.license_validator._calculate_sha256")
    def test_check_integrity_failure(self, mock_sha, mock_paths, fs):
        fs.create_file(str(mock_paths["manifest"]), contents=json.dumps({"config.dat": "expected_hash"}))
        fs.create_file(str(mock_paths["config"]), contents=b"content")
        mock_sha.return_value = "wrong_hash"

        from src.core.license_validator import _check_integrity_with_manifest

        with patch("src.core.license_validator.AuditManager.instance") as mock_audit:
            status, msg = _check_integrity_with_manifest(mock_paths)
            assert status == LicenseStatus.INVALID
            assert "compromessa" in msg
            assert mock_audit.return_value.log_action.called

    @patch("src.core.license_validator.get_license_info")
    @patch("src.core.license_validator.get_hardware_id")
    @patch("src.core.license_validator.get_trusted_time")
    def test_validate_license_data_expired(self, mock_time, mock_hwid, mock_info, mock_paths):
        from datetime import datetime

        # Mock info: scaduta
        mock_info.return_value = {"Hardware ID": "HW123", "Scadenza Licenza": "01/01/2020"}
        mock_hwid.return_value = "HW123"
        # Mock current time: 2023
        mock_time.return_value = (datetime(2023, 1, 1), True)

        from src.core.license_validator import _validate_license_data

        status, msg = _validate_license_data(mock_paths)
        assert status == LicenseStatus.EXPIRED
        assert "SCADUTA" in msg

    @patch("src.core.license_validator.get_license_info")
    @patch("src.core.license_validator.get_hardware_id")
    def test_validate_license_data_wrong_hwid(self, mock_hwid, mock_info, mock_paths):
        mock_info.return_value = {"Hardware ID": "HW_ATTESO", "Scadenza Licenza": "01/01/2099"}
        mock_hwid.return_value = "HW_RILEVATO"

        from src.core.license_validator import _validate_license_data

        with patch("src.core.license_validator.AuditManager.instance") as mock_audit:
            status, msg = _validate_license_data(mock_paths)
            assert status == LicenseStatus.INVALID
            assert "Hardware ID non valido" in msg
            assert mock_audit.return_value.log_action.called

    @patch("src.core.license_validator.get_license_info")
    def test_get_license_expiry_client(self, mock_info):
        mock_info.return_value = {"Cliente": "Mario Rossi", "Scadenza Licenza": "31/12/2025"}
        assert get_license_expiry() == "31/12/2025"
        assert get_license_client() == "Mario Rossi"

        mock_info.return_value = None
        assert get_license_expiry() == "N/D"
        assert get_license_client() == "N/D"
