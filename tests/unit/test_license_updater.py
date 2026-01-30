import os
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest
from cryptography.fernet import Fernet

from src.core.license_updater import (
    GRACE_PERIOD_KEY,
    check_emergency_grace_period,
    check_grace_period,
    get_github_token,
    get_license_dir,
    is_license_folder_empty,
    run_update,
    update_grace_timestamp,
)


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
    mocker.patch("src.core.config_manager.get_data_path", return_value="/fake/path")
    path = get_license_dir()
    # Convert to str for substring assertion
    assert "/fake/path" in str(path).replace("\\", "/")
    assert "Licenza" in str(path)


def test_update_grace_timestamp(mocker, mock_license_dir):
    mocker.patch(
        "src.core.license_updater.get_license_dir", return_value=mock_license_dir
    )
    fixed_now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    mocker.patch(
        "src.core.time_manager.get_trusted_time", return_value=(fixed_now, True)
    )

    update_grace_timestamp()

    token_path = os.path.join(mock_license_dir, "validity.token")
    assert os.path.exists(token_path)

    with open(token_path, "rb") as f:
        encrypted_data = f.read()

    cipher = Fernet(GRACE_PERIOD_KEY)
    decrypted_data = cipher.decrypt(encrypted_data).decode("utf-8")
    assert datetime.fromisoformat(decrypted_data) == fixed_now


def test_check_grace_period_valid(mocker, mock_license_dir):
    mocker.patch(
        "src.core.license_updater.get_license_dir", return_value=mock_license_dir
    )

    # Create valid token (1 day ago)
    last_online = datetime.now(timezone.utc) - timedelta(days=1)
    cipher = Fernet(GRACE_PERIOD_KEY)
    encrypted_time = cipher.encrypt(last_online.isoformat().encode("utf-8"))

    token_path = os.path.join(mock_license_dir, "validity.token")
    with open(token_path, "wb") as f:
        f.write(encrypted_time)

    mocker.patch(
        "src.core.time_manager.get_trusted_time",
        return_value=(datetime.now(timezone.utc), True),
    )

    assert check_grace_period() is True


def test_check_grace_period_expired(mocker, mock_license_dir):
    mocker.patch(
        "src.core.license_updater.get_license_dir", return_value=mock_license_dir
    )

    # Create expired token (4 days ago)
    last_online = datetime.now(timezone.utc) - timedelta(days=4)
    cipher = Fernet(GRACE_PERIOD_KEY)
    encrypted_time = cipher.encrypt(last_online.isoformat().encode("utf-8"))

    token_path = os.path.join(mock_license_dir, "validity.token")
    with open(token_path, "wb") as f:
        f.write(encrypted_time)

    mocker.patch(
        "src.core.time_manager.get_trusted_time",
        return_value=(datetime.now(timezone.utc), True),
    )

    with pytest.raises(Exception, match="SCADUTO"):
        check_grace_period()


def test_check_emergency_grace_period_new(mocker, mock_license_dir):
    mocker.patch(
        "src.core.license_updater.get_license_dir", return_value=mock_license_dir
    )
    mocker.patch(
        "src.core.time_manager.get_trusted_time",
        return_value=(datetime.now(timezone.utc), True),
    )

    allowed, msg, days = check_emergency_grace_period()
    assert allowed is True
    assert days == 3
    assert os.path.exists(os.path.join(mock_license_dir, "emergency_grace.token"))


def test_is_license_folder_empty(mocker, mock_license_dir):
    mocker.patch(
        "src.core.license_updater.get_license_dir", return_value=mock_license_dir
    )

    # Initially empty
    assert is_license_folder_empty() is True

    # Add files
    with open(os.path.join(mock_license_dir, "config.dat"), "w") as f:
        f.write("data")
    with open(os.path.join(mock_license_dir, "manifest.json"), "w") as f:
        f.write("{}")

    assert is_license_folder_empty() is False


def test_run_update_success(mocker, mock_license_dir):
    mocker.patch(
        "src.core.license_updater.get_license_dir", return_value=mock_license_dir
    )
    mocker.patch(
        "src.core.license_validator.get_hardware_id", return_value="FAKE_HW_ID"
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"fake content"
    mocker.patch("requests.get", return_value=mock_response)

    success = run_update()
    assert success is True
    assert os.path.exists(os.path.join(mock_license_dir, "config.dat"))
    assert os.path.exists(os.path.join(mock_license_dir, "manifest.json"))


def test_run_update_fail(mocker, mock_license_dir):
    mocker.patch(
        "src.core.license_updater.get_license_dir", return_value=mock_license_dir
    )
    mocker.patch(
        "src.core.license_validator.get_hardware_id", return_value="FAKE_HW_ID"
    )

    mock_response = MagicMock()
    mock_response.status_code = 404
    mocker.patch("requests.get", return_value=mock_response)

    success = run_update()
    assert success is False
