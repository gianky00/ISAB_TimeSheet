import os
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import pytest
from cryptography.fernet import Fernet

from src.core.license_updater import (
    check_emergency_grace_period,
    check_grace_period,
    get_github_token,
    get_license_dir,
    is_license_folder_empty,
    run_update,
    update_grace_timestamp,
)
from src.core.secrets_manager import SecretsManager


@pytest.fixture
def grace_key():
    return SecretsManager.get_grace_period_key()


@pytest.fixture
def mock_license_dir(tmp_path):
    license_dir = tmp_path / "Licenza"
    license_dir.mkdir()
    return license_dir


def test_get_github_token():
    token = get_github_token()
    assert isinstance(token, str)
    assert len(token) > 0


def test_get_license_dir(mocker):
    mocker.patch("src.core.license_updater.get_data_path", return_value="/fake/path")
    path = get_license_dir()
    # Convert to str for substring assertion
    assert "/fake/path" in str(path).replace("\\", "/")
    assert "Licenza" in str(path)


def test_update_grace_timestamp(mocker, mock_license_dir, grace_key):
    mocker.patch("src.core.license_updater.get_license_dir", return_value=mock_license_dir)
    fixed_now = datetime(2026, 1, 1, tzinfo=UTC)
    mocker.patch("src.core.time_manager.get_trusted_time", return_value=(fixed_now, True))

    update_grace_timestamp()

    token_path = os.path.join(mock_license_dir, "validity.token")
    assert os.path.exists(token_path)

    with open(token_path, "rb") as f:
        encrypted_data = f.read()

    cipher = Fernet(grace_key)
    decrypted_data = cipher.decrypt(encrypted_data).decode("utf-8")
    assert datetime.fromisoformat(decrypted_data) == fixed_now


def test_check_grace_period_valid(mocker, mock_license_dir, grace_key):
    mocker.patch("src.core.license_updater.get_license_dir", return_value=mock_license_dir)

    # Create valid token (1 day ago)
    last_online = datetime.now(UTC) - timedelta(days=1)
    cipher = Fernet(grace_key)
    encrypted_time = cipher.encrypt(last_online.isoformat().encode("utf-8"))

    token_path = os.path.join(mock_license_dir, "validity.token")
    with open(token_path, "wb") as f:
        f.write(encrypted_time)

    mocker.patch(
        "src.core.time_manager.get_trusted_time",
        return_value=(datetime.now(UTC), True),
    )

    assert check_grace_period() is True


def test_check_grace_period_expired(mocker, mock_license_dir, grace_key):
    mocker.patch("src.core.license_updater.get_license_dir", return_value=mock_license_dir)

    # Create expired token (4 days ago)
    last_online = datetime.now(UTC) - timedelta(days=4)
    cipher = Fernet(grace_key)
    encrypted_time = cipher.encrypt(last_online.isoformat().encode("utf-8"))

    token_path = os.path.join(mock_license_dir, "validity.token")
    with open(token_path, "wb") as f:
        f.write(encrypted_time)

    mocker.patch(
        "src.core.time_manager.get_trusted_time",
        return_value=(datetime.now(UTC), True),
    )

    with pytest.raises(Exception, match="SCADUTO"):
        check_grace_period()


def test_check_emergency_grace_period_new(mocker, mock_license_dir):
    mocker.patch("src.core.license_updater.get_license_dir", return_value=mock_license_dir)
    mocker.patch(
        "src.core.time_manager.get_trusted_time",
        return_value=(datetime.now(UTC), True),
    )

    allowed, _msg, days = check_emergency_grace_period()
    assert allowed is True
    assert days == 3
    assert os.path.exists(os.path.join(mock_license_dir, "emergency_grace.token"))


def test_is_license_folder_empty(mocker, mock_license_dir):
    mocker.patch("src.core.license_updater.get_license_dir", return_value=mock_license_dir)

    # Initially empty
    assert is_license_folder_empty() is True

    # Add files
    with open(os.path.join(mock_license_dir, "config.dat"), "w") as f:
        f.write("data")
    with open(os.path.join(mock_license_dir, "manifest.json"), "w") as f:
        f.write("{}")

    assert is_license_folder_empty() is False


def test_run_update_success(mocker, mock_license_dir):
    mocker.patch("src.core.license_updater.get_license_dir", return_value=mock_license_dir)
    mocker.patch("src.core.license_validator.get_hardware_id", return_value="FAKE_HW_ID")
    # Mock status locale come EXPIRED per forzare il download
    mocker.patch(
        "src.core.license_validator.get_detailed_license_status",
        return_value=("EXPIRED", "Expired"),
    )

    def mock_requests_get(url, **kwargs):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        if url.endswith("/manifest.json"):
            mock_resp.content = b'{"config.dat": "new_hash"}'
        elif url.endswith("/config.dat"):
            mock_resp.content = b"fake_encrypted_data"
        else:
            # Chiamata alla cartella base
            mock_resp.status_code = 200
        return mock_resp

    mocker.patch("requests.get", side_effect=mock_requests_get)

    # Mock della validazione in memoria (decifratura e check HWID)
    mock_cipher = MagicMock()
    mock_cipher.decrypt.return_value = b'{"Hardware ID": "FAKE_HW_ID", "Cliente": "Test"}'
    mocker.patch("src.core.license_updater.Fernet", return_value=mock_cipher)
    mocker.patch("src.core.secrets_manager.SecretsManager.get_license_key", return_value=b"key")

    success = run_update()
    assert success is True
    assert os.path.exists(os.path.join(mock_license_dir, "config.dat"))
    assert os.path.exists(os.path.join(mock_license_dir, "manifest.json"))


def test_run_update_fail(mocker, mock_license_dir):
    mocker.patch("src.core.license_updater.get_license_dir", return_value=mock_license_dir)
    mocker.patch("src.core.license_validator.get_hardware_id", return_value="FAKE_HW_ID")

    # Simula cartella licenza mancante (Revocata)
    mock_response = MagicMock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)

    # In caso di 404, run_update solleva eccezione "REVOCATA"
    with pytest.raises(Exception, match="REVOCATA"):
        run_update()
