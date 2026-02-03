from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtCore import QRect

from src.core.telegram_bridge import TelegramUIBridge


class TestTelegramUIBridgeRobust:
    @pytest.fixture
    def mock_mw(self):
        mw = MagicMock()
        mw.telegram = MagicMock()
        # Assicuriamoci che app e bot siano mockati per evitare crash su attributi mancanti
        mw.telegram.app = MagicMock()
        mw.telegram.app.bot = MagicMock()
        mw.telegram.loop = MagicMock()
        mw.telegram.pending_data = {}  # Dizionario reale per supportare operazioni 'in'
        mw.pdl_panel = MagicMock()
        mw.scarico_panel = MagicMock()
        return mw

    @pytest.fixture
    def bridge(self, mock_mw):
        return TelegramUIBridge(mock_mw)

    def test_handle_intent_add_pdl(self, bridge):
        intent = {"action": "add", "object": "pdl", "items": ["12345", "67890"]}

        with patch("src.utils.validators.InputValidator.validate_pdl") as mock_val:
            mock_val.side_effect = lambda x: MagicMock(valid=True, sanitized_value=x)
            bridge._handle_intent("chat_id", intent)
            bridge.mw.pdl_panel.add_rows_simple.assert_called_once()

    @patch("src.core.telegram_bridge.asyncio.run_coroutine_threadsafe")
    @patch("src.core.telegram_bridge.get_installed_printers", return_value=["Printer1"])
    def test_handle_intent_print_pdl(self, mock_printers, mock_run_safe, bridge):
        intent = {"action": "print", "object": "pdl", "items": ["123"]}

        # chat_id deve essere un intero o stringa convertibile
        bridge._handle_intent(123, intent)

        assert 123 in bridge.telegram.pending_data
        mock_run_safe.assert_called()

    def test_handle_intent_download_generic(self, bridge):
        intent = {"action": "download", "object": "unknown"}

        bridge._handle_intent(123, intent)

        bridge.telegram.send_message_sync.assert_called()
        # Verifica che il messaggio contenga l'errore atteso
        args = bridge.telegram.send_message_sync.call_args[0][0]
        assert "Non so come scaricare" in args

    @patch("src.core.telegram_bridge.QGuiApplication")
    @patch("src.core.telegram_bridge.QPainter")
    @patch("src.core.telegram_bridge.QPixmap")
    @patch("src.core.telegram_bridge.QBuffer")
    def test_handle_screenshot(
        self, mock_buffer_cls, mock_pixmap_cls, mock_painter_cls, mock_qgui_app, bridge
    ):
        # Setup mocks for desktop screenshot path (when mode != "app")
        mock_screen = MagicMock()
        mock_screen.geometry.return_value = QRect(0, 0, 100, 100)
        mock_qgui_app.screens.return_value = [mock_screen]

        mock_pixmap_instance = MagicMock()
        mock_pixmap_cls.return_value = mock_pixmap_instance

        mock_buffer = MagicMock()
        mock_buffer_cls.return_value = mock_buffer
        mock_buffer.data.return_value.data.return_value = b"fake_png_data"

        # Call with argument that triggers the 'else' branch (not "app")
        bridge._handle_screenshot("chat_id")

        bridge.telegram.send_photo_sync.assert_called()
        assert "Desktop" in bridge.telegram.send_photo_sync.call_args[1]["caption"]
