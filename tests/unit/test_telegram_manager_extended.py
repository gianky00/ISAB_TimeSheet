from unittest.mock import AsyncMock, MagicMock

import pytest
from telegram import Update, User

from src.core.telegram_manager import TelegramService


class TestTelegramManagerExtended:
    @pytest.fixture
    def service(self):
        return TelegramService()

    @pytest.mark.asyncio
    async def test_check_auth_denied(self, service):
        """Verifica che l'accesso venga negato per chat_id non autorizzati."""
        service.connected_chat_id = "12345"

        mock_user = MagicMock(spec=User)
        mock_user.id = 99999
        mock_update = MagicMock(spec=Update)
        mock_update.effective_user = mock_user
        mock_update.message = AsyncMock()

        res = await service._check_auth(mock_update)
        assert res is False
        mock_update.message.reply_text.assert_called_with("⛔ Accesso Negato")

    @pytest.mark.asyncio
    async def test_handle_text_input_db_query_state(self, service, mocker):
        """Verifica la transizione di stato per una ricerca DB."""
        service.connected_chat_id = "123"
        chat_id = 123
        service.user_states[chat_id] = "WAITING_DB_QUERY_STRUMENTALE_2024"

        mock_update = MagicMock(spec=Update)
        mock_user = MagicMock(spec=User)
        mock_user.id = 123
        mock_update.effective_user = mock_user
        mock_update.effective_chat.id = chat_id
        mock_update.message.text = "Ricerca test"
        mock_update.message.reply_chat_action = AsyncMock()

        # Mock signal
        mock_signal = mocker.patch.object(service.command_received, "emit")

        await service._handle_text_input(mock_update, MagicMock())

        mock_signal.assert_called_once()
        args = mock_signal.call_args[0]
        assert args[0] == "search_db_pdf"
        assert args[1]["db"] == "strumentale"
        assert args[1]["query"] == "Ricerca test"
        assert args[1]["year"] == "2024"
        assert service.user_states[chat_id] is None

    @pytest.mark.asyncio
    async def test_process_with_ai_intent_detection(self, service, mocker):
        """Verifica che l'AI riconosca un intento JSON e emetta il segnale."""
        service.connected_chat_id = "123"
        chat_id = 123

        # Mock LyraClient
        mock_client = MagicMock()
        mock_client.ask.return_value = '{"action": "download", "object": "pdl", "items": ["12345"]}'
        mocker.patch("src.core.lyra_client.LyraClient", return_value=mock_client)
        mocker.patch("src.core.secrets_manager.SecretsManager.get_gemini_api_key", return_value="fake_key")

        mock_intent_signal = mocker.patch.object(service.intent_received, "emit")

        # Bypass ThreadPoolExecutor per rendere il test deterministico
        def mock_submit(fn, *args, **kwargs):
            fn() # Esegue sincronicamente nel test
            return MagicMock()

        mocker.patch.object(service.ai_executor, "submit", side_effect=mock_submit)

        await service._process_with_ai(chat_id, "scarica pdl 12345")

        mock_intent_signal.assert_called_once_with(str(chat_id), {"action": "download", "object": "pdl", "items": ["12345"]})

    @pytest.mark.asyncio
    async def test_handle_nav_actions_menu_switching(self, service):
        """Verifica lo switch tra i menu di navigazione."""
        mock_query = AsyncMock()
        mock_query.data = "nav_bots"

        await service._handle_nav_actions("nav_bots", mock_query)

        # Verifica che il testo del messaggio sia stato aggiornato con il menu bots
        args = mock_query.edit_message_text.call_args[0][0]
        assert "🤖 *Seleziona Piattaforma*" in args

    @pytest.mark.asyncio
    async def test_handle_toggle_merge_all_pdl(self, service, mocker):
        """Verifica il toggle dell'impostazione merge_all."""
        chat_id = 123
        service.pdl_settings[chat_id] = {"merge_all": False}

        mock_query = AsyncMock()
        mock_update = MagicMock()
        mock_context = MagicMock()

        # Mock _handle_button per evitare ricorsione infinita nel test
        mocker.patch.object(service, "_handle_button", new_callable=AsyncMock)

        await service._handle_toggle_merge_all_pdl(mock_query, chat_id, mock_update, mock_context)

        assert service.pdl_settings[chat_id]["merge_all"] is True
        service._handle_button.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_photo_sync_delegation(self, service, mocker):
        """Verifica che l'invio sincrono deleghi correttamente alla coroutine asincrona."""
        service.loop = MagicMock()
        service.connected_chat_id = "123"

        mock_run_threadsafe = mocker.patch("asyncio.run_coroutine_threadsafe")

        service.send_photo_sync(b"fake_data", "Caption")

        mock_run_threadsafe.assert_called_once()
