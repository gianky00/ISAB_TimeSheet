"""
Helper per migrare dal vecchio sistema di logging al nuovo.
"""

import logging
from typing import Any

from .logger import get_logger as get_new_logger


class LoggingAdapter:
    """
    Adapter che converte chiamate standard logging in structured logging.

    Usage:
        # Vecchio codice:
        # logger = logging.getLogger(__name__)

        # Nuovo codice (compatibile):
        from src.core.logging.migration import get_logger
        logger = get_logger(__name__)

        # Funziona sia con vecchio che nuovo sistema!
    """

    def __init__(self, name: str):  # noqa: ANN204
        self._structured_logger = get_new_logger(name)
        self._std_logger = logging.getLogger(name)

    def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Debug log."""
        # Estrai extra da kwargs se presente
        extra = kwargs.pop("extra", {})
        formatted_msg = msg % args if args else msg
        self._structured_logger.debug(formatted_msg, **extra)

    def info(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Info log."""
        extra = kwargs.pop("extra", {})
        formatted_msg = msg % args if args else msg
        self._structured_logger.info(formatted_msg, **extra)

    def warning(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Warning log."""
        extra = kwargs.pop("extra", {})
        formatted_msg = msg % args if args else msg
        self._structured_logger.warning(formatted_msg, **extra)

    def error(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Error log."""
        extra = kwargs.pop("extra", {})
        formatted_msg = msg % args if args else msg
        self._structured_logger.error(formatted_msg, **extra)

    def critical(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """Critical log."""
        extra = kwargs.pop("extra", {})
        formatted_msg = msg % args if args else msg
        self._structured_logger.critical(formatted_msg, **extra)

    def exception(self, msg: Any, *args: Any, exc_info: bool = True, **kwargs: Any) -> None:
        """Exception log."""
        import sys  # noqa: PLC0415

        extra = kwargs.pop("extra", {})
        formatted_msg = msg % args if args else msg

        # Ottieni exception corrente
        exc = sys.exc_info()[1] if exc_info else None

        if isinstance(exc, Exception):
            self._structured_logger.exception(formatted_msg, exc=exc, **extra)
        else:
            self._structured_logger.error(formatted_msg, **extra)


def get_logger(name: str) -> LoggingAdapter:
    """
    Ottiene logger compatibile con vecchio e nuovo sistema.

    Args:
        name: Nome logger (tipicamente __name__)

    Returns:
        LoggingAdapter che funziona con entrambi i sistemi
    """
    return LoggingAdapter(name)


def migrate_logging_call(old_code: str) -> str:
    """
    Converte codice vecchio logging in nuovo formato.

    Args:
        old_code: Snippet di codice con vecchio logging

    Returns:
        Codice convertito

    Example:
        >>> old = "logging.getLogger(__name__)"
        >>> new = migrate_logging_call(old)
        >>> print(new)
        'get_logger(__name__)'
    """
    # Sostituzioni comuni
    replacements = [
        ("import logging", "from src.core.logging import get_logger"),
        ("logging.getLogger(__name__)", "get_logger(__name__)"),
        ("logging.getLogger(", "get_logger("),
        ("logger.log(logging.INFO,", "logger.info("),
        ("logger.log(logging.DEBUG,", "logger.debug("),
        ("logger.log(logging.WARNING,", "logger.warning("),
        ("logger.log(logging.ERROR,", "logger.error("),
    ]

    migrated = old_code
    for old, new in replacements:
        migrated = migrated.replace(old, new)

    return migrated
