"""
Tests for LicenseValidator logic.
"""

import hashlib
import json
from unittest.mock import patch

import pytest

from src.core import license_validator


@pytest.fixture
def mock_paths(tmp_path):  # noqa: ANN001
    """Mocks file system paths for license files."""
    license_dir = tmp_path / "Licenza"
    license_dir.mkdir()
    config_path = license_dir / "config.dat"
    manifest_path = license_dir / "manifest.json"

    with patch("src.core.license_validator._get_license_paths") as mock_get:
        mock_get.return_value = {
            "dir": license_dir,
            "config": config_path,
            "manifest": manifest_path,
        }
        yield config_path, manifest_path


@pytest.fixture
def mock_secrets():
    """Mocks SecretsManager to return a fixed key."""
    with patch("src.core.license_validator.SecretsManager") as mock_sm:
        # Generate a real key for Fernet to use
        from cryptography.fernet import Fernet  # noqa: PLC0415

        key = Fernet.generate_key()
        # SecretsManager.get_license_key() returns base64 encoded bytes
        mock_sm.get_license_key.return_value = key
        yield key


def create_mock_license(config_path, manifest_path, key, payload):  # noqa: ANN001
    """Helper to create valid license files."""
    from cryptography.fernet import Fernet  # noqa: PLC0415

    # Encrypt payload
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(json.dumps(payload).encode())

    with open(config_path, "wb") as f:
        f.write(encrypted_data)

    # Create manifest
    config_hash = hashlib.sha256(encrypted_data).hexdigest()
    with open(manifest_path, "w") as f:
        json.dump({"config.dat": config_hash}, f)


@patch("src.core.license_validator.get_hardware_id", return_value="HW123")
@patch("src.core.license_validator.get_trusted_time")
def test_valid_license(mock_time, mock_hw, mock_paths, mock_secrets):  # noqa: ANN001
    config_path, manifest_path = mock_paths
    key = mock_secrets

    # Set time to be before expiry
    from datetime import datetime  # noqa: PLC0415

    mock_time.return_value = (datetime(2025, 1, 1), True)

    # Create valid license
    payload = {
        "Hardware ID": "HW123",
        "Scadenza Licenza": "01/01/2026",
        "Cliente": "Test Client",
    }
    create_mock_license(config_path, manifest_path, key, payload)

    status, msg = license_validator.get_detailed_license_status()
    assert status == license_validator.LicenseStatus.VALID
    assert "Test Client" in msg


@patch("src.core.license_validator.get_hardware_id", return_value="HW_DIFFERENT")
@patch("src.core.license_validator.get_trusted_time")
def test_invalid_hardware_id(mock_time, mock_hw, mock_paths, mock_secrets):  # noqa: ANN001
    config_path, manifest_path = mock_paths
    key = mock_secrets

    # Create license for different HW
    payload = {"Hardware ID": "HW123", "Scadenza Licenza": "01/01/2026"}
    create_mock_license(config_path, manifest_path, key, payload)

    status, msg = license_validator.get_detailed_license_status()
    assert status == license_validator.LicenseStatus.INVALID
    assert "Hardware ID non valido" in msg


@patch("src.core.license_validator.get_hardware_id", return_value="HW123")
@patch("src.core.license_validator.get_trusted_time")
def test_expired_license(mock_time, mock_hw, mock_paths, mock_secrets):  # noqa: ANN001
    config_path, manifest_path = mock_paths
    key = mock_secrets

    # Set time to be AFTER expiry
    from datetime import datetime  # noqa: PLC0415

    mock_time.return_value = (datetime(2027, 1, 1), True)

    payload = {"Hardware ID": "HW123", "Scadenza Licenza": "01/01/2026"}
    create_mock_license(config_path, manifest_path, key, payload)

    status, msg = license_validator.get_detailed_license_status()
    assert status == license_validator.LicenseStatus.EXPIRED
    assert "SCADUTA" in msg


def test_tampered_license(mock_paths, mock_secrets):  # noqa: ANN001
    config_path, manifest_path = mock_paths
    key = mock_secrets

    payload = {"Hardware ID": "HW123"}
    create_mock_license(config_path, manifest_path, key, payload)

    # Tamper with the config file
    with open(config_path, "ab") as f:
        f.write(b"tampered")

    status, msg = license_validator.get_detailed_license_status()
    assert status == license_validator.LicenseStatus.INVALID
    assert "Integrità licenza compromessa" in msg
