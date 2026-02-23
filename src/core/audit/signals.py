import logging
from typing import Any

logger = logging.getLogger(__name__)


class AuditSignals:
    """Singleton per i segnali di AuditManager (compatibile con PyQt6)."""

    _instance: Any = None

    @classmethod
    def instance(cls) -> Any:
        """Restituisce l'istanza singleton del contenitore segnali."""
        if cls._instance is None:
            try:
                from PyQt6.QtCore import QObject, pyqtSignal

                class _Signals(QObject):
                    """Contenitore per i segnali basati su Qt."""

                    log_added = pyqtSignal(dict)
                    logs_updated = pyqtSignal()

                cls._instance = _Signals()
            except ImportError:
                logger.warning("PyQt6 non trovato, segnali Audit disabilitati.")

                class _MockSignals:
                    """Mock per i segnali in assenza di ambiente GUI."""

                    def emit(self, *args: Any, **kwargs: Any) -> None:
                        """Simula l'emissione di un segnale."""

                    class _Signal:
                        """Simula un singolo segnale Qt."""

                        def connect(self, *args: Any, **kwargs: Any) -> None:
                            """Simula la connessione di uno slot."""

                        def emit(self, *args: Any, **kwargs: Any) -> None:
                            """Simula l'emissione del segnale."""

                    log_added = _Signal()
                    logs_updated = _Signal()

                cls._instance = _MockSignals()
        return cls._instance
