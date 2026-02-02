import pytest
from unittest.mock import MagicMock, patch
from PyQt6.QtCore import QObject
from src.gui.controllers.navigation_controller import NavigationController

class MockMainWindow(QObject):
    def __init__(self):
        super().__init__()
        self.page_stack = MagicMock()
        self.sidebar = MagicMock()
        self._current_page_index = -1
        # Placeholder attributes for panels
        self._panel_initialized_0 = False
        self.dashboard_panel = None
        
        self.settings_panel = None

@pytest.fixture
def mock_mw(qapp):
    return MockMainWindow()

@pytest.fixture
def nav_controller(mock_mw):
    return NavigationController(mock_mw)

class TestNavigationControllerRobust:

    def test_get_panel_already_initialized(self, nav_controller, mock_mw):
        """Test recupero pannello già inizializzato."""
        mock_mw._panel_initialized_0 = True
        existing_panel = MagicMock()
        mock_mw.page_stack.widget.return_value = existing_panel
        
        panel = nav_controller.get_panel(0)
        
        assert panel == existing_panel
        nav_controller.mw.page_stack.widget.assert_called_with(0)

    def test_get_panel_lazy_load_success(self, nav_controller, mock_mw):
        """Test lazy loading pannello."""
        mock_mw._panel_initialized_0 = False
        placeholder = MagicMock()
        mock_mw.page_stack.widget.return_value = placeholder
        
        new_panel = MagicMock()
        
        # Mock creator
        with patch.object(nav_controller, "_create_dashboard", return_value=new_panel):
            panel = nav_controller.get_panel(0)
            
            assert panel == new_panel
            # Verifica sostituzione widget
            mock_mw.page_stack.removeWidget.assert_called_with(placeholder)
            mock_mw.page_stack.insertWidget.assert_called_with(0, new_panel)
            assert getattr(mock_mw, "_panel_initialized_0") is True

    def test_get_panel_creation_error(self, nav_controller, mock_mw):
        """Test gestione errore creazione pannello."""
        mock_mw._panel_initialized_0 = False
        
        with patch.object(nav_controller, "_create_dashboard", side_effect=Exception("Boom")):
            with patch("src.gui.controllers.navigation_controller.QMessageBox.critical") as mock_box:
                panel = nav_controller.get_panel(0)
                
                # Ritorna il placeholder originale (o quello che widget(0) ritorna)
                assert panel == mock_mw.page_stack.widget.return_value
                mock_box.assert_called()

    def test_navigate_to_same_page(self, nav_controller, mock_mw):
        """Test navigazione stessa pagina."""
        mock_mw._current_page_index = 0
        
        nav_controller.navigate_to(0)
        
        # Non deve fare nulla tranne aggiornare sidebar
        mock_mw.page_stack.setCurrentIndex.assert_not_called()
        mock_mw.sidebar.set_active_button.assert_called_with(0)

    def test_navigate_to_settings_unsaved_cancel(self, nav_controller, mock_mw):
        """Test navigazione da settings non salvati (annulla)."""
        mock_mw._current_page_index = 7 # Settings
        mock_mw.settings_panel = MagicMock()
        mock_mw.settings_panel.has_unsaved_changes.return_value = True
        mock_mw.settings_panel.prompt_save_if_needed.return_value = False # Cancel
        
        nav_controller.navigate_to(0)
        
        # Rimane su settings
        assert mock_mw._current_page_index == 7
        mock_mw.page_stack.setCurrentIndex.assert_not_called()

    def test_navigate_to_settings_unsaved_proceed(self, nav_controller, mock_mw):
        """Test navigazione da settings non salvati (procedi)."""
        mock_mw._current_page_index = 7 # Settings
        mock_mw.settings_panel = MagicMock()
        mock_mw.settings_panel.has_unsaved_changes.return_value = True
        mock_mw.settings_panel.prompt_save_if_needed.return_value = True # Save/Discard -> True
        
        # Mock get_panel per target
        with patch.object(nav_controller, "get_panel"):
            nav_controller.navigate_to(0)
            
            assert mock_mw._current_page_index == 0
            mock_mw.page_stack.setCurrentIndex.assert_called_with(0)

    def test_navigate_to_panel_bot(self, nav_controller, mock_mw):
        """Test navigazione verso pannello bot annidato."""
        mock_mw.automazioni_widget = MagicMock()
        
        # Mock get_panel per automazioni (idx 1)
        with patch.object(nav_controller, "get_panel"):
            nav_controller.navigate_to_panel("dettagli_oda") # Mapped to (0, 0) -> Auto index 1, sub 0
            
            assert mock_mw._current_page_index == 1
            mock_mw.automazioni_widget.set_active_tab.assert_called_with(0, 0)

    def test_navigate_to_panel_db(self, nav_controller, mock_mw):
        """Test navigazione verso pannello DB."""
        with patch.object(nav_controller, "get_panel"):
            nav_controller.navigate_to_panel("db_timbrature") # Mapped to 3
            
            assert mock_mw._current_page_index == 3

    def test_try_connect_signals(self, nav_controller, mock_mw):
        """Test connessione segnali lazy."""
        # Setup scenario: both panels exist, not connected
        mock_mw.timbrature_bot_panel = MagicMock()
        mock_mw.timbrature_db_panel = MagicMock()
        mock_mw._timbrature_signals_connected = False
        
        nav_controller._try_connect_signals()
        
        mock_mw.timbrature_bot_panel.data_updated.connect.assert_called_with(
            mock_mw.timbrature_db_panel.refresh_data
        )
        assert mock_mw._timbrature_signals_connected is True
