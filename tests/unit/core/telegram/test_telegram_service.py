import asyncio
from unittest.mock import MagicMock, patch

import pytest
import telegram

from src.core.telegram.service import TelegramService


class TestTelegramService:
    @pytest.fixture
    def service(self):
        with patch("src.core.config_manager.load_config") as mock_config:
            mock_config.return_value = {"telegram_token": "fake_token", "telegram_chat_id": "12345"}
            return TelegramService()

    def test_init(self, service):
        assert service.app is None
        assert service.stop_event.is_set() is False

    @patch("threading.Thread")
    @patch("src.core.config_manager.load_config")
    def test_start_service(self, mock_config, mock_thread, service):
        mock_config.return_value = {"telegram_token": "TOKEN", "telegram_chat_id": "ID"}

        service.start_service()

        assert mock_thread.called
        assert service._service_thread is not None

    def test_stop_service_not_running(self, service):
        # Non deve crashare se non è in esecuzione
        service.stop_service()
        assert True

    @patch("src.core.telegram.service.Application.builder")
    def test_build_application(self, mock_builder, service):
        service._build_application("TOKEN")
        assert mock_builder.return_value.token.called

    @patch("src.core.telegram.service.get_asset_path", return_value="icon.png")
    @patch("src.core.telegram.service.asyncio.run_coroutine_threadsafe")
    def test_send_message_sync(self, mock_run, mock_icon, service):
        service.connected_chat_id = "12345"
        service.loop = MagicMock()
        service.loop.is_running.return_value = True

        service.send_message_sync("Hello")

        assert mock_run.called

    @patch("src.core.telegram.service.get_asset_path", return_value="icon.png")
    def test_check_auth(self, mock_icon, service):
        service.connected_chat_id = "12345"

        # Match
        mock_update = MagicMock()
        mock_update.effective_user.id = 12345
        res = asyncio.run(service._check_auth(mock_update))
        assert res is True

        # No match
        mock_update.effective_user.id = 999
        res = asyncio.run(service._check_auth(mock_update))
        assert res is False

    @patch("src.core.telegram.service.get_asset_path", return_value="icon.png")
    async def test_handle_error_conflict(self, mock_icon, service):
        mock_context = MagicMock()
        mock_context.error = telegram.error.Conflict("Conflict")

        await service._handle_error(None, mock_context)

        assert service.stop_event.is_set() is True
