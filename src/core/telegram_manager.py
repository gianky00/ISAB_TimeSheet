import asyncio
import json
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import telegram
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
from src.core.contabilita_manager import ContabilitaManager
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
        self.pdl_settings = {}  # Settings specifici per PDL (es. merge_all)
        self.pending_data = {}
        self._start_lock = threading.Lock()
        self.ai_executor = ThreadPoolExecutor(
            max_workers=3, thread_name_prefix="Telegram_AI"
        )

    def start_service(self):
        """Avvia o riavvia il servizio in modo thread-safe."""
        with self._start_lock:
            if self.thread and self.thread.is_alive():
                self.log_signal.emit("Riavvio del servizio Telegram in corso...")
                self.stop_service()
                time.sleep(2.0)  # Wait for TCP connections to fully close

            config = config_manager.load_config()
            token = config.get("telegram_token", "")
            self.connected_chat_id = config.get("telegram_chat_id", "")
            if not token:
                self.log_signal.emit("⚠️ Telegram Token mancante.")
                return

            self.stop_event.clear()
            self.thread = threading.Thread(
                target=self._run_async_loop, args=(token,), daemon=True
            )
            self.thread.start()

    def stop_service(self):
        """Ferma il servizio e attende la sua terminazione (metodo bloccante)."""
        if self.thread and self.thread.is_alive():
            self.log_signal.emit("⏳ Arresto servizio Telegram in corso...")
            self.stop_event.set()
            self.thread.join(timeout=12)
            if self.thread.is_alive():
                self.log_signal.emit(
                    "⚠️ Timeout: il thread di Telegram non si è fermato correttamente."
                )
            else:
                self.log_signal.emit("Servizio Telegram fermato.")

    def _run_async_loop(self, token):
        """Loop principale asincrono del bot Telegram."""
        res = self._execute_loop(self._main_loop_logic)

        # Supporto critico per mock asincroni nei test
        if res is not None and hasattr(res, "__await__"):
            import threading

            done = threading.Event()

            def run_mock():
                asyncio.run(res)
                done.set()

            # Eseguiamo il mock in un thread separato per non bloccare il loop del test
            # e attendiamo la sincronizzazione.
            t = threading.Thread(target=run_mock, daemon=True)
            t.start()
            t.join(timeout=5.0)

    async def _main_loop_logic(self):
        """Logica interna del loop asincrono (separata per testabilità)."""
        config = config_manager.load_config()
        token = config.get("telegram_token", "")
        self.app = self._build_application(token)
        self._add_handlers()
        self.log_signal.emit("✅ Servizio Telegram Attivo")

        try:
            await self.app.initialize()
            if not self.stop_event.is_set():
                await self.app.updater.start_polling(drop_pending_updates=True)
                await self.app.start()
                while not self.stop_event.is_set():
                    await asyncio.sleep(1)
        finally:
            await self._shutdown_application()

    def _build_application(self, token: str) -> Application:
        return (
            Application.builder()
            .token(token)
            .read_timeout(10)
            .connect_timeout(10)
            .build()
        )

    def _add_handlers(self):
        self.app.add_handler(CommandHandler("start", self._cmd_start))
        self.app.add_handler(CommandHandler("status", self._cmd_status))
        self.app.add_handler(CommandHandler("stop", self._cmd_stop))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_text_input)
        )
        self.app.add_handler(MessageHandler(filters.PHOTO, self._handle_photo))
        self.app.add_handler(MessageHandler(filters.VOICE, self._handle_voice))
        self.app.add_handler(CallbackQueryHandler(self._handle_button))
        self.app.add_error_handler(self._handle_error)

    async def _shutdown_application(self):
        self.log_signal.emit("Spegnimento del bot Telegram...")
        try:

            async def sequence():
                if self.app.updater and self.app.updater.is_running:
                    await self.app.updater.stop()
                if self.app.running:
                    await self.app.stop()
                await self.app.shutdown()

            await asyncio.wait_for(sequence(), timeout=5.0)
            self.log_signal.emit("Bot Telegram spento.")
        except Exception as e:
            self.log_signal.emit(f"⚠️ Errore spegnimento: {e}")

    def _execute_loop(self, main_coro_func):
        """Esegue una coroutine nel loop del thread dedicato."""
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(main_coro_func())
        except Exception as e:
            if not self.stop_event.is_set():
                self.log_signal.emit(f"❌ Errore critico loop: {e}")
        finally:
            self.log_signal.emit("Thread Telegram terminato.")
            if self.loop and self.loop.is_running():
                self.loop.close()

    async def _handle_error(
        self, update: object, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Gestisce gli errori globali del bot."""
        if isinstance(context.error, telegram.error.Conflict):
            self.log_signal.emit(
                "🔴 CONFLITTO TELEGRAM: Rilevata altra istanza attiva. Arresto servizio."
            )
            self.stop_event.set()
        elif isinstance(context.error, telegram.error.NetworkError):
            self.log_signal.emit(f"⚠️ Errore Rete Telegram: {context.error}")
        else:
            self.log_signal.emit(f"❌ Errore Telegram Imprevisto: {context.error}")

    def _get_main_keyboard(self):
        """Menu Principale Gerarchico."""
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🤖 Bot", callback_data="nav_bots"),
                    InlineKeyboardButton("🗄️ Database", callback_data="nav_db"),
                ],
                [
                    InlineKeyboardButton("✨ Lyra AI", callback_data="nav_lyra"),
                    InlineKeyboardButton(
                        "⚙️ Utility & Stato", callback_data="nav_utility"
                    ),
                ],
            ]
        )

    def _get_back_button(self, callback_data):
        return InlineKeyboardButton("🔙 Indietro", callback_data=callback_data)

    async def _check_auth(self, update: Update) -> bool:
        if not update.effective_user:
            return False
        user_id = str(update.effective_user.id)
        if self.connected_chat_id and user_id != self.connected_chat_id:
            try:
                if update.message:
                    await update.message.reply_text("⛔ Accesso Negato")
            except Exception:
                pass
            return False
        return True

    async def _cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_chat:
            return

        chat_id = str(update.effective_chat.id)

        if not self.connected_chat_id:
            self.connected_chat_id = chat_id
            config_manager.set_config_value("telegram_chat_id", chat_id)
            if update.message:
                await update.message.reply_text(
                    f"✅ Dispositivo associato! Chat ID: {chat_id}"
                )

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

    async def _handle_text_input(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        if (
            not await self._check_auth(update)
            or not update.effective_chat
            or not update.message
            or not update.message.text
        ):
            return

        chat_id = update.effective_chat.id
        state = self.user_states.get(chat_id)
        text = update.message.text

        # 1. Gestione Ricerca DB
        if isinstance(state, str) and state.startswith("WAITING_DB_QUERY_"):
            await self._handle_db_query_input(chat_id, state, text, update)
            return

        # 2. Gestione Intenti NLU (senza stato)
        if not state:
            await self._handle_nlu_or_query(chat_id, text)
            return

        # 3. Gestione Input Sequenziali (OdA, PDL, Time)
        await self._handle_sequential_input(chat_id, state, text, update)

    async def _handle_db_query_input(self, chat_id, state, text, update):
        parts = state.replace("WAITING_DB_QUERY_", "").split("_")
        params = {"db": parts[0].lower(), "query": text, "chat_id": str(chat_id)}
        if len(parts) > 1:
            params["year"] = parts[1]

        await update.message.reply_chat_action("typing")
        self.command_received.emit("search_db_pdf", params)
        self.user_states[chat_id] = None

    async def _handle_nlu_or_query(self, chat_id, text):
        keywords = ["scarica", "stampa", "avvia", "pdl", "oda", "stato", "riavvia"]
        if any(k in text.lower() for k in keywords):
            await self._process_with_ai(chat_id, text)
        else:
            self.query_received.emit(str(chat_id), text)

    async def _handle_sequential_input(self, chat_id, state, text, update):
        items = [
            i.strip()
            for i in text.replace(",", "\n").replace(";", "\n").split("\n")
            if i.strip()
        ]
        if not items:
            return

        if state == "WAITING_PDL":
            self.data_received.emit("pdl", items)
        elif state == "WAITING_ODA":
            self.data_received.emit("oda", items)
        elif state == "WAITING_BP":
            self.data_received.emit("bp", items)
        elif state == "WAITING_AUTOPILOT_TIME":
            if re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", items[0]):
                self.command_received.emit("set_autopilot", {"time": items[0]})
            else:
                await update.message.reply_text("❌ Formato non valido. Usa HH:MM.")
                return

        self.user_states[chat_id] = None
        await update.message.reply_text(
            "✅ Operazione completata.", reply_markup=self._get_main_keyboard()
        )

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
                if isinstance(data, str) and not is_audio:
                    res = client.ask(data)
                    try:
                        clean = res.replace("```json", "").replace("```", "").strip()
                        intent = json.loads(clean)
                        if "action" in intent:
                            self.intent_received.emit(str(chat_id), intent)
                            return
                    except Exception:
                        pass
                    self.send_message_sync(f"🤖 **Lyra**: {res}")
                else:
                    prompt = (
                        "Sei l'interfaccia NLU di SyncroJob. Analizza il messaggio e restituisci SOLO JSON.\n"
                        "Azioni: 'download', 'print', 'status', 'restart'.\n"
                        "Oggetti: 'pdl', 'oda', 'timbrature'.\n"
                        "Items: codici PDL (es. 123456/C o 123456 senza suffisso) o OdA.\n"
                        'JSON: {"action": "...", "object": "...", "items": [...]}'
                    )
                    res = client.analyze_media(data, prompt, "audio/ogg")
                    try:
                        clean = res.replace("```json", "").replace("```", "").strip()
                        intent = json.loads(clean)
                        self.intent_received.emit(str(chat_id), intent)
                    except Exception:
                        self.send_message_sync(f"Comando non riconosciuto: {res}")
            except Exception as e:
                self.send_message_sync(f"❌ Errore AI: {e}")

        self.ai_executor.submit(run)

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
        """Gestisce tutti i callback dei bottoni inline."""
        query = update.callback_query
        if not query or not query.message or not isinstance(query.message, Message):
            return
        if (
            self.connected_chat_id
            and update.effective_user
            and str(update.effective_user.id) != self.connected_chat_id
        ):
            return
        await query.answer()
        chat_id = query.message.chat_id
        data = query.data
        if not data:
            return

        # Dispatcher per ridurre la complessità C901
        if data == "menu_main" or data.startswith("nav_"):
            await self._handle_nav_actions(data, query)
        elif data.startswith("db_"):
            await self._handle_db_actions(data, query, chat_id)
        elif self._is_bot_data(data):
            await self._handle_bot_actions(data, query, chat_id, update, context)
        elif self._is_utility_data(data):
            await self._handle_utility_actions(data, query, chat_id)

    def _is_bot_data(self, data: str) -> bool:
        """Verifica se il callback data appartiene alle azioni dei bot."""
        prefixes = ["menu_", "run_", "input_", "clear_", "list_", "confirm_"]
        return (
            any(data.startswith(p) for p in prefixes) or data == "toggle_merge_all_pdl"
        )

    def _is_utility_data(self, data: str) -> bool:
        """Verifica se il callback data appartiene alle utility."""
        items = ["status", "screenshot", "snap_app", "snap_pc", "stop_all"]
        prefixes = ["app_", "set_", "toggle_"]
        return data in items or any(data.startswith(p) for p in prefixes)

    async def _handle_nav_actions(self, data, query):
        """Gestisce i bottoni di navigazione dei menu."""
        if data == "menu_main":
            await query.edit_message_text(
                "🚀 *Command Center*",
                reply_markup=self._get_main_keyboard(),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "nav_bots":
            keyboard = [
                [
                    InlineKeyboardButton(
                        "🏭 Portale Fornitori", callback_data="nav_portale"
                    )
                ],
                [InlineKeyboardButton("🛡️ SafeWork", callback_data="nav_safework")],
                [self._get_back_button("menu_main")],
            ]
            await query.edit_message_text(
                "🤖 *Seleziona Piattaforma*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "nav_db":
            keyboard = [
                [
                    InlineKeyboardButton(
                        "⏱️ Timbrature Isab", callback_data="db_info_timbrature"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📊 Strumentale", callback_data="db_select_year_strumentale"
                    )
                ],
                [InlineKeyboardButton("🏗️ DataEase", callback_data="db_info_dataease")],
                [self._get_back_button("menu_main")],
            ]
            await query.edit_message_text(
                "🗄️ *Seleziona Database*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "nav_lyra":
            await query.edit_message_text(
                "✨ **Lyra AI Assistant**\n\nPuoi inviare vocali, foto di rapportini o domande sui dati.\n_Scrivi o parla direttamente qui!_",
                reply_markup=InlineKeyboardMarkup(
                    [[self._get_back_button("menu_main")]]
                ),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "nav_utility":
            keyboard = [
                [
                    InlineKeyboardButton("📊 Stato", callback_data="status"),
                    InlineKeyboardButton("📸 Screenshot", callback_data="screenshot"),
                ],
                [
                    InlineKeyboardButton(
                        "⚙️ Impostazioni", callback_data="menu_settings"
                    ),
                    InlineKeyboardButton("🛑 Stop Globale", callback_data="stop_all"),
                ],
                [InlineKeyboardButton("⚡ Manutenzione", callback_data="menu_power")],
                [self._get_back_button("menu_main")],
            ]
            await query.edit_message_text(
                "⚙️ *Utility & Stato*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "nav_portale":
            keyboard = [
                [InlineKeyboardButton("📥 Scarico TS", callback_data="menu_ts")],
                [InlineKeyboardButton("📤 Carico TS", callback_data="menu_carico")],
                [
                    InlineKeyboardButton(
                        "📋 Dettagli OdA", callback_data="menu_oda_details"
                    )
                ],
                [InlineKeyboardButton("⏱️ Timbrature", callback_data="menu_timbrature")],
                [InlineKeyboardButton("📦 Prenota BP", callback_data="menu_prenota_bp")],
                [self._get_back_button("nav_bots")],
            ]
            await query.edit_message_text(
                "🏭 *Portale Fornitori*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data == "nav_safework":
            keyboard = [
                [InlineKeyboardButton("🛡️ Scarico PDL", callback_data="menu_pdl")],
                [self._get_back_button("nav_bots")],
            ]
            await query.edit_message_text(
                "🛡️ *SafeWork*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )

    async def _handle_db_actions(self, data, query, chat_id):
        """Gestisce le azioni legate ai database."""
        if data == "db_select_year_strumentale":
            years = ContabilitaManager.get_available_years()
            if not years:
                await query.edit_message_text(
                    "⚠️ Nessun anno disponibile nel database.",
                    reply_markup=InlineKeyboardMarkup(
                        [[self._get_back_button("nav_db")]]
                    ),
                )
                return

            keyboard = []
            row = []
            for y in sorted(years, reverse=True):
                row.append(
                    InlineKeyboardButton(
                        str(y), callback_data=f"db_year_strumentale_{y}"
                    )
                )
                if len(row) == 3:
                    keyboard.append(row)
                    row = []
            if row:
                keyboard.append(row)
            keyboard.append([self._get_back_button("nav_db")])
            await query.edit_message_text(
                "📅 *Seleziona Anno*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data.startswith("db_year_"):
            parts = data.replace("db_year_", "").split("_")
            db_name = parts[0]
            year = parts[1]
            self.user_states[chat_id] = f"WAITING_DB_QUERY_{db_name.upper()}_{year}"
            await query.edit_message_text(
                f"📊 **Strumentale {year}**\nCosa stai cercando? (es. nome fornitore, descrizione...)",
                reply_markup=InlineKeyboardMarkup(
                    [[self._get_back_button("db_select_year_strumentale")]]
                ),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
        elif data.startswith("db_info_"):
            db_name = data.replace("db_info_", "")
            self.user_states[chat_id] = f"WAITING_DB_QUERY_{db_name.upper()}"
            await query.edit_message_text(
                f"🗄️ **DB {db_name.capitalize()}**\nScrivi cosa cercare, Lyra risponderà.",
                reply_markup=InlineKeyboardMarkup([[self._get_back_button("nav_db")]]),
                parse_mode=constants.ParseMode.MARKDOWN,
            )

    async def _handle_menu_pdl(self, query, chat_id):
        merge_all = self.pdl_settings.get(chat_id, {}).get("merge_all", False)
        merge_icon = "✅" if merge_all else "❌"
        keyboard = [
            [InlineKeyboardButton("➕ Inserisci", callback_data="input_pdl")],
            [
                InlineKeyboardButton("📋 Lista", callback_data="list_pdl"),
                InlineKeyboardButton("🗑️ Svuota", callback_data="clear_pdl"),
            ],
            [
                InlineKeyboardButton(
                    f"🔗 Unisci Tutto: {merge_icon}",
                    callback_data="toggle_merge_all_pdl",
                )
            ],
            [InlineKeyboardButton("🖨️ Avvia (Print ON)", callback_data="run_pdl_on")],
            [InlineKeyboardButton("📄 Avvia (Print OFF)", callback_data="run_pdl_off")],
            [self._get_back_button("nav_safework")],
        ]
        await query.edit_message_text(
            "🛡️ *SafeWork PDL*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def _handle_toggle_merge_all_pdl(self, query, chat_id, update, context):
        if chat_id not in self.pdl_settings:
            self.pdl_settings[chat_id] = {}
        current = self.pdl_settings[chat_id].get("merge_all", False)
        self.pdl_settings[chat_id]["merge_all"] = not current
        query.data = "menu_pdl"
        await self._handle_button(update, context)

    async def _handle_menu_ts(self, query):
        keyboard = [
            [InlineKeyboardButton("➕ OdA", callback_data="input_oda")],
            [
                InlineKeyboardButton("📋 Lista", callback_data="list_ts"),
                InlineKeyboardButton("🗑️ Svuota", callback_data="clear_ts"),
            ],
            [InlineKeyboardButton("▶ Avvia", callback_data="run_ts")],
            [self._get_back_button("nav_portale")],
        ]
        await query.edit_message_text(
            "📥 *Portale TS*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def _handle_menu_oda_details(self, query):
        keyboard = [
            [InlineKeyboardButton("➕ OdA", callback_data="input_oda")],
            [
                InlineKeyboardButton("📋 Lista", callback_data="list_ts"),
                InlineKeyboardButton("🗑️ Svuota", callback_data="clear_ts"),
            ],
            [InlineKeyboardButton("▶ Avvia Dettagli", callback_data="run_oda_details")],
            [self._get_back_button("nav_portale")],
        ]
        await query.edit_message_text(
            "📋 *Dettagli OdA*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def _handle_menu_carico(self, query):
        await query.edit_message_text(
            "📤 *Carico TS*",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "▶ Avvia Carico", callback_data="run_carico"
                        )
                    ],
                    [self._get_back_button("nav_portale")],
                ]
            ),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def _handle_menu_timbrature(self, query):
        await query.edit_message_text(
            "⏱️ *Timbrature*",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🕒 Ieri", callback_data="run_timbrature_yesterday"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "📅 Oggi", callback_data="run_timbrature_today"
                        )
                    ],
                    [self._get_back_button("nav_portale")],
                ]
            ),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def _handle_input_pdl(self, query, chat_id):
        self.user_states[chat_id] = "WAITING_PDL"
        await query.edit_message_text("⌨️ Inserisci PDL:")

    async def _handle_input_oda(self, query, chat_id):
        self.user_states[chat_id] = "WAITING_ODA"
        await query.edit_message_text("⌨️ Inserisci OdA:")

    async def _handle_run_pdl_on(self, query):
        from src.utils.printing import get_installed_printers

        printers = get_installed_printers()
        keyboard = [
            [
                InlineKeyboardButton(
                    f"🖨️ {p[:30]}", callback_data=f"sel_print_run_{p[:25]}"
                )
            ]
            for p in printers[:6]
        ]
        keyboard.append([self._get_back_button("menu_pdl")])
        await query.edit_message_text(
            "Seleziona la stampante:", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def _handle_run_pdl_off(self, query):
        await query.edit_message_text(
            "Vuoi ricevere il PDF unito in chat?",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "✅ Sì, invia in chat",
                            callback_data="confirm_merge_yes_noprint",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "❌ No", callback_data="confirm_merge_no_noprint"
                        )
                    ],
                    [self._get_back_button("menu_pdl")],
                ]
            ),
        )

    async def _handle_bot_actions(self, data, query, chat_id, update, context):
        """Gestisce le azioni di controllo dei Bot con dispatch map."""
        # 1. Menu e Input diretti
        if await self._handle_menu_and_input_dispatch(
            data, query, chat_id, update, context
        ):
            return

        # 2. Selezione Stampante e Conferma Run PDL
        if data.startswith("sel_print_run_"):
            await self._handle_printer_selection(data, query, chat_id)
        elif data.startswith("confirm_merge_"):
            await self._handle_run_pdl_confirm(data, query, chat_id)

        # 3. Comandi Run diretti e Liste
        else:
            self._handle_direct_bot_commands(data, chat_id)

    async def _handle_menu_and_input_dispatch(
        self, data, query, chat_id, update, context
    ) -> bool:
        """Dispatcher per menu e input. Ritorna True se gestito."""
        map = {
            "menu_pdl": lambda: self._handle_menu_pdl(query, chat_id),
            "toggle_merge_all_pdl": lambda: self._handle_toggle_merge_all_pdl(
                query, chat_id, update, context
            ),
            "menu_ts": lambda: self._handle_menu_ts(query),
            "menu_oda_details": lambda: self._handle_menu_oda_details(query),
            "menu_carico": lambda: self._handle_menu_carico(query),
            "menu_timbrature": lambda: self._handle_menu_timbrature(query),
            "menu_prenota_bp": lambda: self._handle_menu_prenota_bp(query, chat_id),
            "input_pdl": lambda: self._handle_input_pdl(query, chat_id),
            "input_oda": lambda: self._handle_input_oda(query, chat_id),
            "input_bp": lambda: self._handle_input_bp(query, chat_id),
            "run_pdl_on": lambda: self._handle_run_pdl_on(query),
            "run_pdl_off": lambda: self._handle_run_pdl_off(query),
        }
        if handler := map.get(data):
            await handler()
            return True
        return False

    async def _handle_menu_prenota_bp(self, query, chat_id):
        keyboard = [
            [InlineKeyboardButton("➕ Inserisci BP", callback_data="input_bp")],
            [InlineKeyboardButton("▶ Avvia", callback_data="run_prenota_bp")],
            [self._get_back_button("nav_portale")],
        ]
        await query.edit_message_text(
            "📦 *Prenota BP*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def _handle_input_bp(self, query, chat_id):
        self.user_states[chat_id] = "WAITING_BP"
        await query.edit_message_text(
            "⌨️ Inserisci BP (Formato: NUMERO [NOTE]):\nEs: `123456 Urgente`\nEs: `987654`"
        )

    async def _handle_printer_selection(self, data, query, chat_id):
        sn = data.replace("sel_print_run_", "")
        fpn = self._get_full_printer_name(sn)
        self.user_states[chat_id] = {"printer": fpn}
        await query.edit_message_text(
            f"Stampante: `{fpn}`. Vuoi il PDF unito in chat?",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "✅ Sì, invia", callback_data="confirm_merge_yes_print"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "❌ No", callback_data="confirm_merge_no_print"
                        )
                    ],
                    [self._get_back_button("menu_pdl")],
                ]
            ),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def _handle_run_pdl_confirm(self, data, query, chat_id):
        p = self.user_states.pop(chat_id, {}).get("printer", "")
        merge_all = self.pdl_settings.get(chat_id, {}).get("merge_all", False)

        # Configurazione base run_pdl
        params = {"merge_all": merge_all}

        if "_print" in data:
            if not p:
                return
            self.command_received.emit("set_printer", {"printer": p})
            params.update({"print": True, "merge_and_send": ("_yes_" in data)})
            msg = f"✅ Avvio con stampa su `{p}`"
        else:
            params.update({"print": False, "merge_and_send": ("_yes_" in data)})
            msg = "✅ Avvio scarico"

        self.command_received.emit("run_pdl", params)
        await query.edit_message_text(
            f"{msg}, invio PDF={params['merge_and_send']}, merge finale={merge_all}."
        )

    def _handle_direct_bot_commands(self, data, chat_id):
        direct_map = {
            "run_ts": ("run_ts", {}),
            "run_timbrature_yesterday": ("run_timbrature", {"period": "yesterday"}),
            "run_timbrature_today": ("run_timbrature", {"period": "today"}),
            "run_oda_details": ("run_oda_details", {}),
            "run_carico": ("run_carico", {}),
            "run_prenota_bp": ("run_prenota_bp", {}),
            "list_pdl": ("list_pdl", {"chat_id": str(chat_id)}),
            "clear_pdl": ("clear_pdl", {}),
            "list_ts": ("list_ts", {"chat_id": str(chat_id)}),
            "clear_ts": ("clear_ts", {}),
        }
        if cmd := direct_map.get(data):
            self.command_received.emit(cmd[0], cmd[1])

    async def _handle_utility_actions(self, data, query, chat_id):
        """Gestisce le azioni di utility e impostazioni."""
        if data == "status":
            self.status_requested.emit(str(chat_id))
        elif data == "screenshot":
            await self._show_screenshot_menu(query)
        elif data in ["snap_app", "snap_pc"]:
            self.screenshot_requested.emit(data.replace("snap_", ""))
        elif data == "stop_all":
            self.command_received.emit("stop_all", {})
        elif data.startswith("app_"):
            self._handle_app_commands(data)
        elif data == "menu_power":
            await self._show_power_menu(query)
        elif data.startswith("menu_"):
            await self._handle_utility_menus(data, query, chat_id)
        elif data.startswith("set_") or data.startswith("toggle_"):
            await self._handle_setting_changes(data, query, chat_id)

    async def _show_screenshot_menu(self, query):
        keyboard = [
            [
                InlineKeyboardButton("🖼️ App", callback_data="snap_app"),
                InlineKeyboardButton("🖥️ PC", callback_data="snap_pc"),
            ],
            [self._get_back_button("nav_utility")],
        ]
        await query.edit_message_text(
            "📸 Screenshot:", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def _show_power_menu(self, query):
        keyboard = [
            [InlineKeyboardButton("🔄 Riavvia App", callback_data="app_restart")],
            [InlineKeyboardButton("🔌 Test Net", callback_data="app_conn_test")],
            [self._get_back_button("nav_utility")],
        ]
        await query.edit_message_text(
            "⚡ Manutenzione:", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def _handle_app_commands(self, data):
        if data == "app_restart":
            self.command_received.emit("restart_app", {})
        elif data == "app_conn_test":
            self.command_received.emit("test_connectivity", {})

    async def _handle_utility_menus(self, data, query, chat_id):
        if data == "menu_settings":
            await self._show_settings_menu(query)
        elif data == "menu_autopilot":
            await self._show_autopilot_menu(query)
        elif data == "menu_printers":
            await self._show_printers_menu(query)

    async def _show_settings_menu(self, query):
        config = config_manager.load_config()
        fornitori = config.get("fornitori", [])
        keyboard = [
            [InlineKeyboardButton(f"🏢 {f}", callback_data=f"set_forn_{f}")]
            for f in fornitori[:6]
        ]
        keyboard.extend(
            [
                [InlineKeyboardButton("📅 Autopilot", callback_data="menu_autopilot")],
                [InlineKeyboardButton("🖨️ Stampante", callback_data="menu_printers")],
                [self._get_back_button("nav_utility")],
            ]
        )
        await query.edit_message_text(
            "⚙️ Impostazioni:", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def _show_autopilot_menu(self, query):
        keyboard = [
            [InlineKeyboardButton("🔄 Toggle", callback_data="toggle_autopilot")],
            [InlineKeyboardButton("🕒 Orario", callback_data="input_autopilot_time")],
            [self._get_back_button("menu_settings")],
        ]
        await query.edit_message_text(
            "📅 Autopilot:", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def _show_printers_menu(self, query):
        printers = get_installed_printers()
        keyboard = [
            [InlineKeyboardButton(f"🖨️ {p[:30]}", callback_data=f"set_print_{p[:30]}")]
            for p in printers[:6]
        ]
        keyboard.append([self._get_back_button("menu_settings")])
        await query.edit_message_text(
            "🖨️ Stampanti:", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def _handle_setting_changes(self, data, query, chat_id):
        if data.startswith("set_forn_"):
            self.command_received.emit(
                "set_fornitore", {"fornitore": data.replace("set_forn_", "")}
            )
        elif data == "toggle_autopilot":
            enabled = not config_manager.load_config().get(
                "timbrature_autopilot_enabled", False
            )
            self.command_received.emit("set_autopilot", {"enabled": enabled})
        elif data == "input_autopilot_time":
            self.user_states[chat_id] = "WAITING_AUTOPILOT_TIME"
            await query.edit_message_text("🕒 Inserisci orario (HH:MM):")
        elif data.startswith("set_print_"):
            self.command_received.emit(
                "set_printer", {"printer": data.replace("set_print_", "")}
            )

    def _get_full_printer_name(self, short_name: str) -> str:
        """Helper per recuperare il nome completo della stampante."""
        for p in get_installed_printers():
            if p.startswith(short_name):
                return p
        return short_name

    def send_message_sync(self, message: str):
        """
        Invia un messaggio di testo in modo sincrono (thread-safe).

        Args:
            message: Testo del messaggio.
        """
        if not self.connected_chat_id:
            config = config_manager.load_config()
            self.connected_chat_id = config.get("telegram_chat_id", "")

        if self.loop and self.loop.is_running() and self.connected_chat_id:
            try:
                asyncio.run_coroutine_threadsafe(
                    self._send_message_async(self.connected_chat_id, message), self.loop
                )
            except Exception as e:
                self.log_signal.emit(f"❌ Errore invio Telegram: {e}")

    def send_photo_sync(self, photo_bytes: bytes, caption: str = ""):
        """
        Invia un'immagine in modo sincrono (thread-safe).

        Args:
            photo_bytes: Dati binari dell'immagine.
            caption: Didascalia opzionale.
        """
        if not self.connected_chat_id:
            config = config_manager.load_config()
            self.connected_chat_id = config.get("telegram_chat_id", "")

        if self.loop and self.loop.is_running() and self.connected_chat_id:
            try:
                asyncio.run_coroutine_threadsafe(
                    self._send_photo_async(
                        self.connected_chat_id, photo_bytes, caption
                    ),
                    self.loop,
                )
            except Exception as e:
                self.log_signal.emit(f"❌ Errore invio foto: {e}")

    def send_document_sync(self, file_path: str, caption: str = ""):
        """
        Invia un documento in modo sincrono (thread-safe).

        Args:
            file_path: Percorso del file sul disco.
            caption: Didascalia opzionale.
        """
        if not self.connected_chat_id:
            config = config_manager.load_config()
            self.connected_chat_id = config.get("telegram_chat_id", "")

        if self.loop and self.loop.is_running() and self.connected_chat_id:
            try:
                asyncio.run_coroutine_threadsafe(
                    self._send_document_async(
                        self.connected_chat_id, file_path, caption
                    ),
                    self.loop,
                )
            except Exception as e:
                self.log_signal.emit(f"❌ Errore invio documento: {e}")

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
            except Exception as e:
                self.log_signal.emit(f"❌ Fallito invio messaggio a Telegram: {e}")

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
            except Exception as e:
                self.log_signal.emit(f"❌ Fallito invio foto a Telegram: {e}")

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
            except Exception as e:
                self.log_signal.emit(f"❌ Fallito invio documento a Telegram: {e}")
