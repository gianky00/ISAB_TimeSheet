from unittest.mock import MagicMock, patch

import pytest

from src.application.services.app_initializer import AppInitializer


class TestAppInitializerCoverage:
    """Test di copertura per la nuova architettura di AppInitializer."""

    @pytest.fixture(autouse=True)
    def reset_state(self):
        AppInitializer._core_initialized = False
        yield
        AppInitializer._core_initialized = False

    @pytest.fixture
    def mock_core_deps(self, mocker):
        """Mock per le dipendenze SRP di initialize_core."""
        return {
            "license_verify": mocker.patch(
                "src.application.services.initialization.license_verifier.LicenseVerifier.verify_license"
            ),
            "db_init": mocker.patch(
                "src.application.services.initialization.migration_engine.DatabaseMigrationEngine.initialize_database"
            ),
            "setup_logging": mocker.patch.object(AppInitializer, "_setup_logging"),
            "ensure_driver": mocker.patch(
                "src.infrastructure.utils.resource_manager.ResourceManager.ensure_automation_driver"
            ),
            "preload": mocker.patch.object(AppInitializer, "_preload_heavy_modules"),
            "get_bots": mocker.patch(
                "src.application.services.app_initializer.get_available_bots", return_value=[]
            ),
        }

    def test_initialize_core_success(self, mock_core_deps):
        """Test: Inizializzazione core completa con successo."""
        res = AppInitializer.initialize_core()

        assert res is True
        assert AppInitializer._core_initialized is True
        mock_core_deps["setup_logging"].assert_called_once()
        mock_core_deps["db_init"].assert_called_once()
        mock_core_deps["license_verify"].assert_called_once()

    def test_initialize_core_already_done(self, mock_core_deps):
        """Test: Ritorna True subito se già inizializzato."""
        AppInitializer._core_initialized = True
        res = AppInitializer.initialize_core()
        assert res is True
        mock_core_deps["setup_logging"].assert_not_called()

    def test_initialize_core_failure_wrapped(self, mock_core_deps):
        """Test: Gestione eccezioni wrappate in StartupError."""
        mock_core_deps["db_init"].side_effect = Exception("DB Crash")

        from src.application.services.exceptions import StartupError

        with pytest.raises(StartupError, match="DB Crash"):
            AppInitializer.initialize_core()

        assert AppInitializer._core_initialized is False

    def test_init_generator_flow(self, mocker):
        """Test: Il generatore produce gli step attesi per la GUI."""
        mock_mw = MagicMock()
        mocker.patch.object(mock_mw.navigation_controller, "get_panel", return_value=MagicMock())
        mocker.patch("src.application.services.config_manager.load_config", return_value={})

        gen = AppInitializer.init_generator(mock_mw)

        steps = list(gen)
        assert len(steps) > 0
        assert steps[-1][1] == 100
        assert "Sistema Pronto" in steps[-1][0]

    @patch("src.application.services.app_initializer.configure_logging")
    def test_setup_logging(self, mock_conf):
        AppInitializer._setup_logging()
        mock_conf.assert_called_once()
