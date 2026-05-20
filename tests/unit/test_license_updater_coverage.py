from unittest.mock import MagicMock, patch

import pytest

from src.core.license_updater import (
    _save_license_files,
    check_emergency_grace_period,
    check_grace_period,
    get_github_token,
    run_update,
)


class TestLicenseUpdater:
    @pytest.fixture
    def mock_paths(self, tmp_path):
        data_dir = tmp_path / "AppData"
        license_dir = data_dir / "Licenza"
        license_dir.mkdir(parents=True)
        with patch("src.core.paths.get_data_path", return_value=str(data_dir)):
            yield license_dir

    @patch("src.core.license_validator.get_hardware_id", return_value="HWID")
    @patch("src.core.license_validator.get_detailed_license_status")
    @patch("requests.get")
    def test_run_update_success(self, mock_get, mock_status, mock_hwid, mock_paths):
        import json

        from cryptography.fernet import Fernet

        fake_key = Fernet.generate_key().decode()
        cipher = Fernet(fake_key.encode())

        # Payload JSON valido con HWID per superare validazione
        payload = json.dumps({"Hardware ID": "HWID"}).encode("utf-8")
        fake_license_content = cipher.encrypt(payload)

        mock_status.return_value = ("VALID", "OK")

        # Mock per la lista directory, manifest.json e config.dat
        res_dir = MagicMock()
        res_dir.status_code = 200
        res_dir.json.return_value = [{"name": "manifest.json", "download_url": "url"}]

        res_man = MagicMock()
        res_man.status_code = 200
        res_man.content = b'{"config.dat": "hash"}'

        res_conf = MagicMock()
        res_conf.status_code = 200
        res_conf.content = fake_license_content

        mock_get.side_effect = [res_dir, res_man, res_conf]

        # Patch interna per evitare download reali e fornire chiave
        with (
            patch("src.core.license_updater._save_license_files", return_value=True),
            patch("src.core.secrets_manager.SecretsManager.get_license_key", return_value=fake_key),
        ):
            assert run_update() is True

    def test_save_license_files(self, mock_paths):
        files = {"test.dat": b"content"}
        assert _save_license_files(str(mock_paths), files) is True
        assert (mock_paths / "test.dat").read_bytes() == b"content"

    def test_get_github_token(self):
        token = get_github_token()
        assert isinstance(token, str)
        assert token.startswith("ghp_")

    def test_check_grace_period_no_token(self, mock_paths):
        with pytest.raises(Exception, match="Nessuna validazione"):
            check_grace_period()

    def test_emergency_grace_activation(self, mock_paths):
        from datetime import datetime
        token_path = mock_paths / "emergency_grace.token"
        with (
            patch("src.core.license_updater.time_manager.get_trusted_time", return_value=(datetime.now(), True)),
            patch("src.core.license_updater.SecretsManager.get_grace_period_key", return_value=b'6h4_H9_z8z8H9Z9H9z8z8H9Z9H9z8z8H9Z9H9z8z8H9='),
            patch("src.core.license_updater._get_emergency_grace_token_path", return_value=token_path),
        ):
            success, _msg, days = check_emergency_grace_period()
            assert success is True
            assert token_path.exists()
            assert days == 3
