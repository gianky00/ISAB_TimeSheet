"""
Tests for AppInitializer startup sequence.
"""

from unittest.mock import MagicMock, patch

from src.core.app_initializer import AppInitializer
from src.core.license_validator import LicenseStatus


class TestAppInitializer:
    def test_initialize_core_idempotency(self, mocker):
        """Verifica che l'inizializzazione core non venga rieseguita se gia' fatta."""
        AppInitializer._core_initialized = False  # Reset state

        # Mocking components to avoid real side effects
        mocker.patch("src.core.app_initializer.AppInitializer._setup_logging")
        mocker.patch("src.core.database.db_manager.init_db")
        mocker.patch("src.core.license_updater.run_update")
        mocker.patch(
            "src.core.license_validator.get_detailed_license_status",
            return_value=(LicenseStatus.VALID, "OK"),
        )

        success = AppInitializer.initialize_core()
        assert success is True
        assert AppInitializer._core_initialized is True

        # Seconda chiamata: non deve chiamare init_db di nuovo
        with patch("src.core.database.db_manager.init_db") as mock_init:
            success2 = AppInitializer.initialize_core()
            assert success2 is True
            assert not mock_init.called

    def test_init_generator_steps(self, mocker):
        """Verifica che il generatore di inizializzazione GUI emetta gli step corretti."""
        mock_mw = MagicMock()
        mock_mw.navigation_controller.get_panel.return_value = MagicMock()

        # Mock PageIndex to avoid real imports if needed, but it's usually safe

        gen = AppInitializer.init_generator(mock_mw)

        steps = list(gen)
        # Dovrebbe esserci uno step per ogni pannello + telegram + pronto
        assert len(steps) > 5

        # Verifica che l'ultimo step sia "Sistema Pronto" al 100%
        last_name, last_prog = steps[-1]
        assert "Pronto" in last_name
        assert last_prog == 100

        # Verifica che il navigation controller sia stato chiamato per caricare i pannelli
        assert mock_mw.navigation_controller.get_panel.called

    @patch("src.core.database.db_manager.init_db", side_effect=Exception("DB Error"))
    def test_initialize_core_failure_handling(self, mock_db_init, mocker):
        """Verifica che un errore nel core sollevi eccezione."""
        import pytest

        AppInitializer._core_initialized = False
        mocker.patch("src.core.app_initializer.AppInitializer._setup_logging")
        mocker.patch("src.core.license_updater.run_update")
        mocker.patch(
            "src.core.license_validator.get_detailed_license_status",
            return_value=(LicenseStatus.VALID, "OK"),
        )

        with pytest.raises(Exception, match="DB Error"):
            AppInitializer.initialize_core()

        assert AppInitializer._core_initialized is False
