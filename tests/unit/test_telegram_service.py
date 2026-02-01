from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from telegram import Message, Update, User

from src.core.telegram_manager import TelegramService


@pytest.fixture
def mock_config(mocker):
    """Mock config manager to return a test token and chat id."""
    mock_conf = mocker.patch("src.core.config_manager.load_config")
    mock_conf.value = {
        "telegram_token": "TEST_TOKEN",
        "telegram_chat_id": "123456789",
    }
    mock_conf.return_value = mock_conf.value
    return mock_conf


@pytest.fixture
def telegram_service(mock_config):
    """Fixture for TelegramService."""
    with patch("PyQt6.QtCore.QObject.__init__"):
        service = TelegramService()
    service.loop = MagicMock()
    service.app = AsyncMock()
    service.app.bot = AsyncMock()
    service.connected_chat_id = "123456789"
    return service


@pytest.mark.asyncio
async def test_check_auth_success(telegram_service):
    """Test auth success when chat_id matches."""
    update = MagicMock(spec=Update)
    user = MagicMock(spec=User)
    user.id = 123456789
    update.effective_user = user

    result = await telegram_service._check_auth(update)
    assert result is True


@pytest.mark.asyncio
async def test_check_auth_failure(telegram_service):
    """Test auth failure when chat_id mismatch."""
    update = MagicMock(spec=Update)
    user = MagicMock(spec=User)
    user.id = 987654321
    update.effective_user = user
    update.message = AsyncMock(spec=Message)

    result = await telegram_service._check_auth(update)
    assert result is False
    update.message.reply_text.assert_called_once_with("⛔ Accesso Negato")


@pytest.mark.asyncio
async def test_send_message_async(telegram_service):
    """Test async message sending."""
    await telegram_service._send_message_async("123", "Hello")
    telegram_service.app.bot.send_message.assert_called_with(
        chat_id="123", text="Hello", parse_mode=None
    )


def test_send_message_sync(telegram_service):
    """Test sync message sending (delegation to loop)."""
    with patch("asyncio.run_coroutine_threadsafe") as mock_run:
        telegram_service.loop.is_running.return_value = True
        telegram_service.send_message_sync("Hello")
        mock_run.assert_called_once()
