from unittest.mock import MagicMock, patch

import pytest

from src.core.telegram.service import TelegramService


class TestTelegramService:
    @pytest.fixture
    def service(self):
        return TelegramService()

    @patch("src.core.config_manager.load_config")
    @patch("src.core.telegram.service.threading.Thread")
    def test_start_service_success(self, mock_thread, mock_config, service):
        mock_config.return_value = {"telegram_token": "TOKEN", "telegram_chat_id": "123"}

        service.start_service()

        assert mock_thread.called
        assert service.connected_chat_id == "123"

    @patch("src.core.config_manager.load_config")
    def test_start_service_missing_token(self, mock_config, service):
        mock_config.return_value = {"telegram_token": ""}

        # Patch dell'intero oggetto segnale
        service.log_signal = MagicMock()
        service.start_service()

        assert any("mancante" in args[0] for args, _ in service.log_signal.emit.call_args_list)

    def test_stop_service_not_running(self, service):
        service.stop_service()
        assert not service.stop_event.is_set()

    @patch("src.core.telegram.service.asyncio.run_coroutine_threadsafe")
    def test_send_message_sync(self, mock_run, service):
        service.connected_chat_id = "123"
        service.loop = MagicMock()
        service.loop.is_running.return_value = True

        service.send_message_sync("Hello")

        assert mock_run.called

    @pytest.mark.asyncio
    async def test_check_auth(self, service):
        service.connected_chat_id = "123"

        mock_update = MagicMock()
        mock_update.effective_user.id = 123
        assert await service._check_auth(mock_update) is True

        mock_update.effective_user.id = 456
        assert await service._check_auth(mock_update) is False

    def test_build_application(self, service):
        with patch("src.core.telegram.service.Application.builder") as mock_builder:
            service._build_application("TOKEN")
            assert mock_builder.return_value.token.called
