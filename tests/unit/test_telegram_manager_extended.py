import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.core.telegram_manager import TelegramService

class TestTelegramServiceExtended:
    @pytest.fixture
    def service(self):
        return TelegramService()

    @pytest.mark.asyncio
    async def test_nav_routing(self, service):
        # Test the navigation dispatcher
        mock_query = MagicMock()
        mock_query.data = "nav_bots"
        mock_query.edit_message_text = AsyncMock()
        
        await service._handle_nav_actions("nav_bots", mock_query)
        
        # Check if it edited the message with the bots menu
        args, kwargs = mock_query.edit_message_text.call_args
        assert "🤖 *Seleziona Piattaforma*" in args[0]

    @pytest.mark.asyncio
    async def test_check_auth_failure(self, service):
        service.connected_chat_id = "999" # Expected ID
        
        mock_update = MagicMock()
        mock_update.effective_user.id = 123 # Different ID
        mock_update.message.reply_text = AsyncMock()
        
        authorized = await service._check_auth(mock_update)
        assert authorized is False
        mock_update.message.reply_text.assert_called_with("⛔ Accesso Negato")

    @pytest.mark.asyncio
    async def test_handle_text_input_db_query(self, service):
        chat_id = 12345
        service.user_states[chat_id] = "WAITING_DB_QUERY_STRUMENTALE_2024"
        
        mock_update = MagicMock()
        mock_update.effective_chat.id = chat_id
        mock_update.message.text = "fornitore rossi"
        mock_update.message.reply_chat_action = AsyncMock()
        
        # We mock the signal itself
        mock_signal = MagicMock()
        service.command_received = mock_signal
        
        await service._handle_text_input(mock_update, MagicMock())
        
        # Should emit search command
        mock_signal.emit.assert_called_once()
        args = mock_signal.emit.call_args[0]
        assert args[0] == "search_db_pdf"
        assert args[1]["query"] == "fornitore rossi"
        assert args[1]["year"] == "2024"
        assert service.user_states[chat_id] is None

    @pytest.mark.asyncio
    async def test_utility_actions_status(self, service):
        mock_query = MagicMock()
        chat_id = "123"
        
        mock_signal = MagicMock()
        service.status_requested = mock_signal
        
        await service._handle_utility_actions("status", mock_query, chat_id)
        mock_signal.emit.assert_called_with(chat_id)
