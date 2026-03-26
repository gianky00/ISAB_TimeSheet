"""
Main logger implementation con multi-sink support.
"""

import inspect
import sys
from contextlib import suppress
from typing import Any

from .config import get_config
from .context import get_context
from .formatters import HumanFormatter, JSONFormatter
from .sampling import get_sampler
from .sinks import get_bot_sink

# Registry di logger
_loggers: dict[str, "StructuredLogger"] = {}
_initialized = False


class StructuredLogger:
    """
    Logger enterprise con structured logging e multi-sink.

    Features:
    - Output JSON per AI analysis
    - Output human-readable per debug
    - File separato per errori
    - Rotation automatica
    - Context propagation
    - PII masking
    """

    def __init__(self, name: str, config: Any = None) -> None:
        """
        Inizializza logger.

        Args:
            name: Nome logger (tipicamente __name__ del modulo)
            config: Configurazione custom (opzionale)
        """
        self.name = name
        self.config = config or get_config()

        # Formatters
        self.json_formatter = JSONFormatter(mask_sensitive=True)
        self.human_formatter = HumanFormatter(colorize=True, show_context=True)

        # File handles (apriamo file in append mode)
        self._json_file = None
        self._human_file = None
        self._errors_file = None

        # Livello minimo
        self.min_level = self._parse_level(self.config.default_level)

    def _parse_level(self, level_str: str) -> int:
        """Converte stringa livello a valore numerico."""
        return {
            "DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50,
        }.get(level_str.upper(), 20)

    def _get_source_info(self) -> dict[str, Any]:
        """
        Estrae informazioni sulla sorgente del log (file, funzione, linea).

        Returns:
            Dict con file, function, line
        """
        with suppress(Exception):
            # Risali nello stack per trovare il caller reale
            # (salta frames interni del logger)
            frame = inspect.currentframe()
            if (
                frame is None
                or frame.f_back is None
                or frame.f_back.f_back is None
                or frame.f_back.f_back.f_back is None
            ):
                return {}

            # Salta i frame del logger stesso
            caller_frame = frame.f_back.f_back.f_back

            if caller_frame:
                return {
                    "file": caller_frame.f_code.co_filename,
                    "function": caller_frame.f_code.co_name,
                    "line": caller_frame.f_lineno,
                }

        return {}

    def _should_log(self, level: str) -> bool:
        """Verifica se il livello deve essere loggato."""
        level_value = self._parse_level(level)
        return level_value >= self.min_level

    def _write_to_sinks(  # noqa: PLR0912
        self,
        level: str,
        message: str,
        extra: dict[str, Any] | None = None,
        exception: Exception | None = None,
    ) -> None:
        """
        Scrive log in tutti i sink configurati.

        Args:
            level: Livello log
            message: Messaggio
            extra: Dati extra
            exception: Eccezione (opzionale)
        """
        # Sampling check
        context = get_context().to_dict()
        sampler = get_sampler()
        if not sampler.should_log(level, context, extra):
            return

        # Source info
        source_info = self._get_source_info()

        # Console output
        if self.config.console_enabled:
            console_line = self.human_formatter.format(
                level, self.name, message, extra, exception, source_info
            )
            try:
                print(console_line)
            except UnicodeEncodeError:
                # Fallback per console Windows legacy che non supporta UTF-8
                safe_line = console_line.encode("ascii", "replace").decode("ascii")
                print(safe_line)
            except Exception:  # noqa: S110
                # Ignora errori di scrittura su stdout (es. broken pipe o null handle)
                pass

            # Se c'è exception, stampa anche lo stack trace
            if exception:
                import traceback  # noqa: PLC0415

                with suppress(Exception):
                    print(traceback.format_exc())

        # JSON file output
        if self.config.json_log_file:
            json_line = self.json_formatter.format(level, self.name, message, extra, exception, source_info)
            try:
                with self.config.json_log_file.open("a", encoding="utf-8") as f:
                    f.write(json_line + "\n")
            except Exception as e:
                print(f"[LOGGER ERROR] Failed to write JSON log: {e}", file=sys.stderr)

        # Human file output
        if self.config.human_log_file:
            # Usa formatter senza colori per file
            file_formatter = HumanFormatter(colorize=False, show_context=True)
            human_line = file_formatter.format(level, self.name, message, extra, exception, source_info)
            try:
                with self.config.human_log_file.open("a", encoding="utf-8") as f:
                    f.write(human_line + "\n")

                    # Stack trace separato
                    if exception:
                        import traceback  # noqa: PLC0415

                        f.write(traceback.format_exc() + "\n")
            except Exception as e:
                print(f"[LOGGER ERROR] Failed to write human log: {e}", file=sys.stderr)

        # Errors file (solo ERROR e CRITICAL)
        if level in ("ERROR", "CRITICAL") and self.config.errors_log_file:
            json_line = self.json_formatter.format(level, self.name, message, extra, exception, source_info)
            try:
                with self.config.errors_log_file.open("a", encoding="utf-8") as f:
                    f.write(json_line + "\n")
            except Exception as e:
                print(f"[LOGGER ERROR] Failed to write errors log: {e}", file=sys.stderr)

        # Bot-specific log file (se ha trace_id e bot_type)
        context = get_context().to_dict()
        if context.get("trace_id") and context.get("bot_type"):
            bot_sink = get_bot_sink()
            bot_sink.write(level, self.name, message, context, extra, exception, source_info)

    def log(
        self,
        level: str,
        message: str,
        extra: dict[str, Any] | None = None,
        exception: Exception | None = None,
    ) -> None:
        """
        Log generico.

        Args:
            level: Livello (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Messaggio log
            extra: Dati extra (opzionale)
            exception: Eccezione (opzionale)
        """
        if not self._should_log(level):
            return

        self._write_to_sinks(level, message, extra, exception)

    def debug(self, message: str, **extra: Any) -> None:
        """Log a livello DEBUG."""
        self.log("DEBUG", message, extra=extra or None)

    def info(self, message: str, **extra: Any) -> None:
        """Log a livello INFO."""
        self.log("INFO", message, extra=extra or None)

    def warning(self, message: str, **extra: Any) -> None:
        """Log a livello WARNING."""
        self.log("WARNING", message, extra=extra or None)

    def error(self, message: str, **extra: Any) -> None:
        """Log a livello ERROR."""
        self.log("ERROR", message, extra=extra or None)

    def critical(self, message: str, **extra: Any) -> None:
        """Log a livello CRITICAL."""
        self.log("CRITICAL", message, extra=extra or None)

    def exception(self, message: str, exc: Exception, **extra: Any) -> None:
        """
        Log exception con stack trace completo.

        Args:
            message: Messaggio descrittivo
            exc: Eccezione da loggare
            **extra: Dati extra
        """
        self.log("ERROR", message, extra=extra or None, exception=exc)


def configure_logging(config: Any = None) -> None:
    """
    Configura il sistema di logging globale.

    Args:
        config: Configurazione custom (opzionale)

    Note:
        Questa funzione dovrebbe essere chiamata una volta all'avvio
        dell'applicazione.
    """
    global _initialized  # noqa: PLW0603

    if _initialized:
        return

    # Usa config fornita o default
    cfg = config or get_config()

    # Assicurati che le directory esistano
    cfg.ensure_directories()

    _initialized = True


def get_logger(name: str, config: Any = None) -> StructuredLogger:
    """
    Factory per ottenere logger.

    Usage:
        logger = get_logger(__name__)
        logger.info("Messaggio", extra_field="value")

    Args:
        name: Nome logger (tipicamente __name__ del modulo)
        config: Configurazione custom (opzionale)

    Returns:
        Istanza StructuredLogger
    """
    # Auto-configure al primo utilizzo
    if not _initialized:
        configure_logging(config)

    # Cache logger per nome
    if name not in _loggers:
        _loggers[name] = StructuredLogger(name, config)

    return _loggers[name]


def set_level(level: str) -> None:
    """
    Imposta livello minimo di logging per tutti i logger.

    Args:
        level: Uno tra DEBUG, INFO, WARNING, ERROR, CRITICAL
    """
    config = get_config()
    config.default_level = level.upper()

    # Aggiorna logger esistenti
    for logger_obj in _loggers.values():
        logger_obj.min_level = logger_obj._parse_level(level)
