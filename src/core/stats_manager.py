"""
SyncroJob - Statistics Manager
Gestisce il salvataggio persistente delle statistiche di utilizzo.
"""

import json
from contextlib import suppress
from datetime import datetime
from typing import Any, Optional

from src.core import config_manager


class StatsManager:
    """
    Gestore delle statistiche di utilizzo dei bot.
    Utilizza il pattern Singleton e salva i dati nel file di configurazione globale.
    """

    _instance: Optional["StatsManager"] = None

    def __new__(cls) -> "StatsManager":
        """Assicura un'unica istanza del manager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self) -> None:
        """Inizializza il manager caricando i dati da config.json."""
        self.stats: dict[str, Any] = self._load_stats()

    def _load_stats(self) -> dict[str, Any]:
        """Carica le statistiche dal config_manager con migrazione automatica."""
        config = config_manager.load_config()

        # Se non ci sono statistiche nel config, prova a migrare dal vecchio file
        if not config.get("statistics"):
            old_file = config_manager.CONFIG_DIR / "statistics.json"
            if old_file.exists():
                with suppress(Exception), old_file.open("r", encoding="utf-8") as f:
                    old_stats: dict[str, Any] = json.load(f)
                    if old_stats:
                        config_manager.set_config_value("statistics", old_stats)
                        return old_stats
            return {}

        return config.get("statistics", {})  # type: ignore[no-any-return]

    def _save_stats(self) -> None:
        """Salva le statistiche nel config_manager."""
        config_manager.set_config_value("statistics", self.stats)

    def increment_usage(self, bot_id: str) -> None:
        """Incrementa il contatore di utilizzo per un bot e aggiorna l'ultimo avvio."""
        if bot_id not in self.stats:
            self.stats[bot_id] = {"runs": 0, "errors": 0, "last_run": None}

        # Ensure structure integrity for old stats
        if "runs" not in self.stats[bot_id]:
            self.stats[bot_id]["runs"] = 0
        if "errors" not in self.stats[bot_id]:
            self.stats[bot_id]["errors"] = 0

        self.stats[bot_id]["runs"] += 1
        self.stats[bot_id]["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_stats()

    def increment_error(self, bot_id: str) -> None:
        """Incrementa il contatore di errori per un bot."""
        if bot_id not in self.stats:
            self.stats[bot_id] = {"runs": 0, "errors": 0, "last_run": None}

        # Ensure structure integrity
        if "errors" not in self.stats[bot_id]:
            self.stats[bot_id]["errors"] = 0

        self.stats[bot_id]["errors"] += 1
        self._save_stats()

    def get_all_stats(self) -> dict[str, Any]:
        """Restituisce tutte le statistiche."""
        return self.stats
