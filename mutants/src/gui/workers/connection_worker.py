import requests
from PyQt6.QtCore import QThread, pyqtSignal


class ConnectionTestWorker(QThread):
    """Worker asincrono per testare le connessioni di rete."""

    result_ready = pyqtSignal(bool, str, str)  # success, title, message

    def __init__(self, test_type, token_or_key):
        super().__init__()
        self.test_type = test_type  # 'telegram' or 'gemini'
        self.token_or_key = token_or_key

    def run(self):
        try:
            if self.test_type == "telegram":
                self._test_telegram()
            elif self.test_type == "gemini":
                self._test_gemini()
        except Exception as e:
            self.result_ready.emit(False, "Eccezione", f"Errore durante il test: {e}")

    def _test_telegram(self):
        url = f"https://api.telegram.org/bot{self.token_or_key}/getMe"
        resp = requests.get(url, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            if data.get("ok"):
                bot_name = data["result"]["first_name"]
                username = data["result"]["username"]
                self.result_ready.emit(
                    True, "Successo", f"Connesso a: {bot_name} (@{username})"
                )
            else:
                self.result_ready.emit(
                    False, "Errore API", f"Risposta negativa: {data}"
                )
        else:
            self.result_ready.emit(
                False, "Errore HTTP", f"Status Code: {resp.status_code}"
            )

    def _test_gemini(self):
        # Simple list models check
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.token_or_key}"
        resp = requests.get(url, timeout=10)

        if resp.status_code == 200:
            self.result_ready.emit(
                True, "Successo", "API Key valida! Connessione stabilita."
            )
        else:
            self.result_ready.emit(
                False,
                "Errore",
                f"API Key non valida o errore server.\nStatus: {resp.status_code}",
            )
