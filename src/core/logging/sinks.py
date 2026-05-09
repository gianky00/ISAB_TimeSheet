"""
Advanced sinks per output specializzati.
"""

import json
from contextlib import suppress
from typing import Any

from .config import get_config
from .formatters import JSONFormatter


class BotLogSink:
    """
    Sink specializzato per log di singole esecuzioni bot.

    Ogni bot run (identificato da trace_id) ha il proprio file JSON.
    """

    def __init__(self, config: Any = None) -> None:
        self.config = config or get_config()
        self.formatter = JSONFormatter(mask_sensitive=True)

        # Cache file handles aperti (trace_id -> file handle)
        self._open_files: dict[str, Any] = {}

    def write(  # noqa: PLR0913
        self,
        level: str,
        logger_name: str,
        message: str,
        context: dict[str, Any],
        extra: dict[str, Any] | None = None,
        exception: Exception | None = None,
        source_info: dict[str, Any] | None = None,
    ) -> None:
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
        json_line = self.formatter.format(level, logger_name, message, extra, exception, source_info)

        # Scrivi su file
        try:
            with file_path.open("a", encoding="utf-8") as f:
                f.write(json_line + "\n")
        except Exception as e:
            print(f"[BOT SINK ERROR] Failed to write: {e}")

    def close_all(self) -> None:
        """Chiude tutti i file aperti."""
        for handle in self._open_files.values():
            with suppress(Exception):
                handle.close()
        self._open_files.clear()

    def get_bot_run_logs(self, bot_type: str, trace_id: str) -> list[dict[str, Any]]:
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

        logs: list[dict[str, Any]] = []
        try:
            with file_path.open(encoding="utf-8") as f:
                logs.extend(json.loads(line) for line in f)
        except Exception as e:
            print(f"[BOT SINK ERROR] Failed to read: {e}")

        return logs


class MetricsRotatingSink:
    """
    Sink per metriche con rotazione automatica.

    Ruota file metrics quando raggiunge dimensione massima.
    """

    def __init__(self, config: Any = None, max_size_mb: float = 10.0) -> None:
        self.config = config or get_config()
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.metrics_file = self.config.metrics_dir / "performance.jsonl"

        # Assicura directory
        self.config.metrics_dir.mkdir(parents=True, exist_ok=True)

    def write(self, metric_dict: dict[str, Any]) -> None:
        """
        Scrive metrica su file.

        Args:
          metric_dict: Metrica come dizionario
        """
        # Check rotazione
        self._rotate_if_needed()

        # Scrivi metrica
        try:
            with self.metrics_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(metric_dict, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[METRICS SINK ERROR] Failed to write: {e}")

    def _rotate_if_needed(self) -> None:
        """Ruota file se necessario."""
        if not self.metrics_file.exists():
            return

        # Check dimensione
        size = self.metrics_file.stat().st_size

        if size > self.max_size_bytes:
            # Ruota: rinomina file corrente con timestamp
            from datetime import UTC, datetime  # noqa: PLC0415

            timestamp = datetime.now(UTC).astimezone().strftime("%Y%m%d_%H%M%S")
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

    def __init__(self, config: Any = None) -> None:
        self.config = config or get_config()
        self.aggregated_dir = self.config.metrics_dir / "aggregated"
        self.aggregated_dir.mkdir(parents=True, exist_ok=True)

    def write_daily_summary(self, date: str, summary: dict[str, Any]) -> None:
        """
        Scrive summary giornaliero.

        Args:
          date: Data in formato YYYY-MM-DD
          summary: Dict con summary
        """
        file_path = self.aggregated_dir / f"daily_{date}.json"

        try:
            file_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"[AGGREGATED SINK ERROR] Failed to write: {e}")

    def read_daily_summary(self, date: str) -> dict[str, Any] | None:
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
            data: dict[str, Any] = json.loads(file_path.read_text(encoding="utf-8"))
            return data  # noqa: TRY300
        except Exception as e:
            print(f"[AGGREGATED SINK ERROR] Failed to read: {e}")
            return None


# Singleton instances
_bot_sink: BotLogSink | None = None
_metrics_sink: MetricsRotatingSink | None = None
_aggregated_sink: AggregatedMetricsSink | None = None


def get_bot_sink() -> BotLogSink:
    """Restituisce istanza singleton del bot sink."""
    global _bot_sink  # noqa: PLW0603
    if _bot_sink is None:
        _bot_sink = BotLogSink()
    return _bot_sink


def get_metrics_sink() -> MetricsRotatingSink:
    """Restituisce istanza singleton del metrics sink."""
    global _metrics_sink  # noqa: PLW0603
    if _metrics_sink is None:
        _metrics_sink = MetricsRotatingSink()
    return _metrics_sink


def get_aggregated_sink() -> AggregatedMetricsSink:
    """Restituisce istanza singleton del aggregated sink."""
    global _aggregated_sink  # noqa: PLW0603
    if _aggregated_sink is None:
        _aggregated_sink = AggregatedMetricsSink()
    return _aggregated_sink
