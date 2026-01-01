import pytest
from PyQt6.QtWidgets import QMainWindow
from unittest.mock import MagicMock, patch
from src.gui.main_window import MainWindow

class TestMainWindow:

    @pytest.fixture
    def app(self, qapp):
        return qapp

    @patch('src.gui.main_window.check_for_updates')
    @patch('src.gui.main_window.LyraSentinel')
    @patch('src.gui.main_window.config_manager.load_config')
    @patch('src.gui.main_window.apply_theme')
    def test_init(self, mock_theme, mock_conf, mock_sentinel, mock_update, app, qtbot):
        mock_conf.return_value = {}
        
        window = MainWindow()
        qtbot.addWidget(window)
        
        assert window.windowTitle() == "Bot TS - Timesheet Manager"
        assert window.page_stack.count() >= 6
        assert window.btn_home.isChecked()

    def test_navigation(self, app, qtbot):
        # Mock internal components to avoid side effects
        with patch('src.gui.main_window.check_for_updates'), \
             patch('src.gui.main_window.LyraSentinel'), \
             patch('src.gui.main_window.config_manager.load_config', return_value={}):
             
            window = MainWindow()
            qtbot.addWidget(window)
            
            # Click Automazioni
            window.btn_automazioni.click()
            assert window.page_stack.currentIndex() == 1
            assert window.btn_automazioni.isChecked()
            
            # Click Database
            window.btn_database.click()
            assert window.page_stack.currentIndex() == 3
            assert window.btn_database.isChecked()

    def test_navigate_to_panel(self, app, qtbot):
        with patch('src.gui.main_window.check_for_updates'), \
             patch('src.gui.main_window.LyraSentinel'), \
             patch('src.gui.main_window.config_manager.load_config', return_value={}):
             
            window = MainWindow()
            qtbot.addWidget(window)
            
            # Test deep link navigation
            window.navigate_to_panel("timbrature") # Should go to Automazioni -> Timbrature (Tab 2)
            assert window.page_stack.currentIndex() == 1
            # Main tab 0 (Portale Fornitori) -> subtab 2 (Timbrature)
            assert window.automazioni_widget.currentIndex() == 0
            assert window.tab_fornitori.currentIndex() == 2
