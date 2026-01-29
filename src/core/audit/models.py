from enum import Enum

class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
