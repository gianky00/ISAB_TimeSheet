import pytest
from unittest.mock import MagicMock, patch
from src.gui.contabilita_panel import ContabilitaPanel

@patch('src.gui.contabilita_kpi_panel.ContabilitaKPIPanel', new_callable=MagicMock)
@patch('src.gui.contabilita_panel.ContabilitaManager')
class TestContabilitaExtra:

    @pytest.fixture
    def app(self, qapp):
        return qapp

    def test_contabilita_panel_init(self, mock_manager, mock_kpi_panel, app, qtbot):
        # Mock for ContabilitaPanel's direct calls
        mock_manager.get_available_years.return_value = [2023, 2024]
        mock_manager.get_data_by_year.return_value = []
        mock_manager.get_giornaliere_by_year.return_value = []
        mock_manager.get_attivita_programmate_data.return_value = []
        mock_manager.get_certificati_campione_data.return_value = []

        panel = ContabilitaPanel()
        qtbot.addWidget(panel)
        
        assert panel is not None
        mock_kpi_panel.assert_called_once()
        assert panel.main_tabs.count() >= 5
        assert panel.kpi_panel is not None
        assert panel.tab_preventivi is not None
        assert panel.tab_giornaliere is not None
        assert panel.tab_attivita is not None
        assert panel.tab_certificati is not None

    def test_contabilita_panel_tab_switch(self, mock_manager, mock_kpi_panel, app, qtbot):
        # Mocks are already applied by the class-level decorators
        mock_manager.get_available_years.return_value = [2023, 2024]
        mock_manager.get_data_by_year.return_value = []
        mock_manager.get_giornaliere_by_year.return_value = []
        mock_manager.get_attivita_programmate_data.return_value = []
        mock_manager.get_certificati_campione_data.return_value = []

        panel = ContabilitaPanel()
        qtbot.addWidget(panel)
        
        # Switch to "Giornaliere" (Index 1)
        panel.main_tabs.setCurrentIndex(1)
        assert panel.main_tabs.currentWidget() == panel.tab_giornaliere
        
        # Switch to "Attività Programmate" (Index 2)
        panel.main_tabs.setCurrentIndex(2)
        assert panel.main_tabs.currentWidget() == panel.tab_attivita

        # Switch to "KPI" (Index 4)
        panel.main_tabs.setCurrentIndex(4)
        assert panel.main_tabs.currentWidget() == panel.kpi_panel