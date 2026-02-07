"""
Enhanced metadata enrichment per log entries.
"""

import os
import platform
import socket
from pathlib import Path
from typing import Any, Optional

try:
    from src.core.version import __version__ as VERSION
except ImportError:
    VERSION = "unknown"


class MetadataEnricher:
    """
    Arricchisce log entries con metadata automatici.

    Metadata inclusi:
    - Informazioni applicazione (version, environment)
    - Informazioni sistema (hostname, os, python version)
    - Informazioni processo (pid, user)
    - Informazioni session/request (se disponibili)
    """

    _instance: Optional["MetadataEnricher"] = None
    _cache: dict[str, Any] | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if MetadataEnricher._cache is None:
            MetadataEnricher._cache = self._build_static_metadata()

    def _build_static_metadata(self) -> dict[str, Any]:
        """
        Costruisce metadata statici (calcolati una volta sola).

        Returns:
            Dict con metadata statici
        """
        metadata = {}

        # Application info
        metadata["app_name"] = "SyncroJob"
        metadata["app_version"] = VERSION

        # Environment detection
        metadata["environment"] = self._detect_environment()

        # System info
        try:
            metadata["hostname"] = socket.gethostname()
        except Exception:
            metadata["hostname"] = "unknown"

        metadata["platform"] = platform.system()
        metadata["platform_release"] = platform.release()
        metadata["python_version"] = platform.python_version()

        # User info
        try:
            metadata["user"] = os.getlogin()
        except Exception:
            metadata["user"] = os.environ.get("USERNAME") or os.environ.get("USER") or "unknown"

        return metadata

    def _detect_environment(self) -> str:
        """
        Rileva environment corrente.

        Returns:
            Uno tra: "development", "production", "test"
        """
        # Check variabile ambiente
        env = os.environ.get("SYNCROJOB_ENV", "").lower()
        if env in ("dev", "development"):
            return "development"
        if env in ("prod", "production"):
            return "production"
        if env in ("test", "testing"):
            return "test"

        # Euristica: se eseguito da pytest o unittest, è test
        import sys

        if "pytest" in sys.modules or "unittest" in sys.modules:
            return "test"

        # Euristica: se eseguito da IDE (pycharm, vscode), è development
        if any(ide in sys.executable.lower() for ide in ("pycharm", "vscode", "code")):
            return "development"

        # Euristica: se eseguito da .exe compilato, è production
        if getattr(sys, "frozen", False):
            return "production"

        # Default: development
        return "development"

    def get_static_metadata(self) -> dict[str, Any]:
        """
        Restituisce metadata statici (cached).

        Returns:
            Dict con metadata statici
        """
        if self._cache is None:
            return {}
        return self._cache.copy()

    def get_dynamic_metadata(self) -> dict[str, Any]:
        """
        Restituisce metadata dinamici (calcolati ogni volta).

        Returns:
            Dict con metadata dinamici
        """
        metadata: dict[str, Any] = {}

        # Process info (può cambiare tra fork/spawn)
        metadata["process_id"] = os.getpid()
        metadata["parent_process_id"] = os.getppid()

        # Working directory
        try:
            metadata["working_directory"] = str(Path.cwd())
        except Exception:
            metadata["working_directory"] = "unknown"

        return metadata

    def get_full_metadata(self) -> dict[str, Any]:
        """
        Restituisce tutti i metadata (statici + dinamici).

        Returns:
            Dict con metadata completi
        """
        metadata = self.get_static_metadata()
        metadata.update(self.get_dynamic_metadata())
        return metadata

    def enrich_log_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        """
        Arricchisce log entry con metadata.

        Args:
            entry: Log entry da arricchire

        Returns:
            Log entry arricchito
        """
        # Aggiungi metadata se non già presenti
        if "metadata" not in entry:
            entry["metadata"] = {}

        # Aggiungi metadata statici
        for key, value in self.get_static_metadata().items():
            if key not in entry["metadata"]:
                entry["metadata"][key] = value

        # Aggiungi metadata dinamici selezionati
        dynamic = self.get_dynamic_metadata()
        if "process_id" not in entry["metadata"]:
            entry["metadata"]["process_id"] = dynamic["process_id"]

        return entry


# Singleton instance
_enricher = None


def get_enricher() -> MetadataEnricher:
    """Restituisce istanza singleton del metadata enricher."""
    global _enricher
    if _enricher is None:
        _enricher = MetadataEnricher()
    return _enricher


def enrich_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """
    Helper function per arricchire log entry.

    Args:
        entry: Log entry da arricchire

    Returns:
        Log entry arricchito
    """
    return get_enricher().enrich_log_entry(entry)
