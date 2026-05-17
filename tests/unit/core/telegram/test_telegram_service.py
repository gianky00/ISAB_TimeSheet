from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.telegram.service import TelegramService


class TestTelegramService:
    @pytest.fixture
    def service(self):
        return TelegramService()

    @patch("src.core.config_manager.load_config")
    def test_start_service_missing_token(self, mock_load, service):
        mock_load.return_value = {"telegram_token": ""}
        mock_log = MagicMock()
        service.log_signal.connect(mock_log.emit)

        service.start_service()
        assert mock_log.emit.called
        assert "Token mancante" in mock_log.emit.call_args[0][0]

    @patch("src.core.telegram.service.threading.Thread")
    @patch("src.core.config_manager.load_config")
    def test_start_service_success(self, mock_load, mock_thread, service):
        mock_load.return_value = {"telegram_token": "valid_token", "telegram_chat_id": "123"}

        service.start_service()
        assert mock_thread.called
        assert service.connected_chat_id == "123"

    def test_stop_service_not_running(self, service):
        # Should not crash
        service.stop_service()

    @patch("src.core.telegram.service.asyncio.run_coroutine_threadsafe")
    def test_send_message_sync(self, mock_run, service):
        service.loop = MagicMock()
        service.loop.is_running.return_value = True
        service.connected_chat_id = "123"

        service.send_message_sync("hello")
        assert mock_run.called

    @pytest.mark.asyncio
    async def test_send_message_async_success(self, service):
        service.app = MagicMock()
        service.app.bot = AsyncMock()

        await service._send_message_async("123", "hello")
        assert service.app.bot.send_message.called
        _args, kwargs = service.app.bot.send_message.call_args
        assert kwargs["text"] == "hello"

    @pytest.mark.asyncio
    async def test_send_document_async_success(self, service, tmp_path):
        service.app = MagicMock()
        service.app.bot = AsyncMock()
        f = tmp_path / "test.txt"
        f.write_text("content")

        await service._send_document_async("123", str(f), "caption")
        assert service.app.bot.send_document.called
        _args, kwargs = service.app.bot.send_document.call_args
        assert kwargs["caption"] == "caption"

    @pytest.mark.asyncio
    async def test_check_auth(self, service):
        service.connected_chat_id = "123"

        # Valid user
        update = MagicMock()
        update.effective_user.id = 123
        assert await service._check_auth(update) is True

        # Invalid user
        update.effective_user.id = 456
        update.message = AsyncMock()
        assert await service._check_auth(update) is False
        assert update.message.reply_text.called

    def test_add_handlers(self, service):
        service.app = MagicMock()
        service._add_handlers()
        # verify at least some handlers are added
        assert service.app.add_handler.called
        assert service.app.add_error_handler.called
