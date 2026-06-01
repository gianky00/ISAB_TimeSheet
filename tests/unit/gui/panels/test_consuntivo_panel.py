"""Unit tests for ConsuntivoPanel."""

from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from src.gui.panels.consuntivo_panel import ConsuntivoPanel


class MockTabs(QWidget):
    """Real QWidget for AnimatedTabWidget."""

    currentChanged = Signal(int)  # noqa: N815

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.addTab = MagicMock()
        self.setCurrentIndex = MagicMock()
        self.count = MagicMock(return_value=0)
        self.widget = MagicMock()


class MockNewTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.tcl_combo = MagicMock()
        self.stato_combo = MagicMock()
        self.tipo_prev_combo = MagicMock()
        self.tipo_econ_combo = MagicMock()

    def _update_dynamic_path(self):
        pass


class MockModifyTab(QWidget):
    def _scan_directory(self):
        pass


@pytest.fixture
def mock_controller():
    """Mock per ConsuntivoController."""
    mock = MagicMock()
    mock.get_config_options.return_value = {
        "tcl": ["TCL1"],
        "stati": ["S1"],
        "tipologie": ["P1"],
        "economie": ["E1"],
    }
    return mock


def test_consuntivo_panel_init(qtbot, mock_controller):
    with (
        patch("src.gui.panels.consuntivo_panel.AnimatedTabWidget", MockTabs),
        patch("src.gui.panels.consuntivo_panel.CreaNuovoTab", MockNewTab),
        patch("src.gui.panels.consuntivo_panel.ModificaEsistenteTab", MockModifyTab),
        patch("src.gui.panels.consuntivo_panel.ImpostazioniTab", QWidget),
        patch("src.gui.panels.consuntivo_panel.QTimer.singleShot"),
        patch("src.gui.workers.consuntivo_worker.ConsuntivoWorker.start"),
    ):
        panel = ConsuntivoPanel(mock_controller)
        qtbot.addWidget(panel)
        assert panel.tabs is not None


def test_consuntivo_panel_preload(qtbot, mock_controller):
    with (
        patch("src.gui.panels.consuntivo_panel.AnimatedTabWidget", MockTabs),
        patch("src.gui.panels.consuntivo_panel.CreaNuovoTab", MockNewTab),
        patch("src.gui.panels.consuntivo_panel.ModificaEsistenteTab", MockModifyTab),
        patch("src.gui.panels.consuntivo_panel.ImpostazioniTab", QWidget),
        patch("src.gui.panels.consuntivo_panel.QTimer.singleShot"),
    ):
        panel = ConsuntivoPanel(mock_controller)
        qtbot.addWidget(panel)

        result = {
            "options": {
                "tcl": ["T1"],
                "stati": ["S1"],
                "tipologie": ["P1"],
                "economie": ["E1"],
            }
        }
        panel._on_pre_load_finished(result)

        assert panel._tab_new.tcl_combo.addItems.called
        assert panel._data_preloaded is True


def test_consuntivo_panel_tab_change(qtbot, mock_controller):
    with (
        patch("src.gui.panels.consuntivo_panel.AnimatedTabWidget", MockTabs),
        patch("src.gui.panels.consuntivo_panel.CreaNuovoTab", MockNewTab),
        patch("src.gui.panels.consuntivo_panel.ModificaEsistenteTab", MockModifyTab),
        patch("src.gui.panels.consuntivo_panel.ImpostazioniTab", QWidget),
        patch("src.gui.panels.consuntivo_panel.QTimer.singleShot"),
    ):
        panel = ConsuntivoPanel(mock_controller)
        qtbot.addWidget(panel)

        # Ora isinstance(panel._tab_new, CreaNuovoTab) è True perché CreaNuovoTab È MockNewTab
        # Patchiamo i metodi sulle istanze create
        panel._tab_new._update_dynamic_path = MagicMock()
        panel._tab_modify._scan_directory = MagicMock()

        # Simuliamo widget()
        panel.tabs.widget.side_effect = [panel._tab_new, panel._tab_modify]

        panel._on_tab_changed(0)
        assert panel._tab_new._update_dynamic_path.called

        panel._on_tab_changed(1)
        assert panel._tab_modify._scan_directory.called
