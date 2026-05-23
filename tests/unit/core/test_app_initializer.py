from unittest.mock import MagicMock, patch

import pytest

from src.core.app_initializer import AppInitializer
from src.core.exceptions import StartupError


class TestAppInitializer:
    @pytest.fixture(autouse=True)
    def reset_initializer(self):
        AppInitializer._core_initialized = False
        AppInitializer._startup_alerts = []

    @patch("src.core.app_initializer.configure_logging")
    @patch("src.core.app_initializer.LicenseVerifier.verify_license")
    @patch("src.core.app_initializer.DatabaseMigrationEngine.initialize_database")
    @patch("src.core.app_initializer.ResourceManager.ensure_automation_driver")
    @patch("src.core.app_initializer.AppInitializer._preload_heavy_modules")
    def test_initialize_core_success(self, mock_preload, mock_driver, mock_db, mock_lic, mock_log, fs):  # noqa: PLR0913
        progress = MagicMock()
        success = AppInitializer.initialize_core(progress_callback=progress)

        assert success is True
        assert AppInitializer._core_initialized is True
        assert progress.called
        assert mock_lic.called
        assert mock_db.called

    def test_initialize_core_already_done(self):
        AppInitializer._core_initialized = True
        assert AppInitializer.initialize_core() is True

    @patch("src.core.app_initializer.LicenseVerifier.verify_license", side_effect=Exception("REVOCATA"))
    def test_initialize_core_critical_failure(self, mock_lic):
        with pytest.raises(Exception, match="REVOCATA"):
            AppInitializer.initialize_core()

    @patch("src.core.app_initializer.LicenseVerifier.verify_license", side_effect=Exception("Random Error"))
    def test_initialize_core_generic_failure(self, mock_lic):
        with pytest.raises(StartupError):
            AppInitializer.initialize_core()

    def test_alerts_management(self):
        AppInitializer.add_alert("warning", "Test Alert")
        alerts = AppInitializer.get_alerts()
        assert len(alerts) == 1
        assert alerts[0] == ("warning", "Test Alert")

    def test_init_generator(self):
        mock_mw = MagicMock()
        mock_panel = MagicMock()
        mock_mw.navigation_controller.get_panel.return_value = mock_panel

        gen = AppInitializer.init_generator(mock_mw)
        results = list(gen)

        assert len(results) > 10
        assert results[-1] == ("Sistema Pronto", 100)
        assert mock_mw.navigation_controller.get_panel.call_count == 12

    @patch("src.utils.helpers.cleanup_bot_processes")
    @patch("playwright.sync_api.sync_playwright")
    def test_preload_heavy_modules(self, mock_pw, mock_cleanup):
        # Mocking the context manager / entry point for playwright
        mock_instance = MagicMock()
        mock_pw.return_value = mock_instance

        # Simula errore nel lancio browser
        mock_instance.start.return_value.chromium.launch.side_effect = Exception("Browser Fail")

        # Non deve crashare l'app
        AppInitializer._preload_heavy_modules()
        assert mock_cleanup.called
        assert mock_pw.called
