import pytest
from PySide6.QtCore import QEvent, QPoint
from PySide6.QtGui import QColor, QEnterEvent, QPaintEvent
from PySide6.QtWidgets import QApplication

from src.gui.widgets.effects import HoverPulseFrame


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_hover_pulse_frame_initialization(qapp):
    frame = HoverPulseFrame()
    assert frame.get_pulse_value() == 1.0
    assert frame._anim.loopCount() == -1


def test_hover_pulse_frame_custom_color(qapp):
    frame = HoverPulseFrame(accent_color="#FF0000")
    assert frame._accent_color == QColor("#FF0000")


def test_hover_pulse_frame_events(qapp):
    frame = HoverPulseFrame()

    # Enter event
    enter_event = QEnterEvent(QPoint(0, 0), QPoint(0, 0), QPoint(0, 0))
    frame.enterEvent(enter_event)
    assert frame._anim.state() == frame._anim.State.Running

    # Leave event
    leave_event = QEvent(QEvent.Type.Leave)
    frame.leaveEvent(leave_event)
    assert frame._anim.state() == frame._anim.State.Stopped
    assert frame.get_pulse_value() == 1.0


def test_hover_pulse_frame_set_pulse_value(qapp):
    frame = HoverPulseFrame()
    frame.set_pulse_value(0.5)
    assert frame.get_pulse_value() == 0.5
    assert frame.pulse_value == 0.5


def test_hover_pulse_frame_paint_event(qapp):
    frame = HoverPulseFrame()
    event = QPaintEvent(frame.rect())
    # Should not raise any exceptions
    frame.paintEvent(event)
