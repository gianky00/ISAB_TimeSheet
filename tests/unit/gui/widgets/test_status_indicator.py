import sys

import pytest
from PySide6.QtCore import QAbstractAnimation
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication

from src.gui.styles import COLORS
from src.gui.widgets.status_indicator import StatusIndicator


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() or QApplication(sys.argv)
    return app


def test_status_indicator_initialization(qapp):
    indicator = StatusIndicator()
    assert indicator.width() == 20
    assert indicator.height() == 20
    assert indicator.animation.state() == QAbstractAnimation.State.Stopped


def test_set_status_running(qapp):
    indicator = StatusIndicator()
    indicator.set_status("running", "Running task")
    assert indicator.animation.state() == QAbstractAnimation.State.Running
    assert indicator.toolTip() == "Running task"


def test_set_status_success(qapp):
    indicator = StatusIndicator()
    indicator.set_status("running", "Running task")
    indicator.set_status("success", "Done")
    assert indicator.animation.state() == QAbstractAnimation.State.Stopped
    assert indicator.opacity_effect.opacity() == 1.0
    assert indicator.toolTip() == "Done"


def test_set_status_error(qapp):
    indicator = StatusIndicator()
    indicator.set_status("running", "Running")
    indicator.set_status("error", "Failed")
    assert indicator.animation.state() == QAbstractAnimation.State.Stopped
    assert indicator.toolTip() == "Failed"


def test_set_status_idle(qapp):
    indicator = StatusIndicator()
    indicator.set_status("running", "Running")
    indicator.set_status("idle", "Ready")
    assert indicator.animation.state() == QAbstractAnimation.State.Stopped
    assert indicator.toolTip() == "Ready"


def test_set_status_unknown(qapp):
    indicator = StatusIndicator()
    indicator.set_status("running", "Running")
    indicator.set_status("unknown", "Unknown state")
    assert indicator.animation.state() == QAbstractAnimation.State.Stopped
    assert indicator.current_color == QColor(COLORS["text_muted"])
