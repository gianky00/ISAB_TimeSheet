"""SyncroJob - Diagnostics Collector.

Modulo responsabile esclusivamente della raccolta di informazioni diagnostiche,
telemetria hardware, specifiche di sistema ed ambiente operativo.
"""

import logging
import os
import platform
from datetime import UTC, datetime
from typing import Any

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from src.core.paths import get_version

logger = logging.getLogger(__name__)


class DiagnosticsCollector:
    """Raccoglitore specializzato in telemetria hardware, configurazione sistema ed ambiente."""

    @staticmethod
    def collect_system_info() -> dict[str, Any]:
        """Raccoglie informazioni dettagliate di sistema, CPU, memoria e variabili ambiente.

        Returns:
            Dizionario contenente la telemetria di sistema.
        """
        sys_info: dict[str, Any] = {
            "app_version": get_version(),
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "timestamp": datetime_now_iso(),
            "python_version": platform.python_version(),
            "processor": platform.processor(),
        }

        # Filtra le variabili d'ambiente per evitare di esporre segreti
        safe_env = {
            k: v
            for k, v in os.environ.items()
            if not any(
                s in k.upper() for s in ("TOKEN", "KEY", "PASS", "SECRET", "API", "AUTH", "CREDENTIAL")
            )
        }
        sys_info["env_filtered"] = safe_env

        # Raccolta telemetria memoria e hardware (via psutil se disponibile)
        if PSUTIL_AVAILABLE:
            try:
                mem = psutil.virtual_memory()
                sys_info["memory"] = {
                    "total": f"{mem.total / (1024**3):.2f} GB",
                    "available": f"{mem.available / (1024**3):.2f} GB",
                    "percent": f"{mem.percent}%",
                }

                sys_info["cpu"] = {
                    "cores_physical": psutil.cpu_count(logical=False),
                    "cores_logical": psutil.cpu_count(logical=True),
                    "usage_percent": psutil.cpu_percent(interval=0.1),
                }

                disk = psutil.disk_usage("/")
                sys_info["disk"] = {
                    "total": f"{disk.total / (1024**3):.2f} GB",
                    "free": f"{disk.free / (1024**3):.2f} GB",
                    "percent": f"{disk.percent}%",
                }
            except Exception as e:
                logger.warning(f"Errore durante la lettura delle metriche hardware psutil: {e}")
                sys_info["system_info_error"] = str(e)
        else:
            sys_info["memory"] = "psutil not installed"
            logger.debug("Libreria psutil non installata, telemetria hardware saltata.")

        return sys_info


def datetime_now_iso() -> str:
    """Restituisce il timestamp UTC corrente in formato ISO string."""
    return datetime.now(UTC).astimezone().isoformat()
