from unittest.mock import MagicMock, patch

import pytest

from src.core.app_initializer import AppInitializer, _yield


class TestAppInitializer:
    @pytest.fixture(autouse=True)
    def reset_state(self):
        AppInitializer._core_initialized = False
        yield
        AppInitializer._core_initialized = False

    @patch("src.core.license_validator.get_detailed_license_status")
    @patch("src.core.database.db_manager.init_db")
    def test_initialize_core_success(self, mock_db_init, mock_license):
        from src.core.license_validator import LicenseStatus

        mock_license.return_value = (LicenseStatus.VALID, "OK")

        with patch.object(AppInitializer, "_setup_logging"):
            result = AppInitializer.initialize_core()

        assert result is True
        assert AppInitializer._core_initialized is True

    @patch("src.core.license_updater.run_update")
    @patch("src.core.license_validator.get_detailed_license_status")
    @patch("src.core.database.db_manager.init_db")
    def test_initialize_core_license_update(self, mock_db_init, mock_license, mock_update):
        from src.core.license_validator import LicenseStatus

        mock_license.return_value = (LicenseStatus.EXPIRED, "License expired")

        with patch.object(AppInitializer, "_setup_logging"):
            result = AppInitializer.initialize_core()

        assert result is True
        mock_update.assert_called_once()

    def test_initialize_core_already_initialized(self):
        AppInitializer._core_initialized = True

        result = AppInitializer.initialize_core()

        assert result is True

    @patch("src.core.database.db_manager.init_db", side_effect=Exception("DB Error"))
    def test_initialize_core_failure(self, mock_db_init):
        # Patch license check to avoid other side effects
        with patch("src.core.license_validator.get_detailed_license_status", return_value=(MagicMock(), "OK")):
            with patch.object(AppInitializer, "_setup_logging"):
                result = AppInitializer.initialize_core()

        assert result is False

    @patch("src.core.app_initializer.QApplication")
    def test_yield_processes_events(self, mock_qapp):
        mock_app = MagicMock()
        mock_qapp.instance.return_value = mock_app

        _yield()

        mock_app.processEvents.assert_called_once()

    @patch("src.core.app_initializer.QApplication")
    def test_yield_no_app(self, mock_qapp):
        mock_qapp.instance.return_value = None

        # Should not raise
        _yield()

    def test_init_generator_is_generator(self):
        mock_mw = MagicMock()

        gen = AppInitializer.init_generator(mock_mw)

        assert hasattr(gen, "__next__")

    @patch("src.core.config_manager.load_config", return_value={})
    def test_init_generator_yields_steps(self, mock_config):
        mock_mw = MagicMock()

        gen = AppInitializer.init_generator(mock_mw)

        first_step = next(gen)
        assert isinstance(first_step, tuple)
        assert len(first_step) == 2
        name, prog = first_step
        assert isinstance(name, str)
        assert isinstance(prog, int)

    @patch("src.core.logging.configure_logging")
    def test_setup_logging_enterprise(self, mock_configure):
        AppInitializer._setup_logging()
        mock_configure.assert_called_once()

    @patch("src.core.logging.configure_logging", side_effect=Exception("Logging error"))
    def test_setup_logging_fallback(self, mock_configure):
        # Should not raise, falls back to basicConfig
        AppInitializer._setup_logging()

    @patch("src.gui.styles.apply_theme")
    @patch("PyQt6.QtGui.QFont")
    def test_setup_app_style(self, mock_font, mock_theme):
        mock_app = MagicMock()

        AppInitializer.setup_app_style(mock_app)

        mock_app.setStyle.assert_called_once_with("Fusion")
        mock_app.setApplicationName.assert_called_once_with("SyncroJob")
