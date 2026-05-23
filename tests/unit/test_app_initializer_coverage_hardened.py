from unittest.mock import MagicMock

import pytest

from src.core.app_initializer import AppInitializer


class TestAppInitializerHardened:
    """Test di copertura per AppInitializer con isolamento profondo."""

    @pytest.fixture(autouse=True)
    def reset_state(self, mocker):
        AppInitializer._core_initialized = False
        # Mock global components to avoid real FS/DB access
        mocker.patch("src.core.initialization.license_verifier.LicenseVerifier.verify_license")
        mocker.patch("src.core.initialization.migration_engine.DatabaseMigrationEngine.initialize_database")
        mocker.patch("src.utils.resource_manager.ResourceManager.ensure_automation_driver")
        yield
        AppInitializer._core_initialized = False

    def test_initialize_success(self, mocker):
        """Test inizializzazione completa con successo."""
        mocker.patch.object(AppInitializer, "_setup_logging")
        mocker.patch.object(AppInitializer, "_preload_heavy_modules")
        mocker.patch("src.core.app_initializer.get_available_bots", return_value=[])

        res = AppInitializer.initialize_core()
        assert res is True
        assert AppInitializer._core_initialized is True

    def test_initialize_with_cloud_sync(self, mocker):
        """Test inizializzazione che innesca logica di ambiente."""
        mocker.patch.object(AppInitializer, "_setup_logging")
        mocker.patch.object(AppInitializer, "_preload_heavy_modules")

        # Simula presenza OneDrive
        mocker.patch("os.environ.get", side_effect=lambda k, d=None: "C:\\OneDrive" if k == "OneDrive" else d)

        res = AppInitializer.initialize_core()
        assert res is True

    def test_init_generator_robustness(self, mocker):
        """Verifica che il generatore gestisca bene i null."""
        mock_mw = MagicMock()
        # Mock NavigationController
        mocker.patch.object(mock_mw.navigation_controller, "get_panel", return_value=None)
        mocker.patch("src.core.config_manager.load_config", return_value={})

        gen = AppInitializer.init_generator(mock_mw)
        steps = list(gen)
        assert len(steps) > 0
        assert steps[-1][1] == 100
