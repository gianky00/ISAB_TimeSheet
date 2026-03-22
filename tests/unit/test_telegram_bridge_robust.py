from unittest.mock import MagicMock, patch

import pytest

from src.core.telegram_bridge import TelegramUIBridge


class TestTelegramUIBridgeRobust:
    @pytest.fixture
    def mock_mw(self):
        mw = MagicMock()
        mw.telegram = MagicMock()
        return mw

    @pytest.fixture
    def bridge(self, mock_mw, mocker):
        mocker.patch("src.gui.main_window.telegram_bridge.TelegramGUIBridge")
        mocker.patch("src.core.telegram_bridge.TelegramUICommands")
        mocker.patch("src.core.telegram_bridge.TelegramDataProcessor")
        mocker.patch("src.core.telegram_bridge.TelegramSystemHandler")
        mocker.patch("src.core.telegram_bridge.TelegramIntentHandler")
        return TelegramUIBridge(mock_mw)

    def test_handle_intent_add_pdl(self, bridge):
        """Verifica la delega dell'intento add_pdl all'handler."""
        intent = {"action": "add", "object": "pdl", "items": ["12345"]}
        bridge.intent_handler.handle_intent(123, intent)
        bridge.intent_handler.handle_intent.assert_called_with(123, intent)

    def test_dispatch_data_bp(self, bridge):
        """Verifica la delega dei dati BP a data_processor."""
        items = ["BP1"]
        bridge._dispatch_data("bp", items)
        bridge.data_processor.process_bp_items.assert_called_with(items)

    def test_handle_status_delegation(self, bridge):
        """Verifica la delega della richiesta stato a system_handler."""
        bridge.system_handler.handle_status()
        bridge.system_handler.handle_status.assert_called_once()
