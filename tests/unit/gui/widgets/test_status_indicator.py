import pytest
from PySide6.QtCore import QAbstractAnimation
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QApplication

from src.gui.widgets.status_indicator import StatusIndicator


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_status_indicator_initialization(qapp):
    indicator = StatusIndicator()
    assert indicator.toolTip() == "Pronto"
    assert indicator.animation.state() == QAbstractAnimation.State.Stopped


def test_status_indicator_set_status_running(qapp):
    indicator = StatusIndicator()
    indicator.set_status("running", "Running task")
    assert indicator.toolTip() == "Running task"
    assert indicator.animation.state() == QAbstractAnimation.State.Running


def test_status_indicator_set_status_success(qapp):
    indicator = StatusIndicator()
    indicator.set_status("running")  # Start animation
    indicator.set_status("success", "Task completed")
    assert indicator.toolTip() == "Task completed"
    assert indicator.animation.state() == QAbstractAnimation.State.Stopped
    assert indicator.opacity_effect.opacity() == 1.0


def test_status_indicator_set_status_error(qapp):
    indicator = StatusIndicator()
    indicator.set_status("error", "Task failed")
    assert indicator.toolTip() == "Task failed"
    assert indicator.animation.state() == QAbstractAnimation.State.Stopped
    assert indicator.opacity_effect.opacity() == 1.0


def test_status_indicator_set_status_idle(qapp):
    indicator = StatusIndicator()
    indicator.set_status("idle", "Idle state")
    assert indicator.toolTip() == "Idle state"
    assert indicator.animation.state() == QAbstractAnimation.State.Stopped
    assert indicator.opacity_effect.opacity() == 1.0


def test_status_indicator_paint_event(qapp):
    indicator = StatusIndicator()
    event = QPaintEvent(indicator.rect())
    # Should not raise any exceptions
    indicator.paintEvent(event)
