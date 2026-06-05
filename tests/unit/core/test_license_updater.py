import json
from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest
from cryptography.fernet import Fernet

from src.application.services.exceptions import LicenseError
from src.application.services.license_updater import (
    check_emergency_grace_period,
    check_grace_period,
    get_license_dir,
    is_license_folder_empty,
    run_update,
    update_grace_timestamp,
)
from src.application.services.license_validator import LicenseStatus


class TestLicenseUpdater:
    @pytest.fixture(autouse=True)
    def setup_env(self, fs):
        self.license_dir = get_license_dir()
        fs.create_dir(str(self.license_dir))
        self.v_token = self.license_dir / "validity.token"
        self.e_token = self.license_dir / "emergency_grace.token"

        # Mock keys
        self.grace_key = Fernet.generate_key()
        self.license_key = Fernet.generate_key()

    @patch("src.application.services.time_manager.get_trusted_time")
    @patch("src.application.services.secrets_manager.SecretsManager.get_grace_period_key")
    def test_update_grace_timestamp(self, mock_key, mock_time, fs):
        mock_key.return_value = self.grace_key
        fixed_now = datetime(2026, 5, 23, 10, 0, 0, tzinfo=UTC)
        mock_time.return_value = (fixed_now, True)

        update_grace_timestamp()

        assert self.v_token.exists()
        cipher = Fernet(self.grace_key)
        decrypted = cipher.decrypt(self.v_token.read_bytes()).decode()
        assert decrypted == fixed_now.isoformat()

    @patch("src.application.services.time_manager.get_trusted_time")
    @patch("src.application.services.secrets_manager.SecretsManager.get_grace_period_key")
    def test_check_grace_period_valid(self, mock_key, mock_time, fs):
        mock_key.return_value = self.grace_key
        last_online = datetime(2026, 5, 20, 10, 0, 0, tzinfo=UTC)
        now = datetime(2026, 5, 22, 10, 0, 0, tzinfo=UTC)
        mock_time.return_value = (now, True)

        # Crea token valido (2 giorni fa)
        cipher = Fernet(self.grace_key)
        self.v_token.write_bytes(cipher.encrypt(last_online.isoformat().encode()))

        assert check_grace_period() is True

    @patch("src.application.services.time_manager.get_trusted_time")
    @patch("src.application.services.secrets_manager.SecretsManager.get_grace_period_key")
    def test_check_grace_period_expired(self, mock_key, mock_time, fs):
        mock_key.return_value = self.grace_key
        last_online = datetime(2026, 5, 10, 10, 0, 0, tzinfo=UTC)
        now = datetime(2026, 5, 23, 10, 0, 0, tzinfo=UTC)
        mock_time.return_value = (now, True)

        cipher = Fernet(self.grace_key)
        self.v_token.write_bytes(cipher.encrypt(last_online.isoformat().encode()))

        with pytest.raises(LicenseError, match="SCADUTO"):
            check_grace_period()

    @patch("src.application.services.time_manager.get_trusted_time")
    @patch("src.application.services.secrets_manager.SecretsManager.get_grace_period_key")
    def test_check_emergency_grace_period_activation(self, mock_key, mock_time, fs):
        mock_key.return_value = self.grace_key
        mock_time.return_value = (datetime(2026, 1, 1), True)

        active, _msg, days = check_emergency_grace_period()
        assert active is True
        assert days == 3
        assert self.e_token.exists()

    def test_is_license_folder_empty(self, fs):
        assert is_license_folder_empty() is True
        fs.create_file(str(self.license_dir / "config.dat"))
        fs.create_file(str(self.license_dir / "manifest.json"))
        assert is_license_folder_empty() is False

    @patch("src.application.services.license_updater.requests.get")
    @patch("src.application.services.license_validator.get_hardware_id", return_value="HW123")
    @patch("src.application.services.secrets_manager.SecretsManager.get_github_token", return_value="TOKEN")
    @patch("src.application.services.secrets_manager.SecretsManager.get_license_key")
    @patch("src.application.services.license_validator.get_detailed_license_status")
    def test_run_update_revoked(self, mock_status, mock_lic_key, mock_gh, mock_hwid, mock_get, fs):  # noqa: PLR0913
        # Simula 404 sul server (Cartella non trovata -> Revoca)
        mock_res = MagicMock()
        mock_res.status_code = 404
        mock_get.return_value = mock_res

        fs.create_file(str(self.license_dir / "config.dat"))

        with pytest.raises(LicenseError, match="REVOCATA"):
            run_update()

        assert not (self.license_dir / "config.dat").exists()

    @patch("src.application.services.license_updater.requests.get")
    @patch("src.application.services.license_validator.get_hardware_id", return_value="HW123")
    @patch("src.application.services.secrets_manager.SecretsManager.get_github_token", return_value="TOKEN")
    @patch("src.application.services.secrets_manager.SecretsManager.get_license_key")
    @patch("src.application.services.license_validator.get_detailed_license_status")
    @patch("src.application.services.license_validator._calculate_sha256", return_value="old_hash")
    def test_run_update_download_success(  # noqa: PLR0913
        self, mock_sha, mock_status, mock_lic_key, mock_gh, mock_hwid, mock_get, fs
    ):
        mock_lic_key.return_value = self.license_key
        mock_status.return_value = (LicenseStatus.VALID, "")

        # 1. Check dir (200)
        res_dir = MagicMock(status_code=200)
        # 2. Download manifest (new hash)
        res_man = MagicMock(status_code=200, content=json.dumps({"config.dat": "new_hash"}).encode())
        # 3. Download config.dat
        payload = {"Hardware ID": "HW123", "Other": "Data"}
        encrypted = Fernet(self.license_key).encrypt(json.dumps(payload).encode())
        res_conf = MagicMock(status_code=200, content=encrypted)

        mock_get.side_effect = [res_dir, res_man, res_conf]

        with patch("src.application.services.license_updater.update_grace_timestamp"):
            success = run_update()
            assert success is True
            assert (self.license_dir / "config.dat").exists()
            assert (self.license_dir / "manifest.json").exists()

    @patch("src.application.services.license_updater.requests.get")
    @patch("src.application.services.license_validator.get_hardware_id", return_value="HW123")
    def test_run_update_hwid_mismatch(self, mock_hwid, mock_get, fs):
        # Download di una licenza con HWID diverso
        res_dir = MagicMock(status_code=200)
        res_man = MagicMock(status_code=200, content=json.dumps({"config.dat": "new"}).encode())

        wrong_payload = {"Hardware ID": "WRONG_HW"}
        encrypted = Fernet(self.license_key).encrypt(json.dumps(wrong_payload).encode())
        res_conf = MagicMock(status_code=200, content=encrypted)

        mock_get.side_effect = [res_dir, res_man, res_conf]

        with patch(
            "src.application.services.secrets_manager.SecretsManager.get_license_key",
            return_value=self.license_key,
        ):
            with patch(
                "src.application.services.license_validator.get_detailed_license_status",
                return_value=(LicenseStatus.INVALID, ""),
            ):
                success = run_update()
                assert success is False
