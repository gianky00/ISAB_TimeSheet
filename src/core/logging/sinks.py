"""
Advanced sinks per output specializzati.
"""

import json
from typing import Any, Dict, Optional

from .config import get_config
from .formatters import JSONFormatter


class BotLogSink:
    """
    Sink specializzato per log di singole esecuzioni bot.

    Ogni bot run (identificato da trace_id) ha il proprio file JSON.
    """

    def __init__(self, config=None):
        self.config = config or get_config()
        self.formatter = JSONFormatter(mask_sensitive=True)

        # Cache file handles aperti (trace_id -> file handle)
        self._open_files: Dict[str, Any] = {}

    def write(
        self,
        level: str,
        logger_name: str,
        message: str,
        context: Dict[str, Any],
        extra: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None,
        source_info: Optional[Dict[str, Any]] = None,
    ):
        """
        Scrive log nel file specifico del bot run.

        Args:
            level: Livello log
            logger_name: Nome logger
            message: Messaggio
            context: Context con trace_id
            extra: Dati extra
            exception: Eccezione
            source_info: Info sorgente
        """
        # Estrai trace_id e bot_type
        trace_id = context.get("trace_id")
        bot_type = context.get("bot_type")

        if not trace_id or not bot_type:
            # Senza trace_id o bot_type, non possiamo scrivere
            return

        # Determina path file
        file_path = self.config.get_bot_log_path(bot_type, trace_id)

        # Assicura che directory esista
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Formatta log
        json_line = self.formatter.format(
            level, logger_name, message, extra, exception, source_info
        )

        # Scrivi su file
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(json_line + "\n")
        except Exception as e:
            print(f"[BOT SINK ERROR] Failed to write: {e}")

    def close_all(self):
        """Chiude tutti i file aperti."""
        for handle in self._open_files.values():
            try:
                handle.close()
            except Exception:
                pass
        self._open_files.clear()

    def get_bot_run_logs(self, bot_type: str, trace_id: str) -> list:
        """
        Legge tutti i log di un bot run.

        Args:
            bot_type: Tipo bot
            trace_id: Trace ID

        Returns:
            Lista di log entries
        """
        file_path = self.config.get_bot_log_path(bot_type, trace_id)

        if not file_path.exists():
            return []

        logs = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    logs.append(json.loads(line))
        except Exception as e:
            print(f"[BOT SINK ERROR] Failed to read: {e}")

        return logs


class MetricsRotatingSink:
    """
    Sink per metriche con rotazione automatica.

    Ruota file metrics quando raggiunge dimensione massima.
    """

    def __init__(self, config=None, max_size_mb: float = 10.0):
        self.config = config or get_config()
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.metrics_file = self.config.metrics_dir / "performance.jsonl"

        # Assicura directory
        self.config.metrics_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metric_dict: Dict[str, Any]):
        """
        Scrive metrica su file.

        Args:
            metric_dict: Metrica come dizionario
        """
        # Check rotazione
        self._rotate_if_needed()

        # Scrivi metrica
        try:
            with open(self.metrics_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(metric_dict, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[METRICS SINK ERROR] Failed to write: {e}")

    def _rotate_if_needed(self):
        """Ruota file se necessario."""
        if not self.metrics_file.exists():
            return

        # Check dimensione
        size = self.metrics_file.stat().st_size

        if size > self.max_size_bytes:
            # Ruota: rinomina file corrente con timestamp
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            rotated_file = self.metrics_file.with_suffix(f".{timestamp}.jsonl")

            try:
                self.metrics_file.rename(rotated_file)
            except Exception as e:
                print(f"[METRICS SINK ERROR] Failed to rotate: {e}")


class AggregatedMetricsSink:
    """
    Sink per metriche aggregate (summary giornaliero).

    Calcola statistiche aggregate e le salva in file separato.
    """

    def __init__(self, config=None):
        self.config = config or get_config()
        self.aggregated_dir = self.config.metrics_dir / "aggregated"
        self.aggregated_dir.mkdir(parents=True, exist_ok=True)

    def write_daily_summary(self, date: str, summary: Dict[str, Any]):
        """
        Scrive summary giornaliero.

        Args:
            date: Data in formato YYYY-MM-DD
            summary: Dict con summary
        """
        file_path = self.aggregated_dir / f"daily_{date}.json"

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[AGGREGATED SINK ERROR] Failed to write: {e}")

    def read_daily_summary(self, date: str) -> Optional[Dict[str, Any]]:
        """
        Legge summary giornaliero.

        Args:
            date: Data in formato YYYY-MM-DD

        Returns:
            Summary o None
        """
        file_path = self.aggregated_dir / f"daily_{date}.json"

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[AGGREGATED SINK ERROR] Failed to read: {e}")
            return None


# Singleton instances
_bot_sink = None
_metrics_sink = None
_aggregated_sink = None


def get_bot_sink() -> BotLogSink:
    """Restituisce istanza singleton del bot sink."""
    global _bot_sink
    if _bot_sink is None:
        _bot_sink = BotLogSink()
    return _bot_sink


def get_metrics_sink() -> MetricsRotatingSink:
    """Restituisce istanza singleton del metrics sink."""
    global _metrics_sink
    if _metrics_sink is None:
        _metrics_sink = MetricsRotatingSink()
    return _metrics_sink


def get_aggregated_sink() -> AggregatedMetricsSink:
    """Restituisce istanza singleton del aggregated sink."""
    global _aggregated_sink
    if _aggregated_sink is None:
        _aggregated_sink = AggregatedMetricsSink()
    return _aggregated_sink
