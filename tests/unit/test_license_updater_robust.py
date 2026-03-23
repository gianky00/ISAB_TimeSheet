from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from cryptography.fernet import Fernet

from src.core import license_updater
from src.core.secrets_manager import SecretsManager


class TestLicenseUpdaterRobust:
    @pytest.fixture
    def grace_key(self):
        return SecretsManager.get_grace_period_key()

    @pytest.fixture
    def mock_data_dir(self, tmp_path):  # noqa: ANN001
        data_dir = tmp_path / "AppData"
        license_dir = data_dir / "Licenza"
        license_dir.mkdir(parents=True)
        with patch("src.core.config_manager.get_data_path", return_value=str(data_dir)):
            yield license_dir

    @pytest.fixture
    def mock_time(self):
        now = datetime.now(UTC)
        with patch("src.core.time_manager.get_trusted_time") as mock:
            mock.return_value = (now, True)
            yield mock

    @pytest.fixture
    def mock_requests(self):
        with patch("requests.get") as mock:
            yield mock

    def test_run_update_success(self, mock_requests, mock_data_dir, mock_time):  # noqa: ANN001
        def side_effect(url, **kwargs):  # noqa: ANN001, ANN003, ANN202
            resp = MagicMock()
            resp.status_code = 200
            if "config.dat" in url:
                resp.content = b"data"
            elif "manifest.json" in url:
                resp.content = b'{"valid":true}'
            return resp

        mock_requests.side_effect = side_effect
        with patch("src.core.license_validator.get_hardware_id", return_value="HWID"):
            with patch(
                "src.core.license_validator.get_detailed_license_status", return_value=("VALID", "OK")
            ):
                with patch("src.core.license_updater._save_license_files", return_value=True):
                    assert license_updater.run_update() is True

    def test_grace_period_valid(self, mock_data_dir, mock_time, grace_key):  # noqa: ANN001
        cipher = Fernet(grace_key)
        yesterday = datetime.now(UTC) - timedelta(days=1)
        token = cipher.encrypt(yesterday.isoformat().encode("utf-8"))
        (mock_data_dir / "validity.token").write_bytes(token)
        assert license_updater.check_grace_period() is True

    def test_emergency_grace_activation(self, mock_data_dir, mock_time):  # noqa: ANN001
        success, _msg, days = license_updater.check_emergency_grace_period()
        assert success is True
        assert (mock_data_dir / "emergency_grace.token").exists()
        assert days == 3  # noqa: PLR2004
