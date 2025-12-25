"""
Bot TS - Statistics Manager
Gestisce il salvataggio persistente delle statistiche di utilizzo.
"""
import json
from pathlib import Path
from src.core import config_manager

class StatsManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StatsManager, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        """Inizializza il manager caricando i dati."""
        self.stats_file = config_manager.CONFIG_DIR / "statistics.json"
        self.stats = self._load_stats()

    def _load_stats(self) -> dict:
        """Carica le statistiche dal file JSON."""
        if not self.stats_file.exists():
            return {}
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Errore caricamento statistiche: {e}")
            return {}

    def _save_stats(self):
        """Salva le statistiche su file."""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=4)
        except Exception as e:
            print(f"Errore salvataggio statistiche: {e}")

    def increment_usage(self, bot_id: str):
        """Incrementa il contatore di utilizzo per un bot."""
        if bot_id not in self.stats:
            self.stats[bot_id] = {"runs": 0, "errors": 0}

        self.stats[bot_id]["runs"] += 1
        self._save_stats()

    def increment_error(self, bot_id: str):
        """Incrementa il contatore di errori per un bot."""
        if bot_id not in self.stats:
            self.stats[bot_id] = {"runs": 0, "errors": 0}

        self.stats[bot_id]["errors"] += 1
        self._save_stats()

    def get_all_stats(self) -> dict:
        """Restituisce tutte le statistiche."""
        return self.stats
