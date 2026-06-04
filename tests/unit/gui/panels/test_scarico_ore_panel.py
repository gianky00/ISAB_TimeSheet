"""Unit tests for ScaricoOrePanel."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QObject, Qt, Signal

from src.gui.panels.scarico_ore_panel import ScaricoOrePanel


class MockController(QObject):
    """Mock del controller con segnali PySide6 reali."""

    status_changed = Signal(str)
    update_finished = Signal(bool, str)

    def __init__(self):
        super().__init__()
        self.format_number = MagicMock(side_effect=lambda x: f"{x:.2f}")
        self.start_import = MagicMock()


@pytest.fixture
def mock_controller():
    return MockController()


@pytest.fixture
def panel(qtbot, mock_controller, mocker):
    """Istanza di ScaricoOrePanel per i test."""
    mocker.patch("src.application.services.config_manager.load_config", return_value={"dataease_path": "/test/path"})
    mocker.patch("pathlib.Path.exists", return_value=True)
    mocker.patch("src.gui.components.scarico_ore.ScaricoOreTableModel.load_data_async")

    p = ScaricoOrePanel(mock_controller)
    p.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    p.show()
    qtbot.addWidget(p)
    return p


class TestScaricoOrePanel:
    """Test suite per ScaricoOrePanel."""

    def test_initialization(self, panel):
        """Verifica lbl'inizializzazione del pannello."""
        assert panel.controller is not None
        assert panel.filters is not None
        assert panel.table_view is not None

    def test_start_update_success(self, qtbot, panel, mock_controller):
        """Verifica lbl'avvio della sincronizzazione."""
        qtbot.mouseClick(panel.filters.update_btn, Qt.MouseButton.LeftButton)

        assert mock_controller.start_import.called
        assert mock_controller.start_import.call_args[0][0] == "/test/path"

    def test_on_update_finished_success(self, qtbot, panel, mock_controller, mocker):
        """Verifica il completamento con successo dell'aggiornamento."""
        mock_load_data = mocker.patch.object(panel, "_load_data")
        mock_controller.update_finished.emit(True, "OK")
        assert mock_load_data.called

    def test_perform_search(self, qtbot, panel, mocker):
        """Verifica lbl'applicazione del filtro di ricerca."""
        mock_set_filter = mocker.patch.object(panel.source_model, "set_filter")
        panel.filters.search_input.setText("test")
        panel._perform_search("test")
        mock_set_filter.assert_called_with("test", {})

    def test_update_selection_totals(self, qtbot, panel):
        """Verifica lbl'aggiornamento delle ore selezionate."""
        panel._update_selection_totals(42.5)
        assert "42.50" in panel.filters.lbl_selection.text()

    def test_ui_loading_state(self, panel):
        """Verifica lo stato visivo di caricamento."""
        panel._set_ui_loading(True)
        # In environment offscreen, isHidden() è più affidabile di isVisible()
        assert not panel.shimmer.isHidden()
        assert panel.table_view.isHidden()

        panel._set_ui_loading(False)
        assert panel.shimmer.isHidden()
        assert not panel.table_view.isHidden()

    def test_set_search_query_api(self, panel, mocker):
        """Verifica lbl'API pubblica per la ricerca."""
        mock_search = mocker.patch.object(panel, "_perform_search")
        panel.set_search_query("api")
        assert panel.filters.search_input.text() == "api"
        mock_search.assert_called_with("api")
