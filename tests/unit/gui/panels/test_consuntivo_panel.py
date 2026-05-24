"""Unit tests for ConsuntivoPanel."""

from unittest.mock import MagicMock

import pytest

from src.gui.panels.consuntivo_panel import ConsuntivoPanel


@pytest.fixture
def mock_controller():
    """Mock per ConsuntivoController."""
    mock = MagicMock()
    # Mock dei metodi chiamati durante l'init dei tab interni
    mock.get_config_options.return_value = {
        "tcl": ["TCL1"],
        "stati": ["S1"],
        "tipologie": ["P1"],
        "economie": ["E1"],
    }
    mock.get_dynamic_path.return_value = "/mock/path"
    mock.get_master_path.return_value = "/mock/master.xlsm"
    return mock


class TestConsuntivoPanel:
    """Test suite per ConsuntivoPanel."""

    def test_initialization(self, qtbot, mock_controller, mocker):
        """Verifica l'inizializzazione del pannello."""
        # Patch totale dei componenti interni per isolamento atomico
        mocker.patch("src.gui.panels.consuntivo_panel.AnimatedTabWidget")
        mocker.patch("src.gui.panels.consuntivo_panel.CreaNuovoTab")
        mocker.patch("src.gui.panels.consuntivo_panel.ModificaEsistenteTab")
        mocker.patch("src.gui.panels.consuntivo_panel.ImpostazioniTab")

        mocker.patch("PySide6.QtCore.QTimer.singleShot")
        mocker.patch("src.gui.workers.consuntivo_worker.ConsuntivoWorker.start")

        panel = ConsuntivoPanel(mock_controller)
        qtbot.addWidget(panel)

        assert panel.tabs is not None
        assert panel._tab_new is not None
        assert panel._tab_modify is not None

    def test_pre_load_finished_populates_ui(self, qtbot, mock_controller, mocker):
        """Verifica che il termine del preload popoli le combo."""
        mocker.patch("src.gui.panels.consuntivo_panel.AnimatedTabWidget")
        mocker.patch("src.gui.panels.consuntivo_panel.CreaNuovoTab")
        mocker.patch("src.gui.panels.consuntivo_panel.ModificaEsistenteTab")
        mocker.patch("src.gui.panels.consuntivo_panel.ImpostazioniTab")
        mocker.patch("PySide6.QtCore.QTimer.singleShot")

        panel = ConsuntivoPanel(mock_controller)
        qtbot.addWidget(panel)

        # Simuliamo il risultato del worker
        result = {"options": {"tcl": ["T1", "T2"], "stati": ["S1"], "tipologie": ["P1"], "economie": ["E1"]}}
        panel._on_pre_load_finished(result)

        # Verifichiamo che i metodi di popolamento siano stati chiamati sui mock dei tab
        assert panel._tab_new.tcl_combo.addItems.called
        assert panel._data_preloaded is True

    def test_set_current_tab(self, qtbot, mock_controller, mocker):
        """Verifica il cambio tab programmatico."""
        mocker.patch("src.gui.panels.consuntivo_panel.CreaNuovoTab")
        mocker.patch("src.gui.panels.consuntivo_panel.ModificaEsistenteTab")
        mocker.patch("src.gui.panels.consuntivo_panel.ImpostazioniTab")

        mock_tabs_class = mocker.patch("src.gui.panels.consuntivo_panel.AnimatedTabWidget")
        mock_tabs = mock_tabs_class.return_value
        mock_tabs.count.return_value = 3

        mocker.patch("PySide6.QtCore.QTimer.singleShot")

        panel = ConsuntivoPanel(mock_controller)
        qtbot.addWidget(panel)

        panel.set_current_tab(1)
        assert panel.tabs.setCurrentIndex.called

    def test_on_tab_changed_triggers_refresh(self, qtbot, mock_controller, mocker):
        """Verifica che il cambio tab attivi le logiche di refresh."""
        mocker.patch("src.gui.panels.consuntivo_panel.AnimatedTabWidget")
        mocker.patch("src.gui.panels.consuntivo_panel.CreaNuovoTab")
        mocker.patch("src.gui.panels.consuntivo_panel.ModificaEsistenteTab")
        mocker.patch("src.gui.panels.consuntivo_panel.ImpostazioniTab")
        mocker.patch("PySide6.QtCore.QTimer.singleShot")

        panel = ConsuntivoPanel(mock_controller)
        qtbot.addWidget(panel)

        # Simuliamo il widget restituito da AnimatedTabWidget.widget(index)
        panel.tabs.widget.side_effect = [panel._tab_new, panel._tab_modify]

        panel._on_tab_changed(0)
        assert panel._tab_new._update_dynamic_path.called

        panel._on_tab_changed(1)
        assert panel._tab_modify._scan_directory.called
