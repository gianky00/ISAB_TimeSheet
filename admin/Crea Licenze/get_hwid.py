import subprocess
import sys
from contextlib import suppress

def get_windows_hwid():
    """Recupera l'Hardware ID (Seriale Disco) esattamente come il validator."""
    CREATE_NO_WINDOW = 0x08000000
    
    # Tentativo 1: WMIC
    with suppress(Exception):
        cmd = ["wmic", "diskdrive", "get", "serialnumber"]
        output = subprocess.check_output(
            cmd, shell=False, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW
        ).decode()
        parts = output.strip().split("\n")
        if len(parts) > 1 and parts[1].strip():
            return parts[1].strip()

    # Tentativo 2: PowerShell
    with suppress(Exception):
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-CimInstance -Class Win32_DiskDrive | Select-Object -ExpandProperty SerialNumber",
        ]
        output = (
            subprocess.check_output(cmd, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)
            .decode()
            .strip()
        )
        if output:
            return output.splitlines()[0].strip()

    return "NON_TROVATO"

if __name__ == "__main__":
    hwid = get_windows_hwid()
    # Pulisce esattamente come admin_license_gui.py
    clean_hwid = hwid.strip().rstrip(".")
    print(clean_hwid)
