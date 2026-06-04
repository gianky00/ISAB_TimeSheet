import sys

import pytest
from PySide6.QtWidgets import QApplication

from src.gui.components.activity_timeline import ActivityTimelineWidget
from src.infrastructure.bots.base.step_manager import StepStatus


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() or QApplication(sys.argv)
    return app


def test_activity_timeline_initialization(qapp):
    widget = ActivityTimelineWidget()
    assert widget is not None
    assert len(widget.nodes) == 0


def test_set_steps(qapp):
    widget = ActivityTimelineWidget()
    steps = [("step1", "Start Bot"), ("step2", "Running Task")]
    widget.set_steps(steps)

    assert len(widget.nodes) == 2
    assert widget.nodes[0].name == "Start Bot"
    assert widget.nodes[1].name == "Running Task"


def test_on_step_changed_running(qapp):
    widget = ActivityTimelineWidget()
    widget.set_steps([("1", "Task")])

    # Simula cambiamento di stato
    widget.on_step_changed(0, "Task", StepStatus.RUNNING)
    assert widget.nodes[0].status == StepStatus.RUNNING


def test_on_step_changed_completed(qapp):
    widget = ActivityTimelineWidget()
    widget.set_steps([("1", "Task")])

    widget.on_step_changed(0, "Task", StepStatus.RUNNING)
    widget.on_step_changed(0, "Task", StepStatus.COMPLETED)

    assert widget.nodes[0].status == StepStatus.COMPLETED
    assert len(widget.nodes[0].duration_str) > 0


def test_animation_triggers(qapp, qtbot):
    widget = ActivityTimelineWidget()
    widget.show()
    qtbot.addWidget(widget)

    from PySide6.QtCore import QPropertyAnimation

    # Test hover events
    widget.enterEvent(None)
    # The state should be running (2)
    assert widget._border_pulse_anim.state() == QPropertyAnimation.Running

    widget.leaveEvent(None)
    # The state should be stopped (0)
    assert widget._border_pulse_anim.state() == QPropertyAnimation.Stopped
