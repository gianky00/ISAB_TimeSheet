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
from src.core.contabilita_manager import ContabilitaManager


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
        self._start_lock = threading.Lock()

    def start_service(self):
        """Avvia o riavvia il servizio in modo thread-safe."""
        with self._start_lock:
            if self.thread and self.thread.is_alive():
                self.log_signal.emit("Riavvio del servizio Telegram in corso...")
                self.stop_service()

            config = config_manager.load_config()
            token = config.get("telegram_token", "")
            self.connected_chat_id = config.get("telegram_chat_id", "")
            if not token:
                self.log_signal.emit("⚠️ Telegram Token mancante.")
                return

            self.stop_event.clear()
            self.thread = threading.Thread(target=self._run_async_loop, args=(token,), daemon=True)
            self.thread.start()

    def stop_service(self):
        """Ferma il servizio e attende la sua terminazione (metodo bloccante)."""
        if self.thread and self.thread.is_alive():
            self.log_signal.emit("⏳ Arresto servizio Telegram in corso...")
            self.stop_event.set()
            self.thread.join(timeout=12)
            if self.thread.is_alive():
                self.log_signal.emit("⚠️ Timeout: il thread di Telegram non si è fermato correttamente.")
            else:
                self.log_signal.emit("Servizio Telegram fermato.")
    
    def _run_async_loop(self, token):
        async def main():
            self.app = (
                Application.builder()
                .token(token)
                .read_timeout(10)
                .connect_timeout(10)
                .build()
            )
            self.app.add_handler(CommandHandler("start", self._cmd_start))
            self.app.add_handler(CommandHandler("status", self._cmd_status))
            self.app.add_handler(CommandHandler("stop", self._cmd_stop))
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_text_input))
            self.app.add_handler(MessageHandler(filters.PHOTO, self._handle_photo))
            self.app.add_handler(MessageHandler(filters.VOICE, self._handle_voice))
            self.app.add_handler(CallbackQueryHandler(self._handle_button))
            
            self.log_signal.emit("✅ Servizio Telegram Attivo")

            try:
                await self.app.initialize()
                if self.stop_event.is_set(): return
                
                await self.app.updater.start_polling(drop_pending_updates=True)
                await self.app.start()

                while not self.stop_event.is_set():
                    await asyncio.sleep(1)

            finally:
                self.log_signal.emit("Spegnimento del bot Telegram...")
                if self.app.updater and self.app.updater.is_running:
                    await self.app.updater.stop()
                if self.app.running:
                    await self.app.stop()
                await self.app.shutdown()
                self.log_signal.emit("Bot Telegram spento.")

        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(main())
        except Exception as e:
            if not self.stop_event.is_set():
                self.log_signal.emit(f"❌ Errore critico nel loop di Telegram: {e}")
        finally:
            self.log_signal.emit("Thread Telegram terminato.")
            if self.loop and self.loop.is_running():
                self.loop.close()

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
                    InlineKeyboardButton("⚙️ Utility & Stato", callback_data="nav_utility"),
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
            except:
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
            await update.message.reply_text(f"✅ Dispositivo associato! Chat ID: {chat_id}")

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
        
        if isinstance(state, str) and state.startswith("WAITING_DB_QUERY_"):
            parts = state.replace("WAITING_DB_QUERY_", "").split("_")
            db_type = parts[0].lower()
            year = parts[1] if len(parts) > 1 else None

            await update.message.reply_chat_action("typing")
            
            params = {"db": db_type, "query": text, "chat_id": str(chat_id)}
            if year:
                params["year"] = year

            # Invia comando per ricerca DB e generazione PDF
            self.command_received.emit("search_db_pdf", params)
            self.user_states[chat_id] = None
            return

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
                if isinstance(data, str) and not is_audio:
                     res = client.ask(data)
                     try:
                        clean = res.replace("```json", "").replace("```", "").strip()
                        intent = json.loads(clean)
                        if "action" in intent:
                             self.intent_received.emit(str(chat_id), intent)
                             return
                     except: pass
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
        if not query or not query.message or not isinstance(query.message, Message): return
        if self.connected_chat_id and str(update.effective_user.id) != self.connected_chat_id: return
        await query.answer()
        chat_id = query.message.chat_id
        data = query.data
        if not data: return

        if data == "menu_main":
            await query.edit_message_text("🚀 *Command Center*", reply_markup=self._get_main_keyboard(), parse_mode=constants.ParseMode.MARKDOWN)
        
        elif data == "nav_bots":
            keyboard = [[InlineKeyboardButton("🏭 Portale Fornitori", callback_data="nav_portale")], [InlineKeyboardButton("🛡️ SafeWork", callback_data="nav_safework")], [self._get_back_button("menu_main")]]
            await query.edit_message_text("🤖 *Seleziona Piattaforma*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "nav_db":
            keyboard = [
                [InlineKeyboardButton("⏱️ Timbrature Isab", callback_data="db_info_timbrature")],
                [InlineKeyboardButton("📊 Strumentale", callback_data="db_select_year_strumentale")],
                [InlineKeyboardButton("🏗️ DataEase", callback_data="db_info_dataease")],
                [self._get_back_button("menu_main")]
            ]
            await query.edit_message_text("🗄️ *Seleziona Database*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "db_select_year_strumentale":
            years = ContabilitaManager.get_available_years()
            if not years:
                await query.edit_message_text("⚠️ Nessun anno disponibile nel database.", reply_markup=InlineKeyboardMarkup([[self._get_back_button("nav_db")]]))
                return
            
            keyboard = []
            # Crea righe di 3 anni
            row = []
            for y in sorted(years, reverse=True):
                row.append(InlineKeyboardButton(str(y), callback_data=f"db_year_strumentale_{y}"))
                if len(row) == 3:
                    keyboard.append(row)
                    row = []
            if row:
                keyboard.append(row)
            
            keyboard.append([self._get_back_button("nav_db")])
            await query.edit_message_text("📅 *Seleziona Anno*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)

        elif data.startswith("db_year_"):
            parts = data.replace("db_year_", "").split("_")
            db_name = parts[0]
            year = parts[1]
            self.user_states[chat_id] = f"WAITING_DB_QUERY_{db_name.upper()}_{year}"
            await query.edit_message_text(f"📊 **Strumentale {year}**\nCosa stai cercando? (es. nome fornitore, descrizione...)", reply_markup=InlineKeyboardMarkup([[self._get_back_button("db_select_year_strumentale")]]), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "nav_lyra":
            await query.edit_message_text("✨ **Lyra AI Assistant**\n\nPuoi inviare vocali, foto di rapportini o domande sui dati.\n_Scrivi o parla direttamente qui!_", reply_markup=InlineKeyboardMarkup([[self._get_back_button("menu_main")]]), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "nav_utility":
            keyboard = [[InlineKeyboardButton("📊 Stato", callback_data="status"), InlineKeyboardButton("📸 Screenshot", callback_data="screenshot")], [InlineKeyboardButton("⚙️ Impostazioni", callback_data="menu_settings"), InlineKeyboardButton("🛑 Stop Globale", callback_data="stop_all")], [InlineKeyboardButton("⚡ Manutenzione", callback_data="menu_power")], [self._get_back_button("menu_main")]]
            await query.edit_message_text("⚙️ *Utility & Stato*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "nav_portale":
            keyboard = [[InlineKeyboardButton("📥 Scarico TS", callback_data="menu_ts")], [InlineKeyboardButton("📤 Carico TS", callback_data="menu_carico")], [InlineKeyboardButton("📋 Dettagli OdA", callback_data="menu_oda_details")], [InlineKeyboardButton("⏱️ Timbrature", callback_data="menu_timbrature")], [self._get_back_button("nav_bots")]]
            await query.edit_message_text("🏭 *Portale Fornitori*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "nav_safework":
            keyboard = [[InlineKeyboardButton("🛡️ Scarico PDL", callback_data="menu_pdl")], [self._get_back_button("nav_bots")]]
            await query.edit_message_text("🛡️ *SafeWork*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)

        elif data.startswith("db_info_"):
            db_name = data.replace("db_info_", "")
            self.user_states[chat_id] = f"WAITING_DB_QUERY_{db_name.upper()}"
            await query.edit_message_text(f"🗄️ **DB {db_name.capitalize()}**\nScrivi cosa cercare, Lyra risponderà.", reply_markup=InlineKeyboardMarkup([[self._get_back_button("nav_db")]]), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "menu_pdl":
            keyboard = [[InlineKeyboardButton("➕ Inserisci", callback_data="input_pdl")], [InlineKeyboardButton("📋 Lista", callback_data="list_pdl"), InlineKeyboardButton("🗑️ Svuota", callback_data="clear_pdl")], [InlineKeyboardButton("🖨️ Avvia (Print ON)", callback_data="run_pdl_on")], [InlineKeyboardButton("📄 Avvia (Print OFF)", callback_data="run_pdl_off")], [self._get_back_button("nav_safework")]]
            await query.edit_message_text("🛡️ *SafeWork PDL*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "menu_ts":
            keyboard = [[InlineKeyboardButton("➕ OdA", callback_data="input_oda")], [InlineKeyboardButton("📋 Lista", callback_data="list_ts"), InlineKeyboardButton("🗑️ Svuota", callback_data="clear_ts")], [InlineKeyboardButton("▶ Avvia", callback_data="run_ts")], [self._get_back_button("nav_portale")]]
            await query.edit_message_text("📥 *Portale TS*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "menu_oda_details":
            keyboard = [[InlineKeyboardButton("➕ OdA", callback_data="input_oda")], [InlineKeyboardButton("📋 Lista", callback_data="list_ts"), InlineKeyboardButton("🗑️ Svuota", callback_data="clear_ts")], [InlineKeyboardButton("▶ Avvia Dettagli", callback_data="run_oda_details")], [self._get_back_button("nav_portale")]]
            await query.edit_message_text("📋 *Dettagli OdA*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "menu_carico":
            await query.edit_message_text("📤 *Carico TS*", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("▶ Avvia Carico", callback_data="run_carico")], [self._get_back_button("nav_portale")]]), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "menu_timbrature":
            await query.edit_message_text("⏱️ *Timbrature*", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🕒 Ieri", callback_data="run_timbrature_yesterday")], [InlineKeyboardButton("📅 Oggi", callback_data="run_timbrature_today")], [self._get_back_button("nav_portale")]]), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "screenshot":
            await query.edit_message_text("📸 Screenshot:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🖼️ App", callback_data="snap_app"), InlineKeyboardButton("🖥️ PC", callback_data="snap_pc")], [self._get_back_button("nav_utility")]]))

        elif data == "menu_power":
            await query.edit_message_text("⚡ Manutenzione:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Riavvia App", callback_data="app_restart")], [InlineKeyboardButton("🔌 Test Net", callback_data="app_conn_test")], [self._get_back_button("nav_utility")]]))

        elif data == "menu_settings":
            config = config_manager.load_config()
            fornitori = config.get("fornitori", [])
            keyboard = [[InlineKeyboardButton(f"🏢 {f}", callback_data=f"set_forn_{f}")] for f in fornitori[:6]]
            keyboard.extend([[InlineKeyboardButton("📅 Autopilot", callback_data="menu_autopilot")], [InlineKeyboardButton("🖨️ Stampante", callback_data="menu_printers")], [self._get_back_button("nav_utility")]])
            await query.edit_message_text("⚙️ Impostazioni:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif data == "menu_autopilot":
            await query.edit_message_text("📅 Autopilot:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Toggle", callback_data="toggle_autopilot")], [InlineKeyboardButton("🕒 Orario", callback_data="input_autopilot_time")], [self._get_back_button("menu_settings")]]))

        elif data == "menu_printers":
            printers = get_installed_printers()
            keyboard = [[InlineKeyboardButton(f"🖨️ {p[:30]}", callback_data=f"set_print_{p[:30]}")] for p in printers[:6]]
            keyboard.append([self._get_back_button("menu_settings")])
            await query.edit_message_text("🖨️ Stampanti:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif data == "input_pdl":
            self.user_states[chat_id] = "WAITING_PDL"
            await query.edit_message_text("⌨️ Inserisci PDL:")

        elif data == "input_oda":
            self.user_states[chat_id] = "WAITING_ODA"
            await query.edit_message_text("⌨️ Inserisci OdA:")

        elif data == "run_pdl_on":
            printers = get_installed_printers()
            keyboard = [[InlineKeyboardButton(f"🖨️ {p[:30]}", callback_data=f"sel_print_run_{p[:25]}")] for p in printers[:6]]
            keyboard.append([self._get_back_button("menu_pdl")])
            await query.edit_message_text("Seleziona la stampante:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif data == "run_pdl_off":
            await query.edit_message_text("Vuoi ricevere il PDF unito in chat?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Sì, invia in chat", callback_data="confirm_merge_yes_noprint")], [InlineKeyboardButton("❌ No", callback_data="confirm_merge_no_noprint")], [self._get_back_button("menu_pdl")]]))

        elif data.startswith("sel_print_run_"):
            sn = data.replace("sel_print_run_", "")
            fpn = self._get_full_printer_name(sn)
            self.user_states[chat_id] = {"printer": fpn}
            await query.edit_message_text(f"Stampante: `{fpn}`. Vuoi il PDF unito in chat?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Sì, invia in chat", callback_data="confirm_merge_yes_print")], [InlineKeyboardButton("❌ No", callback_data="confirm_merge_no_print")], [self._get_back_button("menu_pdl")]]), parse_mode=constants.ParseMode.MARKDOWN)

        elif data == "confirm_merge_yes_print":
            p = self.user_states.pop(chat_id, {}).get("printer", "")
            if p:
                self.command_received.emit("set_printer", {"printer": p})
                self.command_received.emit("run_pdl", {"print": True, "merge_and_send": True})
                await query.edit_message_text(f"✅ Avvio con stampa su `{p}` e invio PDF.")

        elif data == "confirm_merge_no_print":
            p = self.user_states.pop(chat_id, {}).get("printer", "")
            if p:
                self.command_received.emit("set_printer", {"printer": p})
                self.command_received.emit("run_pdl", {"print": True, "merge_and_send": False})
                await query.edit_message_text(f"✅ Avvio con stampa su `{p}`.")
        elif data == "confirm_merge_yes_noprint":
            self.command_received.emit("run_pdl", {"print": False, "merge_and_send": True})
            await query.edit_message_text("✅ Avvio scarico con invio PDF.")

        elif data == "confirm_merge_no_noprint":
            self.command_received.emit("run_pdl", {"print": False, "merge_and_send": False})
            await query.edit_message_text("✅ Avvio scarico.")

        elif data == "run_ts": self.command_received.emit("run_ts", {})
        elif data == "run_timbrature_yesterday": self.command_received.emit("run_timbrature", {"period": "yesterday"})
        elif data == "run_timbrature_today": self.command_received.emit("run_timbrature", {"period": "today"})
        elif data == "run_oda_details": self.command_received.emit("run_oda_details", {})
        elif data == "run_carico": self.command_received.emit("run_carico", {})
        elif data == "list_pdl": self.command_received.emit("list_pdl", {"chat_id": str(chat_id)})
        elif data == "clear_pdl": self.command_received.emit("clear_pdl", {})
        elif data == "list_ts": self.command_received.emit("list_ts", {"chat_id": str(chat_id)})
        elif data == "clear_ts": self.command_received.emit("clear_ts", {})
        elif data == "status": self.status_requested.emit(str(chat_id))
        elif data == "snap_app": self.screenshot_requested.emit("app")
        elif data == "snap_pc": self.screenshot_requested.emit("pc")
        elif data == "stop_all": self.command_received.emit("stop_all", {})
        elif data == "app_restart": self.command_received.emit("restart_app", {})
        elif data == "app_conn_test": self.command_received.emit("test_connectivity", {})
        elif data.startswith("set_forn_"): self.command_received.emit("set_fornitore", {"fornitore": data.replace("set_forn_", "")})

        elif data == "toggle_autopilot":
            config = config_manager.load_config()
            self.command_received.emit("set_autopilot", {"enabled": not config.get("timbrature_autopilot_enabled", False)})

        elif data == "input_autopilot_time":
            self.user_states[chat_id] = "WAITING_AUTOPILOT_TIME"
            await query.edit_message_text("🕒 Inserisci orario (HH:MM):")

        elif data.startswith("set_print_"): self.command_received.emit("set_printer", {"printer": data.replace("set_print_", "")})

    def _get_full_printer_name(self, short_name: str) -> str:
        """Helper per recuperare il nome completo della stampante."""
        for p in get_installed_printers():
            if p.startswith(short_name):
                return p
        return short_name

    def send_message_sync(self, message: str):
        if not self.connected_chat_id:
            config = config_manager.load_config()
            self.connected_chat_id = config.get("telegram_chat_id", "")

        if self.loop and self.loop.is_running() and self.connected_chat_id:
            try:
                asyncio.run_coroutine_threadsafe(
                    self._send_message_async(self.connected_chat_id, message),
                    self.loop
                )
            except Exception as e:
                self.log_signal.emit(f"❌ Errore invio Telegram: {e}")

    def send_photo_sync(self, photo_bytes: bytes, caption: str = ""):
        if not self.connected_chat_id:
            config = config_manager.load_config()
            self.connected_chat_id = config.get("telegram_chat_id", "")

        if self.loop and self.loop.is_running() and self.connected_chat_id:
            try:
                asyncio.run_coroutine_threadsafe(
                    self._send_photo_async(self.connected_chat_id, photo_bytes, caption),
                    self.loop
                )
            except Exception as e:
                self.log_signal.emit(f"❌ Errore invio foto: {e}")

    def send_document_sync(self, file_path: str, caption: str = ""):
        if not self.connected_chat_id:
            config = config_manager.load_config()
            self.connected_chat_id = config.get("telegram_chat_id", "")

        if self.loop and self.loop.is_running() and self.connected_chat_id:
            try:
                asyncio.run_coroutine_threadsafe(
                    self._send_document_async(self.connected_chat_id, file_path, caption),
                    self.loop
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