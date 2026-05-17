import pytest
from PySide6.QtCore import QAbstractAnimation
from PySide6.QtGui import QCloseEvent, QHideEvent, QShowEvent
from PySide6.QtWidgets import QApplication

from src.gui.widgets.priority_badge import PriorityBadge


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_priority_badge_initialization(qapp):
    badge = PriorityBadge(priority="alta")
    assert badge.priority == "alta"
    assert badge.anim.state() == QAbstractAnimation.State.Running


def test_priority_badge_set_priority(qapp):
    badge = PriorityBadge()
    badge.set_priority("bassa")
    assert badge.priority == "bassa"
    assert "background-color" in badge.dot.styleSheet()


def test_priority_badge_stop_animation(qapp):
    badge = PriorityBadge()
    badge.stop_animation()
    assert badge.anim.state() == QAbstractAnimation.State.Stopped


def test_priority_badge_events(qapp):
    badge = PriorityBadge()

    # Hide event
    hide_event = QHideEvent()
    badge.hideEvent(hide_event)
    assert badge.anim.state() == QAbstractAnimation.State.Stopped

    # Show event
    show_event = QShowEvent()
    badge.showEvent(show_event)
    assert badge.anim.state() == QAbstractAnimation.State.Running

    # Close event
    close_event = QCloseEvent()
    badge.closeEvent(close_event)
    assert badge.anim.state() == QAbstractAnimation.State.Stopped


def test_priority_badge_pulse_scale(qapp):
    badge = PriorityBadge()
    badge.set_pulse_scale(0.8)
    assert badge.get_pulse_scale() == 0.8
    assert badge.pulse_scale == 0.8
    assert badge.dot.size().width() == int(8 * 0.8)
