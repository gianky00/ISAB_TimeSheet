# ruff: noqa: PLR0913
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtWidgets import QApplication

from src.application.services.app_initializer import AppInitializer


class TestAppInitializerRobust:
    @pytest.fixture(autouse=True)
    def reset_state(self):
        """Resetta lo stato interno tra i test."""
        AppInitializer._core_initialized = False
        yield
        AppInitializer._core_initialized = False

    @pytest.fixture
    def mock_qapp(self):
        """Mocka QApplication."""
        return QApplication([]) if not QApplication.instance() else QApplication.instance()

    @patch("src.application.services.app_initializer.AppInitializer._setup_logging")
    @patch(
        "src.application.services.initialization.migration_engine.DatabaseMigrationEngine.initialize_database"
    )
    @patch("src.application.services.initialization.license_verifier.LicenseVerifier.verify_license")
    @patch("src.infrastructure.utils.resource_manager.ResourceManager.ensure_automation_driver")
    @patch("src.application.services.app_initializer.get_available_bots")
    @patch("src.application.services.app_initializer.AppInitializer._preload_heavy_modules")
    def test_initialize_core_success(
        self,
        mock_preload,
        mock_bots,
        mock_driver,
        mock_license,
        mock_db,
        mock_log,
    ):
        """Test inizializzazione core completa con successo."""
        mock_bots.return_value = []

        result = AppInitializer.initialize_core()

        assert result is True
        assert AppInitializer._core_initialized is True
        mock_log.assert_called_once()
        mock_db.assert_called_once()
        mock_license.assert_called_once()
        mock_driver.assert_called_once()
        mock_preload.assert_called_once()

    @patch("src.application.services.app_initializer.AppInitializer._setup_logging")
    @patch("src.application.services.initialization.license_verifier.LicenseVerifier.verify_license")
    def test_initialize_core_license_invalid(
        self,
        mock_license,
        mock_log,
    ):
        """Test blocco inizializzazione se licenza invalida."""
        # Simula licenza NON valida (solleva eccezione nel codice reale)
        mock_license.side_effect = Exception("Licenza non valida")

        # Mi aspetto eccezione bloccante
        with pytest.raises(Exception, match="Licenza non valida"):
            AppInitializer.initialize_core()

        assert AppInitializer._core_initialized is False

    @patch("src.application.services.app_initializer.logger")
    @patch(
        "src.application.services.initialization.migration_engine.DatabaseMigrationEngine.initialize_database"
    )
    def test_initialize_core_failure(
        self,
        mock_db_init,
        mock_logger,
    ):
        """Test gestione errore critico in init core (DB failure)."""
        mock_db_init.side_effect = Exception("DB Error")

        # Patch dependencies to avoid early exit on other steps
        with (
            patch.object(AppInitializer, "_setup_logging"),
            patch.object(AppInitializer, "_verify_environment"),
            patch("src.application.services.initialization.license_verifier.LicenseVerifier.verify_license"),
        ):
            # Mi aspetto eccezione StartupError (wrappata)
            from src.application.services.exceptions import StartupError

            with pytest.raises(StartupError, match="DB Error"):
                AppInitializer.initialize_core()

            assert AppInitializer._core_initialized is False

    def test_init_generator_flow(self):
        """Test del generatore di inizializzazione GUI."""
        mock_mw = MagicMock()
        mock_nav = mock_mw.navigation_controller

        # Esegui generatore
        gen = AppInitializer.init_generator(mock_mw)

        steps = []
        for name, prog in gen:
            steps.append((name, prog))

        # Verifiche
        assert len(steps) > 5
        assert steps[-1][1] == 100  # Ultimo step 100%

        # Verifica chiamate ai pannelli (verifica indici principali)
        expected_indices = [0, 1, 10, 3, 4, 9, 5, 6, 7, 11, 8, 12]
        for idx in expected_indices:
            mock_nav.get_panel.assert_any_call(idx)

    @patch("src.application.services.app_initializer.configure_logging")
    def test_setup_logging_success(self, mock_conf):
        """Test configurazione logging."""
        AppInitializer._setup_logging()
        mock_conf.assert_called_once()

    @patch("src.application.services.app_initializer.configure_logging", side_effect=Exception("Log Fail"))
    @patch("logging.basicConfig")
    def test_setup_logging_fallback(self, mock_basic, mock_conf):
        """Test fallback logging base su errore."""
        AppInitializer._setup_logging()
        mock_basic.assert_called_once()
