from unittest.mock import MagicMock

import pytest

from src.core.app_initializer import AppInitializer
from src.core.license_validator import LicenseStatus


class TestAppInitializerCoverage:

    @pytest.fixture
    def mock_license(self, mocker):
        """Mock per le funzioni di licenza."""
        return {
            "get_status": mocker.patch("src.core.app_initializer.get_detailed_license_status"),
            "run_update": mocker.patch("src.core.app_initializer.run_update"),
            "check_grace": mocker.patch("src.core.app_initializer.check_emergency_grace_period"),
            "get_hwid": mocker.patch("src.core.app_initializer.get_hardware_id")
        }

    @pytest.fixture
    def mock_ui(self, mocker):
        """Mock per QMessageBox e sys.exit."""
        return {
            "msgbox": mocker.patch("src.core.app_initializer.QMessageBox"),
            "exit": mocker.patch("sys.exit")
        }

    def test_check_license_valid_immediate(self, mock_license):
        """Test: Licenza valida al primo colpo."""
        mock_license["get_status"].return_value = (LicenseStatus.VALID, "OK")

        res = AppInitializer._check_license()

        assert res is True
        mock_license["run_update"].assert_not_called()

    def test_check_license_recovery_via_update(self, mock_license):
        """Test: Licenza recuperata dopo aggiornamento online."""
        # Primo call fallisce, secondo (dopo update) riesce
        mock_license["get_status"].side_effect = [
            (LicenseStatus.INVALID, "Expired"),
            (LicenseStatus.VALID, "OK")
        ]

        res = AppInitializer._check_license()

        assert res is True
        mock_license["run_update"].assert_called_once()

    def test_check_license_grace_period_allowed(self, mock_license, mock_ui):
        """Test: Accesso consentito tramite periodo di grazia."""
        mock_license["get_status"].return_value = (LicenseStatus.INVALID, "No internet")
        mock_license["check_grace"].return_value = (True, "Grace active", 3)
        mock_license["get_hwid"].return_value = "HW123"

        res = AppInitializer._check_license()

        assert res is True
        mock_ui["msgbox"].warning.assert_called_once()

    def test_check_license_fatal_failure(self, mock_license, mock_ui):
        """Test: Accesso negato (licenza invalida e grazia scaduta)."""
        mock_license["get_status"].return_value = (LicenseStatus.INVALID, "Blocked")
        mock_license["check_grace"].return_value = (False, "Grace expired", 0)

        res = AppInitializer._check_license()

        assert res is False
        mock_ui["msgbox"].critical.assert_called_once()

    def test_initialize_full_success(self, mocker):
        """Test: Workflow completo di inizializzazione riuscito."""
        mocker.patch.object(AppInitializer, "_check_license", return_value=True)
        mocker.patch.object(AppInitializer, "_init_db", return_value=True)

        assert AppInitializer.initialize() is True

    def test_initialize_fail_license_exits(self, mocker, mock_ui):
        """Test: initialize chiama sys.exit se la licenza fallisce."""
        mocker.patch.object(AppInitializer, "_check_license", return_value=False)

        AppInitializer.initialize()
        mock_ui["exit"].assert_called_with(1)

    def test_init_db_success(self, mocker):
        """Test: Inizializzazione DB riuscita."""
        mock_db = mocker.patch("src.core.app_initializer.db_manager.init_db")
        assert AppInitializer._init_db() is True
        mock_db.assert_called_once()

    def test_setup_app_style(self, mocker):
        """Test: Configurazione stili e metadati app."""
        mock_app = MagicMock()
        mock_apply = mocker.patch("src.core.app_initializer.apply_theme")

        AppInitializer.setup_app_style(mock_app)

        mock_app.setStyle.assert_called_with("Fusion")
        mock_apply.assert_called_with(mock_app, "light")
        mock_app.setApplicationName.assert_called_with("SyncroJob")
