import pytest
from unittest.mock import MagicMock, patch
from PyQt6.QtWidgets import QApplication

from src.gui.panels.contabilita_panel import ContabilitaPanel
from src.gui.panels.dashboard_panel import DashboardPanel

class TestSprintCGUIDeep:
    """Test suite di integrazione profonda per la GUI V9.0."""

    @pytest.mark.skip(reason="Incompatibilità rendering AnimatedTabWidget in ambiente headless Windows V9.0.")
    def test_contabilita_tab_synchronization(self, qtbot, mocker):
        """Verifica che il refresh del panel si propaghi ai tab interni."""
        mocker.patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2024])
        panel = ContabilitaPanel()
        qtbot.addWidget(panel)
        
        # Simula refresh
        panel._safe_refresh_tabs()
        assert panel.main_tabs.count() > 0

    @pytest.mark.skip(reason="Incompatibilità rendering in ambiente headless Windows V9.0.")
    def test_dashboard_widget_layout(self, qtbot, mocker):
        """Verifica la corretta disposizione dei widget nella Dashboard."""
        mocker.patch("src.core.stats_manager.StatsManager.get_all_stats", return_value={})
        panel = DashboardPanel()
        qtbot.addWidget(panel)
        assert panel.activity_feed is not None
