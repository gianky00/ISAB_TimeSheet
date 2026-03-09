import base64
import hashlib
import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from cryptography.fernet import Fernet

from src.core.audit_manager import AuditManager
from src.core.license_validator import (
    LicenseStatus,
    _calculate_sha256,
    _check_integrity_with_manifest,
    _get_license_paths,
    _validate_license_data,
    get_detailed_license_status,
    get_hardware_id,
    get_license_client,
    get_license_expiry,
    get_license_info,
    verify_license,
)
from src.core.secrets_manager import SecretsManager

@pytest.fixture(autouse=True)
def mock_no_migration(mocker):
    return mocker.patch("src.core.license_validator._check_and_migrate_local_license", return_value=False)

@pytest.fixture
def mock_license_dir(tmp_path):
    d = tmp_path / "Licenza"
    d.mkdir()
    return d

@pytest.fixture
def mock_secrets_manager(mocker):
    key_b64 = Fernet.generate_key()
    key_raw = base64.urlsafe_b64decode(key_b64)
    mocker.patch.object(SecretsManager, "get_license_key", return_value=key_raw)
    return key_b64

def test_validate_license_data_expired_untrusted(mocker):
    """Verifica che una licenza scaduta venga rilevata anche con orario non fidato."""
    payload = {"Hardware ID": "SAME", "Scadenza Licenza": "01/01/2020"}
    mocker.patch("src.core.license_validator.get_license_info", return_value=payload)
    mocker.patch("src.core.license_validator.get_hardware_id", return_value="SAME")
    
    # Mock orario scaduto
    mocker.patch(
        "src.core.license_validator.get_trusted_time",
        return_value=(datetime(2024, 1, 1, tzinfo=UTC), False),
    )

    status, msg = _validate_license_data({})
    assert status == LicenseStatus.EXPIRED
    assert "SCADUTA" in msg

def test_get_detailed_license_status_valid(mocker, mock_license_dir, mock_secrets_manager):
    # Setup manuale per controllo totale
    paths = {
        "dir": mock_license_dir,
        "config": mock_license_dir / "config.dat",
        "manifest": mock_license_dir / "manifest.json",
    }
    mocker.patch("src.core.license_validator._get_license_paths", return_value=paths)
    mocker.patch("src.core.license_validator.get_hardware_id", return_value="FAKE_HW_ID")
    
    cipher = Fernet(mock_secrets_manager)
    license_data = {
        "Hardware ID": "FAKE_HW_ID",
        "Scadenza Licenza": "31/12/2099",
        "Cliente": "Test"
    }
    enc = cipher.encrypt(json.dumps(license_data).encode())
    paths["config"].write_bytes(enc)
    paths["manifest"].write_text(json.dumps({"config.dat": hashlib.sha256(enc).hexdigest()}))

    mocker.patch("src.core.time_manager.get_trusted_time", return_value=(datetime.now(UTC), True))

    status, msg = get_detailed_license_status()
    assert status == LicenseStatus.VALID
    assert "Test" in msg
