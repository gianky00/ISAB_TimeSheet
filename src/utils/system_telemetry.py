"""
SyncroJob - Utility per Telemetria di Sistema
Funzioni centralizzate per raccogliere informazioni su CPU, RAM, network e sistema.
"""

import ctypes
import os
import platform
import socket
import time
from ctypes import Structure, byref, sizeof, wintypes
from dataclasses import dataclass
from typing import Optional

# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class OSInfo:
    """Informazioni sul sistema operativo."""

    system: str
    release: str
    version: str
    machine: str
    hostname: str


@dataclass
class CPUInfo:
    """Informazioni sulla CPU."""

    count: int
    frequency_ghz: Optional[float]
    percent: float


@dataclass
class RAMInfo:
    """Informazioni sulla memoria RAM."""

    total_gb: float
    used_gb: float
    available_gb: float
    percent: float


@dataclass
class NetworkInfo:
    """Informazioni sulla rete."""

    ip_address: str
    is_connected: bool
    io_rate_kbs: float


@dataclass
class ProcessInfo:
    """Informazioni sul processo corrente."""

    pid: int
    ram_mb: float
    threads: int


@dataclass
class SystemTelemetry:
    """Telemetria completa del sistema."""

    os_info: OSInfo
    cpu_info: CPUInfo
    ram_info: RAMInfo
    network_info: NetworkInfo
    process_info: ProcessInfo
    uptime_formatted: str


# =============================================================================
# WINDOWS MEMORY API (per RAM processo senza psutil)
# =============================================================================


class PROCESS_MEMORY_COUNTERS_EX(Structure):
    """Struttura Windows per info memoria processo."""

    _fields_ = [
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


def get_process_ram_mb_windows() -> float:
    """
    Ottiene l'uso RAM del processo corrente su Windows senza psutil.

    Returns:
        RAM usata in MB, 0.0 in caso di errore
    """
    try:
        if not hasattr(ctypes, "windll") or not hasattr(ctypes.windll, "psapi"):
            return 0.0

        psapi = ctypes.windll.psapi
        kernel32 = ctypes.windll.kernel32

        # Configura signature per 64-bit
        if not getattr(psapi.GetProcessMemoryInfo, "argtypes", None):
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
            return counters.WorkingSetSize / 1024 / 1024

    except Exception:
        pass

    return 0.0


# =============================================================================
# FUNZIONI DI RACCOLTA DATI
# =============================================================================


def get_os_info() -> OSInfo:
    """
    Raccoglie informazioni sul sistema operativo.

    Returns:
        OSInfo con i dati del sistema
    """
    try:
        hostname = socket.gethostname()
    except Exception:
        hostname = "unknown"

    return OSInfo(
        system=platform.system(),
        release=platform.release(),
        version=platform.version(),
        machine=platform.machine(),
        hostname=hostname,
    )


def get_cpu_info() -> CPUInfo:
    """
    Raccoglie informazioni sulla CPU.

    Richiede psutil per dati completi.

    Returns:
        CPUInfo con i dati della CPU
    """
    try:
        import psutil

        freq = psutil.cpu_freq()
        freq_ghz = freq.current / 1000 if freq else None

        return CPUInfo(
            count=psutil.cpu_count(logical=True) or 0,
            frequency_ghz=freq_ghz,
            percent=psutil.cpu_percent(interval=0.1),
        )
    except ImportError:
        return CPUInfo(count=0, frequency_ghz=None, percent=0.0)


def get_ram_info() -> RAMInfo:
    """
    Raccoglie informazioni sulla memoria RAM.

    Richiede psutil per dati completi.

    Returns:
        RAMInfo con i dati della RAM
    """
    try:
        import psutil

        ram = psutil.virtual_memory()
        return RAMInfo(
            total_gb=ram.total / (1024**3),
            used_gb=ram.used / (1024**3),
            available_gb=ram.available / (1024**3),
            percent=ram.percent,
        )
    except ImportError:
        return RAMInfo(total_gb=0, used_gb=0, available_gb=0, percent=0)


def get_network_info(last_bytes: int = 0, dt: float = 1.0) -> NetworkInfo:
    """
    Raccoglie informazioni sulla rete.

    Args:
        last_bytes: Bytes totali dal campionamento precedente
        dt: Intervallo di tempo in secondi

    Returns:
        NetworkInfo con i dati di rete
    """
    # IP Address
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
    except Exception:
        ip_address = "127.0.0.1"

    # Connection status e I/O rate
    try:
        import psutil

        net_stats = psutil.net_if_stats()
        is_connected = any(stats.isup for stats in net_stats.values())

        # Calcola I/O rate
        net = psutil.net_io_counters()
        current_bytes = net.bytes_recv + net.bytes_sent
        io_rate_kbs = (current_bytes - last_bytes) / dt / 1024 if dt > 0 else 0

    except ImportError:
        is_connected = True
        io_rate_kbs = 0.0

    return NetworkInfo(
        ip_address=ip_address,
        is_connected=is_connected,
        io_rate_kbs=io_rate_kbs,
    )


def get_process_info() -> ProcessInfo:
    """
    Raccoglie informazioni sul processo corrente.

    Returns:
        ProcessInfo con i dati del processo
    """
    pid = os.getpid()

    try:
        import psutil

        process = psutil.Process(pid)
        ram_mb = process.memory_info().rss / (1024 * 1024)
        threads = process.num_threads()
    except ImportError:
        # Fallback a Windows API per RAM
        ram_mb = get_process_ram_mb_windows()
        threads = 0

    return ProcessInfo(pid=pid, ram_mb=ram_mb, threads=threads)


def get_uptime_formatted() -> str:
    """
    Calcola e formatta l'uptime del sistema.

    Returns:
        Stringa formattata tipo "2d 5h" o "3h 25m"
    """
    try:
        import psutil

        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)

        if hours >= 24:
            days = hours // 24
            hours = hours % 24
            return f"{days}d {hours}h"
        else:
            return f"{hours}h {minutes}m"
    except ImportError:
        return "N/A"


def get_full_telemetry() -> SystemTelemetry:
    """
    Raccoglie la telemetria completa del sistema.

    Returns:
        SystemTelemetry con tutti i dati
    """
    return SystemTelemetry(
        os_info=get_os_info(),
        cpu_info=get_cpu_info(),
        ram_info=get_ram_info(),
        network_info=get_network_info(),
        process_info=get_process_info(),
        uptime_formatted=get_uptime_formatted(),
    )


# =============================================================================
# FUNZIONI DI FORMATTAZIONE
# =============================================================================


def format_bytes(bytes_value: int) -> str:
    """
    Formatta un valore in bytes in una stringa leggibile.

    Args:
        bytes_value: Valore in bytes

    Returns:
        Stringa tipo "1.5 GB" o "256 MB"
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.1f} PB"


def format_frequency(freq_mhz: float) -> str:
    """
    Formatta una frequenza in MHz in una stringa leggibile.

    Args:
        freq_mhz: Frequenza in MHz

    Returns:
        Stringa tipo "3.40 GHz"
    """
    if freq_mhz >= 1000:
        return f"{freq_mhz / 1000:.2f} GHz"
    return f"{freq_mhz:.0f} MHz"
