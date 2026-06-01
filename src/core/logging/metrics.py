"""Performance metrics tracking e storage."""

import json
from collections import defaultdict
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any, Optional

from .config import get_config


class PerformanceMetric:
    """Singola metrica di performance."""

    def __init__(
        self,
        operation: str,
        duration_ms: float,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.operation = operation
        self.duration_ms = duration_ms
        self.timestamp = datetime.now(UTC)
        self.metadata = metadata or {}

    def to_dict(self) -> dict[str, Any]:
        """Converte metrica in dizionario."""
        return {
            "operation": self.operation,
            "duration_ms": round(self.duration_ms, 2),
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class MetricsSink:
    """Sink per metriche di performance.

    Scrive metriche in file JSONL (newline-delimited JSON).

    Inizializza la classe.
    """

    def __init__(self, config: Any = None) -> None:
        self.config = config or get_config()
        self.metrics_file = self.config.metrics_dir / "performance.jsonl"

        # Assicura che directory esista
        self.config.metrics_dir.mkdir(parents=True, exist_ok=True)

    def write_metric(self, metric: PerformanceMetric) -> None:
        """Scrive metrica su file.

        Args:
          metric: Metrica da scrivere
        """
        with suppress(Exception), self.metrics_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(metric.to_dict(), ensure_ascii=False) + "\n")

    def read_metrics(
        self,
        operation: str | None = None,
        limit: int | None = None,
    ) -> list[PerformanceMetric]:
        """Legge metriche da file.

        Args:
          operation: Filtra per operation specifica (opzionale)
          limit: Numero massimo metriche da leggere (opzionale)

        Returns:
          Lista di metriche
        """
        if not self.metrics_file.exists():
            return []

        metrics = []
        count = 0

        with suppress(Exception), self.metrics_file.open("r", encoding="utf-8") as f:
            for line in f:
                if limit and count >= limit:
                    break

                data = json.loads(line)

                # Filtra per operation se specificato
                if operation and data.get("operation") != operation:
                    continue

                metric = PerformanceMetric(
                    operation=data["operation"],
                    duration_ms=data["duration_ms"],
                    metadata=data.get("metadata", {}),
                )
                ts_str = data["timestamp"]
                if ts_str.endswith("Z"):
                    metric.timestamp = datetime.fromisoformat(ts_str)
                else:
                    metric.timestamp = datetime.fromisoformat(ts_str)

                if metric.timestamp.tzinfo is None:
                    metric.timestamp = metric.timestamp.replace(tzinfo=UTC)

                metrics.append(metric)
                count += 1

        return metrics


class PerformanceTracker:
    """Tracker per monitorare performance nel tempo.

    Features:
    - Registra metriche
    - Calcola statistiche (avg, min, max, p95, p99)
    - Rileva anomalie (operazioni lente)

    Inizializza la classe.
    """

    _instance: Optional["PerformanceTracker"] = None

    @classmethod
    def instance(cls) -> "PerformanceTracker":
        """Restituisce istanza singleton."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        self.sink = MetricsSink()
        self._in_memory_metrics: dict[str, list[float]] = defaultdict(list)  # operation -> [durations]
        self._baselines: dict[str, float] = {}  # operation -> baseline_ms

    def track(
        self,
        operation: str,
        duration_ms: float,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Registra metrica di performance.

        Args:
          operation: Nome operazione (es: "bot.scarico_ts.download")
          duration_ms: Durata in millisecondi
          metadata: Metadata aggiuntivi (opzionale)
        """
        # Crea metrica
        metric = PerformanceMetric(operation, duration_ms, metadata)

        # Scrivi su file
        self.sink.write_metric(metric)

        # Aggiungi a cache in-memory (per statistiche real-time)
        self._in_memory_metrics[operation].append(duration_ms)

        # Mantieni solo ultimi 1000 valori in memory
        if len(self._in_memory_metrics[operation]) > 1000:  # noqa: PLR2004
            self._in_memory_metrics[operation] = self._in_memory_metrics[operation][-1000:]

    def get_statistics(self, operation: str) -> dict[str, float] | None:
        """Calcola statistiche per operazione.

        Args:
          operation: Nome operazione

        Returns:
          Dict con statistiche (avg, min, max, p50, p95, p99) o None
        """
        durations = self._in_memory_metrics.get(operation)
        if not durations:
            return None

        sorted_durations = sorted(durations)
        count = len(sorted_durations)

        return {
            "count": float(count),
            "avg": sum(sorted_durations) / count,
            "min": sorted_durations[0],
            "max": sorted_durations[-1],
            "p50": sorted_durations[int(count * 0.50)],
            "p95": sorted_durations[int(count * 0.95)],
            "p99": sorted_durations[int(count * 0.99)],
        }

    def set_baseline(self, operation: str, baseline_ms: float) -> None:
        """Imposta baseline per operazione.

        Args:
          operation: Nome operazione
          baseline_ms: Baseline in millisecondi
        """
        self._baselines[operation] = baseline_ms

    def get_baseline(self, operation: str) -> float | None:
        """Restituisce baseline per operazione.

        Args:
          operation: Nome operazione

        Returns:
          Baseline in millisecondi o None
        """
        return self._baselines.get(operation)


# Singleton access
def get_tracker() -> PerformanceTracker:
    """Restituisce istanza singleton del performance tracker."""
    return PerformanceTracker.instance()
