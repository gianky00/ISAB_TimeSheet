from typing import Any

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
        images: list[Any] | None = None,
        provider: str | None = None,
        model_name: str | None = None,
        ollama_url: str | None = None,
    ):
        super().__init__()
        self.api_key = api_key
        self.question = question
        self.context = context
        self.images = images or []
        self.provider = provider
        self.model_name = model_name
        self.ollama_url = ollama_url

    def run(self) -> None:
        """Esegue la chiamata asincrona all'API Lyra."""
        try:
            client = LyraClient(
                api_key=self.api_key,
                provider=self.provider,
                model_name=self.model_name,
                ollama_url=self.ollama_url,
            )
            answer = client.ask(self.question, self.context, self.images)
            if not answer:
                answer = "⚠️ L'AI non ha restituito alcuna risposta. Verifica che il modello sia caricato correttamente."
            self.finished.emit(answer)
        except Exception as e:
            self.finished.emit(f"Errore critico durante l'interazione AI:\n{e}")


class ModelListWorker(QThread):
    """Thread worker per il recupero asincrono della lista dei modelli disponibili."""

    finished = pyqtSignal(list)

    def __init__(self, api_key: str, provider: str | None = None, ollama_url: str | None = None):
        super().__init__()
        self.api_key = api_key
        self.provider = provider
        self.ollama_url = ollama_url

    def run(self) -> None:
        """Recupera la lista dei modelli supportati dal provider configurato."""
        try:
            client = LyraClient(api_key=self.api_key, provider=self.provider, ollama_url=self.ollama_url)
            models = client.list_models()
            self.finished.emit(models)
        except Exception:
            self.finished.emit([])
