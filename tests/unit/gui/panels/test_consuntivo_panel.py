"""Unit tests for ConsuntivoPanel."""

from unittest.mock import MagicMock

import pytest

from src.gui.panels.consuntivo_panel import ConsuntivoPanel


@pytest.fixture
def mock_controller():
    """Mock per ConsuntivoController."""
    mock = MagicMock()
    # Mock dei metodi chiamati durante lbl'init dei tab interni
    mock.get_config_options.return_value = {
        "tcl": ["TCL1"],
        "stati": ["S1"],
        "tipologie": ["P1"],
        "economie": ["E1"],
    }
    mock.get_dynamic_path.return_value = "/mock/path"
    mock.get_master_path.return_value = "/mock/master.xlsm"
    return mock


@pytest.fixture
def panel(qtbot, mock_controller, mocker):
    """Istanza di ConsuntivoPanel per i test."""
    # Patch dei metodi IO dei tab interni
    mocker.patch(
        "src.gui.widgets.contabilita.consuntivo.modifica_esistente_tab.ModificaEsistenteTab._scan_directory"
    )
    mocker.patch("src.gui.widgets.contabilita.consuntivo.crea_nuovo_tab.CreaNuovoTab._update_dynamic_path")
    mocker.patch("src.gui.workers.consuntivo_worker.ConsuntivoWorker.start")

    p = ConsuntivoPanel(mock_controller)
    qtbot.addWidget(p)
    return p


class TestConsuntivoPanel:
    """Test suite per ConsuntivoPanel."""

    def test_initialization(self, panel):
        """Verifica lbl'inizializzazione del pannello."""
        assert panel.tabs.count() == 3
        assert panel._tab_new is not None
        assert panel._tab_modify is not None

    def test_pre_load_finished_populates_ui(self, qtbot, panel):
        """Verifica che il termine del preload popoli le combo."""
        result = {"options": {"tcl": ["T1", "T2"], "stati": ["S1"], "tipologie": ["P1"], "economie": ["E1"]}}

        panel._on_pre_load_finished(result)

        assert panel._tab_new.tcl_combo.count() == 2
        assert panel._tab_new.tcl_combo.itemText(0) == "T1"
        assert panel._data_preloaded is True

    def test_set_current_tab(self, panel):
        """Verifica il cambio tab programmatico."""
        panel.set_current_tab(1)
        assert panel.tabs.currentIndex() == 1

    def test_on_tab_changed_triggers_refresh(self, panel, mocker):
        """Verifica che il cambio tab attivi le logiche di refresh."""
        # Non possiamo patchare di nuovo qui se già patchati nel fixture?
        # In realtà sì, mocker.patch.object sull'istanza.
        mock_upd = mocker.patch.object(panel._tab_new, "_update_dynamic_path")
        mock_scan = mocker.patch.object(panel._tab_modify, "_scan_directory")

        panel.tabs.setCurrentIndex(0)
        assert mock_upd.called

        panel.tabs.setCurrentIndex(1)
        assert mock_scan.called
