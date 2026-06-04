from unittest.mock import AsyncMock, MagicMock

import pytest

from src.api.telegram.handlers.messages import handle_photo, handle_text_input, handle_voice


class TestTelegramMessages:
    @pytest.mark.asyncio
    async def test_handle_text_input_no_state(self):
        service = MagicMock()
        service._check_auth = AsyncMock(return_value=True)
        service.user_states = {}

        update = MagicMock()
        update.effective_chat.id = 123
        update.message.text = "Hello Bot"

        await handle_text_input(service, update, MagicMock())
        assert service.query_received.emit.called
        assert service.query_received.emit.call_args[0][0] == "123"
        assert service.query_received.emit.call_args[0][1] == "Hello Bot"

    @pytest.mark.asyncio
    async def test_handle_text_input_db_query(self):
        service = MagicMock()
        service._check_auth = AsyncMock(return_value=True)
        service.user_states = {123: "WAITING_DB_QUERY_PDL_2024"}

        update = MagicMock()
        update.effective_chat.id = 123
        update.message.text = "SearchMe"
        update.message.reply_chat_action = AsyncMock()

        await handle_text_input(service, update, MagicMock())
        assert service.command_received.emit.called
        args, _kwargs = service.command_received.emit.call_args
        assert args[0] == "search_db_pdf"
        assert args[1]["db"] == "pdl"
        assert args[1]["query"] == "SearchMe"
        assert service.user_states[123] is None

    @pytest.mark.asyncio
    async def test_handle_text_input_sequential(self):
        service = MagicMock()
        service._check_auth = AsyncMock(return_value=True)
        service.user_states = {123: "WAITING_ODA"}

        update = MagicMock()
        update.effective_chat.id = 123
        update.message.text = "ODA1, ODA2"
        update.message.reply_text = AsyncMock()

        await handle_text_input(service, update, MagicMock())
        assert service.data_received.emit.called
        assert service.data_received.emit.call_args[0][0] == "oda"
        assert service.data_received.emit.call_args[0][1] == ["ODA1", "ODA2"]

    @pytest.mark.asyncio
    async def test_handle_photo(self):
        service = MagicMock()
        service._check_auth = AsyncMock(return_value=True)

        update = MagicMock()
        update.effective_chat.id = 123
        mock_photo = MagicMock()
        mock_photo.file_id = "file123"
        update.message.photo = [mock_photo]
        update.message.caption = "My Photo"

        context = MagicMock()
        mock_file = AsyncMock()
        mock_file.download_as_bytearray.return_value = bytearray(b"fake_bytes")
        # get_file is awaited, so it must be an AsyncMock
        context.bot.get_file = AsyncMock(return_value=mock_file)

        await handle_photo(service, update, context)
        assert service.photo_received.emit.called
        assert service.photo_received.emit.call_args[0][1] == b"fake_bytes"
        assert service.photo_received.emit.call_args[0][2] == "My Photo"

    @pytest.mark.asyncio
    async def test_handle_voice(self):
        service = MagicMock()
        update = MagicMock()
        update.message.reply_text = AsyncMock()

        await handle_voice(service, update, MagicMock())
        assert "non supportati" in update.message.reply_text.call_args[0][0]
