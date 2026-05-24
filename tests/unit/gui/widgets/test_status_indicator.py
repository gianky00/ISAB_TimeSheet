"""Unit tests for StatusIndicator."""

from PySide6.QtCore import QAbstractAnimation

from src.gui.widgets.status_indicator import StatusIndicator


class TestStatusIndicator:
    """Test suite per StatusIndicator."""

    def test_initialization(self, qtbot):
        widget = StatusIndicator()
        qtbot.addWidget(widget)

        assert widget.width() == 20
        assert widget.height() == 20
        assert widget.animation.state() == QAbstractAnimation.State.Stopped

    def test_set_status_running(self, qtbot):
        widget = StatusIndicator()
        qtbot.addWidget(widget)

        widget.set_status("running", "In esecuzione...")
        assert widget.animation.state() == QAbstractAnimation.State.Running
        assert widget.toolTip() == "In esecuzione..."

    def test_set_status_success(self, qtbot):
        widget = StatusIndicator()
        qtbot.addWidget(widget)
        widget.set_status("running")

        widget.set_status("success", "Fatto")
        assert widget.animation.state() == QAbstractAnimation.State.Stopped
        assert widget.opacity_effect.opacity() == 1.0

    def test_set_status_error(self, qtbot):
        widget = StatusIndicator()
        qtbot.addWidget(widget)

        widget.set_status("error", "Errore")
        from PySide6.QtGui import QColor

        from src.gui.styles import COLORS

        assert widget.current_color == QColor(COLORS["error_red"])

    def test_paint_event_no_crash(self, qtbot):
        widget = StatusIndicator()
        qtbot.addWidget(widget)
        widget.update()
