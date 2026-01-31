"""
Performance metrics tracking e storage.
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import get_config


class PerformanceMetric:
    """Singola metrica di performance."""

    def __init__(
        self,
        operation: str,
        duration_ms: float,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.operation = operation
        self.duration_ms = duration_ms
        self.timestamp = datetime.now()
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Converte metrica in dizionario."""
        return {
            "operation": self.operation,
            "duration_ms": round(self.duration_ms, 2),
            "timestamp": self.timestamp.isoformat() + "Z",
            "metadata": self.metadata,
        }


class MetricsSink:
    """
    Sink per metriche di performance.

    Scrive metriche in file JSONL (newline-delimited JSON).
    """

    def __init__(self, config=None):
        self.config = config or get_config()
        self.metrics_file = self.config.metrics_dir / "performance.jsonl"

        # Assicura che directory esista
        self.config.metrics_dir.mkdir(parents=True, exist_ok=True)

    def write_metric(self, metric: PerformanceMetric):
        """
        Scrive metrica su file.

        Args:
            metric: Metrica da scrivere
        """
        try:
            with open(self.metrics_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(metric.to_dict(), ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[METRICS ERROR] Failed to write metric: {e}")

    def read_metrics(
        self,
        operation: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[PerformanceMetric]:
        """
        Legge metriche da file.

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

        try:
            with open(self.metrics_file, "r", encoding="utf-8") as f:
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
                    metric.timestamp = datetime.fromisoformat(
                        data["timestamp"].replace("Z", "")
                    )

                    metrics.append(metric)
                    count += 1

        except Exception as e:
            print(f"[METRICS ERROR] Failed to read metrics: {e}")

        return metrics


class PerformanceTracker:
    """
    Tracker per monitorare performance nel tempo.

    Features:
    - Registra metriche
    - Calcola statistiche (avg, min, max, p95, p99)
    - Rileva anomalie (operazioni lente)
    """

    _instance = None

    @classmethod
    def instance(cls):
        """Restituisce istanza singleton."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.sink = MetricsSink()
        self._in_memory_metrics = defaultdict(list)  # operation -> [durations]
        self._baselines = {}  # operation -> baseline_ms

    def track(
        self,
        operation: str,
        duration_ms: float,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Registra metrica di performance.

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
        if len(self._in_memory_metrics[operation]) > 1000:
            self._in_memory_metrics[operation] = self._in_memory_metrics[operation][
                -1000:
            ]

    def get_statistics(self, operation: str) -> Optional[Dict[str, float]]:
        """
        Calcola statistiche per operazione.

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

        stats = {
            "count": count,
            "avg": sum(sorted_durations) / count,
            "min": sorted_durations[0],
            "max": sorted_durations[-1],
            "p50": sorted_durations[int(count * 0.50)],
            "p95": sorted_durations[int(count * 0.95)],
            "p99": sorted_durations[int(count * 0.99)],
        }

        return stats

    def set_baseline(self, operation: str, baseline_ms: float):
        """
        Imposta baseline per operazione.

        Args:
            operation: Nome operazione
            baseline_ms: Baseline in millisecondi
        """
        self._baselines[operation] = baseline_ms

    def get_baseline(self, operation: str) -> Optional[float]:
        """
        Restituisce baseline per operazione.

        Args:
            operation: Nome operazione

        Returns:
            Baseline in millisecondi o None
        """
        return self._baselines.get(operation)

    def is_anomaly(
        self,
        operation: str,
        duration_ms: float,
        threshold_multiplier: float = 3.0,
    ) -> bool:
        """
        Verifica se durata è anomala.

        Args:
            operation: Nome operazione
            duration_ms: Durata da verificare
            threshold_multiplier: Moltiplicatore baseline (default: 3x)

        Returns:
            True se anomalia, False altrimenti
        """
        baseline = self.get_baseline(operation)
        if baseline is None:
            # Auto-calcola baseline da statistiche
            stats = self.get_statistics(operation)
            if stats:
                baseline = stats["p95"]  # Usa p95 come baseline
                self.set_baseline(operation, baseline)
            else:
                return False  # Non abbastanza dati

        return duration_ms > (baseline * threshold_multiplier)

    def load_baselines_from_file(self, file_path: Path):
        """
        Carica baselines da file JSON.

        Args:
            file_path: Path al file JSON
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self._baselines = json.load(f)
        except Exception as e:
            print(f"[METRICS ERROR] Failed to load baselines: {e}")

    def save_baselines_to_file(self, file_path: Path):
        """
        Salva baselines su file JSON.

        Args:
            file_path: Path al file JSON
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self._baselines, f, indent=2)
        except Exception as e:
            print(f"[METRICS ERROR] Failed to save baselines: {e}")

    def auto_learn_baselines(self):
        """
        Auto-learn baselines dalle metriche correnti.

        Calcola p95 per ogni operazione e lo imposta come baseline.
        """
        for operation in self._in_memory_metrics.keys():
            stats = self.get_statistics(operation)
            if stats and stats["count"] >= 10:  # Minimo 10 campioni
                self.set_baseline(operation, stats["p95"])

    def generate_report(self) -> Dict[str, Any]:
        """
        Genera report performance completo.

        Returns:
            Dict con report
        """
        report = {
            "timestamp": datetime.now().isoformat() + "Z",
            "operations": {},
        }

        for operation in self._in_memory_metrics.keys():
            stats = self.get_statistics(operation)
            baseline = self.get_baseline(operation)

            report["operations"][operation] = {
                "statistics": stats,
                "baseline_ms": baseline,
            }

        return report


# Singleton access
def get_tracker() -> PerformanceTracker:
    """Restituisce istanza singleton del performance tracker."""
    return PerformanceTracker.instance()
