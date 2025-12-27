"""
Bot TS - Bot Worker
Thread worker per eseguire i bot in background.
"""
import traceback
import threading
from PyQt6.QtCore import pyqtSignal, QThread

class BotWorker(QThread):
    """Thread worker per eseguire i bot in background."""

    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)
    request_input_signal = pyqtSignal(str, dict, threading.Event)

    def __init__(self, bot, data):
        super().__init__()
        self.bot = bot
        self.data = data
        self._is_running = True

    def run(self):
        """Esegue il bot."""
        try:
            # Collega i callback
            self.bot.set_log_callback(self.log_signal.emit)

            # Setup input callback se supportato dal bot
            if hasattr(self.bot, 'set_input_callback'):
                self.bot.set_input_callback(self._request_input_wrapper)

            result = self.bot.execute(self.data)
            self.finished_signal.emit(result)
        except Exception as e:
            error_trace = traceback.format_exc()
            self.log_signal.emit(f"[ERRORE CRITICO] {e}\n{error_trace}")
            self.finished_signal.emit(False)

    def _request_input_wrapper(self, prompt: str) -> str:
        """Wrapper thread-safe per chiedere input alla GUI."""
        result_container = {}
        event = threading.Event()
        self.request_input_signal.emit(prompt, result_container, event)
        event.wait()
        return result_container.get('value', '')

    def stop(self):
        """Richiede lo stop del bot."""
        self._is_running = False
        if self.bot:
            self.bot.request_stop()
