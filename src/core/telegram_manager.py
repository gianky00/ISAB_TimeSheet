import asyncio
import json
import re
import threading

from PyQt6.QtCore import QObject, pyqtSignal
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update,
    constants,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from src.core import config_manager
from src.core.secrets_manager import SecretsManager
from src.utils.printing import get_installed_printers


class TelegramService(QObject):
    """
    Bridge intelligente tra Telegram e l'applicazione PyQt6.
    Supporta comandi vocali, NLU e dialoghi contestuali.
    """

    log_signal = pyqtSignal(str)
    command_received = pyqtSignal(str, dict)
    data_received = pyqtSignal(str, list)
    status_requested = pyqtSignal(str)
    screenshot_requested = pyqtSignal(str)
    query_received = pyqtSignal(str, str)
    photo_received = pyqtSignal(str, bytes, str)
    intent_received = pyqtSignal(str, dict)

    def __init__(self):
        super().__init__()
        self.app = None
        self.loop = None
        self.stop_event = threading.Event()
        self.thread = None
        self.connected_chat_id = None
        self.user_states = {}
        self.pending_data = {}

    def start_service(self):
        config = config_manager.load_config()
        token = config.get("telegram_token", "")
        self.connected_chat_id = config.get("telegram_chat_id", "")
        if not token:
            self.log_signal.emit("⚠️ Telegram Token mancante.")
            return
        if self.thread and self.thread.is_alive():
            self.stop_service()
            self.thread.join(timeout=2)
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run_async_loop, args=(token,), daemon=True)
        self.thread.start()

    def stop_service(self):
        if self.app and self.loop and self.loop.is_running():
            self.log_signal.emit("⏳ Arresto Telegram...")
            self.stop_event.set()
            asyncio.run_coroutine_threadsafe(self._stop_app(), self.loop)

    async def _stop_app(self):
        if self.app:
            try:
                await self.app.stop()
                await self.app.shutdown()
            except:
                pass

    def _run_async_loop(self, token):
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.app = Application.builder().token(token).build()
            self.app.add_handler(CommandHandler("start", self._cmd_start))
            self.app.add_handler(CommandHandler("status", self._cmd_status))
            self.app.add_handler(CommandHandler("stop", self._cmd_stop))
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_text_input))
            self.app.add_handler(MessageHandler(filters.PHOTO, self._handle_photo))
            self.app.add_handler(MessageHandler(filters.VOICE, self._handle_voice))
            self.app.add_handler(CallbackQueryHandler(self._handle_button))
            self.log_signal.emit("✅ Servizio Telegram Attivo")
            self.app.run_polling(drop_pending_updates=True, stop_signals=None)
        except Exception as e:
            if not self.stop_event.is_set():
                self.log_signal.emit(f"❌ Errore Telegram: {e}")
        finally:
            if self.loop and self.loop.is_running():
                self.loop.close()

    def _get_main_keyboard(self):
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🛡️ PDL", callback_data="menu_pdl"),
                    InlineKeyboardButton("📥 Scarico TS", callback_data="menu_ts"),
                ],
                [
                    InlineKeyboardButton("📋 Dettagli OdA", callback_data="menu_oda_details"),
                    InlineKeyboardButton("📤 Carico TS", callback_data="menu_carico"),
                ],
                [
                    InlineKeyboardButton("⏱️ Timbrature", callback_data="menu_timbrature"),
                    InlineKeyboardButton("📊 Stato", callback_data="status"),
                ],
                [
                    InlineKeyboardButton("📸 Screenshot", callback_data="screenshot"),
                    InlineKeyboardButton("⚙️ Impostazioni", callback_data="menu_settings"),
                ],
                [
                    InlineKeyboardButton("⚡ Manutenzione", callback_data="menu_power"),
                    InlineKeyboardButton("🛑 Stop Globale", callback_data="stop_all"),
                ],
            ]
        )

    async def _check_auth(self, update: Update) -> bool:
        if not update.effective_user:
            return False
        user_id = str(update.effective_user.id)
        if self.connected_chat_id and user_id != self.connected_chat_id:
            try:
                if update.message:
                    await update.message.reply_text("⛔ Accesso Negato")
            except:
                pass
            return False
        return True

    async def _cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_auth(update):
            return
        if update.message:
            await update.message.reply_text(
                "🚀 *SyncroJob Command Center*",
                reply_markup=self._get_main_keyboard(),
                parse_mode=constants.ParseMode.MARKDOWN,
            )

    async def _cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_auth(update):
            return
        if update.effective_chat:
            self.status_requested.emit(str(update.effective_chat.id))

    async def _cmd_stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_auth(update):
            return
        self.command_received.emit("stop_all", {})
        if update.message:
            await update.message.reply_text("🛑 *Richiesta Stop Inviata*")

    async def _handle_text_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_auth(update):
            return
        if not update.effective_chat or not update.message or not update.message.text:
            return

        chat_id = update.effective_chat.id
        state = self.user_states.get(chat_id)
        text = update.message.text
        if not state:
            cmd_keywords = ["scarica", "stampa", "avvia", "pdl", "oda", "stato", "riavvia"]
            if any(k in text.lower() for k in cmd_keywords):
                await self._process_with_ai(chat_id, text)
            else:
                self.query_received.emit(str(chat_id), text)
            return
        items = [i.strip() for i in text.replace(",", "\n").replace(";", "\n").split("\n") if i.strip()]
        if state == "WAITING_PDL":
            self.data_received.emit("pdl", items)
        elif state == "WAITING_ODA":
            self.data_received.emit("oda", items)
        elif state == "WAITING_AUTOPILOT_TIME":
            if re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", items[0]):
                self.command_received.emit("set_autopilot", {"time": items[0]})
            else:
                await update.message.reply_text("❌ Formato non valido. Usa HH:MM.")
                return
        self.user_states[chat_id] = None
        await update.message.reply_text("✅ Operazione completata.", reply_markup=self._get_main_keyboard())

    async def _handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_auth(update):
            return
        if not update.effective_chat or not update.message or not update.message.voice:
            return

        chat_id = update.effective_chat.id
        file = await context.bot.get_file(update.message.voice.file_id)
        audio_bytes = await file.download_as_bytearray()
        await update.message.reply_chat_action("typing")
        await self._process_with_ai(chat_id, bytes(audio_bytes), is_audio=True)

    async def _process_with_ai(self, chat_id, data, is_audio=False):
        api_key = SecretsManager.get_gemini_api_key()
        if not api_key:
            self.send_message_sync("⚠️ API Key mancante per intelligenza bot.")
            return

        def run():
            try:
                from src.core.lyra_client import LyraClient

                client = LyraClient(api_key=api_key)
                prompt = (
                    "Sei l'interfaccia NLU di SyncroJob. Analizza il messaggio e restituisci SOLO JSON.\n"
                    "Azioni: 'download', 'print', 'status', 'restart'.\n"
                    "Oggetti: 'pdl', 'oda', 'timbrature'.\n"
                    "Items: codici PDL (es. 123456/C o 123456 senza suffisso) o OdA.\n"
                    'JSON: {"action": "...", "object": "...", "items": [...]}'
                )
                res = (
                    client.analyze_media(data, prompt, "audio/ogg")
                    if is_audio
                    else client.ask(f"{prompt}\nMessaggio: {data}")
                )
                try:
                    clean = res.replace("```json", "").replace("```", "").strip()
                    intent = json.loads(clean)
                    self.intent_received.emit(str(chat_id), intent)
                except:
                    self.send_message_sync(f"Comando non riconosciuto: {res}")
            except Exception as e:
                self.send_message_sync(f"❌ Errore AI: {e}")

        threading.Thread(target=run, daemon=True).start()

    async def _handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_auth(update):
            return
        if not update.effective_chat or not update.message or not update.message.photo:
            return

        chat_id = str(update.effective_chat.id)
        photo = update.message.photo[-1]
        caption = update.message.caption or ""
        file = await context.bot.get_file(photo.file_id)
        photo_bytes = await file.download_as_bytearray()
        self.photo_received.emit(chat_id, bytes(photo_bytes), caption)

    async def _handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if not query:
            return
        if (
            self.connected_chat_id
            and update.effective_user
            and str(update.effective_user.id) != self.connected_chat_id
        ):
            return
        await query.answer()

        # Check explicit type
        if not query.message or not isinstance(query.message, Message):
            return

        chat_id = query.message.chat_id
        data = query.data
        if not data:
            return
        if data == "menu_main":
            await query.edit_message_text(
                "🚀 *Command Center*",
                reply_markup=self._get_main_keyboard(),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "menu_pdl":
            keyboard = [
                [InlineKeyboardButton("➕ Inserisci", callback_data="input_pdl")],
                [
                    InlineKeyboardButton("📋 Lista", callback_data="list_pdl"),
                    InlineKeyboardButton("🗑️ Svuota", callback_data="clear_pdl"),
                ],
                [InlineKeyboardButton("🖨️ Avvia (Print ON)", callback_data="run_pdl_on")],
                [InlineKeyboardButton("📄 Avvia (Print OFF)", callback_data="run_pdl_off")],
                [InlineKeyboardButton("🔙 Indietro", callback_data="menu_main")],
            ]
            await query.edit_message_text(
                "🛡️ *SafeWork PDL*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "menu_ts":
            keyboard = [
                [InlineKeyboardButton("➕ OdA", callback_data="input_oda")],
                [
                    InlineKeyboardButton("📋 Lista", callback_data="list_ts"),
                    InlineKeyboardButton("🗑️ Svuota", callback_data="clear_ts"),
                ],
                [InlineKeyboardButton("▶ Avvia", callback_data="run_ts")],
                [InlineKeyboardButton("🔙 Indietro", callback_data="menu_main")],
            ]
            await query.edit_message_text(
                "📥 *Portale TS*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "menu_oda_details":
            keyboard = [
                [InlineKeyboardButton("➕ OdA", callback_data="input_oda")],
                [
                    InlineKeyboardButton("📋 Lista", callback_data="list_ts"),
                    InlineKeyboardButton("🗑️ Svuota", callback_data="clear_ts"),
                ],
                [InlineKeyboardButton("▶ Avvia Dettagli", callback_data="run_oda_details")],
                [InlineKeyboardButton("🔙 Indietro", callback_data="menu_main")],
            ]
            await query.edit_message_text(
                "📋 *Dettagli OdA*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "menu_carico":
            keyboard = [
                [InlineKeyboardButton("▶ Avvia Carico", callback_data="run_carico")],
                [InlineKeyboardButton("🔙 Indietro", callback_data="menu_main")],
            ]
            await query.edit_message_text(
                "📤 *Carico TS*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "menu_timbrature":
            keyboard = [
                [InlineKeyboardButton("🕒 Ieri", callback_data="run_timbrature_yesterday")],
                [InlineKeyboardButton("📅 Oggi", callback_data="run_timbrature_today")],
                [InlineKeyboardButton("🔙 Indietro", callback_data="menu_main")],
            ]
            await query.edit_message_text(
                "⏱️ *Timbrature*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "input_pdl":
            self.user_states[chat_id] = "WAITING_PDL"
            await query.edit_message_text("⌨️ Inserisci PDL:")
        elif data == "input_oda":
            self.user_states[chat_id] = "WAITING_ODA"
            await query.edit_message_text("⌨️ Inserisci OdA:")
        elif data == "run_pdl_on":
            self.command_received.emit("run_pdl", {"print": True})
        elif data == "run_pdl_off":
            self.command_received.emit("run_pdl", {"print": False})
        elif data == "run_ts":
            self.command_received.emit("run_ts", {})
        elif data == "run_timbrature_yesterday":
            self.command_received.emit("run_timbrature", {"period": "yesterday"})
        elif data == "run_timbrature_today":
            self.command_received.emit("run_timbrature", {"period": "today"})
        elif data == "run_oda_details":
            self.command_received.emit("run_oda_details", {})
        elif data == "run_carico":
            self.command_received.emit("run_carico", {})
        elif data == "list_pdl":
            self.command_received.emit("list_pdl", {"chat_id": str(chat_id)})
        elif data == "clear_pdl":
            self.command_received.emit("clear_pdl", {})
        elif data == "list_ts":
            self.command_received.emit("list_ts", {"chat_id": str(chat_id)})
        elif data == "clear_ts":
            self.command_received.emit("clear_ts", {})
        elif data == "status":
            self.status_requested.emit(str(chat_id))
        elif data == "screenshot":
            keyboard = [
                [
                    InlineKeyboardButton("🖼️ App", callback_data="snap_app"),
                    InlineKeyboardButton("🖥️ PC", callback_data="snap_pc"),
                ],
                [InlineKeyboardButton("🔙 Indietro", callback_data="menu_main")],
            ]
            await query.edit_message_text("📸 Screenshot:", reply_markup=InlineKeyboardMarkup(keyboard))
        elif data == "snap_app":
            self.screenshot_requested.emit("app")
        elif data == "snap_pc":
            self.screenshot_requested.emit("pc")
        elif data == "stop_all":
            self.command_received.emit("stop_all", {})
        elif data == "menu_power":
            keyboard = [
                [InlineKeyboardButton("🔄 Riavvia App", callback_data="app_restart")],
                [InlineKeyboardButton("🔌 Test Net", callback_data="app_conn_test")],
                [InlineKeyboardButton("🔙 Indietro", callback_data="menu_main")],
            ]
            await query.edit_message_text("⚡ Manutenzione:", reply_markup=InlineKeyboardMarkup(keyboard))
        elif data == "app_restart":
            self.command_received.emit("restart_app", {})
        elif data == "app_conn_test":
            self.command_received.emit("test_connectivity", {})
        elif data == "menu_settings":
            config = config_manager.load_config()
            fornitori = config.get("fornitori", [])
            keyboard = [
                [InlineKeyboardButton(f"🏢 {f}", callback_data=f"set_forn_{f}")] for f in fornitori[:6]
            ]
            keyboard.append([InlineKeyboardButton("📅 Autopilot", callback_data="menu_autopilot")])
            keyboard.append([InlineKeyboardButton("🖨️ Stampante", callback_data="menu_printers")])
            keyboard.append([InlineKeyboardButton("🔙 Indietro", callback_data="menu_main")])
            await query.edit_message_text("⚙️ Impostazioni:", reply_markup=InlineKeyboardMarkup(keyboard))
        elif data.startswith("set_forn_"):
            self.command_received.emit("set_fornitore", {"fornitore": data.replace("set_forn_", "")})
        elif data == "menu_autopilot":
            keyboard = [
                [InlineKeyboardButton("🔄 Toggle", callback_data="toggle_autopilot")],
                [InlineKeyboardButton("🕒 Orario", callback_data="input_autopilot_time")],
                [InlineKeyboardButton("🔙 Indietro", callback_data="menu_settings")],
            ]
            await query.edit_message_text("📅 Autopilot:", reply_markup=InlineKeyboardMarkup(keyboard))
        elif data == "toggle_autopilot":
            config = config_manager.load_config()
            self.command_received.emit(
                "set_autopilot", {"enabled": not config.get("timbrature_autopilot_enabled", False)}
            )
        elif data == "input_autopilot_time":
            self.user_states[chat_id] = "WAITING_AUTOPILOT_TIME"
            await query.edit_message_text("🕒 Inserisci orario (HH:MM):")
        elif data == "menu_printers":
            printers = get_installed_printers()
            keyboard = [
                [InlineKeyboardButton(f"🖨️ {p[:30]}", callback_data=f"set_print_{p[:30]}")]
                for p in printers[:6]
            ]
            keyboard.append([InlineKeyboardButton("🔙 Indietro", callback_data="menu_settings")])
            await query.edit_message_text("🖨️ Stampanti:", reply_markup=InlineKeyboardMarkup(keyboard))
        elif data.startswith("set_print_"):
            self.command_received.emit("set_printer", {"printer": data.replace("set_print_", "")})
        elif data == "confirm_print_yes":
            printers = get_installed_printers()
            keyboard = [
                [InlineKeyboardButton(f"🖨️ {p[:30]}", callback_data=f"sel_print_run_{p[:25]}")]
                for p in printers[:6]
            ]
            await query.edit_message_text(
                "Seleziona stampante per avviare:", reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif data == "confirm_print_no":
            self.command_received.emit("run_pdl", {"print": False})
            await query.edit_message_text("🚀 Avvio solo scarico.")
        elif data.startswith("sel_print_run_"):
            short_p = data.replace("sel_print_run_", "")
            full_p = short_p
            for p in get_installed_printers():
                if p.startswith(short_p):
                    full_p = p
                    break
            self.command_received.emit("set_printer", {"printer": full_p})
            self.command_received.emit("run_pdl", {"print": True})
            await query.edit_message_text(f"✅ Avvio su: `{full_p}`", parse_mode=constants.ParseMode.MARKDOWN)

    def send_message_sync(self, message: str):
        if self.loop and self.loop.is_running() and self.connected_chat_id:
            asyncio.run_coroutine_threadsafe(
                self._send_message_async(self.connected_chat_id, message), self.loop
            )

    def send_photo_sync(self, photo_bytes: bytes, caption: str = ""):
        if self.loop and self.loop.is_running() and self.connected_chat_id:
            asyncio.run_coroutine_threadsafe(
                self._send_photo_async(self.connected_chat_id, photo_bytes, caption), self.loop
            )

    def send_document_sync(self, file_path: str, caption: str = ""):
        if self.loop and self.loop.is_running() and self.connected_chat_id:
            asyncio.run_coroutine_threadsafe(
                self._send_document_async(self.connected_chat_id, file_path, caption), self.loop
            )

    async def _send_message_async(self, chat_id, text):
        if self.app:
            try:
                if not self.app.bot:
                    await self.app.initialize()
                await self.app.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode=constants.ParseMode.MARKDOWN if "*" in text else None,
                )
            except:
                pass

    async def _send_photo_async(self, chat_id, photo_bytes, caption):
        if self.app:
            try:
                if not self.app.bot:
                    await self.app.initialize()
                await self.app.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_bytes,
                    caption=caption,
                    parse_mode=constants.ParseMode.MARKDOWN if caption else None,
                )
            except:
                pass

    async def _send_document_async(self, chat_id, file_path, caption):
        if self.app:
            try:
                if not self.app.bot:
                    await self.app.initialize()
                with open(file_path, "rb") as f:
                    await self.app.bot.send_document(
                        chat_id=chat_id,
                        document=f,
                        caption=caption,
                        parse_mode=constants.ParseMode.MARKDOWN if caption else None,
                    )
            except:
                pass
