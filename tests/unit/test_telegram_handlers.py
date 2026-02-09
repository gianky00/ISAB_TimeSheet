from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from telegram import CallbackQuery, Chat, Message, Update, User
from telegram.ext import ContextTypes

from src.core.telegram.handlers.callbacks import handle_button
from src.core.telegram.handlers.commands import cmd_start, cmd_status, cmd_stop
from src.core.telegram.handlers.messages import (
    handle_photo,
    handle_text_input,
    handle_voice,
)


class TestTelegramHandlers:
    @pytest.fixture
    def mock_update(self):
        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 12345
        update.effective_user.first_name = "TestUser"
        update.effective_chat = MagicMock(spec=Chat)
        update.effective_chat.id = 67890
        update.message = MagicMock(spec=Message)
        update.message.text = ""
        update.message.reply_text = AsyncMock()
        update.message.reply_photo = AsyncMock()
        update.message.reply_chat_action = AsyncMock()
        return update

    @pytest.fixture
    def mock_context(self):
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        context.user_data = {}
        context.args = []
        # Mock bot for get_file
        context.bot.get_file = AsyncMock()
        return context

    @pytest.fixture
    def mock_service(self):
        service = MagicMock()
        service.user_states = {}
        service.pdl_settings = {}
        service.connected_chat_id = "12345"  # match effective_user.id for tests
        # Mock signals
        service.command_received.emit = MagicMock()
        service.status_requested.emit = MagicMock()
        service.screenshot_requested.emit = MagicMock()
        service.query_received.emit = MagicMock()
        service.data_received.emit = MagicMock()
        service.photo_received.emit = MagicMock()
        service.intent_received.emit = MagicMock()
        service.ai_executor.submit = MagicMock()

        # Async check_auth mock
        service._check_auth = AsyncMock(return_value=True)
        return service

    # --- Commands ---
    @patch("src.core.config_manager.load_config")
    @patch("src.core.config_manager.set_config_value")
    @pytest.mark.asyncio
    async def test_cmd_start_new_pairing(self, mock_set, mock_load, mock_service, mock_update, mock_context):
        # Case: No saved ID, pairing code matches
        mock_load.return_value = {
            "telegram_chat_id": "",
            "telegram_pairing_code": "123456",
        }
        mock_context.args = ["123456"]

        await cmd_start(mock_service, mock_update, mock_context)

        mock_update.message.reply_text.assert_called()
        assert mock_service.connected_chat_id == "67890"  # effective_chat.id

    @patch("src.core.config_manager.load_config")
    @pytest.mark.asyncio
    async def test_cmd_start_already_paired(self, mock_load, mock_service, mock_update, mock_context):
        # Case: Saved ID matches
        mock_load.return_value = {"telegram_chat_id": "67890"}

        await cmd_start(mock_service, mock_update, mock_context)

        mock_update.message.reply_text.assert_called()
        args = mock_update.message.reply_text.call_args[0][0]
        assert "SyncroJob Command Center" in args

    @pytest.mark.asyncio
    async def test_cmd_status(self, mock_service, mock_update, mock_context):
        await cmd_status(mock_service, mock_update, mock_context)
        mock_service.status_requested.emit.assert_called_with("67890")

    @pytest.mark.asyncio
    async def test_cmd_stop(self, mock_service, mock_update, mock_context):
        await cmd_stop(mock_service, mock_update, mock_context)
        mock_service.command_received.emit.assert_called_with("stop_all", {})

    # --- Messages ---
    @pytest.mark.asyncio
    async def test_handle_text_input_simple_query(self, mock_service, mock_update, mock_context):
        mock_update.message.text = "Hello world"
        # Mock user state None
        mock_service.user_states = {"67890": None}

        await handle_text_input(mock_service, mock_update, mock_context)

        # Should emit query_received
        mock_service.query_received.emit.assert_called_with("67890", "Hello world")

    @pytest.mark.asyncio
    async def test_handle_text_input_pdl_state(self, mock_service, mock_update, mock_context):
        mock_update.message.text = "123456"
        mock_service.user_states = {67890: "WAITING_PDL"}

        await handle_text_input(mock_service, mock_update, mock_context)

        mock_service.data_received.emit.assert_called_with("pdl", ["123456"])
        assert mock_service.user_states[67890] is None

    @patch("src.core.telegram.handlers.messages.process_with_ai")
    @pytest.mark.asyncio
    async def test_handle_voice(self, mock_process_ai, mock_service, mock_update, mock_context):
        mock_update.message.voice = MagicMock()
        mock_update.message.voice.file_id = "voice_id"

        mock_file = AsyncMock()
        mock_file.download_as_bytearray = AsyncMock(return_value=b"audio data")
        mock_context.bot.get_file.return_value = mock_file

        await handle_voice(mock_service, mock_update, mock_context)

        mock_process_ai.assert_called_once()
        # Verify call args if needed

    @pytest.mark.asyncio
    async def test_handle_photo(self, mock_service, mock_update, mock_context):
        mock_update.message.photo = [MagicMock(file_id="p1")]
        mock_update.message.caption = "Test caption"

        mock_file = AsyncMock()
        mock_file.download_as_bytearray = AsyncMock(return_value=b"photo bytes")
        mock_context.bot.get_file.return_value = mock_file

        await handle_photo(mock_service, mock_update, mock_context)

        mock_service.photo_received.emit.assert_called_with("67890", b"photo bytes", "Test caption")

    # --- Callbacks ---
    @pytest.mark.asyncio
    async def test_handle_button_menu(self, mock_service, mock_update, mock_context):
        query = MagicMock(spec=CallbackQuery)
        query.data = "menu_main"
        query.answer = AsyncMock()
        query.edit_message_text = AsyncMock()
        query.message = MagicMock()
        mock_update.callback_query = query

        # Mock effective user id matches connected id
        mock_update.effective_user.id = 12345
        mock_service.connected_chat_id = "12345"

        await handle_button(mock_service, mock_update, mock_context)

        query.edit_message_text.assert_called()
        args = query.edit_message_text.call_args[0][0]
        assert "Command Center" in args

    @pytest.mark.asyncio
    async def test_handle_button_direct_command(self, mock_service, mock_update, mock_context):
        query = MagicMock(spec=CallbackQuery)
        query.data = "run_ts"
        query.answer = AsyncMock()
        query.message = MagicMock()
        mock_update.callback_query = query

        await handle_button(mock_service, mock_update, mock_context)

        mock_service.command_received.emit.assert_called_with("run_ts", {})
