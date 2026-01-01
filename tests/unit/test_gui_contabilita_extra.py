import pytest
from unittest.mock import MagicMock, patch
from src.gui.contabilita_panel import ContabilitaPanel

class TestContabilitaExtra:

    @pytest.fixture
    def app(self, qapp):
        return qapp

    # Patch ContabilitaManager, not db_manager directly in the panel
    @patch('src.gui.contabilita_panel.ContabilitaManager') 
    def test_contabilita_panel_init(self, mock_manager, app, qtbot):
        # Mock manager methods that are called during init or refresh
        mock_manager.get_available_years.return_value = [2023, 2024] # Mock years
        mock_manager.get_data_by_year.return_value = [] # Mock data return for prevent crash
        mock_manager.get_giornaliere_by_year.return_value = []
        mock_manager.get_attivita_programmate_data.return_value = []
        mock_manager.get_certificati_campione_data.return_value = []
        
        panel = ContabilitaPanel()
        qtbot.addWidget(panel)
        
        assert panel is not None
        # Use main_tabs attribute which is created in setup_ui
        assert panel.main_tabs.count() >= 4
        # Check sub-tab widgets are created (may be None if not populated yet, but exist)
        assert panel.tab_preventivi is not None
        assert panel.tab_giornaliere is not None
        assert panel.tab_attivita is not None
        assert panel.tab_certificati is not None

    def test_contabilita_panel_tab_switch(self, app, qtbot):
        # Patch ContabilitaManager and db_manager if used directly
        with patch('src.gui.contabilita_panel.ContabilitaManager') as mock_manager:
            # Mock methods that would be called on tab switch or init
            mock_manager.get_available_years.return_value = [2023, 2024]
            mock_manager.get_data_by_year.return_value = []
            mock_manager.get_giornaliere_by_year.return_value = []
            mock_manager.get_attivita_programmate_data.return_value = []
            mock_manager.get_certificati_campione_data.return_value = []

            panel = ContabilitaPanel()
            qtbot.addWidget(panel)
            
            # Trigger UI setup which initializes tabs
            panel._setup_ui() # Ensure tabs are set up
            
            # Switch to "Giornaliere" (Index 1)
            panel.main_tabs.setCurrentIndex(1)
            assert panel.main_tabs.currentWidget() == panel.tab_giornaliere
            
            # Switch to "Attività Programmate" (Index 2)
            panel.main_tabs.setCurrentIndex(2)
            assert panel.main_tabs.currentWidget() == panel.tab_attivita
