from unittest.mock import MagicMock

import pytest

from src.core.app_initializer import AppInitializer
from src.core.license_validator import LicenseStatus


class TestAppInitializerHardened:
    """Test di inizializzazione con focus sulla resilienza e dipendenze."""

    @pytest.fixture
    def mock_deps(self, mocker):
        return {
            "db_manager": mocker.patch("src.core.database.db_manager"),
            "get_status": mocker.patch(
                "src.core.license_validator.get_detailed_license_status"
            ),
            "run_update": mocker.patch("src.core.license_updater.run_update"),
            "setup_logging": mocker.patch.object(AppInitializer, "_setup_logging"),
            "exit": mocker.patch("sys.exit"),
        }

    def test_initialize_success(self, mock_deps):
        """Workflow standard: tutto pronto e valido."""
        AppInitializer._core_initialized = False
        mock_deps["get_status"].return_value = (LicenseStatus.VALID, "Valid")

        result = AppInitializer.initialize_core()

        assert result is True
        mock_deps["db_manager"].init_db.assert_called_once()
        mock_deps["run_update"].assert_not_called()

    def test_initialize_with_cloud_sync(self, mock_deps):
        """Workflow con licenza da aggiornare (sync cloud)."""
        AppInitializer._core_initialized = False
        mock_deps["get_status"].return_value = (LicenseStatus.EXPIRED, "Expired")

        result = AppInitializer.initialize_core()

        assert result is True
        mock_deps["run_update"].assert_called_once()
        mock_deps["db_manager"].init_db.assert_called_once()

    def test_db_init_fatal_fail(self, mock_deps):
        """Se il DB crasha durante init_db, initialize_core deve fallire."""
        AppInitializer._core_initialized = False
        mock_deps["get_status"].return_value = (LicenseStatus.VALID, "Valid")
        mock_deps["db_manager"].init_db.side_effect = Exception("Fatal DB Error")

        result = AppInitializer.initialize_core()

        assert result is False
        assert AppInitializer._core_initialized is False

    def test_setup_app_style_minimal(self, mocker):
        """Verifica setup base stile senza dipendenze pesanti."""
        mock_app = MagicMock()
        mock_apply = mocker.patch("src.gui.styles.apply_theme")

        AppInitializer.setup_app_style(mock_app)

        mock_app.setStyle.assert_called_with("Fusion")
        mock_app.setApplicationName.assert_called_with("SyncroJob")
        mock_apply.assert_called()