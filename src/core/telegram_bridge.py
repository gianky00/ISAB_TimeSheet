"""
SyncroJob - Telegram UI Bridge
Punto di ingresso centrale per la comunicazione tra il servizio Telegram e la Desktop UI.
Refactored V9.5: Modularized into specialized handlers.
"""

import base64
import logging
import threading
from typing import Any

from PyQt6.QtCore import QObject

from src.core.lyra_client import LyraClient
from src.core.notification_manager import NotificationManager
from src.core.secrets_manager import SecretsManager

# Modular Bridge Components
from .telegram.bridge.data_processor import TelegramDataProcessor
from .telegram.bridge.intent_handler import TelegramIntentHandler
from .telegram.bridge.system_handler import TelegramSystemHandler
from .telegram.bridge.ui_commands import TelegramUICommands

logger = logging.getLogger(__name__)


class TelegramUIBridge(QObject):
    """
    Coordina l'interazione tra Telegram e l'applicazione Desktop.
    Delega l'esecuzione effettiva ai sottomoduli specializzati in src/core/telegram/bridge/.
    """

    def __init__(self, main_window: Any) -> None:
        super().__init__()
        self.mw = main_window
        self.telegram = main_window.telegram

        # Inizializza gli handler modulari
        self.ui_commands = TelegramUICommands(self.mw, self.telegram)
        self.data_processor = TelegramDataProcessor(self.mw, self.telegram)
        self.system_handler = TelegramSystemHandler(self.mw, self.telegram)
        self.intent_handler = TelegramIntentHandler(self.mw, self.telegram)

    def setup_connections(self) -> None:
        """Collega i segnali del servizio Telegram agli handler corrispondenti."""
        t = self.telegram

        # 1. Logging & Notifiche
        t.log_signal.connect(lambda m: NotificationManager.instance().add_notification("Telegram", m))

        # 2. Comandi & Dati
        t.command_received.connect(self._dispatch_command)
        t.data_received.connect(self._dispatch_data)

        # 3. Richieste Sistema
        t.status_requested.connect(self.system_handler.handle_status)
        t.screenshot_requested.connect(self.system_handler.handle_screenshot)

        # 4. Intelligenza Artificiale
        t.query_received.connect(self._handle_ai_query)
        t.photo_received.connect(self._handle_photo)
        t.intent_received.connect(self.intent_handler.handle_intent)

    def _dispatch_command(self, command: str, params: dict[str, Any]) -> None:
        """Smista i comandi testuali agli handler UI o Sistema."""
        cmd_map = {
            "search_db_pdf": self.system_handler.handle_search_db_pdf,
            "run_pdl": self.ui_commands.run_pdl_bot,
            "list_pdl": lambda _: self.ui_commands.list_pdl(),
            "clear_pdl": lambda _: self.ui_commands.clear_pdl(),
            "run_ts": lambda _: self.ui_commands.run_ts_bot(),
            "run_carico": lambda _: self.ui_commands.run_carico_bot(),
            "run_prenota_bp": lambda _: self.ui_commands.run_prenota_bp_bot(),
            "run_timbrature": self.ui_commands.run_timbrature_bot,
            "restart_app": lambda _: self.system_handler.handle_restart_app(),
            "stop_all": lambda _: self.ui_commands.stop_all_bots(),
        }

        if handler := cmd_map.get(command):
            handler(params)

    def _dispatch_data(self, data_type: str, items: list[str]) -> None:
        """Smista l'inserimento dati al data processor."""
        data_map = {
            "pdl": self.data_processor.process_pdl_items,
            "oda": self.data_processor.process_oda_items,
            "bp": self.data_processor.process_bp_items,
        }
        if handler := data_map.get(data_type):
            handler(items)

    def _handle_ai_query(self, chat_id: int, query: str) -> None:
        """Gestisce le query testuali libere tramite Lyra."""
        api_key = SecretsManager.get_gemini_api_key()
        if not api_key:
            self.telegram.send_message_sync("⚠️ API Key mancante.")
            return

        def run():
            try:
                resp = LyraClient(api_key=api_key).ask(query)
                self.telegram.send_message_sync(f"🤖 **AI Coach**\n\n{resp}")
            except Exception as e:
                self.telegram.send_message_sync(f"❌ Errore AI: {e}")

        threading.Thread(target=run, daemon=True).start()

    def _handle_photo(self, chat_id: int, photo_bytes: bytes, caption: str | None) -> None:
        """Gestisce l'analisi OCR/AI delle foto inviate."""
        api_key = SecretsManager.get_gemini_api_key()
        if not api_key:
            self.telegram.send_message_sync("⚠️ API Key mancante.")
            return
        self.telegram.send_message_sync("🔍 **Analisi Documento...**")

        def run():
            try:
                img_b64 = base64.b64encode(photo_bytes).decode("utf-8")
                prompt = "Estrai dati da questo rapportino. Tabella Markdown."
                if caption:
                    prompt += f"\nNote: {caption}"
                resp = LyraClient(api_key=api_key).ask(prompt, images=[img_b64])
                self.telegram.send_message_sync(f"📝 **Dati Estratti**\n\n{resp}")
            except Exception as e:
                self.telegram.send_message_sync(f"❌ Errore: {e}")

        threading.Thread(target=run, daemon=True).start()
