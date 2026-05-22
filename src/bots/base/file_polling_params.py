"""Parametri di configurazione per il polling del filesystem."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class FilePollingParams:
    """Parametri per il polling di file nel filesystem."""
    directory: Path | str
    pattern: str = "*"
    timeout: int = 60
    poll_interval: float = 0.5
    min_age: float | None = None
    exclude_patterns: list[str] = field(default_factory=list)
