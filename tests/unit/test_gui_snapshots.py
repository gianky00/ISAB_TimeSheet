import pytest
from PyQt6.QtWidgets import QApplication

# Import panels from new modular locations
from src.gui.panels.contabilita_panel import ContabilitaPanel
from src.gui.panels.scarico_ore_panel import ScaricoOrePanel


class TestGuiSnapshots:
    @pytest.fixture
    def mock_deps(self, mocker):  # noqa: ANN001
        # Mock per ContabilitaManager (evita chiamate DB in refresh_tabs)
        mocker.patch(
            "src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2024, 2025]
        )

        # Mock per ScaricoOreController (evita inizializzazione database reale)
        mocker.patch("src.gui.panels.scarico_ore_panel.ScaricoOreController")

        # Mock per config_manager
        mocker.patch("src.core.config_manager.get_config_value", return_value=[])
        mocker.patch("src.core.config_manager.load_config", return_value={})

    @pytest.mark.skip(reason="Incompatibilità rendering AnimatedTabWidget in ambiente headless Windows.")
    def test_contabilita_panel_structure(self, qtbot, mock_deps):  # noqa: ANN001
        """
        Snapshot-like test: verify ContabilitaPanel has the expected structure
        (TabWidget, Buttons) without actually running data logic.
        """
        panel = ContabilitaPanel()
        qtbot.addWidget(panel)
        QApplication.processEvents()

        # Check Tabs (Preventivi, Giornaliere, Attività, Certificati, KPI)
        assert panel.main_tabs.count() >= 5  # noqa: PLR2004
        assert panel.search_input is not None
        assert panel.update_btn is not None

    @pytest.mark.skip(reason="Incompatibilità rendering in ambiente headless Windows.")
    def test_scarico_ore_panel_instantiation(self, qtbot, mock_deps):  # noqa: ANN001
        """Verify ScaricoOrePanel can be instantiated with its new controller-based structure."""
        panel = ScaricoOrePanel()
        qtbot.addWidget(panel)
        QApplication.processEvents()

        # In V9.0: table_view è presente, search_input è in filters
        assert panel.table_view is not None
        assert panel.filters.search_input is not None
        assert panel.controller is not None
