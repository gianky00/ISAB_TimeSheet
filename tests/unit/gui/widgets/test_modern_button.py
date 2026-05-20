import pytest
from PySide6.QtWidgets import QApplication

from src.gui.widgets.modern_button import ModernButton


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    return app


def test_modern_button_initialization(qapp):
    btn = ModernButton(text="Test", variant=ModernButton.Variant.PRIMARY)
    assert btn.text() == "Test"
    assert btn._variant == ModernButton.Variant.PRIMARY
    assert btn.property("hover_opacity") == 0.0


def test_modern_button_variant_styles(qapp):
    btn = ModernButton(variant=ModernButton.Variant.DANGER)
    # Trigger style application
    btn._apply_style()
    style = btn.styleSheet()
    assert "border-radius: 6px;" in style
