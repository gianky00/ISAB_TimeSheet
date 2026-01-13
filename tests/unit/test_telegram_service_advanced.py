import pytest
import threading
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from src.core.telegram_manager import TelegramService
from PyQt6.QtCore import QCoreApplication

class TestTelegramServiceAdvanced:

    @pytest.fixture
    def service(self, mocker):
        """Fixture per TelegramService con config mockato."""
        mocker.patch("src.core.config_manager.load_config", return_value={
            "telegram_token": "FAKE_TOKEN",
            "telegram_chat_id": "12345"
        })
        return TelegramService()

    def test_start_stop_service_logic(self, service, mocker):
        """Test: Avvio e arresto del thread di servizio."""
        mock_thread = mocker.patch("threading.Thread")
        
        service.start_service()
        assert mock_thread.called
        
        # Simuliamo thread vivo per stop
        service.thread = MagicMock()
        service.thread.is_alive.return_value = True
        
        service.stop_event = threading.Event()
        service.stop_service()
        assert service.stop_event.is_set()

    @pytest.mark.asyncio
    async def test_check_auth_success(self, service):
        """Test: Autorizzazione riuscita per chat_id configurato."""
        service.connected_chat_id = "12345"
        mock_update = MagicMock()
        mock_update.effective_user.id = 12345
        
        res = await service._check_auth(mock_update)
        assert res is True

    @pytest.mark.asyncio
    async def test_check_auth_denied(self, service):
        """Test: Autorizzazione negata per chat_id sconosciuto."""
        service.connected_chat_id = "12345"
        mock_update = MagicMock()
        mock_update.effective_user.id = 99999
        mock_update.message.reply_text = AsyncMock()
        
        res = await service._check_auth(mock_update)
        assert res is False
        assert mock_update.message.reply_text.called

    @pytest.mark.asyncio
    async def test_cmd_start_association(self, service, mocker):
        """Test: Associazione automatica del primo chat_id al comando /start."""
        service.connected_chat_id = None # Reset
        mock_set_config = mocker.patch("src.core.config_manager.set_config_value")
        
        mock_update = MagicMock()
        mock_update.effective_chat.id = 55555
        mock_update.message.reply_text = AsyncMock()
        
        await service._cmd_start(mock_update, MagicMock())
        
        assert service.connected_chat_id == "55555"
        mock_set_config.assert_called_with("telegram_chat_id", "55555")

    @pytest.mark.asyncio
    async def test_handle_text_input_state_machine(self, service):
        """Test: Gestione input testuale basato sullo stato (es. WAITING_PDL)."""
        chat_id = 12345
        service.connected_chat_id = "12345"
        service.user_states[chat_id] = "WAITING_PDL"
        
        mock_update = MagicMock()
        mock_update.effective_chat.id = chat_id
        mock_update.effective_user.id = chat_id
        mock_update.message.text = "PDL1, PDL2"
        mock_update.message.reply_text = AsyncMock()
        
        # Mock del segnale
        mock_signal = MagicMock()
        service.data_received.connect(mock_signal)
        
        await service._handle_text_input(mock_update, MagicMock())
        
        mock_signal.assert_called_with("pdl", ["PDL1", "PDL2"])
        assert service.user_states[chat_id] is None

    @pytest.mark.asyncio
    async def test_cmd_status_emits_signal(self, service):
        """Test: Il comando /status emette il segnale PyQt."""
        service.connected_chat_id = "12345"
        mock_update = MagicMock()
        mock_update.effective_chat.id = 12345
        mock_update.effective_user.id = 12345
        
        mock_signal = MagicMock()
        service.status_requested.connect(mock_signal)
        
        await service._cmd_status(mock_update, MagicMock())
        
        mock_signal.assert_called_with("12345")