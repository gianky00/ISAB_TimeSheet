from unittest.mock import MagicMock, patch

import pytest

from src.core.app_initializer import AppInitializer


class TestAppInitializer:
    @pytest.fixture(autouse=True)
    def reset_state(self):
        AppInitializer._core_initialized = False
        yield
        AppInitializer._core_initialized = False

    @patch("src.core.license_updater.run_update")
    @patch("src.core.license_validator.get_detailed_license_status")
    @patch("src.core.database.db_manager.init_db")
    def test_initialize_core_success(self, mock_db_init, mock_license, mock_update):
        from src.core.license_validator import LicenseStatus  # noqa: PLC0415

        mock_license.return_value = (LicenseStatus.VALID, "OK")

        with patch.object(AppInitializer, "_setup_logging"):
            result = AppInitializer.initialize_core()

        assert result is True
        assert AppInitializer._core_initialized is True
        mock_update.assert_called_once()

    @patch("src.core.license_updater.run_update")
    @patch("src.core.license_validator.get_detailed_license_status")
    @patch("src.core.database.db_manager.init_db")
    def test_initialize_core_license_update(self, mock_db_init, mock_license, mock_update):
        from src.core.license_validator import LicenseStatus  # noqa: PLC0415

        mock_license.return_value = (LicenseStatus.EXPIRED, "License expired")

        with patch.object(AppInitializer, "_setup_logging"):
            with pytest.raises(Exception, match="Licenza non valida"):
                AppInitializer.initialize_core()

        mock_update.assert_called_once()

    def test_initialize_core_already_initialized(self):
        AppInitializer._core_initialized = True

        result = AppInitializer.initialize_core()

        assert result is True

    @patch("src.core.license_updater.run_update")
    @patch("src.core.database.db_manager.init_db", side_effect=Exception("DB Error"))
    def test_initialize_core_failure(self, mock_db_init, mock_update):
        # Patch license check to avoid other side effects
        from src.core.license_validator import LicenseStatus  # noqa: PLC0415

        with patch(
            "src.core.license_validator.get_detailed_license_status",
            return_value=(LicenseStatus.VALID, "OK"),
        ):
            with patch.object(AppInitializer, "_setup_logging"):
                with pytest.raises(Exception, match="Errore imprevisto durante l'avvio"):
                    AppInitializer.initialize_core()
        mock_update.assert_called_once()

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

    @patch("src.gui.styles.theme_manager.apply_theme")
    @patch("PyQt6.QtGui.QFont")
    @patch("PyQt6.QtWidgets.QApplication.instance")
    def test_setup_app_style(self, mock_instance, mock_font, mock_theme):
        mock_app = MagicMock()
        mock_instance.return_value = mock_app

        AppInitializer.setup_app_style(mock_app)

        # Verifica che i metodi siano stati chiamati sul mock_app passato o sull'istanza
        assert mock_app.setStyle.called
        assert mock_app.setApplicationName.called
