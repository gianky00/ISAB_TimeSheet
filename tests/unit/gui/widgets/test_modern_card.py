import pytest
from PySide6.QtCore import QEvent, QPoint
from PySide6.QtGui import QEnterEvent
from PySide6.QtWidgets import QApplication, QLabel

from src.gui.widgets.modern_card import ModernCard, ModernContentCard


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_modern_card_initialization(qapp):
    card = ModernCard(elevation=20)
    assert card.elevation == 20
    assert card.objectName() == "modernCard"
    assert "background-color" in card.styleSheet()


def test_modern_card_enter_leave_events(qapp):
    card = ModernCard(elevation=10)

    enter_event = QEnterEvent(QPoint(0, 0), QPoint(0, 0), QPoint(0, 0))
    card.enterEvent(enter_event)
    assert card.shadow_anim.state() == card.shadow_anim.State.Running
    assert card.shadow_anim.endValue() == 25

    leave_event = QEvent(QEvent.Type.Leave)
    card.leaveEvent(leave_event)
    assert card.shadow_anim.state() == card.shadow_anim.State.Running
    assert card.shadow_anim.endValue() == 10


def test_modern_content_card_initialization(qapp):
    card = ModernContentCard()
    assert card.content_layout is not None
    assert card.content_layout.spacing() == 10


def test_modern_content_card_add_widget(qapp):
    card = ModernContentCard()
    label = QLabel("Test")
    card.addWidget(label)
    assert card.content_layout.count() == 1
    assert card.content_layout.itemAt(0).widget() == label
