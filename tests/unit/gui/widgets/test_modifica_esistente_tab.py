"""Unit tests for ModificaEsistenteTab."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QLabel

from src.gui.widgets.contabilita.consuntivo.modifica_esistente_tab import ModificaEsistenteTab


@pytest.fixture
def mock_config(mocker):
    """Fixture per mockare config_manager."""
    mock = mocker.patch("src.core.config_manager.get_config_value")
    mock.return_value = "/mock/network/path"
    return mock


@pytest.fixture
def mock_listdir(mocker):
    """Fixture per mockare os.listdir."""
    return mocker.patch("os.listdir")


class TestModificaEsistenteTab:
    """Test suite per ModificaEsistenteTab."""

    def test_initialization(self, qtbot, mock_config):
        """Verifica lbl'inizializzazione del tab."""
        widget = ModificaEsistenteTab()
        qtbot.addWidget(widget)

        assert widget.anno_combo.count() > 0
        assert widget.file_combo.count() == 0

        labels = widget.findChildren(QLabel)
        assert any("SELEZIONE CONSUNTIVO" in lbl.text() for lbl in labels)

    def test_scan_directory_success(self, qtbot, mock_config, mock_listdir, mocker):
        """Verifica la scansione dei file e il popolamento della combo."""
        mock_listdir.return_value = ["AAA.xlsm", "BBB.xlsm"]
        mocker.patch("pathlib.Path.is_dir", return_value=True)
        mocker.patch("pathlib.Path.stat", return_value=MagicMock(st_size=102400))

        widget = ModificaEsistenteTab()
        qtbot.addWidget(widget)

        with qtbot.waitSignal(widget._scan_finished, timeout=5000):
            widget._scan_directory(force=True)

        assert widget.file_combo.count() == 2
        assert "BBB.xlsm" in widget.file_combo.itemText(0)

    def test_auto_fill_from_file_manual(self, qtbot, mock_config, mocker):
        """Verifica lbl'estrazione dati chiamando direttamente il metodo con un mock di workbook."""
        widget = ModificaEsistenteTab()
        qtbot.addWidget(widget)

        mock_load = mocker.patch("openpyxl.load_workbook")

        mock_wb = MagicMock()
        mock_wb.sheetnames = ["inserimento dati", "rif.VBA"]

        mock_sheet = MagicMock()
        mock_date = MagicMock()
        mock_date.strftime.return_value = "24/05/2026"

        # Setup celle foglio principale
        cells = {
            "A5": MagicMock(value=mock_date),
            "A7": MagicMock(value="TCL_VAL"),
            "B5": MagicMock(value="ODC_VAL"),
            "A11": MagicMock(value="Desc Line 1"),
        }
        mock_sheet.__getitem__.side_effect = lambda k: cells.get(k, MagicMock(value=""))

        # Setup foglio VBA
        mock_vba_sheet = MagicMock()
        mock_vba_sheet["A4"].value = "PROG_VBA"

        def wb_getitem(name):
            if name == "inserimento dati":
                return mock_sheet
            if name == "rif.VBA":
                return mock_vba_sheet
            raise KeyError(name)

        mock_wb.__getitem__.side_effect = wb_getitem
        mock_load.return_value = mock_wb

        widget._auto_fill_from_file("/mock/file.xlsm")

        assert widget._fields["data"].text() == "24/05/2026"
        assert widget._fields["tcl"].text() == "TCL_VAL"
        assert widget._fields["progressivo"].text() == "PROG_VBA"

    def test_save_to_file_mocked(self, qtbot, mock_config, mocker):
        """Verifica il salvataggio chiamando direttamente il metodo."""
        widget = ModificaEsistenteTab()
        qtbot.addWidget(widget)
        widget.loaded_file = "/mock/file.xlsm"

        mock_load = mocker.patch("openpyxl.load_workbook")
        mocker.patch("pathlib.Path.exists", return_value=True)
        mocker.patch("src.gui.dialogs.confirmation_dialog.ConfirmationDialog.show_info")

        mock_wb = MagicMock()
        mock_wb.sheetnames = ["inserimento dati"]

        cells_set = {}

        class MockSheet:
            def __getitem__(self, key):
                return MagicMock()

            def __setitem__(self, key, val):
                cells_set[key] = val

        mock_sheet = MockSheet()
        mock_wb.__getitem__.return_value = mock_sheet
        mock_load.return_value = mock_wb

        widget._fields["odc"].setText("SAVE_ODC")
        widget._desc_lavoro_display.setPlainText("New Desc")

        widget._save_to_file()

        assert cells_set["B5"] == "SAVE_ODC"
        assert cells_set["A11"] == "New Desc"
        assert mock_wb.save.called

    def test_workflow_step_trigger_manual(self, qtbot, mock_config, mocker):
        """Verifica lbl'attivazione del workflow con uno step valido."""
        mocker.patch("pathlib.Path.exists", return_value=True)

        # Patching MacroWorker
        mock_worker_cls = mocker.patch(
            "src.gui.widgets.contabilita.consuntivo.modifica_esistente_tab.MacroWorker"
        )
        mock_worker_instance = MagicMock()
        mock_worker_cls.return_value = mock_worker_instance

        widget = ModificaEsistenteTab()
        qtbot.addWidget(widget)
        widget.loaded_file = "/mock/file.xlsm"

        # 'carica_dati' è un ID valido presente in WorkflowMapWidget.STEPS
        widget._on_workflow_step("carica_dati")

        assert mock_worker_cls.called
        assert mock_worker_instance.start.called
        assert not widget.isEnabled()

    def test_macro_finished_ui(self, qtbot, mocker):
        """Verifica feedback UI post-macro."""
        mocker.patch("src.gui.dialogs.confirmation_dialog.ConfirmationDialog.show_info")
        widget = ModificaEsistenteTab()
        qtbot.addWidget(widget)
        widget.setEnabled(False)

        widget._on_macro_finished(True, "Success", "step_x")

        assert widget.isEnabled()
        assert "Success" in widget.log_widget._log_text.toHtml()

    def test_scan_error_ui(self, qtbot, mock_listdir, mocker):
        """Verifica feedback UI su errore scansione."""
        mock_listdir.side_effect = Exception("IO Failure")
        mocker.patch("pathlib.Path.is_dir", return_value=True)

        widget = ModificaEsistenteTab()
        qtbot.addWidget(widget)

        with qtbot.waitSignal(widget._scan_error, timeout=5000):
            widget._scan_directory(force=True)

        assert "Errore scansione" in widget.log_widget._log_text.toHtml()
