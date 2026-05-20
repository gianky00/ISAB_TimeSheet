"""
SyncroJob - Bot Worker
Thread dedicato all'esecuzione asincrona dei bot di automazione.
Gestisce il ciclo di vita del driver, l'iniezione delle dipendenze e i segnali verso la GUI.
"""

from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QThread, Signal

from src.bots import create_bot

if TYPE_CHECKING:
    from src.bots.base.base_bot import BaseBot

logger = logging.getLogger(__name__)


class BotWorker(QThread):
    """
    Thread worker per eseguire i bot in background.
    Gestisce l'inizializzazione del bot (pesante) e l'esecuzione.
    """

    log_signal = Signal(str)
    status_signal = Signal(str)
    finished_signal = Signal(bool)
    request_input_signal = Signal(str, dict, threading.Event)
    row_status_signal = Signal(int, bool, str)  # index, success, message
    step_changed_signal = Signal(int, str, object)  # Bridge for timeline
    critical_error_signal = Signal(str, str)  # Bridge for license/fatal errors

    def __init__(
        self,
        bot_id: str | BaseBot,
        bot_params: dict[str, Any] | None = None,
        data: Any | None = None,
        telegram_service: Any | None = None,
    ) -> None:
        """
        Inizializza il worker del bot.

        Args:
          bot_id: ID del bot da creare o istanza già creata.
          bot_params: Parametri per create_bot (se bot_id  str).
          data: I dati di input per il bot.
          telegram_service: Servizio opzionale per notifiche Telegram.
        """
        super().__init__()
        self.bot_id = bot_id
        self.bot_params = bot_params or {}
        self.data = data
        self._is_running = True
        self.telegram_service = telegram_service
        self.bot: BaseBot | None = None

    def run(self) -> None:
        """Avvia l'esecuzione del bot nel thread dedicato."""
        try:
            # 1. Inizializzazione Differita (Background)
            if isinstance(self.bot_id, str):
                self.log_signal.emit("[SETUP] Preparazione ambiente bot...")
                self.bot = create_bot(self.bot_id, **self.bot_params)
            else:
                self.bot = self.bot_id

            if not self.bot:
                self.log_signal.emit("❌ Errore critico: Impossibile creare l'istanza del bot.")
                self.finished_signal.emit(False)
                return

            # 2. Configurazione Bot
            if self.telegram_service:
                self.bot.set_telegram_service(self.telegram_service)

            self.bot.set_log_callback(self.log_signal.emit)

            # Connessione segnali bot -> segnali worker
            self.bot.signals.step_changed.connect(self.step_changed_signal.emit)
            self.bot.signals.critical_error.connect(self.critical_error_signal.emit)

            if hasattr(self.bot, "set_input_callback"):
                self.bot.set_input_callback(self._request_input_wrapper)

            if hasattr(self.bot, "set_progress_callback"):
                self.bot.set_progress_callback(self.row_status_signal.emit)

            # 3. Esecuzione
            exec_data: list[dict[str, Any]] | dict[str, Any] = self.data if self.data is not None else []

            result = self.bot.execute(exec_data)
            self.finished_signal.emit(result)

        except Exception as e:
            logger.exception("Errore fatale durante l'esecuzione del BotWorker")
            self.log_signal.emit(f"[ERRORE CRITICO] {e}")
            self.finished_signal.emit(False)

        finally:
            if self.bot:
                self.bot.cleanup()

    def _request_input_wrapper(self, prompt: str) -> str:
        """
        Wrapper thread-safe per richiedere input all'utente tramite la GUI.
        Blocca l'esecuzione del bot finch  l'utente non risponde.
        """
        result_container: dict[str, str] = {}
        event = threading.Event()
        self.request_input_signal.emit(prompt, result_container, event)
        event.wait()
        return result_container.get("value", "")

    def stop(self) -> None:
        """Interrompe l'esecuzione del bot segnalando la richiesta di stop."""
        self._is_running = False
        if self.bot and hasattr(self.bot, "request_stop"):
            self.bot.request_stop()
