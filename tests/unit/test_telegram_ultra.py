from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.telegram_manager import TelegramService


class TestTelegramServiceUltraFixed:
    @pytest.fixture
    def service(self):
        return TelegramService()

    @pytest.mark.asyncio
    async def test_handle_text_input_states(self, service):  # noqa: ANN001
        from src.core.telegram.handlers.messages import handle_text_input  # noqa: PLC0415

        # Create a proper Update mock with effective_user
        mock_update = MagicMock()
        mock_user = MagicMock()
        mock_user.id = 123
        mock_update.effective_user = mock_user
        mock_update.effective_chat.id = 123
        mock_update.message.text = "123456/S"
        mock_update.message.reply_text = AsyncMock()

        mock_context = MagicMock()

        # Bypass check_auth for simplicity or mock it
        with patch.object(service, "_check_auth", return_value=True):
            service.user_states[123] = "WAITING_PDL"
            mock_signal = MagicMock()
            service.data_received = mock_signal

            await handle_text_input(service, mock_update, mock_context)
            mock_signal.emit.assert_called_with("pdl", ["123456/S"])

    @pytest.mark.asyncio
    async def test_error_handling_auth_fail(self, service):  # noqa: ANN001
        mock_update = MagicMock()
        # effective_user is None
        mock_update.effective_user = None
        res = await service._check_auth(mock_update)
        assert res is False
