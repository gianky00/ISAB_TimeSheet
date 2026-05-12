"""
Context-aware sampling per ridurre volume log.
"""

from typing import Any


class ContextAwareSampler:
    """
    Sampler intelligente che decide se loggare basandosi su context.

    Rules:
    1. Eventi ERROR/CRITICAL: SEMPRE loggati (100%)
    2. Eventi con performance anomala: SEMPRE loggati (100%)
    3. Eventi con trace_id specifico: Basato su config
    4. Eventi normali: Sampling rate configurabile
    """

    def __init__(
        self,
        default_rate: float = 1.0,
        error_rate: float = 1.0,
        slow_operation_rate: float = 1.0,
    ) -> None:
        """
        Inizializza sampler.

        Args:
          default_rate: Rate default (0.0-1.0, default 1.0 = 100%)
          error_rate: Rate per errori (default 1.0 = 100%)
          slow_operation_rate: Rate per operazioni lente (default 1.0 = 100%)
        """
        self.default_rate = self._validate_rate(default_rate)
        self.error_rate = self._validate_rate(error_rate)
        self.slow_operation_rate = self._validate_rate(slow_operation_rate)

        # Override rates per operazione specifica
        self.operation_rates: dict[str, float] = {}

        # Trace IDs da loggare sempre
        self.always_log_traces: set[str] = set()

        # Counter per sampling deterministico
        self._counters: dict[str, int] = {}

    def _validate_rate(self, rate: float) -> float:
        """Valida e normalizza rate."""
        return max(0.0, min(1.0, rate))

    def set_operation_rate(self, operation: str, rate: float) -> None:
        """
        Imposta rate custom per operazione specifica.

        Args:
          operation: Nome operazione
          rate: Rate (0.0-1.0)
        """
        self.operation_rates[operation] = self._validate_rate(rate)

    def add_trace_to_always_log(self, trace_id: str) -> None:
        """
        Marca trace_id da loggare sempre.

        Args:
          trace_id: Trace ID da loggare sempre
        """
        self.always_log_traces.add(trace_id)

    def should_log(
        self,
        level: str,
        context: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> bool:
        """
        Decide se loggare evento.

        Args:
          level: Livello log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
          context: Context corrente (opzionale)
          extra: Dati extra (opzionale)

        Returns:
          True se deve essere loggato, False altrimenti
        """
        context = context or {}
        extra = extra or {}

        # Rule 1: ERROR/CRITICAL sempre loggati
        if level in ("ERROR", "CRITICAL"):
            return self._sample(self.error_rate, "error")

        # Rule 2: Performance anomala sempre loggata
        if self._is_slow_operation(extra):
            return self._sample(self.slow_operation_rate, "slow_op")

        # Rule 3: Trace ID specifico
        trace_id = context.get("trace_id")
        if trace_id and trace_id in self.always_log_traces:
            return True

        # Rule 4: Operation-specific rate
        operation = context.get("function") or extra.get("operation")
        if operation and operation in self.operation_rates:
            return self._sample(self.operation_rates[operation], f"op_{operation}")

        # Rule 5: Default rate
        return self._sample(self.default_rate, "default")

    def _is_slow_operation(self, extra: dict[str, Any]) -> bool:
        """
        Verifica se operazione  lenta.

        Args:
          extra: Dati extra

        Returns:
          True se lenta, False altrimenti
        """
        # Check threshold_exceeded flag
        if extra.get("threshold_exceeded"):
            return True

        # Check durata vs threshold
        duration = extra.get("duration_ms")
        threshold = extra.get("threshold_ms")

        return bool(duration and threshold and duration > threshold)

    def _sample(self, rate: float, key: str) -> bool:
        """
        Esegue sampling con rate specificato.

        Args:
          rate: Rate (0.0-1.0)
          key: Chiave per counter

        Returns:
          True se campionato, False altrimenti
        """
        if rate >= 1.0:
            return True

        if rate <= 0.0:
            return False

        # Sampling deterministico: 1 ogni N
        if key not in self._counters:
            self._counters[key] = 0

        self._counters[key] += 1
        threshold = int(1.0 / rate)

        return (self._counters[key] % threshold) == 0

    def get_stats(self) -> dict[str, Any]:
        """
        Restituisce statistiche sampling.

        Returns:
          Dict con statistiche
        """
        return {
            "default_rate": self.default_rate,
            "error_rate": self.error_rate,
            "slow_operation_rate": self.slow_operation_rate,
            "operation_rates": self.operation_rates.copy(),
            "always_log_traces_count": len(self.always_log_traces),
            "counters": self._counters.copy(),
        }


# Singleton instance
_sampler = None


def get_sampler() -> ContextAwareSampler:
    """Restituisce istanza singleton del sampler."""
    global _sampler  # noqa: PLW0603
    if _sampler is None:
        _sampler = ContextAwareSampler()
    return _sampler


def should_log(
    level: str,
    context: dict[str, Any] | None = None,
    extra: dict[str, Any] | None = None,
) -> bool:
    """
    Helper function per sampling check.

    Args:
      level: Livello log
      context: Context corrente
      extra: Dati extra

    Returns:
      True se deve essere loggato
    """
    return get_sampler().should_log(level, context, extra)
