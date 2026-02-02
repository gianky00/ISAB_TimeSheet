from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import telegram

from src.core.telegram_manager import TelegramService


class TestTelegramServiceAdvanced:
    @pytest.fixture
    def service(self, mocker):
        """Fixture per TelegramService con config mockato."""
        mocker.patch(
            "src.core.config_manager.load_config",
            return_value={"telegram_token": "FAKE_TOKEN", "telegram_chat_id": "12345"},
        )
        return TelegramService()

    def test_start_stop_service_logic(self, service, mocker):
        """Test: Avvio e arresto del thread di servizio."""
        mock_thread = mocker.patch("threading.Thread")

        service.start_service()
        assert mock_thread.called

        service.stop_event.set()  # Simulate stop
        service.stop_service()
        assert service.stop_event.is_set()

    @pytest.mark.asyncio
    async def test_handle_error_conflict(self, service):
        """Test: Gestione errore Conflict Telegram."""
        context = MagicMock()
        context.error = MagicMock()
        # Simula telegram.error.Conflict senza importarlo se possibile, o usa patch
        with patch("telegram.error.Conflict", Exception):
            from telegram.error import Conflict

            context.error = Conflict("test")
            service.stop_event = MagicMock()
            service.log_signal = MagicMock()

            await service._handle_error(None, context)

            service.stop_event.set.assert_called_once()
            service.log_signal.emit.assert_called()

    @pytest.mark.asyncio
    async def test_send_photo_async(self, service):
        """Test invio foto asincrono."""
        service.app = AsyncMock()
        service.app.bot = AsyncMock()

        await service._send_photo_async("123", b"photo", "caption")
        service.app.bot.send_photo.assert_called_with(
            chat_id="123",
            photo=b"photo",
            caption="caption",
            parse_mode=telegram.constants.ParseMode.MARKDOWN,
        )

    @pytest.mark.asyncio
    async def test_send_document_async(self, service):
        """Test invio documento asincrono."""
        service.app = AsyncMock()
        service.app.bot = AsyncMock()

        mock_file = MagicMock()
        # Mock context manager behavior
        mock_file.__enter__.return_value = mock_file
        mock_file.__exit__.return_value = None

        with patch("builtins.open", return_value=mock_file):
            await service._send_document_async("123", "dummy.pdf", "caption")
            
            service.app.bot.send_document.assert_called_with(
                chat_id="123",
                document=mock_file,
                caption="caption",
                parse_mode=telegram.constants.ParseMode.MARKDOWN,
            )
