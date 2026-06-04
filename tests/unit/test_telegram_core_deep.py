from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.api.telegram.handlers import callbacks, messages
from src.api.telegram_manager import TelegramService


class TestTelegramCoreDeep:
    @pytest.fixture
    def service(self):
        return TelegramService()

    @pytest.mark.asyncio
    async def test_handle_voice_logic(self, service):
        mock_update = MagicMock()
        mock_context = MagicMock()
        mock_update.message.reply_text = AsyncMock()

        await messages.handle_voice(service, mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        args = mock_update.message.reply_text.call_args[0][0]
        assert "non supportati" in args

    @pytest.mark.asyncio
    async def test_handle_photo_emit(self, service):
        mock_update = MagicMock()
        mock_context = MagicMock()

        with patch.object(service, "_check_auth", new_callable=AsyncMock, return_value=True):
            mock_photo = MagicMock()
            mock_photo.file_id = "photo123"
            mock_update.message.photo = [mock_photo]
            mock_update.message.caption = "test caption"

            mock_file = AsyncMock()
            mock_file.download_as_bytearray = AsyncMock(return_value=bytearray(b"fake_photo"))
            mock_context.bot.get_file = AsyncMock(return_value=mock_file)

            mock_signal = MagicMock()
            service.photo_received = mock_signal

            await messages.handle_photo(service, mock_update, mock_context)
            mock_signal.emit.assert_called_once()
            args = mock_signal.emit.call_args[0]
            assert args[2] == "test caption"

    @pytest.mark.asyncio
    async def test_handle_button_navigation_complex(self, service):
        # Test full hierarchy navigation
        mock_update = MagicMock()
        mock_context = MagicMock()
        mock_query = AsyncMock()  # Use AsyncMock directly for the query object
        mock_update.callback_query = mock_query

        # Ensure mock_query.edit_message_text is AsyncMock
        mock_query.edit_message_text = AsyncMock()
        mock_query.answer = AsyncMock()

        # Mock auth
        with patch.object(service, "_check_auth", new_callable=AsyncMock, return_value=True):
            # Nav to Utility
            mock_query.data = "nav_utility"
            await callbacks.handle_button(service, mock_update, mock_context)
            # Use any_call or verify arguments. handle_button calls various handlers.
            assert mock_query.edit_message_text.called

            # Nav to Bots
            mock_query.data = "nav_bots"
            await callbacks.handle_button(service, mock_update, mock_context)
            assert mock_query.edit_message_text.called

    def test_sync_send_methods(self, service):
        service.loop = MagicMock()
        service.loop.is_running.return_value = True
        service.connected_chat_id = "12345"
        service.app = MagicMock()

        with patch("asyncio.run_coroutine_threadsafe") as mock_run:
            service.send_message_sync("Test msg")
            mock_run.assert_called_once()

            service.send_photo_sync(b"data", "caption")
            assert mock_run.call_count == 2
