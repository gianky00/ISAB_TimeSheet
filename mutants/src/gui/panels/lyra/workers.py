import traceback
from typing import Any, List, Optional

from PyQt6.QtCore import QThread, pyqtSignal

from src.core.lyra_client import LyraClient


class LyraWorker(QThread):
    """Thread worker dedicato all'interazione con l'API di Lyra (Gemini)."""

    finished = pyqtSignal(str)

    def __init__(
        self,
        api_key: str,
        question: str,
        context: str = "",
        images: Optional[List[Any]] = None,
    ):
        super().__init__()
        self.api_key = api_key
        self.question = question
        self.context = context
        self.images = images or []

    def run(self):
        try:
            if not self.api_key:
                self.finished.emit("Errore critico: Chiave API Gemini non trovata.")
                return
            client = LyraClient(api_key=self.api_key)
            answer = client.ask(self.question, self.context, self.images)
            self.finished.emit(answer)
        except Exception as e:
            self.finished.emit(
                f"Errore critico nel Worker di Lyra:\n{e}\n\n{traceback.format_exc()}"
            )


class ModelListWorker(QThread):
    """Thread worker per il recupero asincrono della lista dei modelli disponibili."""

    finished = pyqtSignal(list)

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    def run(self):
        try:
            if not self.api_key:
                self.finished.emit([])
                return
            client = LyraClient(api_key=self.api_key)
            models = client.list_models()
            self.finished.emit(models)
        except Exception:
            self.finished.emit([])
