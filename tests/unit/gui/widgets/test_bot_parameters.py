from unittest.mock import patch

import pytest
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QApplication

from src.gui.widgets.bot_parameters import BotParametersWidget, HoverPulseFrame


class TestBotParametersWidget:
    @pytest.fixture
    def widget(self, qtbot):
        # Mock config_manager to avoid real file access
        with patch("src.core.config_manager.load_config", return_value={"fornitori": ["F1", "F2"]}):
            w = BotParametersWidget(show_date_range=True)
            qtbot.addWidget(w)
            return w

    def test_initialization(self, widget):
        assert widget.fornitore_combo.count() == 2
        assert widget.societa_combo.currentText() == "ISAB"
        assert widget.show_date_range is True

    def test_get_set_fornitore(self, widget):
        widget.set_fornitore("F2")
        assert widget.get_fornitore() == "F2"

    def test_get_set_societa(self, widget):
        widget.set_societa("PSER")
        assert widget.get_societa() == "PSER"

    def test_get_set_dates(self, widget):
        widget.set_dates("15.10.2023", "20.10.2023")
        da, a = widget.get_dates()
        assert da == "15.10.2023"
        assert a == "20.10.2023"

    def test_browse_path(self, widget):
        with patch("PySide6.QtWidgets.QFileDialog.getExistingDirectory", return_value="/selected/path"):
            widget._browse_path()
            assert widget.get_dest_path() == "/selected/path"

    def test_changed_signal(self, widget, qtbot):
        with qtbot.wait_signal(widget.changed):
            widget.societa_combo.setCurrentIndex(1)

    def test_hover_pulse_frame(self, qtbot):
        frame = HoverPulseFrame()
        qtbot.addWidget(frame)

        # Enter triggers anim
        from PySide6.QtGui import QEnterEvent

        QApplication.sendEvent(frame, QEnterEvent(QPoint(0, 0), QPoint(0, 0), QPoint(0, 0)))
        assert frame._anim.state() == frame._anim.State.Running

        # Leave stops it
        from PySide6.QtCore import QEvent

        QApplication.sendEvent(frame, QEvent(QEvent.Type.Leave))
        assert frame._anim.state() == frame._anim.State.Stopped
