from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtWidgets import QApplication

from src.core.app_initializer import AppInitializer


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
        app = QApplication([]) if not QApplication.instance() else QApplication.instance()
        return app

    @patch("src.core.app_initializer.AppInitializer._setup_logging")
    @patch("src.core.database.db_manager.init_db")
    @patch("src.core.license_validator.get_detailed_license_status")
    @patch("src.core.license_updater.run_update")
    @patch.dict(
        "sys.modules",
        {"pandas": MagicMock(), "numpy": MagicMock(), "selenium": MagicMock()},
    )
    def test_initialize_core_success(self, mock_update, mock_status, mock_db, mock_log):
        """Test inizializzazione core completa con successo."""
        from src.core.license_validator import LicenseStatus

        # Simula licenza valida
        mock_status.return_value = (LicenseStatus.VALID, "Valid")

        result = AppInitializer.initialize_core()

        assert result is True
        assert AppInitializer._core_initialized is True
        mock_log.assert_called_once()
        mock_db.assert_called_once()
        mock_update.assert_not_called()

    @patch("src.core.app_initializer.AppInitializer._setup_logging")
    @patch("src.core.database.db_manager.init_db")
    @patch("src.core.license_validator.get_detailed_license_status")
    @patch("src.core.license_updater.run_update")
    @patch.dict(
        "sys.modules",
        {"pandas": MagicMock(), "numpy": MagicMock(), "selenium": MagicMock()},
    )
    def test_initialize_core_license_invalid(self, mock_update, mock_status, mock_db, mock_log):
        """Test aggiornamento licenza se invalida."""
        from src.core.license_validator import LicenseStatus

        # Simula licenza NON valida
        mock_status.return_value = (LicenseStatus.EXPIRED, "Expired")

        result = AppInitializer.initialize_core()

        assert result is True
        mock_update.assert_called_once()
        mock_db.assert_called_once()

    @patch("src.core.app_initializer.logger")
    def test_initialize_core_failure(self, mock_logger):
        """Test gestione errore critico in init core."""
        # Forziamo errore nel setup logging (o altro step iniziale)
        with patch(
            "src.core.app_initializer.AppInitializer._setup_logging",
            side_effect=Exception("Critical Fail"),
        ):
            result = AppInitializer.initialize_core()

            assert result is False
            assert AppInitializer._core_initialized is False
            mock_logger.critical.assert_called()

    def test_init_generator_flow(self):
        """Test del generatore di inizializzazione GUI."""
        mock_mw = MagicMock()
        mock_nav = mock_mw.navigation_controller

        # Setup PageIndex mocks to match integers used in code
        with patch("src.gui.main_window.page_index.PageIndex") as MockPageIndex:
            # Configura gli attributi come interi
            MockPageIndex.DASHBOARD = 0
            MockPageIndex.AUTOMAZIONI = 1
            MockPageIndex.LYRA = 2
            MockPageIndex.TIMBRATURE = 3
            MockPageIndex.STRUMENTALE = 4
            MockPageIndex.DATAEASE = 5
            MockPageIndex.ANAGRAFICHE = 6
            MockPageIndex.SETTINGS = 7
            MockPageIndex.DIPENDENTI = 11  # Match source code

            # Esegui generatore
            gen = AppInitializer.init_generator(mock_mw)

            steps = []
            for name, prog in gen:
                steps.append((name, prog))

            # Verifiche
            assert len(steps) > 5
            assert steps[-1][1] == 100  # Ultimo step 100%

            # Verifica chiamate ai pannelli
            # Ci aspettiamo chiamate a get_panel per ogni indice nella lista tasks
            expected_indices = [0, 1, 2, 3, 4, 5, 6, 7, 11]
            for idx in expected_indices:
                mock_nav.get_panel.assert_any_call(idx)

    def test_init_generator_panel_error(self):
        """Test resilienza generatore se un pannello fallisce."""
        mock_mw = MagicMock()
        mock_nav = mock_mw.navigation_controller
        # Simula errore su caricamento pannello
        mock_nav.get_panel.side_effect = Exception("Panel Load Error")

        with patch("src.gui.main_window.page_index.PageIndex") as MockPageIndex:
            MockPageIndex.DASHBOARD = 0
            # ... altri ...

            gen = AppInitializer.init_generator(mock_mw)

            # Non deve sollevare eccezioni, deve loggare e continuare
            for _ in gen:
                pass

            # Se siamo arrivati qui senza crash, test passato

    @patch("src.core.logging.configure_logging")
    def test_setup_logging_success(self, mock_conf):
        """Test configurazione logging."""
        AppInitializer._setup_logging()
        mock_conf.assert_called_once()

    @patch("src.core.logging.configure_logging", side_effect=Exception("Log Fail"))
    @patch("logging.basicConfig")
    def test_setup_logging_fallback(self, mock_basic, mock_conf):
        """Test fallback logging base su errore."""
        AppInitializer._setup_logging()
        mock_basic.assert_called_once()

    @patch("src.gui.styles.apply_theme")
    def test_setup_app_style(self, mock_theme, mock_qapp):
        """Test configurazione stile app."""
        with patch("src.core.version.__version__", "1.0.0"):
            AppInitializer.setup_app_style(mock_qapp)

            assert mock_qapp.applicationName() == "SyncroJob"
            assert mock_qapp.applicationVersion() == "1.0.0"
            mock_theme.assert_called_with(mock_qapp, "light")
