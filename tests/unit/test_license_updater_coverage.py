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
    def mock_paths(self, tmp_path):  # noqa: ANN001
        data_dir = tmp_path / "AppData"
        license_dir = data_dir / "Licenza"
        license_dir.mkdir(parents=True)
        with patch("src.core.config_manager.get_data_path", return_value=str(data_dir)):
            yield license_dir

    @patch("src.core.license_validator.get_hardware_id", return_value="HWID")
    @patch("src.core.license_validator.get_detailed_license_status")
    @patch("requests.get")
    def test_run_update_success(self, mock_get, mock_status, mock_hwid, mock_paths):  # noqa: ANN001
        mock_status.return_value = ("VALID", "OK")
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.content = b"fake_data"
        mock_get.return_value = mock_res

        # Patch interna per evitare download reali
        with patch("src.core.license_updater._save_license_files", return_value=True):
            assert run_update() is True

    def test_save_license_files(self, mock_paths):  # noqa: ANN001
        files = {"test.dat": b"content"}
        assert _save_license_files(str(mock_paths), files) is True
        assert (mock_paths / "test.dat").read_bytes() == b"content"

    def test_get_github_token(self):
        token = get_github_token()
        assert isinstance(token, str)
        assert token.startswith("ghp_")

    def test_check_grace_period_no_token(self, mock_paths):  # noqa: ANN001
        with pytest.raises(Exception, match="Nessuna validazione"):
            check_grace_period()

    def test_emergency_grace_activation(self, mock_paths):  # noqa: ANN001
        success, _msg, days = check_emergency_grace_period()
        assert success is True
        assert (mock_paths / "emergency_grace.token").exists()
        assert days == 3  # noqa: PLR2004
