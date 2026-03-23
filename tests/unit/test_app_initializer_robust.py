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
        return QApplication([]) if not QApplication.instance() else QApplication.instance()

    @patch("src.core.app_initializer.AppInitializer._setup_logging")
    @patch("src.core.database.db_manager.init_db")
    @patch("src.core.license_validator.get_detailed_license_status")
    @patch("src.core.license_updater.run_update")
    def test_initialize_core_success(self, mock_update, mock_status, mock_db, mock_log):
        """Test inizializzazione core completa con successo."""
        from src.core.license_validator import LicenseStatus  # noqa: PLC0415

        # Simula licenza valida
        mock_status.return_value = (LicenseStatus.VALID, "Valid")

        result = AppInitializer.initialize_core()

        assert result is True
        assert AppInitializer._core_initialized is True
        mock_log.assert_called_once()
        mock_db.assert_called_once()
        # run_update viene ora chiamato SEMPRE all'inizio
        mock_update.assert_called_once()

    @patch("src.core.app_initializer.AppInitializer._setup_logging")
    @patch("src.core.database.db_manager.init_db")
    @patch("src.core.license_validator.get_detailed_license_status")
    @patch("src.core.license_updater.run_update")
    def test_initialize_core_license_invalid(self, mock_update, mock_status, mock_db, mock_log):
        """Test blocco inizializzazione se licenza invalida."""
        from src.core.license_validator import LicenseStatus  # noqa: PLC0415

        # Simula licenza NON valida
        mock_status.return_value = (LicenseStatus.EXPIRED, "Expired")

        # Mi aspetto eccezione bloccante
        with pytest.raises(Exception, match="Licenza non valida"):
            AppInitializer.initialize_core()

        mock_update.assert_called_once()

    @patch("src.core.app_initializer.logger")
    @patch("src.core.database.db_manager.init_db")
    @patch("src.core.license_updater.run_update")
    def test_initialize_core_failure(self, mock_update, mock_db_init, mock_logger):
        """Test gestione errore critico in init core (DB failure)."""
        from src.core.license_validator import LicenseStatus  # noqa: PLC0415

        mock_db_init.side_effect = Exception("DB Error")

        # Patch dependencies to avoid early exit
        with (
            patch(
                "src.core.license_validator.get_detailed_license_status",
                return_value=(LicenseStatus.VALID, "OK"),
            ),
            patch.object(AppInitializer, "_setup_logging"),
        ):
            # Mi aspetto eccezione
            with pytest.raises(Exception, match="DB Error"):
                AppInitializer.initialize_core()

            assert AppInitializer._core_initialized is False
            mock_update.assert_called_once()

    def test_init_generator_flow(self):
        """Test del generatore di inizializzazione GUI."""
        mock_mw = MagicMock()
        mock_nav = mock_mw.navigation_controller

        # Setup PageIndex mocks to match integers used in code
        with patch("src.gui.main_window.page_index.PageIndex") as MockPageIndex:  # noqa: N806
            # Configura gli attributi come interi (Real values from PageIndex)
            MockPageIndex.DASHBOARD = 0
            MockPageIndex.AUTOMAZIONI = 1
            MockPageIndex.TIMBRATURE = 3
            MockPageIndex.STRUMENTALE = 4
            MockPageIndex.DATAEASE = 5
            MockPageIndex.ANAGRAFICHE = 6
            MockPageIndex.SETTINGS = 7
            MockPageIndex.HELP = 8
            MockPageIndex.NOTIFICATIONS = 9
            MockPageIndex.STORICO_ODA = 10
            MockPageIndex.DIPENDENTI = 11

            # Esegui generatore
            gen = AppInitializer.init_generator(mock_mw)

            steps = []
            for name, prog in gen:
                steps.append((name, prog))

            # Verifiche
            assert len(steps) > 5
            assert steps[-1][1] == 100  # Ultimo step 100%

            # Verifica chiamate ai pannelli
            # Ci aspettiamo chiamate a get_panel per ogni indice nella lista tasks di AppInitializer
            expected_indices = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            for idx in expected_indices:
                mock_nav.get_panel.assert_any_call(idx)

    def test_init_generator_panel_error(self):
        """Test resilienza generatore se un pannello fallisce."""
        mock_mw = MagicMock()
        mock_nav = mock_mw.navigation_controller
        # Simula errore su caricamento pannello
        mock_nav.get_panel.side_effect = Exception("Panel Load Error")

        with patch("src.gui.main_window.page_index.PageIndex") as MockPageIndex:  # noqa: N806
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
