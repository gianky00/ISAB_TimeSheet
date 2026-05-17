import pytest
from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication

from src.gui.widgets.status_card import StatusCard


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_status_card_initialization(qapp):
    card = StatusCard(title="Test", status="Waiting")
    assert card._title_label.text() == "Test"
    assert card._status_label.text() == "Waiting"
    assert card._meta_label.isVisible() is False


def test_status_card_set_status(qapp):
    card = StatusCard(title="Test")
    card.setStatus("Running", status_id="#00FF00")
    assert card._status_label.text() == "Running"
    assert "background-color: #00FF00" in card._icon_bar.styleSheet()


def test_status_card_set_status_no_id(qapp):
    card = StatusCard(title="Test")
    card.setStatus("Running")
    assert card._status_label.text() == "Running"


def test_status_card_set_autopilot(qapp):
    card = StatusCard(title="Test")
    card.setAutopilot(True, "ON")
    assert card._meta_label.isHidden() is False
    assert card._meta_label.text() == "ON"

    card.setAutopilot(False)
    assert card._meta_label.isHidden() is True


def test_status_card_update_status_display(qapp):
    card = StatusCard(title="Test")
    card._update_status_display("Updated")
    assert card._status_label.text() == "Updated"


def test_status_card_mouse_press_event(qapp):
    card = StatusCard(title="Test")
    clicked = False

    def on_clicked():
        nonlocal clicked
        clicked = True

    card.clicked.connect(on_clicked)

    event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPoint(0, 0),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    card.mousePressEvent(event)

    assert clicked is True
