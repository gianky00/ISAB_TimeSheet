from unittest.mock import patch, MagicMock
import pytest
from PyQt6.QtWidgets import QApplication

from src.gui.main_window.main import MainWindow
from src.gui.main_window.page_index import PageIndex

class TestMainWindow:
    @pytest.fixture
    def app(self, qapp):
        return qapp

    @patch("src.gui.main_window.main.QTimer.singleShot")
    @patch("src.gui.main_window.main.ServiceController")
    @patch("src.gui.main_window.main.LyraSentinel")
    @patch("src.gui.main_window.main.config_manager.load_config")
    @patch("src.gui.main_window.main.apply_theme")
    def test_init(self, mock_theme, mock_conf, mock_sentinel, mock_service, mock_timer, app, qtbot):
        mock_conf.return_value = {}
        window = MainWindow()
        qtbot.addWidget(window)

        assert "SyncroJob" in window.windowTitle()
        assert window.page_stack.count() >= 13
        assert window.sidebar.btn_home.isChecked()

    def test_navigation(self, app, qtbot):
        with (
            patch("src.gui.main_window.main.QTimer.singleShot"),
            patch("src.gui.main_window.main.ServiceController"),
            patch("src.gui.main_window.main.LyraSentinel"),
            patch("src.gui.panels.contabilita_panel.ContabilitaManager"),
            patch("src.gui.main_window.main.config_manager.load_config", return_value={}),
        ):
            window = MainWindow()
            qtbot.addWidget(window)
            QApplication.processEvents()

            # Navigazione Automazioni
            window.navigation_controller.navigate_to(PageIndex.AUTOMAZIONI)
            qtbot.waitUntil(lambda: window.page_stack.currentIndex() == PageIndex.AUTOMAZIONI, timeout=2000)
            
            # Ritorno alla Home
            window.navigation_controller.navigate_to(PageIndex.DASHBOARD)
            qtbot.waitUntil(lambda: window.page_stack.currentIndex() == PageIndex.DASHBOARD, timeout=2000)
            assert window.sidebar.btn_home.isChecked()

    def test_navigate_to_panel(self, app, qtbot):
        """Test deep link navigation naming matching the runner expectation."""
        with (
            patch("src.gui.main_window.main.QTimer.singleShot"),
            patch("src.gui.main_window.main.ServiceController"),
            patch("src.gui.main_window.main.LyraSentinel"),
            patch("src.gui.main_window.main.config_manager.load_config", return_value={}),
        ):
            window = MainWindow()
            qtbot.addWidget(window)
            QApplication.processEvents()

            # Deep link: 'timbrature' porta a Automazioni (1) -> Fornitori (0) -> Timbrature (2)
            window.navigation_controller.navigate_to_panel("timbrature")
            qtbot.waitUntil(lambda: window.page_stack.currentIndex() == PageIndex.AUTOMAZIONI, timeout=2000)
            
            # Recupera il widget delle automazioni
            automazioni_panel = window.navigation_controller.get_panel(PageIndex.AUTOMAZIONI)
            
            # Verifica tab Fornitori attivo
            assert automazioni_panel.main_tabs.currentIndex() == 0
            # Verifica tab Timbrature (bot) attivo
            assert automazioni_panel.tab_fornitori.currentIndex() == 2
