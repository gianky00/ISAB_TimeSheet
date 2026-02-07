"""
Configurazione sistema di logging.
"""

from pathlib import Path

from src.core import config_manager


class LoggingConfig:
    """Configurazione centralizzata per il sistema di logging."""

    def __init__(self):
        # Base directory: C:\Users\gianc\AppData\Local\SyncroJob\logs
        self.base_dir = config_manager.CONFIG_DIR / "logs"

        # Sottodirectory per tipo log
        self.application_dir = self.base_dir / "application"
        self.errors_dir = self.base_dir / "errors"
        self.metrics_dir = self.base_dir / "metrics"
        self.bots_dir = self.base_dir / "bots"

        # File paths
        self.json_log_file = self.application_dir / "app.json"
        self.human_log_file = self.application_dir / "app.log"
        self.errors_log_file = self.errors_dir / "errors.json"

        # Rotation settings
        self.rotation_size = "10 MB"  # Rotazione quando file raggiunge 10MB
        self.rotation_time = "00:00"  # Rotazione giornaliera a mezzanotte
        self.retention = "30 days"  # Mantieni log per 30 giorni
        self.errors_retention = "90 days"  # Errori mantenuti 90 giorni
        self.compression = "zip"  # Comprimi log vecchi

        # Performance settings
        self.performance_threshold_ms = 5000  # Alert se operazione > 5sec
        self.sampling_rate = 1.0  # 1.0 = log tutto (100%), 0.01 = log 1%

        # Console output
        self.console_enabled = True
        self.console_level = "DEBUG"

        # Levels
        self.default_level = "INFO"
        self.file_level = "DEBUG"
        self.errors_level = "ERROR"

    def ensure_directories(self):
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
_config = None


def get_config() -> LoggingConfig:
    """Restituisce configurazione singleton."""
    global _config
    if _config is None:
        _config = LoggingConfig()
        _config.ensure_directories()
    return _config
