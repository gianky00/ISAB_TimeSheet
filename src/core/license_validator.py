"""
SyncroJob - License Validator
Gestisce la validazione della licenza software.
"""

import hashlib
import json
import os
import platform
import subprocess
import uuid
from datetime import date
from enum import Enum
from typing import Tuple

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
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_hardware_id():
    """
    Ottiene un ID hardware univoco per la macchina.
    """
    if platform.system() == "Windows":
        return _get_windows_hardware_id()
    elif platform.system() == "Linux":
        return _get_linux_hardware_id()

    # Fallback universale: UUID basato su MAC address
    try:
        return str(uuid.getnode())
    except Exception:
        return "ERROR_GETTING_ID"

def _get_windows_hardware_id():
    """Helper to get hardware ID on Windows."""
    # 1. Try WMIC (Legacy)
    try:
        cmd = ["wmic", "diskdrive", "get", "serialnumber"]
        output = subprocess.check_output(
            cmd, shell=False, stderr=subprocess.DEVNULL
        ).decode()
        parts = output.strip().split("\n")
        if len(parts) > 1:
            serial = parts[1].strip()
            if serial:
                return serial
    except Exception:
        pass

    # 2. Try PowerShell (Disk Serial)
    try:
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-CimInstance -Class Win32_DiskDrive | "
            "Select-Object -ExpandProperty SerialNumber",
        ]
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        output = (
            subprocess.check_output(
                cmd, startupinfo=startupinfo, stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )

        if output:
            return output.splitlines()[0].strip()
    except Exception:
        pass

    # 3. Try PowerShell (System UUID)
    try:
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-CimInstance -Class Win32_ComputerSystemProduct | "
            "Select-Object -ExpandProperty UUID",
        ]
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        output = (
            subprocess.check_output(
                cmd, startupinfo=startupinfo, stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )

        if output:
            return output
    except Exception:
        pass
    return None

def _get_linux_hardware_id():
    """Helper to get hardware ID on Linux."""
    # Try lsblk
    try:
        # Avoid complex pipes with shell=True, execute basic lsblk and parse in python
        cmd = ["lsblk", "--nodeps", "-o", "serial", "-n"]
        output = (
            subprocess.check_output(cmd, shell=False, stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )

        # Take the first line if multiple disks
        first_line = output.split("\n")[0].strip()

        if first_line:
            return first_line
    except Exception:
        pass

    # Fallback to machine-id
    if os.path.exists("/etc/machine-id"):
        try:
            with open("/etc/machine-id", "r") as f:
                return f.read().strip()
        except Exception:
            pass
    return None


def _get_license_paths():
    """Restituisce i percorsi dei file di licenza."""
    from src.core import config_manager

    # Use standard data path via config_manager.get_data_path()
    # This ensures alignment with where data (and license) are expected
    base_data_dir = config_manager.get_data_path()

    license_dir = os.path.join(base_data_dir, "Licenza")
    return {
        "dir": license_dir,
        "config": os.path.join(license_dir, "config.dat"),
        "manifest": os.path.join(license_dir, "manifest.json"),
    }


def get_license_info():
    """
    Ottiene le informazioni della licenza decifrate.

    Returns:
        dict: Dati della licenza o None in caso di errore
    """
    paths = _get_license_paths()
    config_path = paths["config"]

    if not os.path.exists(config_path):
        return None

    try:
        with open(config_path, "rb") as f:
            encrypted_data = f.read()

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
    if not os.path.exists(paths["dir"]):
        try:
            os.makedirs(paths["dir"])
        except OSError:
            return LicenseStatus.ERROR, "Impossibile creare cartella 'Licenza'"

    # Controllo file
    if not os.path.exists(paths["config"]) or not os.path.exists(paths["manifest"]):
        return LicenseStatus.MISSING, "File di licenza mancanti"

    # 1. Verifica integrità tramite manifest
    integrity_status, integrity_msg = _check_integrity_with_manifest(paths)
    if integrity_status != LicenseStatus.VALID:
        return integrity_status, integrity_msg

    # 2. Decifra e valida i dati
    validation_status, validation_msg = _validate_license_data(paths)
    return validation_status, validation_msg


def _check_integrity_with_manifest(paths: dict) -> Tuple[LicenseStatus, str]:
    """Helper to check license file integrity using manifest."""
    try:
        with open(paths["manifest"], "r") as f:
            manifest = json.load(f)

        # Verifica hash config.dat
        if _calculate_sha256(paths["config"]) != manifest.get("config.dat"):
            msg = "Integrità licenza compromessa (config.dat)"
            AuditManager().log_action(
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

def _validate_license_data(paths: dict) -> Tuple[LicenseStatus, str]:
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
            AuditManager().log_action(
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
