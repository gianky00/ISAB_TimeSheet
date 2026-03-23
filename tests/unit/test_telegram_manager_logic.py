from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from telegram import Chat, Message, Update, User

from src.core.telegram_manager import TelegramService


@pytest.fixture
def telegram_service():
    service = TelegramService()
    service.connected_chat_id = "12345"
    return service


@pytest.fixture
def mock_update():
    update = MagicMock(spec=Update)
    user = MagicMock(spec=User)
    user.id = 12345
    update.effective_user = user

    chat = MagicMock(spec=Chat)
    chat.id = 12345
    update.effective_chat = chat

    message = MagicMock(spec=Message)
    message.text = "test"
    message.reply_text = AsyncMock()
    message.reply_chat_action = AsyncMock()
    update.message = message

    return update


class TestTelegramManagerLogic:
    def test_initialization(self, telegram_service):  # noqa: ANN001
        assert telegram_service.connected_chat_id == "12345"
        assert telegram_service.user_states == {}

    @pytest.mark.asyncio
    async def test_auth_success(self, telegram_service, mock_update):  # noqa: ANN001
        result = await telegram_service._check_auth(mock_update)
        assert result is True

    @pytest.mark.asyncio
    async def test_auth_fail(self, telegram_service, mock_update):  # noqa: ANN001
        mock_update.effective_user.id = 99999
        result = await telegram_service._check_auth(mock_update)
        assert result is False
        mock_update.message.reply_text.assert_called_with("⛔ Accesso Negato")

    @pytest.mark.asyncio
    async def test_cmd_stop(self, telegram_service, mock_update):  # noqa: ANN001
        from src.core.telegram.handlers import commands  # noqa: PLC0415

        mock_signal = MagicMock()
        telegram_service.command_received.connect(mock_signal)

        await commands.cmd_stop(telegram_service, mock_update, None)

        mock_signal.assert_called_with("stop_all", {})
        mock_update.message.reply_text.assert_called()

    @pytest.mark.asyncio
    async def test_handle_text_input_waiting_pdl(self, telegram_service, mock_update):  # noqa: ANN001
        from src.core.telegram.handlers import messages  # noqa: PLC0415

        chat_id = mock_update.effective_chat.id
        telegram_service.user_states[chat_id] = "WAITING_PDL"
        mock_update.message.text = "123456\n789012"

        mock_signal = MagicMock()
        telegram_service.data_received.connect(mock_signal)

        await messages.handle_text_input(telegram_service, mock_update, None)

        mock_signal.assert_called_with("pdl", ["123456", "789012"])
        assert telegram_service.user_states[chat_id] is None

    @pytest.mark.asyncio
    async def test_handle_text_input_query(self, telegram_service, mock_update):  # noqa: ANN001
        from src.core.telegram.handlers import messages  # noqa: PLC0415

        chat_id = mock_update.effective_chat.id
        telegram_service.user_states[chat_id] = None
        mock_update.message.text = "How are you?"

        mock_signal = MagicMock()
        telegram_service.query_received.connect(mock_signal)

        await messages.handle_text_input(telegram_service, mock_update, None)

        mock_signal.assert_called_with(str(chat_id), "How are you?")

    @pytest.mark.asyncio
    async def test_handle_text_input_query_emission(self, telegram_service, mock_update):  # noqa: ANN001
        from src.core.telegram.handlers import messages  # noqa: PLC0415

        chat_id = mock_update.effective_chat.id
        telegram_service.user_states[chat_id] = None
        mock_update.message.text = "Scarica PDL 123"

        mock_signal = MagicMock()
        telegram_service.query_received.connect(mock_signal)

        await messages.handle_text_input(telegram_service, mock_update, None)
        mock_signal.assert_called_with(str(chat_id), "Scarica PDL 123")

    @pytest.mark.asyncio
    async def test_handle_nav_actions_main(self, telegram_service):  # noqa: ANN001
        from src.core.telegram.handlers import callbacks  # noqa: PLC0415

        mock_query = AsyncMock()
        mock_query.data = "menu_main"

        update = MagicMock()
        update.callback_query = mock_query
        update.effective_user.id = 12345
        update.effective_chat.id = 12345

        await callbacks.handle_button(telegram_service, update, MagicMock())

        mock_query.edit_message_text.assert_called()
        kwargs = mock_query.edit_message_text.call_args[1]
        assert "🤖 Bot" in str(kwargs["reply_markup"])

    @pytest.mark.asyncio
    async def test_handle_nav_actions_bots(self, telegram_service):  # noqa: ANN001
        from src.core.telegram.handlers import callbacks  # noqa: PLC0415

        mock_query = AsyncMock()
        mock_query.data = "nav_bots"

        update = MagicMock()
        update.callback_query = mock_query
        update.effective_user.id = 12345
        update.effective_chat.id = 12345

        await callbacks.handle_button(telegram_service, update, MagicMock())

        kwargs = mock_query.edit_message_text.call_args[1]
        assert "SafeWork" in str(kwargs["reply_markup"])

    @pytest.mark.asyncio
    async def test_handle_db_actions_strumentale(self, telegram_service):  # noqa: ANN001
        from src.core.telegram.handlers import callbacks  # noqa: PLC0415

        mock_query = AsyncMock()
        mock_query.data = "db_select_year_strumentale"

        update = MagicMock()
        update.callback_query = mock_query
        update.effective_user.id = 12345
        update.effective_chat.id = 12345

        with patch(
            "src.core.telegram.handlers.callbacks.ContabilitaManager.get_available_years",
            return_value=[2024],
        ):
            await callbacks.handle_button(telegram_service, update, MagicMock())
            text = mock_query.edit_message_text.call_args[0][0]
            assert "Seleziona Anno" in text

    @pytest.mark.asyncio
    async def test_handle_utility_actions_status(self, telegram_service):  # noqa: ANN001
        from src.core.telegram.handlers import callbacks  # noqa: PLC0415

        mock_query = AsyncMock()
        mock_query.data = "status"

        update = MagicMock()
        update.callback_query = mock_query
        update.effective_user.id = 12345
        update.effective_chat.id = 12345

        mock_signal = MagicMock()
        telegram_service.status_requested.connect(mock_signal)

        await callbacks.handle_button(telegram_service, update, MagicMock())
        mock_signal.assert_called_with("12345")

    @pytest.mark.asyncio
    async def test_handle_button_dispatcher(self, telegram_service, mock_update):  # noqa: ANN001
        from src.core.telegram.handlers import callbacks  # noqa: PLC0415

        mock_query = AsyncMock()
        mock_query.data = "nav_bots"
        mock_update.callback_query = mock_query
        mock_update.effective_user.id = 12345
        mock_update.effective_chat.id = 12345

        # We can just test the effect of handle_button
        await callbacks.handle_button(telegram_service, mock_update, MagicMock())
        mock_query.edit_message_text.assert_called()
        assert "SafeWork" in str(mock_query.edit_message_text.call_args[1]["reply_markup"])
