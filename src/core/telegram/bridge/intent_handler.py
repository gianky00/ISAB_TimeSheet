"""SyncroJob - Telegram Bridge Intent Handler.

Traduce gli intenti estratti dall'AI in azioni concrete sulla UI.
"""

import asyncio
import logging
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QObject
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.core.telegram.bridge.data_processor import TelegramDataProcessor
from src.core.telegram.bridge.ui_commands import TelegramUICommands
from src.utils.printing import get_installed_printers
from src.utils.validators import InputValidator

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow

logger = logging.getLogger(__name__)


class TelegramIntentHandler(QObject):
    """Gestisce la logica di business derivante dagli intenti AI di Telegram.

    Inizializza la classe.
    """

    def __init__(self, main_window: "MainWindow", telegram_service: Any, system_handler: Any = None) -> None:
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service
        self.system_handler = system_handler
        self.data_processor = TelegramDataProcessor(main_window, telegram_service)

    def handle_intent(self, chat_id: int, intent: dict[str, Any]) -> None:
        """Punto di ingresso per il processing degli intenti AI."""
        action = intent.get("action")
        obj = intent.get("object")
        items = intent.get("items", [])

        # 1. Processamento Dati
        if items:
            self._process_intent_data(str(obj) if obj else "", items)

        # 2. Processamento Azione
        if action == "print" and obj == "pdl":
            self._handle_print_pdl(chat_id, items)
        elif action == "download" and obj == "pdl":
            self._handle_download_pdl(chat_id)
        elif action == "download":
            self._handle_generic_download(str(obj) if obj else "")
        elif action == "status" and self.system_handler:
            self.system_handler.handle_status()
        elif action == "restart" and self.system_handler:
            self.system_handler.handle_restart_app()

    def _process_intent_data(self, obj: str, items: list[Any]) -> None:
        """Aggiunge dati ai pannelli in base all'oggetto dell'intento."""
        if obj == "pdl":
            valid = [i for i in items if InputValidator.validate_pdl(i).valid]
            if valid:
                rows = [{"numero_pdl": InputValidator.validate_pdl(v).sanitized_value} for v in valid]
                panel = getattr(self.mw, "pdl_panel", None)
                if panel:
                    panel.add_rows_simple(rows)
                    self.mw.show_toast(f"Telegram: aggiunti {len(valid)} PDL")
        elif obj == "oda":
            valid = [i for i in items if InputValidator.validate_oda(i).valid]
            if valid:
                rows = [{"numero_oda": InputValidator.validate_oda(v).sanitized_value} for v in valid]
                panel = getattr(self.mw, "scarico_panel", None)
                if panel:
                    panel.add_rows_simple(rows)
                    self.mw.show_toast(f"Telegram: aggiunti {len(valid)} OdA")

    def _handle_print_pdl(self, chat_id: int, items: list[str]) -> None:
        self.telegram.pending_data[chat_id] = {"action": "print", "items": items}
        printers = get_installed_printers()[:6]
        keyboard = [
            [InlineKeyboardButton(f"    {p[:30]}", callback_data=f"sel_print_run_{p[:25]}")] for p in printers
        ]

        self.telegram.send_message_sync("✅ Ho aggiunto i PDL. **Quale stampante utilizzo?**")
        coro = self.telegram.app.bot.send_message(
            chat_id=chat_id,
            text=f"✅ PDL {', '.join(items)} pronti. **Quale stampante uso?**",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        self._run_coroutine(coro)

    def _handle_download_pdl(self, chat_id: int) -> None:
        keyboard = [
            [
                InlineKeyboardButton("✅ S , stampa", callback_data="confirm_print_yes"),
                InlineKeyboardButton("❌ No, solo download", callback_data="confirm_print_no"),
            ]
        ]
        coro = self.telegram.app.bot.send_message(
            chat_id=chat_id,
            text="Aggiunti PDL. **Vuoi che li stampiùanche?**",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        self._run_coroutine(coro)

    def _handle_generic_download(self, obj: str) -> None:
        cmds = TelegramUICommands(self.mw, self.telegram)
        if obj == "oda":
            cmds.run_ts_bot()
        elif obj == "timbrature":
            cmds.run_timbrature_bot({"period": "today"})
        else:
            self.telegram.send_message_sync(f"⚠️ Non so come scaricare '{obj}'.")

    def _run_coroutine(self, coro: Any) -> None:
        """Helper per eseguire coroutine in modo sicuro anche durante i test."""
        if not asyncio.iscoroutine(coro):

            async def _fake() -> None:
                return None

            coro = _fake()
        asyncio.run_coroutine_threadsafe(coro, self.telegram.loop)
