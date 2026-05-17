import pytest
from PySide6.QtWidgets import QApplication, QDialog

from src.gui.dialogs.confirmation_dialog import ConfirmationDialog


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    return app


def test_confirmation_dialog_initialization(qapp):
    dlg = ConfirmationDialog(
        title="Test Titolo", message="Test Messaggio", variant=ConfirmationDialog.Variant.INFO
    )
    assert dlg.windowTitle() == "Test Titolo"


def test_sanitization_html():
    dlg = ConfirmationDialog(title="T", message="T")
    # Test script removal
    raw = "<div>Test</div><script>alert(1)</script>"
    clean = dlg._sanitize_html(raw)
    assert "<script>" not in clean
    assert "<div>Test</div>" in clean

    # Test attribute removal
    raw = "<div onmouseover='alert(1)'>Test</div>"
    clean = dlg._sanitize_html(raw)
    assert "onmouseover" not in clean


def test_variants_initialization(qapp):
    for variant in [
        ConfirmationDialog.Variant.INFO,
        ConfirmationDialog.Variant.WARNING,
        ConfirmationDialog.Variant.ERROR,
    ]:
        dlg = ConfirmationDialog(variant=variant)
        assert dlg is not None


def test_static_helpers(qapp, monkeypatch):
    # Mock exec to avoid opening real dialogs
    monkeypatch.setattr(QDialog, "exec", lambda self: QDialog.DialogCode.Accepted)

    assert ConfirmationDialog.confirm(None, "T", "M") is True

    # Test info/warning/error methods
    ConfirmationDialog.show_info(None, "T", "M")
    ConfirmationDialog.show_warning(None, "T", "M")
    ConfirmationDialog.show_error(None, "T", "M")
