from unittest.mock import MagicMock

import pytest

from src.core.app_initializer import AppInitializer
from src.core.license_validator import LicenseStatus


class TestAppInitializer:
    @pytest.fixture
    def mock_deps(self, mocker):
        return {
            "db": mocker.patch("src.core.app_initializer.db_manager"),
            "license_status": mocker.patch("src.core.app_initializer.get_detailed_license_status"),
            "license_update": mocker.patch("src.core.app_initializer.run_update"),
            "grace": mocker.patch("src.core.app_initializer.check_emergency_grace_period"),
            "msgbox": mocker.patch("src.core.app_initializer.QMessageBox"),
            "exit": mocker.patch("sys.exit"),
        }

    def test_initialize_success(self, mock_deps):
        mock_deps["license_status"].return_value = (LicenseStatus.VALID, "Valid")

        result = AppInitializer.initialize()

        assert result is True
        mock_deps["db"].init_db.assert_called_once()
        mock_deps["exit"].assert_not_called()

    def test_initialize_license_fail_grace_fail(self, mock_deps):
        mock_deps["license_status"].return_value = (LicenseStatus.EXPIRED, "Expired")
        mock_deps["grace"].return_value = (False, "Grace Expired", 0)

        AppInitializer.initialize()

        mock_deps["exit"].assert_called_with(1)
        mock_deps["msgbox"].critical.assert_called()

    def test_initialize_license_fail_grace_allowed(self, mock_deps):
        mock_deps["license_status"].return_value = (LicenseStatus.EXPIRED, "Expired")
        mock_deps["grace"].return_value = (True, "Grace active", 5)

        result = AppInitializer.initialize()

        assert result is True
        mock_deps["msgbox"].warning.assert_called()  # Grace warning
        mock_deps["db"].init_db.assert_called_once()

    def test_db_init_fail(self, mock_deps):
        mock_deps["license_status"].return_value = (LicenseStatus.VALID, "Valid")
        mock_deps["db"].init_db.side_effect = Exception("DB crash")

        AppInitializer.initialize()

        mock_deps["exit"].assert_called_with(1)
        mock_deps["msgbox"].critical.assert_called()

    def test_setup_app_style(self):
        mock_app = MagicMock()
        AppInitializer.setup_app_style(mock_app)

        mock_app.setStyle.assert_called_with("Fusion")
        mock_app.setApplicationName.assert_called_with("SyncroJob")
