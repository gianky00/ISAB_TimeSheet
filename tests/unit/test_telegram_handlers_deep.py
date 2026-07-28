from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.api.telegram.handlers import callbacks
from src.application.services.telegram_manager import TelegramService


@pytest.fixture
def service():
    s = TelegramService()
    s.connected_chat_id = "123"
    return s


class TestTelegramHandlersDeep:
    @pytest.mark.asyncio
    async def test_db_actions_strumentale_flow(self, service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()

        # Test year selection
        with patch(
            "src.application.services.contabilita_manager.ContabilitaManager.get_available_years",
            return_value=[2024],
        ):
            await callbacks._handle_db_actions(service, "db_select_year_strumentale", mock_query, "123")

            # Check if Anno is in the response text
            args, kwargs = mock_query.edit_message_text.call_args
            text = args[0] if args else kwargs.get("text", "")
            assert "Anno" in text

            # Check keyboard
            markup = kwargs.get("reply_markup")
            found_2024 = False
            for row in markup.inline_keyboard:
                for btn in row:
                    if "2024" in btn.callback_data:
                        found_2024 = True
            assert found_2024

    @pytest.mark.asyncio
    async def test_utility_maintenance_actions(self, service):
        mock_query = MagicMock()
        mock_query.edit_message_text = AsyncMock()

        # Maintenance menu
        await callbacks._handle_utility_actions(service, "menu_power", mock_query, "123")
        args, kwargs = mock_query.edit_message_text.call_args
        text = args[0] if args else kwargs.get("text", "")
        assert "Manutenzione" in text

        # Stop all command - connect to signal instead of patching emit
        mock_slot = MagicMock()
        service.command_received.connect(mock_slot)

        await callbacks._handle_utility_actions(service, "stop_all", mock_query, "123")
        mock_slot.assert_called_with("stop_all", {})
