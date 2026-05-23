from unittest.mock import MagicMock, patch

import pytest

from src.core.app_initializer import AppInitializer
from src.core.exceptions import StartupError


class TestAppInitializer:
    @pytest.fixture(autouse=True)
    def reset_state(self):
        AppInitializer._core_initialized = False
        AppInitializer._startup_alerts = []

    def test_add_get_alerts(self):
        AppInitializer.add_alert("error", "msg")
        alerts = AppInitializer.get_alerts()
        assert len(alerts) == 1
        assert alerts[0] == ("error", "msg")

    @patch("src.core.app_initializer.AppInitializer._setup_logging")
    @patch("src.core.app_initializer.AppInitializer._verify_environment")
    @patch("src.core.app_initializer.LicenseVerifier.verify_license")
    @patch("src.core.app_initializer.DatabaseMigrationEngine.initialize_database")
    @patch("src.core.app_initializer.AppInitializer._preload_heavy_modules")
    def test_initialize_core_success(self, mock_preload, mock_db, mock_lic, mock_env, mock_log):
        res = AppInitializer.initialize_core()
        assert res is True
        assert AppInitializer._core_initialized is True

        # Second call should return True immediately
        res2 = AppInitializer.initialize_core()
        assert res2 is True
        assert mock_db.call_count == 1

    @patch("src.core.app_initializer.AppInitializer._setup_logging")
    @patch("src.core.app_initializer.LicenseVerifier.verify_license")
    def test_initialize_core_license_revoked(self, mock_lic, mock_log):
        mock_lic.side_effect = Exception("REVOCATA")
        with pytest.raises(Exception, match="REVOCATA"):
            AppInitializer.initialize_core()

    @patch("src.core.app_initializer.AppInitializer._setup_logging")
    @patch("src.core.app_initializer.LicenseVerifier.verify_license")
    def test_initialize_core_generic_error(self, mock_lic, mock_log):
        mock_lic.side_effect = Exception("Some weird error")
        with pytest.raises(StartupError, match="Startup error: Some weird error"):
            AppInitializer.initialize_core()

    @patch("src.core.app_initializer.get_available_bots", return_value=[])
    @patch("src.utils.resource_manager.ResourceManager.ensure_automation_driver")
    def test_verify_environment(self, mock_driver, mock_bots, fs):
        # Usiamo fs (pyfakefs) per testare la creazione della directory
        step = MagicMock()
        AppInitializer._verify_environment(step)
        assert mock_driver.called
        assert step.called
        # La cartella CONFIG_DIR deve esistere (il path reale è mockato da pyfakefs)
        from src.core.paths import CONFIG_DIR

        assert CONFIG_DIR.exists()

    def test_init_generator_success(self):
        mw = MagicMock()
        mw.navigation_controller.get_panel.return_value = None

        gen = AppInitializer.init_generator(mw)
        results = list(gen)

        assert len(results) > 1
        assert results[-1] == ("Sistema Pronto", 100)
        assert mw.navigation_controller.get_panel.called

    def test_init_generator_panel_error(self):
        mw = MagicMock()
        mw.navigation_controller.get_panel.side_effect = Exception("Panel crash")

        gen = AppInitializer.init_generator(mw)
        results = list(gen)

        # Non deve bloccarsi se un pannello fallisce
        assert results[-1] == ("Sistema Pronto", 100)

    @patch("src.core.app_initializer.cleanup_bot_processes")
    @patch("src.core.app_initializer.sync_playwright")
    def test_preload_heavy_modules(self, mock_pw, mock_cleanup):
        # Mock per evitare l'avvio reale di Chromium
        mock_instance = MagicMock()
        mock_pw.return_value.start.return_value = mock_instance

        AppInitializer._preload_heavy_modules()

        assert mock_cleanup.called
        assert mock_instance.chromium.launch.called

    @patch("src.core.app_initializer.configure_logging")
    def test_setup_logging_success(self, mock_conf):
        AppInitializer._setup_logging()
        assert mock_conf.called

    @patch("src.core.app_initializer.configure_logging", side_effect=Exception("Log fail"))
    @patch("src.core.app_initializer.logging.basicConfig")
    def test_setup_logging_fallback(self, mock_basic, mock_conf):
        AppInitializer._setup_logging()
        assert mock_basic.called
