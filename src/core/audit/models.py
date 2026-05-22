"""Modulo Models."""

from enum import IntEnum

from PySide6.QtCore import QEnum


@QEnum
class Severity(IntEnum):
    """Livelli di gravità per le entry dell'Audit Log."""

    LOW = 0
    MEDIUM = 1
    HIGH = 2

    def to_str(self) -> str:
        """Restituisce la rappresentazione stringa per compatibilità DB."""
        return {
            Severity.LOW: "low",
            Severity.MEDIUM: "medium",
            Severity.HIGH: "high",
        }.get(self, "low")


@QEnum
class Status(IntEnum):
    """Esiti possibili di un'operazione auditata."""

    SUCCESS = 0
    ERROR = 1
    WARNING = 2

    def to_str(self) -> str:
        """Restituisce la rappresentazione stringa per compatibilità DB."""
        return {
            Status.SUCCESS: "success",
            Status.ERROR: "error",
            Status.WARNING: "warning",
        }.get(self, "success")
