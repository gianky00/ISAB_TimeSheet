from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from telegram import Chat, Message, Update, User
from telegram.ext import ContextTypes

from src.api.telegram.handlers import commands, messages
from src.api.telegram.service import TelegramService


class TestTelegramServiceAdvanced:
    @pytest.fixture
    def service(self, qtbot):
        # Patching QObject.__init__ to avoid event loop issues in pure unit tests
        with patch("src.api.telegram.service.QObject.__init__"):
            svc = TelegramService()
            svc.log_signal = MagicMock()
            svc.command_received = MagicMock()
            svc.data_received = MagicMock()
            svc.status_requested = MagicMock()
            svc.query_received = MagicMock()
            svc.intent_received = MagicMock()
            return svc

    @pytest.fixture
    def mock_update(self):
        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 123456
        update.effective_chat = MagicMock(spec=Chat)
        update.effective_chat.id = 123456
        update.message = MagicMock(spec=Message)
        update.message.reply_text = AsyncMock()
        update.message.reply_chat_action = AsyncMock()
        return update

    @pytest.fixture
    def mock_context(self):
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        context.args = []
        return context

    @pytest.mark.asyncio
    async def test_pairing_flow_success(self, service, mock_update, mock_context):
        """Verifica l'accoppiamento con codice OTP corretto."""
        mock_config = {"telegram_chat_id": "", "telegram_pairing_code": "999888"}
        mock_context.args = ["999888"]

        with (
            patch("src.application.services.config_manager.load_config", return_value=mock_config),
            patch("src.application.services.config_manager.set_config_value") as mock_set,
        ):
            await commands.cmd_start(service, mock_update, mock_context)

            # Verifica che il chat_id sia stato salvato
            assert service.connected_chat_id == "123456"
            mock_set.assert_any_call("telegram_chat_id", "123456")

            # Verifica che tra i messaggi inviati ci sia quello di associazione
            all_messages = [call.args[0] for call in mock_update.message.reply_text.call_args_list]
            assert any("Dispositivo associato" in msg for msg in all_messages)
            assert any("SyncroJob Command Center" in msg for msg in all_messages)

    @pytest.mark.asyncio
    async def test_pairing_flow_wrong_code(self, service, mock_update, mock_context):
        """Verifica che un codice OTP errato venga rifiutato."""
        mock_config = {"telegram_chat_id": "", "telegram_pairing_code": "999888"}
        mock_context.args = ["wrong"]

        with patch("src.application.services.config_manager.load_config", return_value=mock_config):
            await commands.cmd_start(service, mock_update, mock_context)

            assert service.connected_chat_id is None
            args, _ = mock_update.message.reply_text.call_args
            assert "Inserisci il codice" in args[0]

    @pytest.mark.asyncio
    async def test_unauthorized_user_blocked(self, service, mock_update):
        """Verifica che utenti non autorizzati siano bloccati."""
        service.connected_chat_id = "999999"  # Utente autorizzato diverso
        mock_update.effective_user.id = 123456  # Utente attuale

        is_auth = await service._check_auth(mock_update)
        assert is_auth is False
        mock_update.message.reply_text.assert_called_with("[BLOCCO] Accesso Negato")

    @pytest.mark.asyncio
    async def test_sequential_input_pdl(self, service, mock_update, mock_context):
        """Testa l'inserimento di una lista di PDL separata da virgole."""
        service.connected_chat_id = "123456"
        service.user_states[123456] = "WAITING_PDL"
        mock_update.message.text = "123456/C, 654321/S ; 111222"

        await messages.handle_text_input(service, mock_update, mock_context)

        # Dovrebbe aver emesso il segnale con la lista pulita
        service.data_received.emit.assert_called_with("pdl", ["123456/C", "654321/S", "111222"])
        assert service.user_states[123456] is None

    @pytest.mark.asyncio
    async def test_db_query_routing(self, service, mock_update, mock_context):
        """Verifica il routing delle query al database browser."""
        service.connected_chat_id = "123456"
        service.user_states[123456] = "WAITING_DB_QUERY_CONTABILITA_2025"
        mock_update.message.text = "COEMI"

        await messages.handle_text_input(service, mock_update, mock_context)

        # Dovrebbe emettere comando di ricerca con parametri corretti
        expected_params = {
            "db": "contabilita",
            "query": "COEMI",
            "chat_id": "123456",
            "year": "2025",
        }
        service.command_received.emit.assert_called_with("search_db_pdf", expected_params)

    def test_send_message_sync_safety(self, service):
        """Verifica la sicurezza del metodo di invio sincrono."""
        service.connected_chat_id = "123456"
        # Senza loop attivo non deve crashare
        service.send_message_sync("test")
        service.log_signal.emit.assert_not_called()  # Non deve loggare errore se semplicemente il loop è chiuso
