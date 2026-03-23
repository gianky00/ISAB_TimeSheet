"""
SyncroJob - Analytics Engine

Anomaly detection, pattern detection e health scoring per log analysis.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

from .viewer import LogViewer


@dataclass
class Anomaly:
    """Rappresenta un'anomalia rilevata nei log."""

    type: Literal["error_spike", "slow_operation", "unusual_pattern", "high_failure_rate"]
    severity: Literal["low", "medium", "high", "critical"]
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    suggestion: str | None = None


@dataclass
class Pattern:
    """Rappresenta un pattern ricorrente nei log."""

    type: Literal["repeated_error", "correlation", "time_based"]
    message: str
    count: int
    examples: list[str] = field(default_factory=list)
    first_seen: datetime | None = None
    last_seen: datetime | None = None


@dataclass
class AnalyticsReport:
    """Report aggregato con anomalie, pattern e suggerimenti."""

    anomalies: list[Anomaly] = field(default_factory=list)
    patterns: list[Pattern] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    health_score: int = 100  # 0-100
    generated_at: datetime = field(default_factory=datetime.now)

    @property
    def has_critical_issues(self) -> bool:
        return any(a.severity == "critical" for a in self.anomalies)

    @property
    def anomaly_count(self) -> int:
        return len(self.anomalies)


class AnomalyDetector:
    """
    Rileva anomalie nei log basandosi su baseline statistiche.

    Tipi di anomalie rilevate:
    - Error rate spike (aumento improvviso errori)
    - Slow operations (operazioni più lente del normale)
    - High failure rate (tasso di fallimento bot elevato)
    """

    def __init__(self, viewer: LogViewer | None = None):  # noqa: ANN204
        self.viewer = viewer or LogViewer()

        # Baseline thresholds (configurabili)
        self.error_rate_threshold = 5.0  # % errori massimo normale
        self.slow_op_threshold_ms = 10000  # 10 secondi
        self.failure_rate_threshold = 10.0  # % fallimenti bot

    def detect_all(self, hours: int = 24) -> list[Anomaly]:
        """Rileva tutte le anomalie nelle ultime N ore."""
        anomalies = []
        anomalies.extend(self.detect_error_rate_spike(hours))
        anomalies.extend(self.detect_slow_operations(hours))
        anomalies.extend(self.detect_high_failure_rate(hours))
        return anomalies

    def detect_error_rate_spike(self, hours: int = 24) -> list[Anomaly]:
        """
        Rileva spike nel tasso di errori.

        Returns:
            Lista di anomalie se error rate > threshold
        """
        anomalies = []
        report = self.viewer.generate_health_report()

        error_rate = report.get("error_rate_percent", 0)

        if error_rate > self.error_rate_threshold:
            severity: Literal["low", "medium", "high", "critical"] = "medium"
            if error_rate > 15:  # noqa: PLR2004
                severity = "high"
            if error_rate > 25:  # noqa: PLR2004
                severity = "critical"

            anomalies.append(
                Anomaly(
                    type="error_spike",
                    severity=severity,
                    message=f"Error rate elevato: {error_rate:.1f}%",
                    details={
                        "current_rate": error_rate,
                        "threshold": self.error_rate_threshold,
                        "total_errors": report.get("level_distribution", {}).get("ERROR", 0),
                    },
                    suggestion="Controlla gli errori recenti nella sezione Audit",
                )
            )

        return anomalies

    def detect_slow_operations(self, hours: int = 24) -> list[Anomaly]:
        """
        Rileva operazioni più lente del normale.

        Returns:
            Lista di anomalie per operazioni lente
        """
        anomalies = []
        slow_ops = self.viewer.get_slow_operations(threshold_ms=self.slow_op_threshold_ms, limit=5)

        for op in slow_ops:
            duration_ms = op.get("duration_ms", 0)
            operation = op.get("operation", "unknown")

            severity: Literal["low", "medium", "high", "critical"] = "low"
            if duration_ms > 60000:  # > 1min  # noqa: PLR2004
                severity = "critical"
            elif duration_ms > 30000:  # > 30s  # noqa: PLR2004
                severity = "high"

            anomalies.append(
                Anomaly(
                    type="slow_operation",
                    severity=severity,
                    message=f"Operazione lenta: {operation} ({duration_ms / 1000:.1f}s)",
                    details={
                        "operation": operation,
                        "duration_ms": duration_ms,
                        "threshold_ms": self.slow_op_threshold_ms,
                    },
                    suggestion="Verifica la connessione di rete o riprova più tardi",
                )
            )

        return anomalies

    def detect_high_failure_rate(self, hours: int = 24) -> list[Anomaly]:
        """
        Rileva tasso di fallimento bot elevato.

        Returns:
            Lista di anomalie se failure rate > threshold
        """
        anomalies = []
        bot_summary = self.viewer.get_bot_runs_summary(hours=hours)

        for bot_run in bot_summary:
            bot_type = bot_run.get("bot_type", "unknown")
            success_rate = bot_run.get("success_rate", 100)
            failure_rate = 100 - success_rate

            if failure_rate > self.failure_rate_threshold:
                severity: Literal["low", "medium", "high", "critical"] = "medium"
                if failure_rate > 30:  # noqa: PLR2004
                    severity = "high"
                if failure_rate > 50:  # noqa: PLR2004
                    severity = "critical"

                anomalies.append(
                    Anomaly(
                        type="high_failure_rate",
                        severity=severity,
                        message=f"Bot {bot_type}: {failure_rate:.0f}% fallimenti",
                        details={
                            "bot_type": bot_type,
                            "failure_rate": failure_rate,
                            "total_runs": bot_run.get("total_runs", 0),
                            "failed_runs": bot_run.get("failed_runs", 0),
                        },
                        suggestion="Verifica le credenziali nelle Impostazioni",
                    )
                )

        return anomalies


class PatternDetector:
    """
    Rileva pattern ricorrenti nei log.

    Tipi di pattern rilevati:
    - Errori ripetuti (stesso messaggio più volte)
    - Correlazioni (errori che seguono sempre altri errori)
    """

    def __init__(self, viewer: LogViewer | None = None):  # noqa: ANN204
        self.viewer = viewer or LogViewer()
        self.min_count = 3  # Minimo occorrenze per pattern

    def detect_all(self, hours: int = 24) -> list[Pattern]:
        """Rileva tutti i pattern nelle ultime N ore."""
        patterns = []
        patterns.extend(self.find_repeated_errors(hours))
        return patterns

    def find_repeated_errors(self, hours: int = 24, min_count: int | None = None) -> list[Pattern]:
        """
        Trova errori che si ripetono frequentemente.

        Returns:
            Lista di pattern di errori ripetuti
        """
        patterns = []
        min_count = min_count or self.min_count

        error_summary = self.viewer.get_error_summary(limit=20)

        for error in error_summary:
            count = error.get("count", 0)
            if count >= min_count:
                patterns.append(
                    Pattern(
                        type="repeated_error",
                        message=error.get("message", "Unknown error"),
                        count=count,
                        examples=[error.get("message", "")[:100]],
                    )
                )

        return patterns


class HealthScorer:
    """Calcola health score 0-100 basato su anomalie e metriche."""

    def calculate(
        self,
        anomalies: list[Anomaly],
        error_rate: float = 0,
        bot_success_rate: float = 100,
    ) -> int:
        """
        Calcola health score.

        Args:
            anomalies: Lista anomalie rilevate
            error_rate: Tasso errori %
            bot_success_rate: Tasso successo bot %

        Returns:
            Score 0-100 (100 = perfetto)
        """
        score = 100

        # Penalità per anomalie
        for anomaly in anomalies:
            if anomaly.severity == "critical":
                score -= 25
            elif anomaly.severity == "high":
                score -= 15
            elif anomaly.severity == "medium":
                score -= 10
            else:
                score -= 5

        # Penalità per error rate
        if error_rate > 5:  # noqa: PLR2004
            score -= min(20, int(error_rate))

        # Penalità per bot failures
        if bot_success_rate < 90:  # noqa: PLR2004
            score -= int((100 - bot_success_rate) / 2)

        return max(0, min(100, score))


def generate_analytics_report(hours: int = 24) -> AnalyticsReport:
    """
    Genera report completo di analytics.

    Args:
        hours: Ore di lookback per analisi

    Returns:
        AnalyticsReport con anomalie, pattern e suggerimenti
    """
    viewer = LogViewer()
    anomaly_detector, pattern_detector, health_scorer = (
        AnomalyDetector(viewer),
        PatternDetector(viewer),
        HealthScorer(),
    )

    # Rileva anomalie e pattern
    anomalies, patterns = anomaly_detector.detect_all(hours), pattern_detector.detect_all(hours)

    # Calcola health score
    health_report = viewer.generate_health_report()
    error_rate = health_report.get("error_rate_percent", 0)

    # Bot success rate medio
    bot_success_rate = health_report.get("bot_runs", {}).get("success_rate_percent", 100)

    health_score = health_scorer.calculate(
        anomalies=anomalies, error_rate=error_rate, bot_success_rate=bot_success_rate
    )

    # Genera suggerimenti
    suggestions = [a.suggestion for a in anomalies if a.suggestion]

    # Suggerimenti generali basati su pattern
    if any(p.count > 10 for p in patterns):  # noqa: PLR2004
        suggestions.append("Problema ricorrente rilevato: contatta il supporto tecnico")

    return AnalyticsReport(
        anomalies=anomalies,
        patterns=patterns,
        suggestions=list(set(suggestions)),  # Deduplica
        health_score=health_score,
    )


# Utility functions per export
def get_health_score(hours: int = 24) -> int:
    """Restituisce solo health score."""
    return generate_analytics_report(hours).health_score


def get_anomalies(hours: int = 24) -> list[Anomaly]:
    """Restituisce lista anomalie."""
    return AnomalyDetector().detect_all(hours)


def get_patterns(hours: int = 24) -> list[Pattern]:
    """Restituisce lista pattern."""
    return PatternDetector().detect_all(hours)
