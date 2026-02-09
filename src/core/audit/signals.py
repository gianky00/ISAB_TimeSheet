import logging
from typing import Any

logger = logging.getLogger(__name__)


class AuditSignals:
    """Singleton per i segnali di AuditManager (compatibile con PyQt6)."""

    _instance: Any = None

    @classmethod
    def instance(cls) -> Any:
        if cls._instance is None:
            try:
                from PyQt6.QtCore import QObject, pyqtSignal

                class _Signals(QObject):
                    log_added = pyqtSignal(dict)
                    logs_updated = pyqtSignal()

                cls._instance = _Signals()
            except ImportError:
                logger.warning("PyQt6 non trovato, segnali Audit disabilitati.")

                class _MockSignals:
                    def emit(self, *args: Any, **kwargs: Any) -> None:
                        pass

                    class _Signal:
                        def connect(self, *args: Any, **kwargs: Any) -> None:
                            pass

                        def emit(self, *args: Any, **kwargs: Any) -> None:
                            pass

                    log_added = _Signal()
                    logs_updated = _Signal()

                cls._instance = _MockSignals()
        return cls._instance
