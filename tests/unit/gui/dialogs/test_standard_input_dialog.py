"""Unit tests for StandardInputDialog."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from src.gui.dialogs.standard_input_dialog import StandardInputDialog


class TestStandardInputDialog:
    """Test suite per StandardInputDialog."""

    def test_initialization(self, qtbot):
        dialog = StandardInputDialog(title="Test Title", label="Test Label", text="Initial")
        qtbot.addWidget(dialog)

        assert dialog.windowTitle() == "Test Title"
        assert dialog.input_field.text() == "Initial"

        from PySide6.QtWidgets import QLabel

        lbls = dialog.findChildren(QLabel)
        assert any("Test Label" in lbl.text() for lbl in lbls)

    def test_get_text(self, qtbot):
        dialog = StandardInputDialog()
        qtbot.addWidget(dialog)
        dialog.input_field.setText("  Hello World  ")
        assert dialog.get_text() == "Hello World"

    def test_accept_reject(self, qtbot):
        dialog = StandardInputDialog()
        qtbot.addWidget(dialog)

        # Test Annulla (Reject)
        with qtbot.waitSignal(dialog.rejected):
            qtbot.mouseClick(dialog.btn_cancel, Qt.MouseButton.LeftButton)

        # Test Salva (Accept)
        dialog2 = StandardInputDialog()
        qtbot.addWidget(dialog2)
        with qtbot.waitSignal(dialog2.accepted):
            qtbot.mouseClick(dialog2.btn_ok, Qt.MouseButton.LeftButton)

    def test_static_get_input_logic(self, qtbot, mocker):
        # Mock exec() su QDialog
        mock_exec = mocker.patch(
            "src.gui.dialogs.standard_input_dialog.QDialog.exec", return_value=QDialog.DialogCode.Accepted
        )

        # Usiamo un approccio di patching più semplice
        # Invece di patchare __init__, mockiamo il ritorno di get_text
        # Ma vogliamo testare che venga chiamato.

        # Mocking lbl'intera istanza creata da get_input
        # Ma SID.get_input crea una NUOVA istanza di SID.
        # Se patchiamo la classe SID, breakiamo il metodo statico se non stiamo attenti.

        # Usiamo patch.object di unittest.mock per il context manager se proprio vogliamo
        from unittest.mock import patch

        original_init = StandardInputDialog.__init__

        def mocked_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self.input_field.setText("Real Result")

        with patch.object(StandardInputDialog, "__init__", mocked_init):
            val, ok = StandardInputDialog.get_input(None, "T", "L")

        assert ok is True
        assert val == "Real Result"
        assert mock_exec.called
