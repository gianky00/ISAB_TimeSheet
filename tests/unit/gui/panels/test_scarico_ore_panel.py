from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QObject, Signal

from src.gui.panels.scarico_ore_panel import ScaricoOrePanel


class MockController(QObject):
    status_changed = Signal(str)
    update_finished = Signal(bool, str)

    def __init__(self):
        super().__init__()
        self.format_number = MagicMock(return_value="10,00")
        self.start_import = MagicMock()


class TestScaricoOrePanel:
    @pytest.fixture
    def controller(self):
        return MockController()

    @pytest.fixture
    def panel(self, controller, qtbot):
        with (
            patch("src.gui.panels.scarico_ore_panel.config_manager.load_config", return_value={}),
            patch(
                "src.gui.panels.scarico_ore_panel.ContabilitaManager.get_scarico_ore_data", return_value=[]
            ),
        ):
            p = ScaricoOrePanel(controller)
            qtbot.addWidget(p)
            return p

    def test_initialization(self, panel):
        assert panel.controller is not None
        assert panel.filters.search_input.placeholderText() != ""

    def test_on_update_finished_success(self, panel, controller):
        with patch.object(panel, "_load_data"):
            panel._on_update_finished(True, "Successo!")
            assert "Successo!" in panel.filters.status_label.text()
            assert panel.filters.update_btn.isEnabled()

    def test_on_update_finished_error(self, panel, controller):
        with patch("src.gui.panels.scarico_ore_panel.ConfirmationDialog.show_error") as mock_err:
            panel._on_update_finished(False, "Errore fatale")
            assert "Errore" in panel.filters.status_label.text()
            assert mock_err.called

    def test_start_update_missing_path(self, panel):
        with (
            patch(
                "src.gui.panels.scarico_ore_panel.config_manager.load_config",
                return_value={"dataease_path": ""},
            ),
            patch("src.gui.panels.scarico_ore_panel.ConfirmationDialog.show_warning") as mock_warn,
        ):
            panel._start_update()
            assert mock_warn.called

    def test_start_update_success(self, panel, controller):
        with patch(
            "src.gui.panels.scarico_ore_panel.config_manager.load_config",
            return_value={"dataease_path": "/some/path"},
        ):
            panel._start_update()
            assert controller.start_import.called

    def test_set_search_query(self, panel):
        panel.set_search_query("FilterText")
        assert panel.filters.search_input.text() == "FilterText"

    def test_on_cache_loaded_ui_transition(self, panel, qtbot):
        """Verifica la transizione UI (shimmer -> tabella) al caricamento dei dati."""
        # Setup: Inizialmente siamo in loading
        panel._set_ui_loading(True)
        # Verifica interna dei flag di visibilità (più robusta)
        assert panel.table_view.isHidden()
        assert not panel.shimmer.isHidden()

        # Simulazione fine caricamento
        panel._on_cache_loaded()

        # Attesa esplicita della transizione UI
        def transition_complete():
            return not panel.table_view.isHidden() and panel.shimmer.isHidden()

        qtbot.wait_until(transition_complete, timeout=2000)
        assert panel.filters.status_label.text() == "Pronto"

    def test_loading_progress_updates_label(self, panel):
        """Verifica che il progresso di caricamento aggiorni la label di stato."""
        panel._on_loading_progress("Caricamento: 50%")
        assert panel.filters.status_label.text() == "Caricamento: 50%"
