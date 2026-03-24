"""
Configurazione sistema di logging.
"""

from pathlib import Path
from typing import Final

from src.core.constants import FileNames
from src.core.paths import LOGS_DIR


class LoggingConfig:
    """Configurazione centralizzata per il sistema di logging."""

    def __init__(self) -> None:
        # Base directory: C:\Users\gianc\AppData\Local\SyncroJob\logs
        self.base_dir: Final[Path] = LOGS_DIR

        # Sottodirectory per tipo log
        self.application_dir: Final[Path] = self.base_dir / "application"
        self.errors_dir: Final[Path] = self.base_dir / "errors"
        self.metrics_dir: Final[Path] = self.base_dir / "metrics"
        self.bots_dir: Final[Path] = self.base_dir / "bots"

        # File paths
        self.json_log_file: Final[Path] = self.application_dir / FileNames.LOG_JSON
        self.human_log_file: Final[Path] = self.application_dir / FileNames.LOG_HUMAN
        self.errors_log_file: Final[Path] = self.errors_dir / FileNames.LOG_ERRORS

        # Rotation settings
        self.rotation_size: Final[str] = "10 MB"  # Rotazione quando file raggiunge 10MB
        self.rotation_time: Final[str] = "00:00"  # Rotazione giornaliera a mezzanotte
        self.retention: Final[str] = "30 days"  # Mantieni log per 30 giorni
        self.errors_retention: Final[str] = "90 days"  # Errori mantenuti 90 giorni
        self.compression: Final[str] = "zip"  # Comprimi log vecchi

        # Performance settings
        self.performance_threshold_ms: Final[int] = 5000  # Alert se operazione > 5sec
        self.sampling_rate: Final[float] = 1.0  # 1.0 = log tutto (100%), 0.01 = log 1%

        # Console output
        self.console_enabled: Final[bool] = True
        self.console_level: Final[str] = "DEBUG"

        # Levels
        self.default_level: Final[str] = "INFO"
        self.file_level: Final[str] = "DEBUG"
        self.errors_level: Final[str] = "ERROR"

    def ensure_directories(self) -> None:
        """Crea tutte le directory necessarie."""
        for directory in (
            self.base_dir,
            self.application_dir,
            self.errors_dir,
            self.metrics_dir,
            self.bots_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)

    def get_bot_log_path(self, bot_name: str, trace_id: str | None = None) -> Path:
        """
        Restituisce path per log specifico bot.

        Args:
            bot_name: Nome del bot (es: "scarico_ts")
            trace_id: ID univoco esecuzione (opzionale)

        Returns:
            Path al file log del bot
        """
        filename = f"{bot_name}_{trace_id}.json" if trace_id else f"{bot_name}.json"

        return self.bots_dir / filename


# Istanza singleton
_config: LoggingConfig | None = None


def get_config() -> LoggingConfig:
    """Restituisce configurazione singleton."""
    global _config  # noqa: PLW0603
    if _config is None:
        _config = LoggingConfig()
        _config.ensure_directories()
    return _config
