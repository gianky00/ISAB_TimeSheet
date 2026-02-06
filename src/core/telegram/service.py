import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress

import telegram
from PyQt6.QtCore import QObject, pyqtSignal
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from src.core import config_manager
from src.core.telegram.handlers import callbacks, commands, messages


class TelegramService(QObject):
    """
    Bridge intelligente tra Telegram e l'applicazione PyQt6.
    Supporta comandi vocali, NLU e dialoghi contestuali.
    Refactored per delegare la logica ai moduli handlers/.
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
        self._execute_loop(lambda: self._main_loop_logic(token))

    async def _main_loop_logic(self, token):
        """Logica interna del loop asincrono (separata per testabilità)."""
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
        # Wrappers to pass 'self' (the service instance) to handlers
        async def wrap_cmd(handler):
            return lambda u, c: handler(self, u, c)

        # Commands
        self.app.add_handler(
            CommandHandler("start", lambda u, c: commands.cmd_start(self, u, c))
        )
        self.app.add_handler(
            CommandHandler("status", lambda u, c: commands.cmd_status(self, u, c))
        )
        self.app.add_handler(
            CommandHandler("stop", lambda u, c: commands.cmd_stop(self, u, c))
        )

        # Messages
        self.app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                lambda u, c: messages.handle_text_input(self, u, c),
            )
        )
        self.app.add_handler(
            MessageHandler(
                filters.PHOTO, lambda u, c: messages.handle_photo(self, u, c)
            )
        )
        self.app.add_handler(
            MessageHandler(
                filters.VOICE, lambda u, c: messages.handle_voice(self, u, c)
            )
        )

        # Callbacks
        self.app.add_handler(
            CallbackQueryHandler(lambda u, c: callbacks.handle_button(self, u, c))
        )

        # Error
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
        self,
        update: object,
        context: ContextTypes.DEFAULT_TYPE,
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

    async def _check_auth(self, update: object) -> bool:
        """Helper per verificare l'autenticazione (usato anche internamente)."""
        # Nota: gli handler esterni devono chiamare service._check_auth(update)
        # Ma _check_auth originale prendeva 'update: Update'.
        # Qui lo rendo pubblico o accessibile come helper.
        # Poiché è usato dagli handler esterni, deve essere accessibile.
        # È definito qui.
        if not hasattr(update, "effective_user") or not update.effective_user:
            return False
        user_id = str(update.effective_user.id)
        if self.connected_chat_id and user_id != self.connected_chat_id:
            with suppress(Exception):
                if hasattr(update, "message") and update.message:
                    await update.message.reply_text("⛔ Accesso Negato")
            return False
        return True

    def send_message_sync(self, message: str):
        """Invia un messaggio di testo in modo sincrono (thread-safe)."""
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
                    parse_mode=telegram.constants.ParseMode.MARKDOWN
                    if "*" in text
                    else None,
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
                    parse_mode=telegram.constants.ParseMode.MARKDOWN
                    if caption
                    else None,
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
                        parse_mode=telegram.constants.ParseMode.MARKDOWN
                        if caption
                        else None,
                    )
            except Exception as e:
                self.log_signal.emit(f"❌ Fallito invio documento a Telegram: {e}")
