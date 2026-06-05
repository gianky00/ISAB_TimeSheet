from unittest.mock import MagicMock

import pytest

from src.application.services.app_initializer import AppInitializer


class TestAppStartupSequence:
    """Test della sequenza di avvio dell'applicazione (V9.4)."""

    @pytest.fixture(autouse=True)
    def reset_state(self):
        AppInitializer._core_initialized = False
        yield
        AppInitializer._core_initialized = False

    @pytest.fixture
    def mock_deps(self, mocker):
        return {
            "license": mocker.patch(
                "src.application.services.initialization.license_verifier.LicenseVerifier.verify_license"
            ),
            "db": mocker.patch(
                "src.application.services.initialization.migration_engine.DatabaseMigrationEngine.initialize_database"
            ),
            "logging": mocker.patch.object(AppInitializer, "_setup_logging"),
            "driver": mocker.patch(
                "src.infrastructure.utils.resource_manager.ResourceManager.ensure_automation_driver"
            ),
            "preload": mocker.patch.object(AppInitializer, "_preload_heavy_modules"),
            "bots": mocker.patch(
                "src.application.services.app_initializer.get_available_bots", return_value=[]
            ),
        }

    def test_initialize_core_idempotency(self, mock_deps):
        """Verifica che l'inizializzazione non venga ripetuta se già fatta."""
        AppInitializer.initialize_core()
        assert AppInitializer._core_initialized is True

        # Seconda chiamata
        AppInitializer.initialize_core()
        # I mock dovrebbero essere stati chiamati solo 1 volta (la prima)
        assert mock_deps["logging"].call_count == 1

    def test_initialize_core_failure_handling(self, mock_deps):
        """Verifica che errori critici vengano catturati e lo stato resettato."""
        mock_deps["db"].side_effect = Exception("Crash")

        from src.application.services.exceptions import StartupError

        with pytest.raises(StartupError):
            AppInitializer.initialize_core()

        assert AppInitializer._core_initialized is False

    def test_init_generator_steps(self, mocker):
        """Verifica il flusso degli step del generatore UI."""
        mock_mw = MagicMock()
        mocker.patch("src.application.services.config_manager.load_config", return_value={})
        mocker.patch.object(mock_mw.navigation_controller, "get_panel", return_value=MagicMock())

        gen = AppInitializer.init_generator(mock_mw)
        steps = [name for name, prog in gen]

        assert len(steps) > 5
        assert "Sistema Pronto" in steps[-1]
