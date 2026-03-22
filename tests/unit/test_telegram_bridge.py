from unittest.mock import MagicMock

import pytest

from src.core.telegram_bridge import TelegramUIBridge


class TestTelegramUIBridge:
    @pytest.fixture
    def mock_mw(self):
        mw = MagicMock()
        mw.telegram = MagicMock()
        return mw

    @pytest.fixture
    def bridge(self, mock_mw, mocker):
        # Mocking sub-handlers to avoid deep init
        mocker.patch("src.gui.main_window.telegram_bridge.TelegramGUIBridge")
        mocker.patch("src.core.telegram_bridge.TelegramUICommands")
        mocker.patch("src.core.telegram_bridge.TelegramDataProcessor")
        mocker.patch("src.core.telegram_bridge.TelegramSystemHandler")
        mocker.patch("src.core.telegram_bridge.TelegramIntentHandler")

        return TelegramUIBridge(mock_mw)

    def test_setup_connections(self, bridge):
        """Verifica il collegamento dei segnali Telegram."""
        bridge.setup_connections()
        bridge.telegram.command_received.connect.assert_called()
        bridge.telegram.data_received.connect.assert_called()
        bridge.telegram.status_requested.connect.assert_called()
        bridge.telegram.intent_received.connect.assert_called()

    def test_dispatch_command_run_ts(self, bridge):
        """Verifica la delega del comando run_ts a ui_commands."""
        # Note: in dispatch_command it's a lambda call
        bridge._dispatch_command("run_ts", {})
        bridge.ui_commands.run_ts_bot.assert_called_once()

    def test_dispatch_command_run_pdl(self, bridge):
        """Verifica la delega del comando run_pdl a ui_commands."""
        params = {"id": "123"}
        bridge._dispatch_command("run_pdl", params)
        bridge.ui_commands.run_pdl_bot.assert_called_with(params)

    def test_dispatch_data_pdl(self, bridge):
        """Verifica la delega del processamento dati PDL a data_processor."""
        items = ["PDL1", "PDL2"]
        bridge._dispatch_data("pdl", items)
        bridge.data_processor.process_pdl_items.assert_called_with(items)
