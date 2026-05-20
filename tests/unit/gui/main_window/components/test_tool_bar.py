import pytest
from PySide6.QtWidgets import QApplication

from src.gui.main_window.components.tool_bar import AnimatedSplitButton


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    return app


def test_animated_split_button_init(qapp):
    btn = AnimatedSplitButton()
    assert btn.is_detached_mode is False
    assert btn.toolTip() == "Sgancia la vista corrente in una finestra esterna (Multi-Window)"


def test_animated_split_button_toggle(qapp):
    btn = AnimatedSplitButton()
    btn.set_state(True)
    assert btn.is_detached_mode is True
    assert btn.toolTip() == "Riaggancia la vista corrente alla finestra principale"
