import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from telegram import Update, Message, User, Chat, CallbackQuery
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
    def test_initialization(self, telegram_service):
        assert telegram_service.connected_chat_id == "12345"
        assert telegram_service.user_states == dict()

    @pytest.mark.asyncio
    async def test_auth_success(self, telegram_service, mock_update):
        result = await telegram_service._check_auth(mock_update)
        assert result is True

    @pytest.mark.asyncio
    async def test_auth_fail(self, telegram_service, mock_update):
        mock_update.effective_user.id = 99999
        result = await telegram_service._check_auth(mock_update)
        assert result is False
        mock_update.message.reply_text.assert_called_with("⛔ Accesso Negato")

    @pytest.mark.asyncio
    async def test_cmd_stop(self, telegram_service, mock_update):
        mock_signal = MagicMock()
        telegram_service.command_received.connect(mock_signal)
        
        await telegram_service._cmd_stop(mock_update, None)
        
        mock_signal.assert_called_with("stop_all", dict())
        mock_update.message.reply_text.assert_called()

    @pytest.mark.asyncio
    async def test_handle_text_input_waiting_pdl(self, telegram_service, mock_update):
        chat_id = mock_update.effective_chat.id
        telegram_service.user_states[chat_id] = "WAITING_PDL"
        mock_update.message.text = "123456\n789012"
        
        mock_signal = MagicMock()
        telegram_service.data_received.connect(mock_signal)
        
        await telegram_service._handle_text_input(mock_update, None)
        
        mock_signal.assert_called_with("pdl", ["123456", "789012"])
        assert telegram_service.user_states[chat_id] is None

    @pytest.mark.asyncio
    async def test_handle_text_input_query(self, telegram_service, mock_update):
        chat_id = mock_update.effective_chat.id
        telegram_service.user_states[chat_id] = None
        mock_update.message.text = "How are you?"
        
        mock_signal = MagicMock()
        telegram_service.query_received.connect(mock_signal)
        
        await telegram_service._handle_text_input(mock_update, None)
        
        mock_signal.assert_called_with(str(chat_id), "How are you?")

    @pytest.mark.asyncio
    async def test_handle_text_input_ai_trigger(self, telegram_service, mock_update):
        chat_id = mock_update.effective_chat.id
        telegram_service.user_states[chat_id] = None
        mock_update.message.text = "Scarica PDL 123"
        
        with patch.object(telegram_service, "_process_with_ai", new_callable=AsyncMock) as mock_ai:
            await telegram_service._handle_text_input(mock_update, None)
            mock_ai.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_nav_actions_main(self, telegram_service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()
        
        await telegram_service._handle_nav_actions("menu_main", mock_query)
        assert mock_query.edit_message_text.called
        kwargs = mock_query.edit_message_text.call_args[1]
        assert "🤖 Bot" in str(kwargs["reply_markup"])

    @pytest.mark.asyncio
    async def test_handle_nav_actions_bots(self, telegram_service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()
        
        await telegram_service._handle_nav_actions("nav_bots", mock_query)
        kwargs = mock_query.edit_message_text.call_args[1]
        assert "SafeWork" in str(kwargs["reply_markup"])

    @pytest.mark.asyncio
    async def test_handle_db_actions_strumentale(self, telegram_service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()
        
        with patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2024]):
            await telegram_service._handle_db_actions("db_select_year_strumentale", mock_query, 12345)
            text = mock_query.edit_message_text.call_args[0][0]
            assert "Seleziona Anno" in text

    @pytest.mark.asyncio
    async def test_handle_utility_actions_status(self, telegram_service):
        mock_query = MagicMock()
        mock_signal = MagicMock()
        telegram_service.status_requested.connect(mock_signal)
        
        await telegram_service._handle_utility_actions("status", mock_query, "12345")
        mock_signal.assert_called_with("12345")

    @pytest.mark.asyncio
    async def test_handle_button_dispatcher(self, telegram_service, mock_update):
        with patch.object(telegram_service, "_handle_nav_actions", new_callable=AsyncMock) as mock_nav, \
             patch.object(telegram_service, "_handle_db_actions", new_callable=AsyncMock) as mock_db:
            
            # Create a real Message and CallbackQuery object if possible, or mock properly
            # We use a trick to pass isinstance(..., Message) by patching Message
            with patch("src.core.telegram_manager.Message", MagicMock):
                query = MagicMock(spec=CallbackQuery)
                query.data = "nav_bots"
                query.answer = AsyncMock()
                query.message = MagicMock() # Will pass isinstance because we patched Message
                
                mock_update.callback_query = query
                mock_update.effective_user.id = 12345
                
                await telegram_service._handle_button(mock_update, None)
                mock_nav.assert_called_once()
                
                query.data = "db_info"
                await telegram_service._handle_button(mock_update, None)
                mock_db.assert_called_once()
