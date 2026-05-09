from enum import Enum


class Severity(Enum):
    """Livelli di gravit  per le entry dell'Audit Log."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(Enum):
    """Esiti possibili di un'operazione auditata."""

    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
