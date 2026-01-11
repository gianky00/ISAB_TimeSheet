import base64
import hashlib
import json
import os
from datetime import date, datetime, timedelta, timezone
from unittest.mock import mock_open

import pytest
from cryptography.fernet import Fernet

from src.core.audit_manager import AuditManager
from src.core.license_validator import (
    LicenseStatus,
    _calculate_sha256,
    _get_license_paths,
    get_detailed_license_status,
    get_hardware_id,
    get_license_client,
    get_license_expiry,
    get_license_info,
    verify_license,
)
from src.core.secrets_manager import SecretsManager


@pytest.fixture
def mock_license_dir(tmp_path):
    license_dir = tmp_path / "Licenza"
    license_dir.mkdir()
    return str(license_dir)


@pytest.fixture
def mock_secrets_manager(mocker):
    key_b64 = Fernet.generate_key()
    key_raw = base64.urlsafe_b64decode(key_b64)
    mocker.patch.object(SecretsManager, "get_license_key", return_value=key_raw)
    return key_b64


@pytest.fixture
def setup_valid_license_files(mock_license_dir, mocker):
    # We need a consistent key for both SecretsManager and creating the file
    key_b64 = Fernet.generate_key()
    key_raw = base64.urlsafe_b64decode(key_b64)
    mocker.patch.object(SecretsManager, "get_license_key", return_value=key_raw)

    cipher = Fernet(key_b64)

    # Dati di licenza validi
    license_data = {
        "Hardware ID": "FAKE_HW_ID",
        "Scadenza Licenza": (date.today() + timedelta(days=365)).strftime("%d/%m/%Y"),  # Valida per 1 anno
        "Cliente": "Test Cliente",
    }
    encrypted_config = cipher.encrypt(json.dumps(license_data).encode("utf-8"))

    # Hash SHA256 per il manifest
    config_hash = hashlib.sha256(encrypted_config).hexdigest()

    manifest_data = {"config.dat": config_hash}

    # Scrivi i file
    with open(os.path.join(mock_license_dir, "config.dat"), "wb") as f:
        f.write(encrypted_config)
    with open(os.path.join(mock_license_dir, "manifest.json"), "w") as f:
        json.dump(manifest_data, f)

    return license_data


def test_calculate_sha256(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello world")
    expected_hash = hashlib.sha256(b"hello world").hexdigest()
    assert _calculate_sha256(str(test_file)) == expected_hash


def test_get_hardware_id_windows_wmic(mocker):
    mocker.patch("platform.system", return_value="Windows")
    mocker.patch(
        "subprocess.check_output",
        side_effect=[
            b"SerialNumber\r\nFAKE_WMIC_SERIAL\r\n",
            Exception("PowerShell failed"),
            Exception("UUID failed"),
        ],
    )
    mocker.patch("src.core.license_validator.uuid.getnode", return_value=12345)
    assert get_hardware_id() == "FAKE_WMIC_SERIAL"


def test_get_hardware_id_windows_powershell_disk(mocker):
    mocker.patch("platform.system", return_value="Windows")
    mocker.patch(
        "subprocess.check_output",
        side_effect=[
            Exception("WMIC failed"),
            b"FAKE_POWERSHELL_DISK_SERIAL\r\n",
            Exception("UUID failed"),
        ],
    )
    mocker.patch("src.core.license_validator.uuid.getnode", return_value=12345)
    assert get_hardware_id() == "FAKE_POWERSHELL_DISK_SERIAL"


def test_get_hardware_id_linux_lsblk(mocker):
    mocker.patch("platform.system", return_value="Linux")
    mocker.patch(
        "subprocess.check_output",
        side_effect=[b"FAKE_LSBLK_SERIAL\n", Exception("machine-id failed")],
    )
    mocker.patch("src.core.license_validator.uuid.getnode", return_value=12345)
    assert get_hardware_id() == "FAKE_LSBLK_SERIAL"


def test_get_hardware_id_linux_machine_id(mocker, tmp_path):
    mocker.patch("platform.system", return_value="Linux")
    mocker.patch("subprocess.check_output", side_effect=Exception("lsblk failed"))

    # Simula il file /etc/machine-id
    machine_id_path = tmp_path / "etc" / "machine-id"
    machine_id_path.parent.mkdir()
    machine_id_path.write_text("FAKE_MACHINE_ID")
    mocker.patch("os.path.exists", side_effect=lambda p: p == str(machine_id_path) or p == "/etc/machine-id")
    mocker.patch("builtins.open", mock_open(read_data="FAKE_MACHINE_ID"))
    mocker.patch("src.core.license_validator.uuid.getnode", return_value=12345)

    assert get_hardware_id() == "FAKE_MACHINE_ID"


def test_get_hardware_id_fallback_uuid(mocker):
    mocker.patch("platform.system", return_value="Unknown")
    mocker.patch("subprocess.check_output", side_effect=Exception("All subprocess calls failed"))
    mocker.patch("src.core.license_validator.uuid.getnode", return_value=12345)
    assert get_hardware_id() == "12345"


def test_get_license_paths(mocker):
    mocker.patch("src.core.config_manager.get_data_path", return_value="/fake/appdata")
    paths = _get_license_paths()
    assert paths["dir"] == os.path.join("/fake/appdata", "Licenza")
    assert paths["config"] == os.path.join(paths["dir"], "config.dat")
    assert paths["manifest"] == os.path.join(paths["dir"], "manifest.json")


def test_get_license_info_success(mocker, mock_license_dir, mock_secrets_manager):
    mocker.patch(
        "src.core.license_validator._get_license_paths",
        return_value={
            "dir": mock_license_dir,
            "config": os.path.join(mock_license_dir, "config.dat"),
            "manifest": os.path.join(mock_license_dir, "manifest.json"),
        },
    )

    # mock_secrets_manager returns the b64 key
    cipher = Fernet(mock_secrets_manager)
    test_payload = {"Cliente": "Test", "Scadenza Licenza": "01/01/2027"}
    encrypted_data = cipher.encrypt(json.dumps(test_payload).encode("utf-8"))

    with open(os.path.join(mock_license_dir, "config.dat"), "wb") as f:
        f.write(encrypted_data)

    info = get_license_info()
    assert info == test_payload


def test_get_license_info_missing_file(mocker, mock_license_dir):
    mocker.patch(
        "src.core.license_validator._get_license_paths",
        return_value={
            "dir": mock_license_dir,
            "config": os.path.join(mock_license_dir, "non_existent.dat"),
            "manifest": os.path.join(mock_license_dir, "manifest.json"),
        },
    )
    assert get_license_info() is None


def test_get_detailed_license_status_missing_dir(mocker, tmp_path):
    mock_paths = {
        "dir": os.path.join(str(tmp_path), "NonEsistente"),
        "config": os.path.join(str(tmp_path), "NonEsistente", "config.dat"),
        "manifest": os.path.join(str(tmp_path), "NonEsistente", "manifest.json"),
    }
    mocker.patch("src.core.license_validator._get_license_paths", return_value=mock_paths)
    mocker.patch(
        "os.path.exists",
        side_effect=lambda p: p != mock_paths["dir"]
        and p != mock_paths["config"]
        and p != mock_paths["manifest"],
    )
    mocker.patch("os.makedirs")

    status, msg = get_detailed_license_status()
    assert status == LicenseStatus.MISSING
    assert "File di licenza mancanti" in msg


def test_get_detailed_license_status_missing_files(mocker, mock_license_dir):
    mocker.patch(
        "src.core.license_validator._get_license_paths",
        return_value={
            "dir": mock_license_dir,
            "config": os.path.join(mock_license_dir, "non_existent.dat"),
            "manifest": os.path.join(mock_license_dir, "non_existent.json"),
        },
    )
    mocker.patch(
        "os.path.exists",
        side_effect=lambda p: p != os.path.join(mock_license_dir, "non_existent.dat")
        and p != os.path.join(mock_license_dir, "non_existent.json"),
    )
    status, msg = get_detailed_license_status()
    assert status == LicenseStatus.MISSING
    assert "File di licenza mancanti" in msg


def test_get_detailed_license_status_invalid_sha(mocker, mock_license_dir, mock_secrets_manager):
    paths = {
        "dir": mock_license_dir,
        "config": os.path.join(mock_license_dir, "config.dat"),
        "manifest": os.path.join(mock_license_dir, "manifest.json"),
    }
    mocker.patch("src.core.license_validator._get_license_paths", return_value=paths)
    mocker.patch("os.path.exists", return_value=True)

    m4 = mock_open(read_data=b"fake_encrypted_config")
    mocker.patch("builtins.open", m4)

    manifest_data = {"config.dat": "invalid_sha"}
    mocker.patch("json.load", return_value=manifest_data)
    mocker.patch("src.core.license_validator._calculate_sha256", return_value="different_sha")
    mocker.patch.object(AuditManager, "log_action")

    status, msg = get_detailed_license_status()
    assert status == LicenseStatus.INVALID
    assert "Integrità licenza compromessa" in msg


def test_get_detailed_license_status_hw_id_mismatch(
    mocker, mock_license_dir, mock_secrets_manager, setup_valid_license_files
):
    mocker.patch(
        "src.core.license_validator._get_license_paths",
        return_value={
            "dir": mock_license_dir,
            "config": os.path.join(mock_license_dir, "config.dat"),
            "manifest": os.path.join(mock_license_dir, "manifest.json"),
        },
    )
    mocker.patch("src.core.license_validator.get_hardware_id", return_value="ANOTHER_HW_ID")
    mocker.patch("src.core.time_manager.get_trusted_time", return_value=(datetime.now(timezone.utc), True))
    mock_audit_log = mocker.patch.object(AuditManager, "log_action")

    status, msg = get_detailed_license_status()
    assert status == LicenseStatus.INVALID
    assert "Hardware ID non valido" in msg
    mock_audit_log.assert_called_once()


def test_get_detailed_license_status_expired(mocker, mock_license_dir, mock_secrets_manager):
    paths = {
        "dir": mock_license_dir,
        "config": os.path.join(mock_license_dir, "config.dat"),
        "manifest": os.path.join(mock_license_dir, "manifest.json"),
    }
    mocker.patch("src.core.license_validator._get_license_paths", return_value=paths)

    # mock_secrets_manager returns b64 key
    cipher = Fernet(mock_secrets_manager)
    license_data = {
        "Hardware ID": "FAKE_HW_ID",
        "Scadenza Licenza": (date.today() - timedelta(days=1)).strftime("%d/%m/%Y"),
        "Cliente": "Test Cliente",
    }
    encrypted_config = cipher.encrypt(json.dumps(license_data).encode("utf-8"))
    config_hash = hashlib.sha256(encrypted_config).hexdigest()
    manifest_data = {"config.dat": config_hash}

    with open(os.path.join(mock_license_dir, "config.dat"), "wb") as f:
        f.write(encrypted_config)
    with open(os.path.join(mock_license_dir, "manifest.json"), "w") as f:
        json.dump(manifest_data, f)

    mocker.patch("src.core.license_validator.get_hardware_id", return_value="FAKE_HW_ID")
    mocker.patch("src.core.time_manager.get_trusted_time", return_value=(datetime.now(timezone.utc), True))

    status, msg = get_detailed_license_status()
    assert status == LicenseStatus.EXPIRED
    assert "Licenza SCADUTA" in msg


def test_get_detailed_license_status_valid(
    mocker, mock_license_dir, mock_secrets_manager, setup_valid_license_files
):
    mocker.patch(
        "src.core.license_validator._get_license_paths",
        return_value={
            "dir": mock_license_dir,
            "config": os.path.join(mock_license_dir, "config.dat"),
            "manifest": os.path.join(mock_license_dir, "manifest.json"),
        },
    )
    mocker.patch("src.core.license_validator.get_hardware_id", return_value="FAKE_HW_ID")
    mocker.patch(
        "src.core.time_manager.get_trusted_time",
        return_value=(datetime.now(timezone.utc) - timedelta(days=1), True),
    )

    status, msg = get_detailed_license_status()
    assert status == LicenseStatus.VALID
    assert "Licenza valida per" in msg


def test_verify_license(mocker):
    mocker.patch(
        "src.core.license_validator.get_detailed_license_status", return_value=(LicenseStatus.VALID, "OK")
    )
    is_valid, msg = verify_license()
    assert is_valid is True
    assert msg == "OK"


def test_get_license_expiry(mocker, mock_license_dir, mock_secrets_manager, setup_valid_license_files):
    mocker.patch(
        "src.core.license_validator._get_license_paths",
        return_value={
            "dir": mock_license_dir,
            "config": os.path.join(mock_license_dir, "config.dat"),
            "manifest": os.path.join(mock_license_dir, "manifest.json"),
        },
    )
    expiry = get_license_expiry()
    expected_year = (date.today() + timedelta(days=365)).year
    assert str(expected_year) in expiry


def test_get_license_client(mocker, mock_license_dir, mock_secrets_manager, setup_valid_license_files):
    mocker.patch(
        "src.core.license_validator._get_license_paths",
        return_value={
            "dir": mock_license_dir,
            "config": os.path.join(mock_license_dir, "config.dat"),
            "manifest": os.path.join(mock_license_dir, "manifest.json"),
        },
    )
    client = get_license_client()
    assert client == "Test Cliente"
