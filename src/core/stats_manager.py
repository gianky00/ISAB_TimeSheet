import json
import queue
import threading
import time
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any, Optional

from src.core import config_manager
from src.core.constants import FileNames


class StatsManager:
    """
    Gestore singleton per le metriche di utilizzo delle automazioni.
    Supporta salvataggi asincroni per non bloccare il thread principale.
    """

    _instance: Optional["StatsManager"] = None

    def __new__(cls) -> "StatsManager":
        """Assicura l'esistenza di un'unica istanza globale del manager (Singleton)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self) -> None:
        """Inizializza il manager caricando i dati storici dalla configurazione globale."""
        self.stats: dict[str, Any] = self._load_stats()
        
        # Meccanismo di salvataggio asincrono
        self._save_queue: queue.Queue = queue.Queue()
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

    def _load_stats(self) -> dict[str, Any]:
        """
        Carica le statistiche dal gestore di configurazione.
        Include un meccanismo di migrazione per recuperare dati da versioni legacy (statistics.json).

        Returns:
            dict: Dizionario contenente le statistiche raggruppate per ID bot.
        """
        config = config_manager.load_config()
        if not config.get("statistics"):
            old_file = config_manager.CONFIG_DIR / FileNames.STATISTICS
            if old_file.exists():
                with suppress(Exception), old_file.open("r", encoding="utf-8") as f:
                    old_stats: dict[str, Any] = json.load(f)
                    if old_stats:
                        config_manager.set_config_value("statistics", old_stats)
                        return old_stats
            return {}
        from typing import cast

        return cast("dict[str, Any]", config.get("statistics", {}))

    def _worker_loop(self) -> None:
        """Loop per il salvataggio asincrono su disco."""
        import logging
        local_logger = logging.getLogger(__name__)

        while True:
            try:
                task = self._save_queue.get()
                if task is None:
                    break
                
                # Esegui il salvataggio effettivo
                stats_to_save = task
                config_manager.set_config_value("statistics", stats_to_save)
                self._save_queue.task_done()
            except Exception as e:
                local_logger.error(f"Stats Save Error: {e}")
                time.sleep(1)

    def _save_stats(self) -> None:
        """Invia una richiesta di salvataggio al worker di background."""
        # Inviamo una copia dei dati per evitare race conditions
        import copy
        self._save_queue.put(copy.deepcopy(self.stats))

    def increment_usage(self, bot_id: str) -> None:
        """
        Incrementa il contatore delle esecuzioni (runs) per un determinato bot.
        Aggiorna inoltre il timestamp dell'ultima attività rilevata.

        Args:
            bot_id: Identificativo unico dell'automazione (es. 'scarico_ts').
        """
        if bot_id not in self.stats:
            self.stats[bot_id] = {"runs": 0, "errors": 0, "last_run": None}
        if "runs" not in self.stats[bot_id]:
            self.stats[bot_id]["runs"] = 0
        if "errors" not in self.stats[bot_id]:
            self.stats[bot_id]["errors"] = 0

        self.stats[bot_id]["runs"] += 1
        self.stats[bot_id]["last_run"] = datetime.now(UTC).astimezone().strftime("%Y-%m-%d %H:%M:%S")
        self._save_stats()

    def increment_error(self, bot_id: str) -> None:
        """
        Registra un fallimento o un errore critico per un determinato bot.

        Args:
            bot_id: Identificativo unico dell'automazione.
        """
        if bot_id not in self.stats:
            self.stats[bot_id] = {"runs": 0, "errors": 0, "last_run": None}
        if "errors" not in self.stats[bot_id]:
            self.stats[bot_id]["errors"] = 0

        self.stats[bot_id]["errors"] += 1
        self._save_stats()

    def get_all_stats(self) -> dict[str, Any]:
        """
        Restituisce l'intero dataset delle statistiche di utilizzo.

        Returns:
            dict: Mappa bot_id -> {runs, errors, last_run}.
        """
        return self.stats
