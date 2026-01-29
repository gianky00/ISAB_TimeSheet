from unittest.mock import MagicMock, patch

import pytest

from src.core.app_initializer import AppInitializer
from src.core.license_validator import LicenseStatus


class TestAppInitializerCoverage:
    """Test di copertura per la nuova architettura di AppInitializer."""

    @pytest.fixture
    def mock_core_deps(self, mocker):
        """Mock per le dipendenze pesanti di initialize_core."""
        return {
            "get_status": mocker.patch(
                "src.core.license_validator.get_detailed_license_status"
            ),
            "run_update": mocker.patch("src.core.license_updater.run_update"),
            "db_init": mocker.patch("src.core.database.db_manager.init_db"),
            "setup_logging": mocker.patch.object(AppInitializer, "_setup_logging"),
        }

    def test_initialize_core_success(self, mock_core_deps):
        """Test: Inizializzazione core completa con licenza valida."""
        AppInitializer._core_initialized = False
        mock_core_deps["get_status"].return_value = (LicenseStatus.VALID, "OK")

        res = AppInitializer.initialize_core()

        assert res is True
        assert AppInitializer._core_initialized is True
        mock_core_deps["setup_logging"].assert_called_once()
        mock_core_deps["db_init"].assert_called_once()
        mock_core_deps["run_update"].assert_not_called()

    def test_initialize_core_already_done(self, mock_core_deps):
        """Test: Ritorna True subito se già inizializzato."""
        AppInitializer._core_initialized = True
        res = AppInitializer.initialize_core()
        assert res is True
        mock_core_deps["setup_logging"].assert_not_called()

    def test_initialize_core_with_license_update(self, mock_core_deps):
        """Test: Esegue update licenza se non valida."""
        AppInitializer._core_initialized = False
        mock_core_deps["get_status"].return_value = (LicenseStatus.INVALID, "Expired")

        res = AppInitializer.initialize_core()

        assert res is True
        mock_core_deps["run_update"].assert_called_once()

    def test_initialize_core_exception(self, mock_core_deps):
        """Test: Gestione eccezioni durante inizializzazione."""
        AppInitializer._core_initialized = False
        mock_core_deps["setup_logging"].side_effect = Exception("Crash")

        res = AppInitializer.initialize_core()

        assert res is False
        assert AppInitializer._core_initialized is False

    def test_setup_app_style(self, mocker):
        """Test: Configurazione stili e metadati app."""
        mock_app = MagicMock()
        mock_apply = mocker.patch("src.gui.styles.apply_theme")

        AppInitializer.setup_app_style(mock_app)

        mock_app.setStyle.assert_called_with("Fusion")
        mock_apply.assert_called_with(mock_app, "light")
        mock_app.setApplicationName.assert_called_with("SyncroJob")

    def test_init_generator_steps(self, mocker):
        """Test: Il generatore produce gli step attesi."""
        mock_mw = MagicMock()
        # Mock per evitare caricamento pannelli reali
        mocker.patch.object(
            mock_mw.navigation_controller, "get_panel", return_value=MagicMock()
        )
        mocker.patch("src.core.config_manager.load_config", return_value={})

        gen = AppInitializer.init_generator(mock_mw)

        steps = list(gen)
        # Verifica che ci siano step e che l'ultimo sia al 100%
        assert len(steps) > 0
        assert steps[-1][1] == 100
        assert "Sistema Pronto" in steps[-1][0]
