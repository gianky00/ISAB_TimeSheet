"""Formatters per output log (JSON e Human-readable)."""

import json
import os
import sys
import threading
import traceback
from datetime import UTC, datetime
from typing import Any

from .context import get_context
from .filters import SensitiveDataFilter


class JSONFormatter:
    """Formatter per output JSON strutturato.

    Produce log in formato JSON parsabile, ottimizzato per AI analysis.

    Inizializza formatter.

    Args:
      mask_sensitive: Se True, maschera dati sensibili
    """

    def __init__(self, mask_sensitive: bool = True) -> None:
        self.mask_sensitive = mask_sensitive

    def format(  # noqa: PLR0913
        self,
        level: str,
        logger_name: str,
        message: str,
        extra: dict[str, Any] | None = None,
        exception: Exception | None = None,
        source_info: dict[str, Any] | None = None,
    ) -> str:
        """Formatta log entry come JSON.

        Args:
          level: Livello log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
          logger_name: Nome logger
          message: Messaggio log
          extra: Dati extra (opzionale)
          exception: Eccezione (opzionale)
          source_info: Info su file/funzione/linea (opzionale)

        Returns:
          Stringa JSON
        """
        # Timestamp ISO 8601
        timestamp = datetime.now(UTC).isoformat() + "Z"

        # Context corrente
        context = get_context().to_dict()

        # Metadata base
        metadata = {
            "logger": logger_name,
            "process_id": os.getpid(),
            "thread_id": threading.get_ident(),
            "thread_name": threading.current_thread().name,
        }

        # Build entry
        entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "context": context,
            "metadata": metadata,
        }

        # Extra data
        if extra:
            # Maschera dati sensibili se richiesto
            if self.mask_sensitive:
                entry["data"] = SensitiveDataFilter.mask_dict(extra)
            else:
                entry["data"] = extra

        # Exception info
        if exception:
            entry["exception"] = {
                "type": type(exception).__name__,
                "message": str(exception),
                "traceback": traceback.format_exc(),
            }

        # Source info (file, function, line)
        if source_info:
            entry["source"] = source_info

        # Tags automatici
        entry["tags"] = self._generate_tags(level, message, context, extra)

        # Security flag
        if self.mask_sensitive:
            entry["security"] = {"pii_masked": True}

        # Serializza a JSON (una riga)
        return json.dumps(entry, ensure_ascii=False, default=str)

    def _generate_tags(
        self,
        level: str,
        message: str,
        context: dict[str, Any],
        extra: dict[str, Any] | None,
    ) -> list[str]:
        """Genera tags automatici per ricerca."""
        tags = [level.lower()]

        # Tag da context
        if "bot_type" in context:
            tags.append(f"bot:{context['bot_type']}")

        if "module" in context:
            tags.append(f"module:{context['module']}")

        msg_lower = message.lower()
        keyword_tags = {
            "error": ["error", "fail"],
            "success": ["success", "completat"],
            "download": ["download", "scaric"],
            "upload": ["upload", "caric"],
            "auth": ["login", "accesso"],
        }
        for tag, keywords in keyword_tags.items():
            if any(k in msg_lower for k in keywords):
                tags.append(tag)

        return list(set(tags))  # Remove duplicates


class HumanFormatter:
    """Formatter per output human-readable.

    Produce log in formato leggibile per troubleshooting manuale.

    Inizializza formatter.

    Args:
      colorize: Se True, usa colori ANSI (solo per console)
      show_context: Se True, mostra context nei log
    """

    def __init__(self, colorize: bool = True, show_context: bool = True) -> None:
        self.colorize = colorize and self._supports_color()
        self.show_context = show_context

    def _supports_color(self) -> bool:
        """Verifica se il terminale supporta colori."""
        if sys.platform != "win32":
            isatty = getattr(sys.stdout, "isatty", None)
            return bool(isatty and isatty())

        return "ANSICON" in os.environ or "WT_SESSION" in os.environ

    def _build_context_string(self) -> str:
        """Costruisce la stringa del context."""
        context = get_context().to_dict()
        if not context:
            return ""
        ctx_parts = []
        if "trace_id" in context:
            ctx_parts.append(f"trace={context['trace_id'][:12]}...")
        if "span_id" in context:
            ctx_parts.append(f"span={context['span_id']}")
        if "bot_type" in context:
            ctx_parts.append(f"bot={context['bot_type']}")

        return f" | {' | '.join(ctx_parts)}" if ctx_parts else ""

    def format(  # noqa: PLR0913
        self,
        level: str,
        logger_name: str,
        message: str,
        extra: dict[str, Any] | None = None,
        exception: Exception | None = None,
        source_info: dict[str, Any] | None = None,
    ) -> str:
        """Formatta log entry come stringa human-readable.

        Args:
          level: Livello log
          logger_name: Nome logger
          message: Messaggio log
          extra: Dati extra (opzionale)
          exception: Eccezione (opzionale)
          source_info: Info su file/funzione/linea (opzionale)

        Returns:
          Stringa formattata
        """
        # Timestamp (rimuovi microsecondi)
        timestamp = datetime.now(UTC).astimezone().strftime("%Y-%m-%d %H:%M:%S")

        # Colorizza livello
        level_colored = self._colorize_level(level) if self.colorize else f"{level:8}"

        # Build line base
        line = f"[{timestamp}] {level_colored} - {logger_name:30} - {message}"

        # Aggiungi context
        if self.show_context:
            line += self._build_context_string()

        # Aggiungi extra data
        if extra:
            extra_str = " | ".join(f"{k}={v}" for k, v in extra.items())
            line += f" | {extra_str}"

        # Aggiungi exception info
        if exception:
            line += f"\n Exception: {type(exception).__name__}: {exception}"

        return line

    def _colorize_level(self, level: str) -> str:
        """Applica colori ANSI al livello."""
        colors = {
            "DEBUG": "\033[36m",  # Cyan
            "INFO": "\033[32m",  # Green
            "WARNING": "\033[33m",  # Yellow
            "ERROR": "\033[31m",  # Red
            "CRITICAL": "\033[35m",  # Magenta
        }
        reset = "\033[0m"

        color = colors.get(level, "")
        return f"{color}{level:8}{reset}"
