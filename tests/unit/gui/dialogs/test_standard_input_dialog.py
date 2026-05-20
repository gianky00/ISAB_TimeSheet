import pytest
from PySide6.QtWidgets import QApplication

from src.gui.dialogs.standard_input_dialog import StandardInputDialog


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    return app


def test_standard_input_dialog_initialization(qapp):
    dlg = StandardInputDialog(title="Test Input", label="Inserire valore")
    assert dlg.windowTitle() == "Test Input"


def test_get_text_logic(qapp):
    dlg = StandardInputDialog(title="T", label="L", text="valore_iniziale")
    assert dlg.get_text() == "valore_iniziale"

    # Simula input utente
    dlg.input_field.setText("  nuovo_valore  ")
    assert dlg.get_text() == "nuovo_valore"
