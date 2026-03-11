import hashlib
import json
from datetime import UTC, datetime

import pytest
from cryptography.fernet import Fernet

from src.core.license_validator import (
    LicenseStatus,
    _validate_license_data,
    get_detailed_license_status,
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
    mocker.patch.object(SecretsManager, "get_license_key", return_value=key_b64)
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
