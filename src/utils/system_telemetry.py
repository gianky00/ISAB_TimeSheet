"""
SyncroJob - System Telemetry Utilities
Monitoraggio risorse di sistema (RAM, CPU) tramite API native Windows.
"""

import ctypes
import logging
from ctypes import Structure, byref, sizeof, wintypes
from typing import Any, ClassVar

logger = logging.getLogger(__name__)

# =============================================================================
# WINDOWS API WRAPPER
# =============================================================================


class PROCESS_MEMORY_COUNTERS_EX(Structure):
    """Struttura Windows per i contatori di memoria del processo."""

    _fields_: ClassVar[list[tuple[str, Any]]] = [
        ("cb", wintypes.DWORD),
        ("PageFaultCount", wintypes.DWORD),
        ("PeakWorkingSetSize", ctypes.c_size_t),
        ("WorkingSetSize", ctypes.c_size_t),
        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
        ("PagefileUsage", ctypes.c_size_t),
        ("PeakPagefileUsage", ctypes.c_size_t),
        ("PrivateUsage", ctypes.c_size_t),
    ]


class FILETIME(Structure):
    """Struttura Windows per timestamp di sistema."""

    _fields_: ClassVar[list[tuple[str, Any]]] = [
        ("dwLowDateTime", wintypes.DWORD),
        ("dwHighDateTime", wintypes.DWORD),
    ]


def get_current_process_ram_mb() -> float:
    """
    Restituisce l'uso attuale della RAM (Working Set) del processo corrente in MB.
    Funziona solo su Windows tramite psapi.dll.
    """
    try:
        if not hasattr(ctypes, "windll") or not hasattr(ctypes.windll, "psapi"):
            return 0.0

        psapi = ctypes.windll.psapi
        kernel32 = ctypes.windll.kernel32

        # Configura firme per Python 64-bit
        if not hasattr(psapi.GetProcessMemoryInfo, "argtypes"):
            psapi.GetProcessMemoryInfo.argtypes = (
                wintypes.HANDLE,
                ctypes.POINTER(PROCESS_MEMORY_COUNTERS_EX),
                wintypes.DWORD,
            )
            psapi.GetProcessMemoryInfo.restype = wintypes.BOOL

        process = kernel32.GetCurrentProcess()
        counters = PROCESS_MEMORY_COUNTERS_EX()
        counters.cb = sizeof(PROCESS_MEMORY_COUNTERS_EX)

        if psapi.GetProcessMemoryInfo(process, byref(counters), sizeof(counters)):
            return float(counters.WorkingSetSize) / 1024 / 1024
    except Exception as e:
        logger.debug(f"Errore recupero RAM: {e}")
    return 0.0
