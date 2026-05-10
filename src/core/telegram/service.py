# mypy: disable-error-code="no-any-unimported"
import asyncio
import threading
import time
from collections.abc import Callable, Coroutine
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from typing import Any

import telegram
from PySide6.QtCore import QObject, Signal
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from src.core import config_manager
from src.core.constants import Icons
from src.core.exceptions import BotError
from src.core.telegram.handlers import callbacks, commands, messages
from src.utils.helpers import get_asset_path


class TelegramService(QObject):
    """
    Bridge intelligente tra Telegram e l'applicazione PySide6.
    Supporta comandi vocali, NLU e dialoghi contestuali.
    Refactored per delegare la logica ai moduli handlers/.
    """

    log_signal = Signal(str)
    command_received = Signal(str, dict)
    data_received = Signal(str, list)
    status_requested = Signal(str)
    screenshot_requested = Signal(str)
    query_received = Signal(str, str)
    photo_received = Signal(str, bytes, str)
    intent_received = Signal(str, dict)

    def __init__(self) -> None:
        super().__init__()
        self.app: Application[Any, Any, Any, Any, Any, Any] | None = None
        self.loop: asyncio.AbstractEventLoop | None = None
        self.stop_event = threading.Event()
        self._service_thread: threading.Thread | None = None
        self.connected_chat_id: str | None = None
        self.user_states: dict[int, Any] = {}
        self.pdl_settings: dict[int, Any] = {}  # Settings specifici per PDL (es. merge_all)
        self.pending_data: dict[str, Any] = {}
        self._start_lock = threading.Lock()
        self.ai_executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="Telegram_AI")

    def start_service(self) -> None:
        """Avvia o riavvia il servizio in modo thread-safe."""
        with self._start_lock:
            if self._service_thread and self._service_thread.is_alive():
                self.log_signal.emit("Riavvio del servizio Telegram in corso...")
                self.stop_service()
                time.sleep(2.0)  # Wait for TCP connections to fully close

            config = config_manager.load_config()
            token = config.get("telegram_token", "")
            self.connected_chat_id = config.get("telegram_chat_id", "")
            if not token:
                icon = get_asset_path(Icons.ALERT)
                self.log_signal.emit(f"<img src='{icon}' width='14' height='14'> Telegram Token mancante.")
                return

            self.stop_event.clear()
            self._service_thread = threading.Thread(target=self._run_async_loop, args=(token,), daemon=True)
            self._service_thread.start()

    def stop_service(self) -> None:
        """Ferma il servizio e attende la sua terminazione (metodo bloccante)."""
        if self._service_thread and self._service_thread.is_alive():
            icon = get_asset_path(Icons.CLOCK)
            self.log_signal.emit(
                f"<img src='{icon}' width='14' height='14'> Arresto servizio Telegram in corso..."
            )
            self.stop_event.set()
            self._service_thread.join(timeout=12)
            if self._service_thread.is_alive():
                icon = get_asset_path(Icons.ALERT)
                self.log_signal.emit(
                    f"<img src='{icon}' width='14' height='14'> Timeout: il thread di Telegram non si  fermato correttamente."
                )
            else:
                self.log_signal.emit("Servizio Telegram fermato.")

    def _run_async_loop(self, token: str) -> None:
        """Loop principale asincrono del bot Telegram."""
        self._execute_loop(lambda: self._main_loop_logic(token))

    async def _main_loop_logic(self, token: str) -> None:
        """Logica interna del loop asincrono (separata per testabilita')."""
        self.app = self._build_application(token)
        self._add_handlers()
        icon = get_asset_path(Icons.CHECK_CIRCLE)
        self.log_signal.emit(f"<img src='{icon}' width='14' height='14'> Servizio Telegram Attivo")

        try:
            await self.app.initialize()
            if not self.stop_event.is_set() and self.app.updater:
                await self.app.updater.start_polling(drop_pending_updates=True)
                await self.app.start()
                while not self.stop_event.is_set():
                    await asyncio.sleep(1)
        finally:
            await self._shutdown_application()

    def _build_application(self, token: str) -> Application[Any, Any, Any, Any, Any, Any]:
        return Application.builder().token(token).read_timeout(10).connect_timeout(10).build()

    def _add_handlers(self) -> None:
        if self.app is None:
            raise BotError("App not initialized")

        # Commands
        self.app.add_handler(CommandHandler("start", lambda u, c: commands.cmd_start(self, u, c)))
        self.app.add_handler(CommandHandler("status", lambda u, c: commands.cmd_status(self, u, c)))
        self.app.add_handler(CommandHandler("stop", lambda u, c: commands.cmd_stop(self, u, c)))

        # Messages
        self.app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                lambda u, c: messages.handle_text_input(self, u, c),
            )
        )
        self.app.add_handler(MessageHandler(filters.PHOTO, lambda u, c: messages.handle_photo(self, u, c)))
        self.app.add_handler(MessageHandler(filters.VOICE, lambda u, c: messages.handle_voice(self, u, c)))

        # Callbacks
        self.app.add_handler(CallbackQueryHandler(lambda u, c: callbacks.handle_button(self, u, c)))

        # Error
        self.app.add_error_handler(self._handle_error)

    async def _shutdown_application(self) -> None:
        self.log_signal.emit("Spegnimento del bot Telegram...")
        try:
            if not self.app:
                return

            async def sequence() -> None:
                if self.app and self.app.updater and self.app.updater.running:
                    await self.app.updater.stop()
                if self.app and self.app.running:
                    await self.app.stop()
                if self.app:
                    await self.app.shutdown()

            await asyncio.wait_for(sequence(), timeout=5.0)
            self.log_signal.emit("Bot Telegram spento.")
        except Exception as e:
            icon = get_asset_path(Icons.ALERT)
            self.log_signal.emit(f"<img src='{icon}' width='14' height='14'> Errore spegnimento: {e}")

    def _execute_loop(self, main_coro_func: Callable[[], Coroutine[Any, Any, None]]) -> None:
        """Esegue una coroutine nel loop del thread dedicato."""
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(main_coro_func())
        except Exception as e:
            if not self.stop_event.is_set():
                icon = get_asset_path(Icons.X_CIRCLE)
                self.log_signal.emit(f"<img src='{icon}' width='14' height='14'> Errore critico loop: {e}")
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
            icon = get_asset_path(Icons.STATUS_DOT_RED)
            self.log_signal.emit(
                f"<img src='{icon}' width='14' height='14'> <b>CONFLITTO TELEGRAM:</b> Rilevata altra istanza attiva. Arresto servizio."
            )
            self.stop_event.set()
        elif isinstance(context.error, telegram.error.NetworkError):
            icon = get_asset_path(Icons.ALERT)
            self.log_signal.emit(
                f"<img src='{icon}' width='14' height='14'> Errore Rete Telegram: {context.error}"
            )
        else:
            icon = get_asset_path(Icons.X_CIRCLE)
            self.log_signal.emit(
                f"<img src='{icon}' width='14' height='14'> Errore Telegram Imprevisto: {context.error}"
            )

    async def _check_auth(self, update: object) -> bool:
        """Helper per verificare l'autenticazione (usato anche internamente)."""
        if not hasattr(update, "effective_user") or not update.effective_user:
            return False
        user_id = str(update.effective_user.id)
        if self.connected_chat_id and user_id != self.connected_chat_id:
            with suppress(Exception):
                if hasattr(update, "message") and update.message:
                    await update.message.reply_text("[BLOCCO] Accesso Negato")
            return False
        return True

    def send_message_sync(self, message: str) -> None:
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
                icon = get_asset_path(Icons.X_CIRCLE)
                self.log_signal.emit(f"<img src='{icon}' width='14' height='14'> Errore invio Telegram: {e}")

    def send_photo_sync(self, photo_bytes: bytes, caption: str = "") -> None:
        """Invia una foto in modo sincrono caricando i byte nel loop asincrono."""
        if not self.connected_chat_id:
            config = config_manager.load_config()
            self.connected_chat_id = config.get("telegram_chat_id", "")

        if self.loop and self.loop.is_running() and self.connected_chat_id:
            try:
                asyncio.run_coroutine_threadsafe(
                    self._send_photo_async(self.connected_chat_id, photo_bytes, caption),
                    self.loop,
                )
            except Exception as e:
                icon = get_asset_path(Icons.X_CIRCLE)
                self.log_signal.emit(f"<img src='{icon}' width='14' height='14'> Errore invio foto: {e}")

    def send_document_sync(self, file_path: str, caption: str = "") -> None:
        """Invia un documento (file locale) in modo sincrono."""
        if not self.connected_chat_id:
            config = config_manager.load_config()
            self.connected_chat_id = config.get("telegram_chat_id", "")

        if self.loop and self.loop.is_running() and self.connected_chat_id:
            try:
                asyncio.run_coroutine_threadsafe(
                    self._send_document_async(self.connected_chat_id, file_path, caption),
                    self.loop,
                )
            except Exception as e:
                icon = get_asset_path(Icons.X_CIRCLE)
                self.log_signal.emit(f"<img src='{icon}' width='14' height='14'> Errore invio documento: {e}")

    async def _send_message_async(self, chat_id: str | int, text: str) -> None:
        try:
            if self.app is None:
                raise BotError("App not initialized")  # noqa: TRY301
            if not self.app.bot:
                await self.app.initialize()
            if self.app.bot is None:
                raise BotError("Bot not initialized")  # noqa: TRY301
            await self.app.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=telegram.constants.ParseMode.MARKDOWN if "*" in text else None,
            )
        except Exception as e:
            icon = get_asset_path(Icons.X_CIRCLE)
            self.log_signal.emit(
                f"<img src='{icon}' width='14' height='14'> Fallito invio messaggio a Telegram: {e}"
            )

    async def _send_photo_async(self, chat_id: str | int, photo_bytes: bytes, caption: str) -> None:
        try:
            if self.app is None:
                raise BotError("App not initialized")  # noqa: TRY301
            if not self.app.bot:
                await self.app.initialize()
            if self.app.bot is None:
                raise BotError("Bot not initialized")  # noqa: TRY301
            await self.app.bot.send_photo(
                chat_id=chat_id,
                photo=photo_bytes,
                caption=caption,
                parse_mode=telegram.constants.ParseMode.MARKDOWN if caption else None,
            )
        except Exception as e:
            icon = get_asset_path(Icons.X_CIRCLE)
            self.log_signal.emit(
                f"<img src='{icon}' width='14' height='14'> Fallito invio foto a Telegram: {e}"
            )

    async def _send_document_async(self, chat_id: str | int, file_path: str, caption: str) -> None:
        try:
            if self.app is None:
                raise BotError("App not initialized")  # noqa: TRY301
            if not self.app.bot:
                await self.app.initialize()
            if self.app.bot is None:
                raise BotError("Bot not initialized")  # noqa: TRY301
            with open(file_path, "rb") as f:
                await self.app.bot.send_document(
                    chat_id=chat_id,
                    document=f,
                    caption=caption,
                    parse_mode=telegram.constants.ParseMode.MARKDOWN if caption else None,
                )
        except Exception as e:
            icon = get_asset_path(Icons.X_CIRCLE)
            self.log_signal.emit(
                f"<img src='{icon}' width='14' height='14'> Fallito invio documento a Telegram: {e}"
            )
