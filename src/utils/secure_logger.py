"""
Logger sicuro che maschera informazioni sensibili.
"""

import logging
import re
from re import Pattern
from typing import ClassVar


class SensitiveDataFilter(logging.Filter):
    """Filtra dati sensibili dai log."""

    PATTERNS: ClassVar[list[tuple[Pattern[str], str]]] = [
        # Password in vari formati
        (
            re.compile(r'password["\s:=]+["\']?[\w@#$%^&*!]+["\']?', re.IGNORECASE),
            "password=***MASKED***",
        ),
        # Token/API keys
        (
            re.compile(
                r'(token|api_key|apikey|secret)["\s:=]+["\']?[\w-]+["\']?',
                re.IGNORECASE,
            ),
            r"\1=***MASKED***",
        ),
        # Codici fiscali
        (
            re.compile(r"[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]"),
            "***CF_MASKED***",
        ),
        # Numeri di carta di credito
        (
            re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"),
            "***CARD_MASKED***",
        ),
        # Email addresses
        (
            re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
            "***EMAIL_MASKED***",
        ),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        """Applica il mascheramento dei dati sensibili al messaggio e agli argomenti del log."""
        if isinstance(record.msg, str):
            for pattern, replacement in self.PATTERNS:
                record.msg = pattern.sub(replacement, record.msg)

        if record.args:
            record.args = tuple(self._mask_value(arg) for arg in record.args)

        return True

    def _mask_value(self, value: object) -> object:
        """Maschera una singola stringa se contiene dati sensibili."""
        if isinstance(value, str):
            masked_value = value
            for pattern, replacement in self.PATTERNS:
                masked_value = pattern.sub(replacement, masked_value)
            return masked_value
        return value


def get_secure_logger(name: str) -> logging.Logger:
    """Ottiene un logger con filtro per dati sensibili."""
    logger = logging.getLogger(name)

    # Aggiungi filtro se non presente
    if not any(isinstance(f, SensitiveDataFilter) for f in logger.filters):
        logger.addFilter(SensitiveDataFilter())

    return logger
