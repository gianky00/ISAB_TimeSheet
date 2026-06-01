import os
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

from src.gui.controllers.bot_controller import BotController


class MockPanel(QWidget):
    bot_results_ready = Signal(str, list)
    status_changed = Signal(str, str)
    autopilot_changed = Signal()

    def __init__(self, bot_id="test_bot", parent=None):
        super().__init__(parent)
        self.bot_id = bot_id


@pytest.fixture
def bot_controller(qtbot):
    # Use a real QObject to avoid PySide6 init crash
    mw = QObject()
    telegram = MagicMock()
    controller = BotController(mw, telegram)
    return controller, mw, telegram


def test_bot_controller_init(bot_controller):
    controller, mw, telegram = bot_controller
    assert controller.mw == mw
    assert controller.telegram == telegram
    assert controller.panels == []


def test_register_panels(qtbot, bot_controller):
    controller, _mw, _telegram = bot_controller
    panel = MockPanel()
    qtbot.addWidget(panel)

    controller.register_panels([panel])
    assert controller.panels == [panel]

    # Check signal connection
    with patch.object(controller, "_handle_bot_results") as mock_handle:
        panel.bot_results_ready.emit("bot1", ["file1"])
        mock_handle.assert_called_once_with("bot1", ["file1"])


def test_handle_bot_results_pdl(bot_controller, tmp_path):
    controller, _mw, telegram = bot_controller
    test_file = tmp_path / "test.pdf"
    test_file.write_text("content")

    controller._handle_bot_results("scarico_pdl", [str(test_file)])
    telegram.send_document_sync.assert_called_once()
    assert os.path.basename(str(test_file)) in telegram.send_document_sync.call_args[1]["caption"]


def test_on_panel_status_changed(qtbot, bot_controller):
    controller, mw, _telegram = bot_controller
    # Add dummy status objects to mw
    mw.status_safework = MagicMock()
    mw.status_portale = MagicMock()

    panel = MockPanel(bot_id="scarico_pdl")
    qtbot.addWidget(panel)

    # Simulate signal call with sender
    with patch.object(controller, "sender", return_value=panel):
        controller._on_panel_status_changed("#FF0000", "Busy")

    mw.status_safework.setStatus.assert_called_once_with("Busy", "#FF0000")


def test_on_autopilot_trigger(bot_controller):
    controller, mw, _telegram = bot_controller
    mw.status_bar_component = MagicMock()
    mw.dashboard_panel = MagicMock()

    controller._on_autopilot_trigger()
    mw.status_bar_component.update_autopilot_ui.assert_called_once()
    mw.dashboard_panel.refresh_live_data.assert_called_once()


def test_get_active_bot_panel_none(bot_controller):
    controller, mw, _telegram = bot_controller
    mw.automazioni_widget = None
    assert controller._get_active_bot_panel() is None


def test_get_active_bot_panel_valid(qtbot, bot_controller):
    controller, mw, _telegram = bot_controller
    auto_widget = MagicMock()
    auto_widget.currentIndex.return_value = 0

    panel = QWidget()
    qtbot.addWidget(panel)
    tab = MagicMock()
    tab.currentWidget.return_value = panel
    auto_widget.tab_fornitori = tab

    mw.automazioni_widget = auto_widget
    assert controller._get_active_bot_panel() == panel
