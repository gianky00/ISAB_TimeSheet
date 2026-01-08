"""
SyncroJob Agent - Il Guardiano
Processo in background per la gestione permanente di Telegram.
"""

import asyncio
import json
import os
import socket
import subprocess
import sys
import threading

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, constants
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Setup Path per caricare i moduli core
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_path not in sys.path:
    sys.path.insert(0, base_path)

from src.core import config_manager
from src.core.lyra_client import LyraClient
from src.core.secrets_manager import SecretsManager


class SyncroJobAgent:
    def __init__(self):
        self.app_socket = None
        self.client_conn = None
        self.tg_app = None
        self.loop = None
        self.port = 5555
        self.connected_chat_id = None
        self.is_running = True

        # Stato per dialoghi intelligenti
        self.user_states = {}
        self.pending_data = {}

    def log(self, msg):
        print(f"[AGENT] {msg}")

    def start(self):
        """Avvia i due motori: Socket Server e Telegram Bot."""
        # 1. Avvia Socket Server in un thread
        threading.Thread(target=self._run_socket_server, daemon=True).start()

        # 2. Avvia Telegram Bot
        config = config_manager.load_config()
        token = config.get("telegram_token")
        self.connected_chat_id = config.get("telegram_chat_id")

        if not token:
            self.log("Errore: Telegram Token non configurato.")
            return

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.tg_app = Application.builder().token(token).build()
        self._setup_handlers()

        self.log("Bot Telegram in avvio...")
        self.tg_app.run_polling(drop_pending_updates=True, stop_signals=None)

    def _setup_handlers(self):
        self.tg_app.add_handler(CommandHandler("start", self._cmd_start))
        self.tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_text))
        self.tg_app.add_handler(MessageHandler(filters.VOICE, self._handle_voice))
        self.tg_app.add_handler(CallbackQueryHandler(self._handle_button))

    # --- COMUNICAZIONE SOCKET ---
    def _run_socket_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind(("127.0.0.1", self.port))
            server.listen(1)
            self.log(f"Socket Server in ascolto sulla porta {self.port}...")
        except Exception as e:
            self.log(f"Errore bind socket: {e}")
            return

        while self.is_running:
            conn, addr = server.accept()
            self.log("Applicazione SyncroJob connessa.")
            self.client_conn = conn
            try:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    # Gestione messaggi in arrivo dall'App (es. log da inviare a TG)
                    msg = json.loads(data.decode())
                    if msg.get("type") == "tg_msg":
                        self._send_to_tg(msg.get("text"), msg.get("photo"))
            except:
                pass
            finally:
                self.log("Applicazione SyncroJob disconnessa.")
                self.client_conn = None
                conn.close()

    def _send_to_app(self, data_dict):
        """Invia un comando all'applicazione principale via socket."""
        if self.client_conn:
            try:
                payload = json.dumps(data_dict).encode()
                self.client_conn.sendall(payload)
                return True
            except:
                self.client_conn = None
        return False

    def _send_to_tg(self, text, photo_bytes_hex=None):
        """Invia un messaggio a Telegram (chiamata thread-safe)."""
        if self.loop and self.connected_chat_id:
            coro = self._async_send(text, photo_bytes_hex)
            asyncio.run_coroutine_threadsafe(coro, self.loop)

    async def _async_send(self, text, photo_hex=None):
        try:
            if photo_hex:
                photo_bytes = bytes.fromhex(photo_hex)
                await self.tg_app.bot.send_photo(
                    chat_id=self.connected_chat_id,
                    photo=photo_bytes,
                    caption=text,
                    parse_mode=constants.ParseMode.MARKDOWN,
                )
            else:
                await self.tg_app.bot.send_message(
                    chat_id=self.connected_chat_id,
                    text=text,
                    parse_mode=constants.ParseMode.MARKDOWN if "*" in text else None,
                )
        except Exception as e:
            self.log(f"Errore invio TG: {e}")

    # --- HANDLERS TELEGRAM ---
    async def _check_auth(self, update: Update):
        uid = str(update.effective_user.id) if update.effective_user else ""
        if self.connected_chat_id and uid != self.connected_chat_id:
            if update.message:
                await update.message.reply_text("⛔ Accesso Negato")
            return False
        return True

    async def _cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_auth(update):
            return
        if not update.message:
            return
        keyboard = [
            [
                InlineKeyboardButton("🛡️ PDL", callback_data="menu_pdl"),
                InlineKeyboardButton("📥 Scarico TS", callback_data="menu_ts"),
            ],
            [
                InlineKeyboardButton("📊 Stato", callback_data="status"),
                InlineKeyboardButton("📸 Screenshot", callback_data="screenshot"),
            ],
            [InlineKeyboardButton("⚡ Power", callback_data="menu_power")],
        ]
        await update.message.reply_text(
            "🚀 *SyncroJob Agent Attivo*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=constants.ParseMode.MARKDOWN,
        )

    async def _handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_auth(update):
            return
        if not update.message or not update.effective_chat:
            return
        text = update.message.text

        # Se l'app è offline, offri di avviarla
        if not self.client_conn:
            keyboard = [[InlineKeyboardButton("🚀 Avvia SyncroJob", callback_data="app_start_now")]]
            await update.message.reply_text(
                "⚠️ *SyncroJob è Offline*\nL'applicazione principale non è in esecuzione sul PC.",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN,
            )
            return

        # Altrimenti processa con AI e invia comando all'App
        await self._process_with_ai(update.effective_chat.id, text)

    async def _handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self._check_auth(update):
            return
        if not update.message or not update.message.voice or not update.effective_chat:
            return
        if not self.client_conn:
            await update.message.reply_text("⚠️ App Offline. Impossibile processare vocale.")
            return

        file = await context.bot.get_file(update.message.voice.file_id)
        audio_bytes = await file.download_as_bytearray()
        await self._process_with_ai(update.effective_chat.id, bytes(audio_bytes), is_audio=True)

    async def _process_with_ai(self, chat_id, data, is_audio=False):
        api_key = SecretsManager.get_gemini_api_key()
        if not api_key:
            self._send_to_tg("⚠️ API Key mancante nell'Agent.")
            return

        # Prompt NLU
        prompt = (
            "Sei l'interfaccia NLU di SyncroJob. Analizza il messaggio e restituisci SOLO JSON.\n"
            "Azioni: 'download', 'print', 'status', 'restart'.\n"
            "Oggetti: 'pdl', 'oda', 'timbrature'.\n"
            "Items: codici PDL (es. 123456/C) o OdA.\n"
            'JSON: {"action": "...", "object": "...", "items": [...]}'
        )

        client = LyraClient(api_key=api_key)
        try:
            res = (
                client.analyze_media(data, prompt, "audio/ogg")
                if is_audio
                else client.ask(f"{prompt}\nMessaggio: {data}")
            )
            clean = res.replace("```json", "").replace("```", "").strip()
            intent = json.loads(clean)
            # Invia l'intento estratto all'App
            self._send_to_app({"type": "intent", "data": intent})
        except:
            self._send_to_tg("❓ Comando non riconosciuto.")

    async def _handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        if not query:
            return
        await query.answer()
        data = query.data
        if not data:
            return

        if data == "app_start_now":
            try:
                # Avvia l'applicazione (assume main.py nella root)
                main_py = os.path.join(base_path, "main.py")
                subprocess.Popen([sys.executable, main_py], creationflags=subprocess.CREATE_NEW_CONSOLE)
                await query.edit_message_text(
                    "🔄 *Avvio in corso...*\nL'applicazione si aprirà tra pochi secondi."
                )
            except Exception as e:
                await query.edit_message_text(f"❌ Errore avvio: {e}")

        elif data == "status":
            if not self._send_to_app({"type": "command", "cmd": "status"}):
                await query.edit_message_text("⚠️ App Offline.")

        elif data == "screenshot":
            keyboard = [
                [
                    InlineKeyboardButton("🖼️ App", callback_data="snap_app"),
                    InlineKeyboardButton("🖥️ PC", callback_data="snap_pc"),
                ]
            ]
            await query.edit_message_text("Scegli screenshot:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif data in ["snap_app", "snap_pc"]:
            mode = "app" if data == "snap_app" else "pc"
            self._send_to_app({"type": "command", "cmd": "screenshot", "mode": mode})

        # Altri pulsanti passano all'app
        else:
            self._send_to_app({"type": "button", "data": data})


if __name__ == "__main__":
    agent = SyncroJobAgent()
    agent.start()
