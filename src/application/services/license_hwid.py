"""SyncroJob - License HWID.

Utility per l'estrazione dell'Hardware ID (HWID) del sistema.
Isolato per evitare dipendenze circolari tra LicenseValidator e SecretsManager.
"""

import os
import platform
import subprocess  # nosec B404
import uuid
from contextlib import suppress
from pathlib import Path


def get_hardware_id() -> str:
    """Recupera un identificativo hardware univoco per la macchina corrente.

    Tenta in ordine:
    1. Serial number del disco primario (Windows/Linux)
    2. UUID del sistema (Windows)
    3. Machine-ID (Linux)
    4. Node ID (Fallback Universale).
    """
    raw_id = ""
    if platform.system() == "Windows":
        raw_id = _get_windows_hardware_id() or "ERROR_GETTING_ID"
    elif platform.system() == "Linux":
        raw_id = _get_linux_hardware_id() or "ERROR_GETTING_ID"
    else:
        try:
            raw_id = str(uuid.getnode())
        except Exception:
            raw_id = "ERROR_GETTING_ID"

    return raw_id.strip().rstrip(".")


def _get_windows_hardware_id() -> str | None:
    """Recupera l'HWID su sistemi Windows tramite WMIC o PowerShell."""
    create_no_window = 0x08000000
    system_root = os.environ.get("SYSTEMROOT", "C:\\Windows")
    wmic_path = os.path.join(system_root, "System32\\wbem\\wmic.exe")
    powershell_path = os.path.join(system_root, "System32\\WindowsPowerShell\\v1.0\\powershell.exe")

    with suppress(Exception):
        cmd = [wmic_path, "diskdrive", "get", "serialnumber"]
        output = subprocess.check_output(  # nosec B603
            cmd, shell=False, stderr=subprocess.DEVNULL, creationflags=create_no_window
        ).decode()
        parts = output.strip().split("\n")
        if len(parts) > 1 and parts[1].strip():
            return parts[1].strip()

    with suppress(Exception):
        cmd = [
            powershell_path,
            "-NoProfile",
            "-Command",
            "Get-CimInstance -Class Win32_DiskDrive | Select-Object -ExpandProperty SerialNumber",
        ]
        output = (
            subprocess.check_output(cmd, stderr=subprocess.DEVNULL, creationflags=create_no_window)  # nosec B603
            .decode()
            .strip()
        )
        if output:
            return output.splitlines()[0].strip()

    with suppress(Exception):
        cmd = [
            powershell_path,
            "-NoProfile",
            "-Command",
            "Get-CimInstance -Class Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID",
        ]
        output = (
            subprocess.check_output(cmd, stderr=subprocess.DEVNULL, creationflags=create_no_window)  # nosec B603
            .decode()
            .strip()
        )
        if output:
            return output
    return None


def _get_linux_hardware_id() -> str | None:
    """Recupera l'HWID su sistemi Linux tramite lsblk o machine-id."""
    with suppress(Exception):
        # Percorso assoluto per mitigare B607
        cmd = ["/usr/bin/lsblk", "--nodeps", "-o", "serial", "-n"]
        output = subprocess.check_output(cmd, shell=False, stderr=subprocess.DEVNULL).decode().strip()  # nosec B603
        if output:
            return output.split("\n")[0].strip()
    machine_id = Path("/etc/machine-id")
    if machine_id.exists():
        with suppress(Exception):
            return machine_id.read_text().strip()
    return None
