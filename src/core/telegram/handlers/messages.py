import json
import re
from contextlib import suppress

from telegram import Update
from telegram.ext import ContextTypes

from src.core.secrets_manager import SecretsManager
from src.core.telegram.ui.keyboards import TelegramUI


async def handle_text_input(service, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Main router for incoming text messages.
    Routes based on current user state (DB query, wizard) or passes to NLU.
    """
    if (
        not await service._check_auth(update)
        or not update.effective_chat
        or not update.message
        or not update.message.text
    ):
        return

    chat_id = update.effective_chat.id
    state = service.user_states.get(chat_id)
    text = update.message.text

    # 1. Gestione Ricerca DB
    if isinstance(state, str) and state.startswith("WAITING_DB_QUERY_"):
        await _handle_db_query_input(service, chat_id, state, text, update)
        return

    # 2. Gestione Intenti NLU (senza stato)
    if not state:
        await _handle_nlu_or_query(service, chat_id, text)
        return

    # 3. Gestione Input Sequenziali (OdA, PDL, Time)
    await _handle_sequential_input(service, chat_id, state, text, update)


async def _handle_db_query_input(service, chat_id, state, text, update):
    """Processes search queries for the database browser."""
    parts = state.replace("WAITING_DB_QUERY_", "").split("_")
    params = {"db": parts[0].lower(), "query": text, "chat_id": str(chat_id)}
    if len(parts) > 1:
        params["year"] = parts[1]

    await update.message.reply_chat_action("typing")
    service.command_received.emit("search_db_pdf", params)
    service.user_states[chat_id] = None


async def _handle_nlu_or_query(service, chat_id, text):
    """Decides whether to process text as an NLU intent or a simple query."""
    keywords = ["scarica", "stampa", "avvia", "pdl", "oda", "stato", "riavvia"]
    if any(k in text.lower() for k in keywords):
        await process_with_ai(service, chat_id, text)
    else:
        service.query_received.emit(str(chat_id), text)


async def _handle_sequential_input(service, chat_id, state, text, update):
    """Handles multi-line or list inputs for specific wizards (PDL, OdA, Time)."""
    items = [i.strip() for i in text.replace(",", "\n").replace(";", "\n").split("\n") if i.strip()]
    if not items:
        return

    if state == "WAITING_PDL":
        service.data_received.emit("pdl", items)
    elif state == "WAITING_ODA":
        service.data_received.emit("oda", items)
    elif state == "WAITING_BP":
        service.data_received.emit("bp", items)
    elif state == "WAITING_AUTOPILOT_TIME":
        if re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", items[0]):
            service.command_received.emit("set_autopilot", {"time": items[0]})
        else:
            await update.message.reply_text("❌ Formato non valido. Usa HH:MM.")
            return

    service.user_states[chat_id] = None
    await update.message.reply_text("✅ Operazione completata.", reply_markup=TelegramUI.get_main_keyboard())


async def handle_voice(service, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles voice messages.
    Downloads audio and sends it to the AI processor for transcription/analysis.
    """
    if not await service._check_auth(update):
        return
    if not update.effective_chat or not update.message or not update.message.voice:
        return

    chat_id = update.effective_chat.id
    file = await context.bot.get_file(update.message.voice.file_id)
    audio_bytes = await file.download_as_bytearray()
    await update.message.reply_chat_action("typing")
    await process_with_ai(service, chat_id, bytes(audio_bytes), is_audio=True)


async def handle_photo(service, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles photo messages.
    Downloads the high-res photo and emits a 'photo_received' signal.
    """
    if not await service._check_auth(update):
        return
    if not update.effective_chat or not update.message or not update.message.photo:
        return

    chat_id = str(update.effective_chat.id)
    photo = update.message.photo[-1]
    caption = update.message.caption or ""
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = await file.download_as_bytearray()
    service.photo_received.emit(chat_id, bytes(photo_bytes), caption)


async def process_with_ai(service, chat_id, data, is_audio=False):
    """
    Submits text or audio data to the Gemini/Lyra AI engine.
    Parses the JSON response to trigger application actions or replies.
    """
    api_key = SecretsManager.get_gemini_api_key()
    if not api_key:
        service.send_message_sync("⚠️ API Key mancante per intelligenza bot.")
        return

    def run():
        try:
            from src.core.lyra_client import LyraClient

            client = LyraClient(api_key=api_key)
            if isinstance(data, str) and not is_audio:
                res = client.ask(data)
                with suppress(Exception):
                    clean = res.replace("```json", "").replace("```", "").strip()
                    intent = json.loads(clean)
                    if "action" in intent:
                        service.intent_received.emit(str(chat_id), intent)
                        return
                service.send_message_sync(f"🤖 **Lyra**: {res}")
            else:
                prompt = (
                    "Sei l'interfaccia NLU di SyncroJob. Analizza il messaggio e restituisci SOLO JSON.\n"
                    "Azioni: 'download', 'print', 'status', 'restart'.\n"
                    "Oggetti: 'pdl', 'oda', 'timbrature'.\n"
                    "Items: codici PDL (es. 123456/C o 123456 senza suffisso) o OdA.\n"
                    'JSON: {"action": "...", "object": "...", "items": [...]}'
                )
                res = client.analyze_media(data, prompt, "audio/ogg")
                with suppress(Exception):
                    clean = res.replace("```json", "").replace("```", "").strip()
                    intent = json.loads(clean)
                    service.intent_received.emit(str(chat_id), intent)
        except Exception as e:
            service.send_message_sync(f"❌ Errore AI: {e}")

    service.ai_executor.submit(run)
