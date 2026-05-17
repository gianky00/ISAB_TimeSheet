# ruff: noqa: PLR0913
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtWidgets import QApplication

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
    @patch("src.core.database.backup_manager.DatabaseBackupManager.execute_backup")
    @patch("src.core.app_initializer.get_detailed_license_status")
    @patch("src.core.app_initializer.run_update")
    @patch("src.core.app_initializer.threading.Thread")
    @patch("src.utils.resource_manager.ResourceManager.ensure_automation_driver")
    @patch("src.core.app_initializer.get_hardware_id")
    @patch("src.core.app_initializer.get_available_bots")
    def test_initialize_core_success(
        self,
        mock_bots,
        mock_hwid,
        mock_driver,
        mock_thread,
        mock_update,
        mock_status,
        mock_backup,
        mock_db,
        mock_log,
    ):
        """Test inizializzazione core completa con successo."""
        from src.core.license_validator import LicenseStatus

        # Simulate synchronous thread execution
        def mock_thread_start(*args, **kwargs):
            if mock_thread.call_args:
                thread_kwargs = mock_thread.call_args.kwargs
                if "target" in thread_kwargs:
                    thread_kwargs["target"]()
            return MagicMock()

        mock_thread.return_value.start.side_effect = mock_thread_start

        # Simula licenza valida
        mock_status.return_value = (LicenseStatus.VALID, "Valid")
        mock_bots.return_value = []

        result = AppInitializer.initialize_core()

        assert result is True
        assert AppInitializer._core_initialized is True
        mock_log.assert_called_once()
        mock_db.assert_called_once()
        mock_update.assert_called_once()

    @patch("src.core.app_initializer.AppInitializer._setup_logging")
    @patch("src.core.database.db_manager.init_db")
    @patch("src.core.database.backup_manager.DatabaseBackupManager.execute_backup")
    @patch("src.core.app_initializer.get_detailed_license_status")
    @patch("src.core.app_initializer.run_update")
    @patch("src.core.app_initializer.threading.Thread")
    @patch("src.utils.resource_manager.ResourceManager.ensure_automation_driver")
    @patch("src.core.app_initializer.get_hardware_id")
    @patch("src.core.app_initializer.get_available_bots")
    def test_initialize_core_license_invalid(
        self,
        mock_bots,
        mock_hwid,
        mock_driver,
        mock_thread,
        mock_update,
        mock_status,
        mock_backup,
        mock_db,
        mock_log,
    ):
        """Test blocco inizializzazione se licenza invalida."""
        from src.core.license_validator import LicenseStatus

        def mock_thread_start(*args, **kwargs):
            if mock_thread.call_args:
                thread_kwargs = mock_thread.call_args.kwargs
                if "target" in thread_kwargs:
                    thread_kwargs["target"]()
            return MagicMock()

        mock_thread.return_value.start.side_effect = mock_thread_start

        # Simula licenza NON valida
        mock_status.return_value = (LicenseStatus.EXPIRED, "Expired")
        mock_bots.return_value = []

        # Mi aspetto eccezione bloccante
        with pytest.raises(Exception, match="Licenza non valida"):
            AppInitializer.initialize_core()

        mock_update.assert_called_once()

    @patch("src.core.app_initializer.logger")
    @patch("src.core.database.db_manager.init_db")
    @patch("src.core.database.backup_manager.DatabaseBackupManager.execute_backup")
    @patch("src.core.app_initializer.run_update")
    @patch("src.core.app_initializer.threading.Thread")
    @patch("src.utils.resource_manager.ResourceManager.ensure_automation_driver")
    @patch("src.core.app_initializer.get_hardware_id")
    @patch("src.core.app_initializer.get_available_bots")
    def test_initialize_core_failure(
        self,
        mock_bots,
        mock_hwid,
        mock_driver,
        mock_thread,
        mock_update,
        mock_backup,
        mock_db_init,
        mock_logger,
    ):
        """Test gestione errore critico in init core (DB failure)."""
        from src.core.license_validator import LicenseStatus

        def mock_thread_start(*args, **kwargs):
            if mock_thread.call_args:
                thread_kwargs = mock_thread.call_args.kwargs
                if "target" in thread_kwargs:
                    thread_kwargs["target"]()
            return MagicMock()

        mock_thread.return_value.start.side_effect = mock_thread_start

        mock_db_init.side_effect = Exception("DB Error")
        mock_bots.return_value = []

        # Patch dependencies to avoid early exit
        with (
            patch(
                "src.core.app_initializer.get_detailed_license_status",
                return_value=(LicenseStatus.VALID, "OK"),
            ),
            patch.object(AppInitializer, "_setup_logging"),
            patch("src.utils.resource_manager.ResourceManager.ensure_automation_driver"),
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
        with patch("src.gui.main_window.page_index.PageIndex") as mock_page_index:
            # Configura gli attributi come interi (Real values from PageIndex)
            mock_page_index.DASHBOARD = 0
            mock_page_index.AUTOMAZIONI = 1
            mock_page_index.TIMBRATURE = 3
            mock_page_index.STRUMENTALE = 4
            mock_page_index.DATAEASE = 5
            mock_page_index.ANAGRAFICHE = 6
            mock_page_index.SETTINGS = 7
            mock_page_index.HELP = 8
            mock_page_index.NOTIFICATIONS = 9
            mock_page_index.STORICO_ODA = 10
            mock_page_index.DIPENDENTI = 11

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

        with patch("src.gui.main_window.page_index.PageIndex") as mock_page_index:
            mock_page_index.DASHBOARD = 0
            # ... altri ...

            gen = AppInitializer.init_generator(mock_mw)

            # Non deve sollevare eccezioni, deve loggare e continuare
            for _ in gen:
                pass

            # Se siamo arrivati qui senza crash, test passato

    @patch("src.core.app_initializer.configure_logging")
    def test_setup_logging_success(self, mock_conf):
        """Test configurazione logging."""
        AppInitializer._setup_logging()
        mock_conf.assert_called_once()

    @patch("src.core.app_initializer.configure_logging", side_effect=Exception("Log Fail"))
    @patch("logging.basicConfig")
    def test_setup_logging_fallback(self, mock_basic, mock_conf):
        """Test fallback logging base su errore."""
        AppInitializer._setup_logging()
        mock_basic.assert_called_once()
