"""
Context management per correlation e tracing.
"""

import threading
import uuid
from contextlib import contextmanager
from typing import Any


class LoggingContext:
    """
    Thread-safe context storage per correlation IDs e metadata.

    Ogni thread ha il proprio context isolato.
    """

    def __init__(self):
        self._local = threading.local()

    def _get_context(self) -> dict[str, Any]:
        """Restituisce context del thread corrente."""
        if not hasattr(self._local, "context"):
            self._local.context = {}
        return self._local.context

    def set(self, key: str, value: Any):
        """Imposta un valore nel context."""
        context = self._get_context()
        context[key] = value

    def get(self, key: str, default=None):
        """Ottiene un valore dal context."""
        return self._get_context().get(key, default)

    def update(self, **kwargs):
        """Aggiorna context con multipli valori."""
        context = self._get_context()
        context.update(kwargs)

    def clear(self):
        """Pulisce il context del thread corrente."""
        if hasattr(self._local, "context"):
            self._local.context = {}

    def to_dict(self) -> dict[str, Any]:
        """Restituisce copia del context corrente."""
        return self._get_context().copy()

    def has(self, key: str) -> bool:
        """Verifica se una chiave esiste nel context."""
        return key in self._get_context()


# Istanza globale singleton
_global_context = LoggingContext()


def get_context() -> LoggingContext:
    """Restituisce istanza globale del context."""
    return _global_context


@contextmanager
def with_context(**context_data):
    """
    Context manager per aggiungere metadata temporanei ai log.

    Usage:
        with with_context(trace_id="abc123", bot_type="scarico_ts"):
            logger.info("Operazione")  # Auto-tagged con context

    Args:
        **context_data: Chiavi e valori da aggiungere al context

    Yields:
        None
    """
    ctx = get_context()

    # Salva context precedente
    previous = ctx.to_dict()

    # Auto-genera trace_id se non fornito
    if "trace_id" not in context_data and "trace_id" not in previous:
        context_data["trace_id"] = generate_trace_id()

    # Imposta nuovo context
    ctx.update(**context_data)

    try:
        yield
    finally:
        # Ripristina context precedente
        ctx.clear()
        ctx.update(**previous)


def generate_trace_id() -> str:
    """
    Genera un trace ID univoco.

    Returns:
        String univoca per identificare trace (es: "trace_abc123def456")
    """
    return f"trace_{uuid.uuid4().hex[:16]}"


def generate_span_id() -> str:
    """
    Genera uno span ID univoco.

    Returns:
        String univoca per identificare span (es: "span_abc123")
    """
    return f"span_{uuid.uuid4().hex[:8]}"


def get_current_trace_id() -> str | None:
    """
    Restituisce il trace_id corrente, se esiste.

    Returns:
        Trace ID corrente o None
    """
    return get_context().get("trace_id")


def get_current_span_id() -> str | None:
    """
    Restituisce lo span_id corrente, se esiste.

    Returns:
        Span ID corrente o None
    """
    return get_context().get("span_id")


def set_audit_id(audit_id: int):
    """
    Imposta l'audit_id nel context corrente.

    Args:
        audit_id: ID dell'entry audit (rowid da AuditDatabase)
    """
    get_context().set("audit_id", audit_id)


def get_current_audit_id() -> int | None:
    """
    Restituisce l'audit_id corrente, se esiste.

    Returns:
        Audit ID corrente o None
    """
    return get_context().get("audit_id")
