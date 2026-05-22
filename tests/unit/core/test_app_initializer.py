from unittest.mock import MagicMock, patch

import pytest

from src.core.app_initializer import AppInitializer


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
    def test_initialize_core_success(self, mock_db, mock_lic, mock_env, mock_log):
        res = AppInitializer.initialize_core()
        assert res is True
        assert AppInitializer._core_initialized is True

        # Second call should return True immediately
        res2 = AppInitializer.initialize_core()
        assert res2 is True
        assert mock_db.call_count == 1

    @patch("src.core.app_initializer.get_available_bots", return_value=[])
    @patch("src.utils.resource_manager.ResourceManager.ensure_automation_driver")
    @patch("src.core.app_initializer.CONFIG_DIR")
    def test_verify_environment(self, mock_dir, mock_driver, mock_bots):
        step = MagicMock()
        AppInitializer._verify_environment(step)
        assert mock_dir.mkdir.called
        assert mock_driver.called
        assert step.called

    def test_init_generator_basic(self):
        mw = MagicMock()
        # Mock navigation_controller.get_panel to do nothing
        mw.navigation_controller.get_panel.return_value = None

        gen = AppInitializer.init_generator(mw)
        results = list(gen)

        assert len(results) > 1
        assert results[-1] == ("Sistema Pronto", 100)
        assert mw.navigation_controller.get_panel.called
