import pytest
from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QEnterEvent, QMouseEvent, QShowEvent
from PySide6.QtWidgets import QApplication

from src.gui.widgets.modern_button import ModernButton


# Create QApplication instance for Qt tests
@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_modern_button_initialization(qapp):
    btn = ModernButton(text="Test", variant=ModernButton.Variant.PRIMARY, size=ModernButton.Size.LARGE)
    assert btn.text() == "Test"
    assert btn._variant == ModernButton.Variant.PRIMARY
    assert btn._size == ModernButton.Size.LARGE
    assert btn._hover_opacity == 0.0


def test_modern_button_ghost_variant(qapp):
    btn = ModernButton(text="Ghost", variant=ModernButton.Variant.GHOST)
    assert "border: 1px solid" in btn.styleSheet()


def test_modern_button_hover_opacity(qapp):
    btn = ModernButton()
    btn.set_hover_opacity(0.5)
    assert btn.get_hover_opacity() == 0.5
    assert btn.hover_opacity == 0.5


def test_modern_button_mouse_events(qapp):
    btn = ModernButton()

    # Press
    mouse_event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPoint(0, 0),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    btn.mousePressEvent(mouse_event)
    assert btn._shadow.blurRadius() == 2

    # Release
    mouse_release_event = QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        QPoint(0, 0),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    btn.mouseReleaseEvent(mouse_release_event)
    assert btn._shadow.blurRadius() == 8


def test_modern_button_enter_leave_events(qapp):
    btn = ModernButton()

    enter_event = QEnterEvent(QPoint(0, 0), QPoint(0, 0), QPoint(0, 0))
    btn.enterEvent(enter_event)
    assert btn._anim.state() == btn._anim.State.Running
    assert btn._anim.endValue() == 0.1

    leave_event = QEvent(QEvent.Type.Leave)
    btn.leaveEvent(leave_event)
    assert btn._anim.state() == btn._anim.State.Running
    assert btn._anim.endValue() == 0.0


def test_modern_button_sizes(qapp):
    btn_small = ModernButton(size=ModernButton.Size.SMALL)
    assert "8px 12px" in btn_small.styleSheet()

    btn_medium = ModernButton(size=ModernButton.Size.MEDIUM)
    assert "10px 20px" in btn_medium.styleSheet()

    btn_large = ModernButton(size=ModernButton.Size.LARGE)
    assert "14px 28px" in btn_large.styleSheet()


def test_modern_button_show_event(qapp):
    btn = ModernButton()
    import unittest.mock

    show_event = QShowEvent()
    with unittest.mock.patch.object(btn, "_apply_style") as mock_apply:
        btn.showEvent(show_event)
        mock_apply.assert_called_once()
