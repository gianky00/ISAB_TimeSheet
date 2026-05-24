from unittest.mock import MagicMock, patch

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from src.gui.controllers.bot_controller import BotController


class MockPanel(QWidget):
    bot_results_ready = Signal(str, list)
    status_changed = Signal(str, str)
    autopilot_changed = Signal()

    def __init__(self, bot_id="test_bot"):
        super().__init__()
        self.bot_id = bot_id


def test_bot_controller_init():
    mw = MagicMock()
    telegram = MagicMock()
    controller = BotController(mw, telegram)
    assert controller.mw == mw
    assert controller.telegram == telegram
    assert controller.panels == []


def test_register_panels(qtbot):
    mw = MagicMock()
    telegram = MagicMock()
    controller = BotController(mw, telegram)

    panel = MockPanel()
    controller.register_panels([panel])

    assert controller.panels == [panel]
    # Check if signals are connected by emitting them
    with patch.object(controller, "_handle_bot_results") as mock_handle:
        panel.bot_results_ready.emit("id", ["res"])
        mock_handle.assert_called_once_with("id", ["res"])


def test_handle_bot_results_pdl(tmp_path):
    mw = MagicMock()
    telegram = MagicMock()
    controller = BotController(mw, telegram)

    # Create a dummy file
    test_file = tmp_path / "test_pdl.pdf"
    test_file.write_text("dummy content")

    controller._handle_bot_results("scarico_pdl", [str(test_file)])

    telegram.send_document_sync.assert_called_once()
    _args, kwargs = telegram.send_document_sync.call_args
    assert args[0] == str(test_file)
    assert "PDL Scaricato" in kwargs["caption"]


def test_on_panel_status_changed_safework():
    mw = MagicMock()
    mw.status_safework = MagicMock()
    telegram = MagicMock()
    controller = BotController(mw, telegram)

    panel = MockPanel(bot_id="scarico_pdl")
    controller.register_panels([panel])

    # Simulate signal
    panel.status_changed.emit("#FF0000", "Error")

    mw.status_safework.setStatus.assert_called_once_with("Error", "#FF0000")


def test_on_panel_status_changed_portale():
    mw = MagicMock()
    mw.status_portale = MagicMock()
    telegram = MagicMock()
    controller = BotController(mw, telegram)

    panel = MockPanel(bot_id="other_bot")
    controller.register_panels([panel])

    # Simulate signal
    panel.status_changed.emit("#00FF00", "Success")

    mw.status_portale.setStatus.assert_called_once_with("Success", "#00FF00")


def test_on_autopilot_trigger():
    mw = MagicMock()
    mw.status_bar_component = MagicMock()
    mw.dashboard_panel = MagicMock()
    telegram = MagicMock()
    controller = BotController(mw, telegram)

    controller._on_autopilot_trigger()

    mw.status_bar_component.update_autopilot_ui.assert_called_once()
    mw.dashboard_panel.refresh_live_data.assert_called_once()


def test_get_active_bot_panel_none():
    mw = MagicMock()
    mw.automazioni_widget = None
    controller = BotController(mw, MagicMock())
    assert controller._get_active_bot_panel() is None


def test_get_active_bot_panel_valid():
    mw = MagicMock()
    auto_widget = MagicMock()
    auto_widget.currentIndex.return_value = 0  # tab_fornitori

    panel = QWidget()
    tab_fornitori = MagicMock()
    tab_fornitori.currentWidget.return_value = panel
    auto_widget.tab_fornitori = tab_fornitori

    mw.automazioni_widget = auto_widget
    controller = BotController(mw, MagicMock())

    assert controller._get_active_bot_panel() == panel
