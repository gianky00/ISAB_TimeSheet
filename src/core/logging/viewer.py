"""
Log viewer e query utility.
"""

import json
import operator
from collections import defaultdict
from contextlib import suppress
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .config import get_config


class LogQuery:
    """Query builder per log JSON."""

    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.filters: list[Any] = []
        self._limit: int | None = None
        self._offset: int = 0

    def level(self, *levels: str) -> "LogQuery":
        """Filtra per livello."""
        self.filters.append(lambda entry: entry.get("level") in levels)
        return self

    def contains_message(self, text: str, case_sensitive: bool = False) -> "LogQuery":
        """Filtra per messaggio contenente testo."""

        def filter_fn(entry):
            message = entry.get("message", "")
            if not case_sensitive:
                message = message.lower()
                text_lower = text.lower()
                return text_lower in message
            return text in message

        self.filters.append(filter_fn)
        return self

    def context_match(self, **kwargs) -> "LogQuery":
        """Filtra per context fields."""

        def filter_fn(entry):
            context = entry.get("context", {})
            return all(context.get(key) == value for key, value in kwargs.items())

        self.filters.append(filter_fn)
        return self

    def trace_id(self, trace_id: str) -> "LogQuery":
        """Filtra per trace_id."""
        return self.context_match(trace_id=trace_id)

    def bot_type(self, bot_type: str) -> "LogQuery":
        """Filtra per bot_type."""
        return self.context_match(bot_type=bot_type)

    def time_range(self, start: datetime | None = None, end: datetime | None = None) -> "LogQuery":
        """Filtra per range temporale."""

        def filter_fn(entry):
            timestamp_str = entry.get("timestamp", "")
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", ""))
            except Exception:
                return False

            if start and timestamp < start:
                return False
            return not (end and timestamp > end)

        self.filters.append(filter_fn)
        return self

    def has_exception(self) -> "LogQuery":
        """Filtra solo entry con exception."""
        self.filters.append(lambda entry: "exception" in entry)
        return self

    def limit(self, count: int) -> "LogQuery":
        """Limita risultati."""
        self._limit = count
        return self

    def offset(self, count: int) -> "LogQuery":
        """Offset risultati."""
        self._offset = count
        return self

    def execute(self) -> list[dict[str, Any]]:
        """Esegue query e restituisce risultati."""
        if not self.log_file.exists():
            return []

        results = []
        skipped = 0

        with suppress(Exception), self.log_file.open("r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)

                # Applica filtri
                if all(filter_fn(entry) for filter_fn in self.filters):
                    # Applica offset
                    if skipped < self._offset:
                        skipped += 1
                        continue

                    results.append(entry)

                    # Applica limit
                    if self._limit and len(results) >= self._limit:
                        break

        return results

    def count(self) -> int:
        """Conta risultati senza caricarli."""
        if not self.log_file.exists():
            return 0

        count = 0

        with suppress(Exception), self.log_file.open("r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                if all(filter_fn(entry) for filter_fn in self.filters):
                    count += 1

        return count


class LogViewer:
    """
    Utility per visualizzare e analizzare log.

    Features:
    - Query con filtri
    - Statistiche aggregate
    - Timeline reconstruction
    - Error analysis
    """

    def __init__(self, config=None):
        self.config = config or get_config()

    def query(self, log_type: str = "application") -> LogQuery:
        """
        Crea query builder.

        Args:
            log_type: Tipo log ("application", "errors")

        Returns:
            LogQuery instance
        """
        if log_type == "application":
            log_file = self.config.json_log_file
        elif log_type == "errors":
            log_file = self.config.errors_log_file
        else:
            raise ValueError(f"Unknown log_type: {log_type}")

        return LogQuery(log_file)

    def get_level_stats(self) -> dict[str, int]:
        """
        Statistiche per livello.

        Returns:
            Dict level -> count
        """
        stats: dict[str, int] = defaultdict(int)

        results = self.query().execute()
        for entry in results:
            level = entry.get("level", "UNKNOWN")
            stats[level] += 1

        return stats.copy()

    def get_error_summary(self, limit: int = 10) -> list[dict[str, Any]]:
        """
        Summary errori più frequenti.

        Args:
            limit: Numero massimo errori da restituire

        Returns:
            Lista di errori con count
        """
        error_messages: dict[str, int] = defaultdict(int)
        error_details = {}

        results = self.query("errors").execute()

        for entry in results:
            message = entry.get("message", "")
            error_messages[message] += 1

            if message not in error_details:
                error_details[message] = {
                    "message": message,
                    "first_seen": entry.get("timestamp"),
                    "exception_type": (entry.get("exception", {}).get("type", "unknown")),
                    "count": 0,
                }

            error_details[message]["count"] = error_messages[message]

        # Ordina per count
        sorted_errors = sorted(error_details.values(), key=operator.itemgetter("count"), reverse=True)

        return sorted_errors[:limit]

    def get_slow_operations(self, threshold_ms: float = 5000, limit: int = 10) -> list[dict[str, Any]]:
        """
        Operazioni più lente.

        Args:
            threshold_ms: Soglia millisecondi
            limit: Numero massimo operazioni da restituire

        Returns:
            Lista di operazioni lente
        """
        slow_ops = []

        results = self.query().execute()

        for entry in results:
            data = entry.get("data", {})
            duration = data.get("duration_ms")

            if duration and duration > threshold_ms:
                slow_ops.append(
                    {
                        "timestamp": entry.get("timestamp"),
                        "operation": entry.get("context", {}).get("function", "unknown"),
                        "duration_ms": duration,
                        "message": entry.get("message"),
                        "trace_id": entry.get("context", {}).get("trace_id"),
                    }
                )

        # Ordina per durata
        slow_ops.sort(key=operator.itemgetter("duration_ms"), reverse=True)

        return slow_ops[:limit]

    def reconstruct_trace(self, trace_id: str) -> list[dict[str, Any]]:
        """
        Ricostruisce timeline completa di un trace.

        Args:
            trace_id: Trace ID da ricostruire

        Returns:
            Lista di entry ordinati per timestamp
        """
        results = self.query().trace_id(trace_id).execute()

        # Ordina per timestamp
        results.sort(key=lambda x: x.get("timestamp", ""))

        return results

    def get_bot_runs_summary(self, bot_type: str | None = None, hours: int = 24) -> list[dict[str, Any]]:
        """
        Summary bot runs recenti.

        Args:
            bot_type: Filtra per bot type (opzionale)
            hours: Ore di lookback

        Returns:
            Lista di bot runs con statistiche
        """
        # Calcola time range
        end = datetime.now()
        start = end - timedelta(hours=hours)

        # Query
        query = self.query().time_range(start, end)

        if bot_type:
            query = query.bot_type(bot_type)

        results = query.execute()

        # Raggruppa per trace_id
        traces = defaultdict(list)
        for entry in results:
            trace_id = entry.get("context", {}).get("trace_id")
            if trace_id:
                traces[trace_id].append(entry)

        # Calcola summary per ogni trace
        summaries = []
        for trace_id, entries in traces.items():
            # Trova primo e ultimo entry
            entries.sort(key=lambda x: x.get("timestamp", ""))
            first = entries[0]
            last = entries[-1]

            # Calcola durata totale
            try:
                start_time = datetime.fromisoformat(first.get("timestamp", "").replace("Z", ""))
                end_time = datetime.fromisoformat(last.get("timestamp", "").replace("Z", ""))
                duration_sec = (end_time - start_time).total_seconds()
            except Exception:
                duration_sec = 0

            # Verifica success/failure
            has_error = any(e.get("level") == "ERROR" for e in entries)

            summaries.append(
                {
                    "trace_id": trace_id,
                    "bot_type": first.get("context", {}).get("bot_type", "unknown"),
                    "start_time": first.get("timestamp"),
                    "end_time": last.get("timestamp"),
                    "duration_sec": round(duration_sec, 2),
                    "entry_count": len(entries),
                    "success": not has_error,
                    "context": first.get("context", {}),
                }
            )

        # Ordina per start_time
        summaries.sort(key=operator.itemgetter("start_time"), reverse=True)

        return summaries

    def generate_health_report(self) -> dict[str, Any]:
        """
        Genera report salute sistema.

        Returns:
            Dict con health report
        """
        # Analizza ultime 24h
        end = datetime.now()
        start = end - timedelta(hours=24)

        results = self.query().time_range(start, end).execute()

        # Statistiche base
        level_stats: dict[str, int] = defaultdict(int)
        for entry in results:
            level_stats[entry.get("level", "UNKNOWN")] += 1

        # Error rate
        total = len(results)
        errors = level_stats.get("ERROR", 0) + level_stats.get("CRITICAL", 0)
        error_rate = (errors / total * 100) if total > 0 else 0

        # Bot runs
        bot_runs = self.get_bot_runs_summary(hours=24)
        successful_runs = sum(1 for run in bot_runs if run["success"])
        failed_runs = sum(1 for run in bot_runs if not run["success"])

        report = {
            "timestamp": datetime.now().isoformat() + "Z",
            "period_hours": 24,
            "total_events": total,
            "level_distribution": level_stats.copy(),
            "error_rate_percent": round(error_rate, 2),
            "bot_runs": {
                "total": len(bot_runs),
                "successful": successful_runs,
                "failed": failed_runs,
                "success_rate_percent": (round(successful_runs / len(bot_runs) * 100, 2) if bot_runs else 0),
            },
            "top_errors": self.get_error_summary(limit=5),
            "slow_operations": self.get_slow_operations(limit=5),
        }

        return report


# Utility functions
def query_logs(log_type: str = "application") -> LogQuery:
    """
    Crea query builder per log.

    Args:
        log_type: Tipo log

    Returns:
        LogQuery instance
    """
    return LogViewer().query(log_type)


def view_trace(trace_id: str) -> list[dict[str, Any]]:
    """
    Visualizza timeline completa di un trace.

    Args:
        trace_id: Trace ID

    Returns:
        Lista di log entries
    """
    return LogViewer().reconstruct_trace(trace_id)


def health_report() -> dict[str, Any]:
    """
    Genera health report del sistema.

    Returns:
        Health report
    """
    return LogViewer().generate_health_report()
