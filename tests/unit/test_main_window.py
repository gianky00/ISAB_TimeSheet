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

            # In the new implementation, we use _preload_background
            # For the test, we can trigger it or just ensure panels are loaded
            window._preload_background()
            
            # Since _preload_background uses QTimer, we might need to wait or 
            # manually initialize what we need for the deep link test
            window.navigation_controller.get_panel(PageIndex.AUTOMAZIONI)

            # Test deep link navigation
            window.navigate_to_panel("timbrature")  # Should go to Automazioni -> Timbrature (Tab 2)
            assert window.page_stack.currentIndex() == PageIndex.AUTOMAZIONI
            
            # Automazioni panel is at index 1
            automazioni_panel = window.navigation_controller.get_panel(PageIndex.AUTOMAZIONI)
            # Timbrature is at index 2 in Portale Fornitori (tab 0 of Automazioni)
            portale_fornitori_tab = automazioni_panel.widget(0)
            assert portale_fornitori_tab.currentIndex() == 2