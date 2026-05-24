"""Unit tests for CreaNuovoTab."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt

from src.gui.widgets.contabilita.consuntivo.crea_nuovo_tab import CreaNuovoTab


@pytest.fixture
def mock_controller():
    """Mock per ConsuntivoController."""
    mock = MagicMock()
    mock.get_config_options.return_value = {
        "tcl": ["TCL1", "TCL2"],
        "stati": ["Stato1"],
        "tipologie": ["Tipo1"],
        "economie": ["Eco1"],
    }
    mock.get_dynamic_path.return_value = "/mock/dynamic/path"
    mock.get_master_path.return_value = "/mock/master.xlsm"
    return mock


class TestCreaNuovoTab:
    """Test suite per CreaNuovoTab."""

    def test_initialization(self, qtbot, mock_controller):
        """Verifica lbl'inizializzazione del tab e il caricamento opzioni."""
        widget = CreaNuovoTab(mock_controller)
        qtbot.addWidget(widget)

        assert widget.tcl_combo.count() == 2
        assert widget.tcl_combo.itemText(0) == "TCL1"
        assert widget.dest_path_edit.text() == "/mock/dynamic/path"

    def test_on_worker_prog_ready(self, qtbot, mock_controller):
        """Verifica lbl'aggiornamento del progressivo dal worker."""
        widget = CreaNuovoTab(mock_controller)
        qtbot.addWidget(widget)

        widget._on_worker_prog_ready("PROG-2026-001")
        assert widget.progressivo_edit.text() == "PROG-2026-001"
        assert widget._cached_prog == "PROG-2026-001"

    def test_generate_trigger_success(self, qtbot, mock_controller, mocker):
        """Verifica lbl'avvio della generazione del consuntivo."""
        mocker.patch("pathlib.Path.exists", return_value=True)
        mock_worker_cls = mocker.patch(
            "src.gui.widgets.contabilita.consuntivo.crea_nuovo_tab.GeneratoreWorker"
        )
        mock_worker = MagicMock()
        mock_worker_cls.return_value = mock_worker

        mocker.patch("src.gui.dialogs.confirmation_dialog.ConfirmationDialog.show_info")

        widget = CreaNuovoTab(mock_controller)
        qtbot.addWidget(widget)

        qtbot.mouseClick(widget.btn_generate, Qt.MouseButton.LeftButton)

        assert mock_worker_cls.called
        assert mock_worker.start.called
        assert not widget.isEnabled()

        widget._on_generate_finished(True, "/path/to/generated.xlsm")
        assert widget.isEnabled()
        assert widget.last_generated_file == "/path/to/generated.xlsm"

    def test_workflow_step_no_file_error(self, qtbot, mock_controller, mocker):
        """Verifica errore se si clicca workflow senza aver generato il file."""
        mock_error = mocker.patch("src.gui.dialogs.confirmation_dialog.ConfirmationDialog.show_error")

        widget = CreaNuovoTab(mock_controller)
        qtbot.addWidget(widget)
        widget.last_generated_file = None

        # Mocking workflow_map per far passare il primo check
        mocker.patch.object(widget.workflow_map, "get_macros_for_step", return_value=["MacroX"])

        widget._on_workflow_step("step1")

        assert mock_error.called

        assert "Genera prima" in mock_error.call_args[0][2]

    def test_macro_execution_workflow(self, qtbot, mock_controller, mocker):
        """Verifica lbl'esecuzione delle macro VBA."""
        mocker.patch("pathlib.Path.exists", return_value=True)
        mock_worker_cls = mocker.patch("src.gui.widgets.contabilita.consuntivo.crea_nuovo_tab.MacroWorker")
        mock_worker = MagicMock()
        mock_worker_cls.return_value = mock_worker

        widget = CreaNuovoTab(mock_controller)
        qtbot.addWidget(widget)

        # Mock macros
        mocker.patch.object(widget.workflow_map, "get_macros_for_step", return_value=["Macro1"])
        widget.last_generated_file = "/mock/file.xlsm"

        widget._on_workflow_step("step1")

        assert mock_worker_cls.called
        assert mock_worker.start.called
        assert not widget.isEnabled()

        mocker.patch("src.gui.dialogs.confirmation_dialog.ConfirmationDialog.show_info")
        widget._on_macro_finished(True, "Macro OK", "step1")
        assert widget.isEnabled()

    def test_generate_error_feedback(self, qtbot, mock_controller, mocker):
        """Verifica feedback in caso di errore generazione."""
        mocker.patch("src.gui.dialogs.confirmation_dialog.ConfirmationDialog.show_error")
        widget = CreaNuovoTab(mock_controller)
        qtbot.addWidget(widget)

        widget._on_generate_finished(False, "Access Denied")

        assert "Access Denied" in widget.log_widget._log_text.toHtml()

    def test_update_dynamic_path_force(self, qtbot, mock_controller, mocker):
        """Verifica il ricalcolo forzato del percorso."""
        mocker.patch("src.gui.widgets.contabilita.consuntivo.crea_nuovo_tab.ProgWorker")
        widget = CreaNuovoTab(mock_controller)
        qtbot.addWidget(widget)

        mock_controller.get_dynamic_path.return_value = "/new/path"
        widget._update_dynamic_path(force=True)

        assert widget.dest_path_edit.text() == "/new/path"
