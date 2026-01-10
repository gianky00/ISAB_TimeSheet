import pytest
from unittest.mock import MagicMock, patch

# Import panels (these imports assume the file structure is correct)
from src.gui.contabilita_panel import ContabilitaPanel
from src.gui.scarico_ore_panel import ScaricoOrePanel

class TestGuiSnapshots:

    @pytest.fixture
    def mock_deps(self, mock_ui_dependencies):
        return mock_ui_dependencies

    def test_contabilita_panel_structure(self, qtbot, mock_deps):
        """
        Snapshot-like test: verify ContabilitaPanel has the expected structure
        (TabWidget, Buttons) without actually running data logic.
        """
        # We need to mock get_config_value or similar if the panel uses it in init
        with patch("src.core.config_manager.get_config_value", return_value=[]):
            panel = ContabilitaPanel()
            qtbot.addWidget(panel)
            
            # Check Tabs
            # ContabilitaPanel uses a QTabWidget named 'main_tabs'
            assert panel.main_tabs.count() >= 3 # Dati, Preventivi, Riepilogo, etc.
            
    def test_scarico_ore_panel_instantiation(self, qtbot, mock_deps):
        """Verify ScaricoOrePanel can be instantiated."""
        with patch("src.core.config_manager.get_config_value", return_value=[]):
            panel = ScaricoOrePanel()
            qtbot.addWidget(panel)
            
            # Check title or label existence
            # ScaricoOrePanel has a table_view
            assert panel.table_view is not None
            # And a search input
            assert panel.search_input is not None
