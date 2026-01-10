from unittest.mock import patch, MagicMock

import pytest

from src.gui.main_window import MainWindow, PageIndex


class TestMainWindow:

    @pytest.fixture
    def app(self, qapp):
        return qapp

    @patch("src.gui.main_window.ServiceController")
    @patch("src.gui.main_window.LyraSentinel")
    @patch("src.gui.main_window.config_manager.load_config")
    @patch("src.gui.main_window.apply_theme")
    def test_init(self, mock_theme, mock_conf, mock_sentinel, mock_service, app, qtbot):
        mock_conf.return_value = {}

        window = MainWindow()
        qtbot.addWidget(window)

        assert window.windowTitle() == "SyncroJob"
        assert window.page_stack.count() >= 6
        assert window.sidebar.btn_home.isChecked()

    def test_navigation(self, app, qtbot):
        # Mock internal components to avoid side effects
        with patch("src.gui.main_window.ServiceController"), patch("src.gui.main_window.LyraSentinel"), patch(
            "src.gui.main_window.config_manager.load_config", return_value={}
        ):

            window = MainWindow()
            qtbot.addWidget(window)

            # Click Automazioni
            window.sidebar.btn_automazioni.click()
            assert window.page_stack.currentIndex() == PageIndex.AUTOMAZIONI
            assert window.sidebar.btn_automazioni.isChecked()

            # Click Database
            window.sidebar.btn_database.click()
            assert window.page_stack.currentIndex() == PageIndex.DATABASE
            assert window.sidebar.btn_database.isChecked()

    def test_navigate_to_panel(self, app, qtbot):
        with patch("src.gui.main_window.ServiceController"), patch("src.gui.main_window.LyraSentinel"), patch(
            "src.gui.main_window.config_manager.load_config", return_value={}
        ):

            window = MainWindow()
            qtbot.addWidget(window)

            # Force preload to ensure panels exist
            window._preload_all_panels()

            # Test deep link navigation
            window.navigate_to_panel("timbrature")  # Should go to Automazioni -> Timbrature (Tab 2)
            assert window.page_stack.currentIndex() == PageIndex.AUTOMAZIONI
            
            # Since _preload_all_panels was called, the panels should be initialized
            # Automazioni panel is at index 1
            automazioni_panel = window.navigation_controller.get_panel(PageIndex.AUTOMAZIONI)
            assert automazioni_panel.currentIndex() == 0 # Portale Fornitori tab
            
            # Sub-tab check: Timbrature is at index 2 in Portale Fornitori
            portale_fornitori_tab = automazioni_panel.widget(0)
            assert portale_fornitori_tab.currentIndex() == 2