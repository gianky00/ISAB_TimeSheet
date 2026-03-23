from unittest.mock import MagicMock

from src.core.app_initializer import AppInitializer
from src.gui.main_window.page_index import PageIndex


class TestAppInitializerDeep:
    """Test approfonditi sul generatore di avvio e logiche di idempotenza."""

    def test_initialize_core_idempotency(self, mocker):  # noqa: ANN001
        """Verifica che chiamate successive a initialize_core non rieseguano i compiti."""
        # Reset state
        AppInitializer._core_initialized = True

        m_log = mocker.patch("src.core.app_initializer.AppInitializer._setup_logging")
        m_db = mocker.patch("src.core.database.db_manager.init_db")

        # Should return immediately because _core_initialized is True
        assert AppInitializer.initialize_core() is True
        m_log.assert_not_called()
        m_db.assert_not_called()

    def test_init_generator_full_flow(self, mocker):  # noqa: ANN001
        """Verifica il flusso completo del generatore di inizializzazione GUI."""
        # Mock main window and navigation controller
        mock_mw = MagicMock()
        mock_nav = MagicMock()
        mock_mw.navigation_controller = mock_nav

        # Mock config_manager
        mocker.patch("src.core.config_manager.load_config", return_value={})
        mocker.patch("src.core.config_manager.set_config_value")

        # Create generator
        gen = AppInitializer.init_generator(mock_mw)

        results = list(gen)

        # Verify yields
        assert len(results) > 0
        assert any("Dashboard" in msg for msg, prog in results)
        assert any(prog == 100 for msg, prog in results)  # noqa: PLR2004

        # Verify that get_panel was called for the expected indices
        # We check some key indices from PageIndex
        mock_nav.get_panel.assert_any_call(PageIndex.DASHBOARD)
        mock_nav.get_panel.assert_any_call(PageIndex.SETTINGS)

    def test_init_generator_panel_failure_resilience(self, mocker):  # noqa: ANN001
        """Verifica che il generatore prosegua anche se un pannello crasha."""
        mock_mw = MagicMock()
        mock_nav = MagicMock()
        mock_mw.navigation_controller = mock_nav

        # Simulate failure for DASHBOARD
        def side_effect(idx):  # noqa: ANN001, ANN202
            if idx == PageIndex.DASHBOARD:
                raise Exception("Dashboard Crash")  # noqa: TRY002, TRY003
            return MagicMock()

        mock_nav.get_panel.side_effect = side_effect

        mocker.patch("src.core.config_manager.load_config", return_value={})

        gen = AppInitializer.init_generator(mock_mw)
        results = list(gen)

        # Verify we still reached the end
        assert any(prog == 100 for msg, prog in results)  # noqa: PLR2004
        # Verify other panels were still attempted
        mock_nav.get_panel.assert_any_call(PageIndex.SETTINGS)
