"""Modulo Signals."""

import logging
from typing import Any

try:
    from PySide6.QtCore import QObject, Signal

    PYSIDE_AVAILABLE = True
except ImportError:
    PYSIDE_AVAILABLE = False

logger = logging.getLogger(__name__)


class _MockSignal:
    """Mock per un singolo segnale Qt."""

    def connect(self, *args: Any, **kwargs: Any) -> None:
        """Simula la connessione di uno slot."""

    def emit(self, *args: Any, **kwargs: Any) -> None:
        """Simula l'emissione del segnale."""


class _MockSignals:
    """Mock per i segnali in assenza di ambiente GUI."""

    def emit(self, *args: Any, **kwargs: Any) -> None:
        """Simula l'emissione di un segnale."""

    log_added = _MockSignal()
    logs_updated = _MockSignal()


class AuditSignals:
    """Singleton per i segnali di AuditManager (compatibile con PySide6)."""

    _instance: Any = None

    @classmethod
    def instance(cls) -> Any:
        """Restituisce l'istanza singleton del contenitore segnali."""
        if cls._instance is None:
            if PYSIDE_AVAILABLE:

                class _Signals(QObject):
                    """Contenitore per i segnali basati su Qt."""

                    log_added = Signal(dict)
                    logs_updated = Signal()

                cls._instance = _Signals()
            else:
                logger.warning("PySide6 non trovato, segnali Audit disabilitati.")
                cls._instance = _MockSignals()
        return cls._instance
