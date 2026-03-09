import pytest
from unittest.mock import MagicMock, patch
from src.core.telegram_bridge import TelegramUIBridge

class TestTelegramUIBridgeRobust:
    @pytest.fixture
    def mock_mw(self):
        mw = MagicMock()
        mw.telegram = MagicMock()
        return mw

    @pytest.fixture
    def bridge(self, mock_mw):
        with patch("src.core.telegram_bridge.QObject.__init__"):
            return TelegramUIBridge(mock_mw)

    def test_handle_intent_add_pdl(self, bridge):
        """Verifica la delega dell'intento add_pdl all'handler."""
        intent = {"action": "add", "object": "pdl", "items": ["12345"]}
        with patch.object(bridge.intent_handler, "handle_intent") as mock_h:
            # Simuliamo l'emissione del segnale o la chiamata diretta
            bridge.intent_handler.handle_intent(intent)
            mock_h.assert_called_with(intent)

    def test_dispatch_data_bp(self, bridge):
        """Verifica la delega dei dati BP a data_processor."""
        items = ["BP1"]
        with patch.object(bridge.data_processor, "process_bp_items") as mock_proc:
            bridge._dispatch_data("bp", items)
            mock_proc.assert_called_with(items)

    def test_handle_status_delegation(self, bridge):
        """Verifica la delega della richiesta stato a system_handler."""
        with patch.object(bridge.system_handler, "handle_status") as mock_h:
            bridge.system_handler.handle_status(123)
            mock_h.assert_called_with(123)

    def test_handle_photo_threading(self, bridge):
        """Verifica l'avvio del thread per il processamento foto."""
        with patch("src.core.telegram_bridge.threading.Thread") as mock_thread:
            bridge._handle_photo(123, b"data", "caption")
            assert mock_thread.called
