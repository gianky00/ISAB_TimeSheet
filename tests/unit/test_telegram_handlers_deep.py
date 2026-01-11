import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.core.telegram_manager import TelegramService

class TestTelegramHandlersDeep:
    @pytest.fixture
    def service(self):
        return TelegramService()

    @pytest.mark.asyncio
    async def test_bot_actions_pdl_flow(self, service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()
        
        # Test PDL Menu
        await service._handle_bot_actions("menu_pdl", mock_query, "123", MagicMock(), MagicMock())
        assert "SafeWork PDL" in mock_query.edit_message_text.call_args[0][0]
        
        # Test PDL Input state
        await service._handle_bot_actions("input_pdl", mock_query, "123", MagicMock(), MagicMock())
        assert service.user_states["123"] == "WAITING_PDL"

    @pytest.mark.asyncio
    async def test_db_actions_strumentale_flow(self, service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()
        
        # Test year selection
        with patch("src.core.contabilita_manager.ContabilitaManager.get_available_years", return_value=[2024]):
            await service._handle_db_actions("db_select_year_strumentale", mock_query, "123")
            assert "2024" in str(mock_query.edit_message_text.call_args[0][1]) # Check keyboard or text

    @pytest.mark.asyncio
    async def test_utility_maintenance_actions(self, service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()
        
        # Maintenance menu
        await service._handle_utility_actions("menu_power", mock_query, "123")
        assert "Manutenzione" in mock_query.edit_message_text.call_args[0][0]
        
        # Stop all command
        with patch.object(service.command_received, "emit") as mock_emit:
            await service._handle_utility_actions("stop_all", mock_query, "123")
            mock_emit.assert_called_with("stop_all", {})
