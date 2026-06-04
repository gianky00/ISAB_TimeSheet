from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.api.telegram.handlers.commands import cmd_start, cmd_status, cmd_stop


class TestTelegramCommands:
    @pytest.mark.asyncio
    @patch("src.application.services.config_manager.load_config")
    async def test_cmd_start_already_associated_wrong_chat(self, mock_load):
        service = MagicMock()
        update = MagicMock()
        update.effective_chat.id = 456
        update.message = AsyncMock()
        mock_load.return_value = {"telegram_chat_id": "123"}

        await cmd_start(service, update, MagicMock())
        assert "[BLOCCO]" in update.message.reply_text.call_args[0][0]

    @pytest.mark.asyncio
    @patch("src.application.services.config_manager.set_config_value")
    @patch("src.application.services.config_manager.load_config")
    async def test_cmd_start_pairing_success(self, mock_load, mock_set):
        service = MagicMock()
        update = MagicMock()
        update.effective_chat.id = 123
        update.message = AsyncMock()
        mock_load.return_value = {"telegram_chat_id": "", "telegram_pairing_code": "654321"}

        context = MagicMock()
        context.args = ["654321"]

        await cmd_start(service, update, context)

        # Check that it sent the "associated" message AND the main menu
        messages = [call.args[0] for call in update.message.reply_text.call_args_list]
        assert any("associato" in m for m in messages)
        assert any("Command Center" in m for m in messages)
        assert mock_set.called

    @pytest.mark.asyncio
    async def test_cmd_status(self):
        service = MagicMock()
        service._check_auth = AsyncMock(return_value=True)
        update = MagicMock()
        update.effective_chat.id = 123

        await cmd_status(service, update, MagicMock())
        assert service.status_requested.emit.called
        assert service.status_requested.emit.call_args[0][0] == "123"

    @pytest.mark.asyncio
    async def test_cmd_stop(self):
        service = MagicMock()
        service._check_auth = AsyncMock(return_value=True)
        update = MagicMock()
        update.message = AsyncMock()

        await cmd_stop(service, update, MagicMock())
        assert service.command_received.emit.called
        args, _kwargs = service.command_received.emit.call_args
        assert args[0] == "stop_all"
        assert update.message.reply_text.called
