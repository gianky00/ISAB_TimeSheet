from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from src.core.license_updater import (
    _download_license_files,
    _save_license_files,
    check_emergency_grace_period,
    check_grace_period,
    get_github_token,
    get_license_dir,
    run_update,
    update_grace_timestamp,
)


class TestLicenseUpdater:
    @pytest.fixture
    def mock_paths(self, tmp_path, mocker):
        license_dir = tmp_path / "Licenza"
        mocker.patch(
            "src.core.license_updater.get_license_dir", return_value=license_dir
        )
        return license_dir

    def test_get_github_token(self):
        token = get_github_token()
        assert len(token) > 0
        assert token.startswith("ghp_")

    def test_get_license_dir(self, tmp_path):
        with patch("src.core.config_manager.get_data_path", return_value=str(tmp_path)):
            d = get_license_dir()
            assert str(tmp_path) in str(d)
            assert "Licenza" in str(d)

    def test_grace_timestamp_lifecycle(self, mock_paths):
        # 1. Update timestamp
        update_grace_timestamp()
        token_path = mock_paths / "validity.token"
        assert token_path.exists()

        # 2. Check valid grace
        assert check_grace_period() is True

        # 3. Check offline grace limit (mock time travel)
        with patch("src.core.time_manager.get_trusted_time") as mock_time:
            # 4 days later (naive)
            future = datetime.now() + timedelta(days=4)
            mock_time.return_value = (future, False)
            with pytest.raises(Exception, match="SCADUTO"):
                check_grace_period()

    def test_check_grace_period_missing_token(self, mock_paths):
        with pytest.raises(Exception, match="Nessuna validazione"):
            check_grace_period()

    def test_check_grace_period_tampered_clock(self, mock_paths):
        update_grace_timestamp()

        with patch("src.core.time_manager.get_trusted_time") as mock_time:
            # 1 hour before
            mock_time.return_value = (datetime.now() - timedelta(hours=1), False)
            with pytest.raises(Exception, match="incoerenza"):
                check_grace_period()

    def test_emergency_grace_lifecycle(self, mock_paths):
        # 1. Activate
        success, msg, days = check_emergency_grace_period()
        assert success is True
        assert days == 3
        token_path = mock_paths / "emergency_grace.token"
        assert token_path.exists()

        # 2. Check active
        success, msg, days = check_emergency_grace_period()
        assert success is True
        assert "attivo" in msg

        # 3. Check expired
        with patch("src.core.time_manager.get_trusted_time") as mock_time:
            mock_time.return_value = (datetime.now() + timedelta(days=4), False)
            success, msg, days = check_emergency_grace_period()
            assert success is False
            assert "SCADUTO" in msg

    def test_emergency_grace_tampered(self, mock_paths):
        check_emergency_grace_period()
        with patch("src.core.time_manager.get_trusted_time") as mock_time:
            mock_time.return_value = (datetime.now() - timedelta(hours=2), False)
            success, msg, days = check_emergency_grace_period()
            assert success is False
            assert "manipolazione" in msg

    def test_download_license_files_success(self, mocker):
        mock_get = mocker.patch("requests.get")
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"content"

        files, error = _download_license_files("url")
        assert error is None
        assert "config.dat" in files
        assert files["config.dat"] == b"content"

    def test_download_license_files_fail(self, mocker):
        mock_get = mocker.patch("requests.get")
        import requests

        mock_get.side_effect = requests.RequestException("Network Error")

        files, error = _download_license_files("url")
        assert files == {}
        assert "Offline" in error

    def test_save_license_files(self, mock_paths):
        files = {"test.file": b"data"}
        mock_paths.mkdir(parents=True, exist_ok=True)

        assert _save_license_files(str(mock_paths), files) is True
        assert (mock_paths / "test.file").read_bytes() == b"data"

    def test_run_update_success(self, mocker, mock_paths):
        mocker.patch("src.core.license_validator.get_hardware_id", return_value="HWID")
        mocker.patch(
            "src.core.license_updater._download_license_files",
            return_value=({"f": b"c"}, None),
        )
        mocker.patch("src.core.license_updater._save_license_files", return_value=True)

        assert run_update() is True

    def test_run_update_fail_download(self, mocker, mock_paths):
        mocker.patch("src.core.license_validator.get_hardware_id", return_value="HWID")
        mocker.patch(
            "src.core.license_updater._download_license_files",
            return_value=({}, "Error"),
        )

        assert run_update() is False
