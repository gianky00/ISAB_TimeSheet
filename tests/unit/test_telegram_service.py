from unittest.mock import AsyncMock, MagicMock

import pytest
from telegram import Message, Update, User
from telegram.ext import ContextTypes

from src.core.telegram_manager import TelegramService


@pytest.fixture
def mock_config(mocker):
    """Mock config manager to return a test token and chat id."""
    mock_conf = mocker.patch("src.core.config_manager.load_config")
    mock_conf.return_value = {"telegram_token": "TEST_TOKEN", "telegram_chat_id": "123456789"}
    return mock_conf


@pytest.fixture
def telegram_service(mock_config):
    """Fixture for TelegramService."""
    service = TelegramService()
    # Mock loop to avoid real asyncio loop creation in tests unless needed
    service.loop = AsyncMock()
    service.app = AsyncMock()
    service.connected_chat_id = "123456789"  # Manually set from config
    return service


@pytest.mark.asyncio
async def test_check_auth_success(telegram_service):
    """Test auth success when chat_id matches."""
    update = MagicMock(spec=Update)
    update.effective_user = MagicMock(spec=User)
    update.effective_user.id = 123456789

    # Needs to be awaited
    result = await telegram_service._check_auth(update)
    assert result is True


@pytest.mark.asyncio
async def test_check_auth_failure(telegram_service):
    """Test auth failure when chat_id mismatch."""
    update = MagicMock(spec=Update)
    update.effective_user = MagicMock(spec=User)
    update.effective_user.id = 987654321
    update.message = AsyncMock(spec=Message)  # Mock async reply_text

    result = await telegram_service._check_auth(update)
    assert result is False
    update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_cmd_start(telegram_service):
    """Test start command."""
    update = MagicMock(spec=Update)
    update.effective_user.id = 123456789
    update.message = AsyncMock(spec=Message)

    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    await telegram_service._cmd_start(update, context)
    update.message.reply_text.assert_called_once()
    args = update.message.reply_text.call_args
    assert "SyncroJob Command Center" in args[0][0]


@pytest.mark.asyncio
async def test_handle_button_menu_main(telegram_service):
    """Test callback query handling."""
    update = MagicMock(spec=Update)
    update.effective_user = MagicMock(spec=User)
    update.effective_user.id = 123456789

    query = AsyncMock()
    query.data = "menu_main"
    # Use spec=Message to pass isinstance check in code
    query.message = MagicMock(spec=Message)
    query.message.chat_id = 123456789
    update.callback_query = query

    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    await telegram_service._handle_button(update, context)

    query.answer.assert_called_once()
    query.edit_message_text.assert_called_once()
    args = query.edit_message_text.call_args
    assert "Command Center" in args[0][0]
