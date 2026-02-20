"""
SyncroJob - License Validator
Gestisce la validazione della licenza software.
"""

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import uuid
from contextlib import suppress
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet

from src.core.audit_manager import AuditManager
from src.core.secrets_manager import SecretsManager
from src.core.time_manager import get_trusted_time


class LicenseStatus(Enum):
    VALID = "Valid"
    MISSING = "Missing"
    INVALID = "Invalid"
    EXPIRED = "Expired"
    ERROR = "Error"
    GRACE = "Grace"


def _calculate_sha256(filepath):
    """Calcola l'hash SHA256 di un file."""
    sha256_hash = hashlib.sha256()
    with Path(filepath).open("rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_hardware_id():
    """
    Ottiene un ID hardware univoco per la macchina.
    """
    if platform.system() == "Windows":
        return _get_windows_hardware_id()
    if platform.system() == "Linux":
        return _get_linux_hardware_id()

    # Fallback universale: UUID basato su MAC address
    try:
        return str(uuid.getnode())
    except Exception:
        return "ERROR_GETTING_ID"


def _get_windows_hardware_id():
    """Helper to get hardware ID on Windows."""
    # Definisce il flag per nascondere la finestra del processo (Windows)
    CREATE_NO_WINDOW = 0x08000000

    # 1. Try WMIC (Legacy)
    with suppress(Exception):
        cmd = ["wmic", "diskdrive", "get", "serialnumber"]
        output = subprocess.check_output(
            cmd, shell=False, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW
        ).decode()
        parts = output.strip().split("\n")
        if len(parts) > 1:
            serial = parts[1].strip()
            if serial:
                return serial

    # 2. Try PowerShell (Disk Serial)
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

    # 3. Try PowerShell (System UUID)
    with suppress(Exception):
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-CimInstance -Class Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID",
        ]
        output = (
            subprocess.check_output(cmd, stderr=subprocess.DEVNULL, creationflags=CREATE_NO_WINDOW)
            .decode()
            .strip()
        )

        if output:
            return output
    return None


def _get_linux_hardware_id():
    """Helper to get hardware ID on Linux."""
    # Try lsblk
    with suppress(Exception):
        # Avoid complex pipes with shell=True, execute basic lsblk and parse in python
        cmd = ["lsblk", "--nodeps", "-o", "serial", "-n"]
        output = subprocess.check_output(cmd, shell=False, stderr=subprocess.DEVNULL).decode().strip()

        # Take the first line if multiple disks
        first_line = output.split("\n")[0].strip()

        if first_line:
            return first_line

    # Fallback to machine-id
    machine_id = Path("/etc/machine-id")
    if machine_id.exists():
        with suppress(Exception):
            return machine_id.read_text().strip()
    return None


def _get_license_paths() -> dict[str, Path]:
    """Restituisce i percorsi dei file di licenza."""
    from src.core import config_manager

    # Use standard data path via config_manager.get_data_path()
    # This ensures alignment with where data (and license) are expected
    base_data_dir = Path(config_manager.get_data_path())

    license_dir = base_data_dir / "Licenza"
    return {
        "dir": license_dir,
        "config": license_dir / "config.dat",
        "manifest": license_dir / "manifest.json",
    }


def _check_and_migrate_local_license(target_paths: dict[str, Any]):
    """
    Check if license files exist in the application directory (e.g. where .exe is)
    or in legacy Roaming AppData. If found, copy them to the standard AppData location.
    """
    # 1. Determine app root
    if getattr(sys, "frozen", False):
        app_dir = Path(sys.executable).parent
    else:
        # In dev mode, look in project root (2 levels up from src/core)
        app_dir = Path(__file__).parent.parent.parent.resolve()

    # 2. Potential legacy locations (including Roaming and old names)
    from platformdirs import user_data_dir

    from src.core.config_manager import APP_NAME

    local_appdata = Path(os.environ.get("LOCALAPPDATA", ""))
    legacy_app_names = ["BotTS", "Bot TS", "SyncroJob"]

    potential_dirs = [
        app_dir / "Licenza",  # Standard portable
        app_dir,              # Flat portable
        Path(user_data_dir(APP_NAME, appauthor=False, roaming=True)) / "Licenza", # Legacy Roaming
    ]

    # Add variant folders in Local AppData
    if local_appdata:
        for old_name in legacy_app_names:
            # Check with and without data subfolder as structure varied
            base_dir = local_appdata / old_name
            base_author = local_appdata / "GiancarloAllegretti" / old_name

            potential_dirs.extend((
                base_dir / "Licenza",
                base_dir / "data" / "Licenza",
                base_author / "Licenza",
                base_author / "data" / "Licenza"
            ))

    for source_dir in potential_dirs:
        config_src = source_dir / "config.dat"
        manifest_src = source_dir / "manifest.json"

        if config_src.exists() and manifest_src.exists():
            with suppress(Exception):
                target_paths["dir"].mkdir(parents=True, exist_ok=True)
                shutil.copy2(config_src, target_paths["config"])
                shutil.copy2(manifest_src, target_paths["manifest"])
                print(f"[MIGRATION] License migrated from {source_dir}")
                return True

    return False


def get_license_info():
    """
    Ottiene le informazioni della licenza decifrate.

    Returns:
        dict: Dati della licenza o None in caso di errore
    """
    paths = _get_license_paths()
    config_path = paths["config"]

    if not config_path.exists():
        _check_and_migrate_local_license(paths)

    if not config_path.exists():
        return None

    try:
        encrypted_data = config_path.read_bytes()

        # Retrieve key securely
        key_raw = SecretsManager.get_license_key()
        if not key_raw:
            return None

        # Fernet requires url-safe base64 encoded bytes
        import base64

        key_b64 = base64.urlsafe_b64encode(key_raw)

        cipher = Fernet(key_b64)
        decrypted_data = cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode("utf-8"))
    except Exception:
        return None


def verify_license():
    """
    Verifica la validità della licenza.

    Wrapper per retrocompatibilità.
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    status, msg = get_detailed_license_status()
    return status == LicenseStatus.VALID, msg


def get_detailed_license_status():
    """
    Verifica dettagliata dello stato licenza.
    Returns:
        tuple: (LicenseStatus, message_str)
    """
    paths = _get_license_paths()

    # Controllo cartella
    if not paths["dir"].exists():
        try:
            paths["dir"].mkdir(parents=True)
        except OSError:
            return LicenseStatus.ERROR, "Impossibile creare cartella 'Licenza'"

    # 0. Check Migration (Fix for manual installation)
    if not (paths["config"].exists() and paths["manifest"].exists()):
        _check_and_migrate_local_license(paths)

    # Controllo file
    if not paths["config"].exists() or not paths["manifest"].exists():
        return LicenseStatus.MISSING, "File di licenza mancanti"

    # 1. Verifica integrità tramite manifest
    integrity_status, integrity_msg = _check_integrity_with_manifest(paths)
    if integrity_status != LicenseStatus.VALID:
        return integrity_status, integrity_msg

    # 2. Decifra e valida i dati
    validation_status, validation_msg = _validate_license_data(paths)
    return validation_status, validation_msg


def _check_integrity_with_manifest(paths: dict[str, Any]) -> tuple[LicenseStatus, str]:
    """Helper to check license file integrity using manifest."""
    try:
        manifest = json.loads(Path(paths["manifest"]).read_text(encoding="utf-8"))

        # Verifica hash config.dat
        if _calculate_sha256(paths["config"]) != manifest.get("config.dat"):
            msg = "Integrità licenza compromessa (config.dat)"
            AuditManager.instance().log_action(
                "Violazione Licenza",
                category="sicurezza",
                entity="File Config",
                status="error",
                severity="high",
            )
            return LicenseStatus.INVALID, msg

    except Exception as e:
        return LicenseStatus.ERROR, f"Errore lettura manifest: {e}"
    return LicenseStatus.VALID, ""


def _validate_license_data(paths: dict[str, Any]) -> tuple[LicenseStatus, str]:
    """Helper to decrypt and validate license data."""
    try:
        payload = get_license_info()
        if not payload:
            return LicenseStatus.INVALID, "Impossibile leggere i dati della licenza"

        # Validazione Hardware ID
        current_hw_id = get_hardware_id()
        license_hw_id = payload.get("Hardware ID", "")

        # Normalizzazione ID
        norm_current = current_hw_id.strip().rstrip(".")
        norm_license = license_hw_id.strip().rstrip(".")

        if norm_current != norm_license and "UNKNOWN" not in current_hw_id:
            msg = f"Hardware ID non valido\nAtteso: {license_hw_id}\nRilevato: {current_hw_id}"
            AuditManager.instance().log_action(
                "Mismatch Hardware",
                category="sicurezza",
                entity="Licenza",
                params={"atteso": license_hw_id, "rilevato": current_hw_id},
                status="error",
                severity="high",
            )
            return LicenseStatus.INVALID, msg

        # Validazione scadenza
        expiry_str = payload.get("Scadenza Licenza", "")
        if expiry_str:
            try:
                day, month, year = map(int, expiry_str.split("/"))
                expiry_date = date(year, month, day)

                # Utilizzo orario fidato (Network Time)
                trusted_now_dt, is_trusted = get_trusted_time()
                trusted_date = trusted_now_dt.date()

                if trusted_date > expiry_date:
                    msg = f"Licenza SCADUTA il {expiry_str}"
                    if not is_trusted:
                        msg += " (Verifica orario di sistema)"
                    return LicenseStatus.EXPIRED, msg
            except ValueError:
                return LicenseStatus.INVALID, "Formato data scadenza non valido"

        cliente = payload.get("Cliente", "Utente")
        return LicenseStatus.VALID, f"Licenza valida per: {cliente}"

    except Exception as e:
        return LicenseStatus.ERROR, f"Errore validazione licenza: {e}"


def get_license_expiry():
    """Restituisce la data di scadenza della licenza."""
    info = get_license_info()
    if info:
        return info.get("Scadenza Licenza", "N/D")
    return "N/D"


def get_license_client():
    """Restituisce il nome del cliente."""
    info = get_license_info()
    if info:
        return info.get("Cliente", "N/D")
    return "N/D"
