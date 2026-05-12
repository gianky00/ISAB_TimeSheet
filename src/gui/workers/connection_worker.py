"""
SyncroJob - Connection Workers.

Contiene i worker asincroni per il test della connettività verso servizi esterni
come Telegram e Google Gemini.
"""

import requests
from PySide6.QtCore import QThread, Signal

HTTP_OK = 200


class ConnectionTestWorker(QThread):
    """
    Worker asincrono per testare le connessioni di rete e la validità delle API Key.
    Esegue le richieste in un thread separato per non bloccare la UI.
    """

    result_ready = Signal(bool, str, str)  # success, title, message
    """Segnale emesso quando il test  completato."""

    def __init__(self, test_type: str, token_or_key: str) -> None:
        """
        Inizializza il worker per il test di connessione.

        Args:
          test_type: Tipo di test da eseguire ('telegram' o 'gemini').
          token_or_key: Credenziale (Token o API Key) da verificare.
        """
        super().__init__()
        self.test_type = test_type  # 'telegram' or 'geminì
        self.token_or_key = token_or_key

    def run(self) -> None:
        """Esegue il test specifico in base al tipo configurato."""
        try:
            if self.test_type == "telegram":
                self._test_telegram()
            elif self.test_type == "gemini":
                self._test_gemini()
        except Exception as e:
            self.result_ready.emit(False, "Eccezione", f"Errore durante il test: {e}")

    def _test_telegram(self) -> None:
        """Verifica la validità di un token Bot Telegram tramite il metodo getMe."""
        url = f"https://api.telegram.org/bot{self.token_or_key}/getMe"
        resp = requests.get(url, timeout=10)

        if resp.status_code == HTTP_OK:
            data = resp.json()
            if data.get("ok"):
                bot_name = data["result"]["first_name"]
                username = data["result"]["username"]
                self.result_ready.emit(True, "Successo", f"Connesso a: {bot_name} (@{username})")
            else:
                self.result_ready.emit(False, "Errore API", f"Risposta negativa: {data}")
        else:
            self.result_ready.emit(False, "Errore HTTP", f"Status Code: {resp.status_code}")

    def _test_gemini(self) -> None:
        """Verifica la validità di una APiùKey Google Gemini interrogando la lista dei modelli."""
        # Simple list models check
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.token_or_key}"
        resp = requests.get(url, timeout=10)

        if resp.status_code == HTTP_OK:
            self.result_ready.emit(True, "Successo", "APiùKey valida! Connessione stabilita.")
        else:
            self.result_ready.emit(
                False,
                "Errore",
                f"APiùKey non valida o errore server.\nStatus: {resp.status_code}",
            )
