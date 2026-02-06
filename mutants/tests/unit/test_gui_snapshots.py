from unittest.mock import patch

import pytest

# Import panels from new modular locations
from src.gui.panels.contabilita_panel import ContabilitaPanel
from src.gui.panels.scarico_ore_panel import ScaricoOrePanel


class TestGuiSnapshots:
    @pytest.fixture
    def mock_deps(self, mock_ui_dependencies):
        return mock_ui_dependencies

    def test_contabilita_panel_structure(self, qtbot, mock_deps):
        """
        Snapshot-like test: verify ContabilitaPanel has the expected structure
        (TabWidget, Buttons) without actually running data logic.
        """
        with patch("src.core.config_manager.get_config_value", return_value=[]):
            panel = ContabilitaPanel()
            qtbot.addWidget(panel)

            # Check Tabs
            assert panel.main_tabs.count() >= 3

    def test_scarico_ore_panel_instantiation(self, qtbot, mock_deps):
        """Verify ScaricoOrePanel can be instantiated."""
        with patch("src.core.config_manager.get_config_value", return_value=[]):
            panel = ScaricoOrePanel()
            qtbot.addWidget(panel)

            # Check title or label existence
            assert panel.table_view is not None
            assert panel.search_input is not None
