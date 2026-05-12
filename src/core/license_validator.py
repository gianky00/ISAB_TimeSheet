"""
SyncroJob - License Validator
Modulo core per la validazione della licenza e dell'integrità del software.
Gestisce l'estrazione dell'Hardware ID (HWID), la decifratura asimmetrica dei certificati (.dat)
e la verifica delle scadenze temporali tramite Trusted Time (Network Time).
"""

import hashlib
import json
import os
import shutil
import sys
from contextlib import suppress
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet

from src.core.audit_manager import AuditManager
from src.core.license_hwid import get_hardware_id
from src.core.logging import get_logger
from src.core.paths import CONFIG_DIR as PATHS_CONFIG_DIR, get_data_path
from src.core.secrets_manager import SecretsManager
from src.core.time_manager import get_trusted_time

logger = get_logger(__name__)


class LicenseStatus(Enum):
    """Enumerazione degli stati possibili della licenza software."""

    VALID = "Valid"
    MISSING = "Missing"
    INVALID = "Invalid"
    EXPIRED = "Expired"
    ERROR = "Error"
    GRACE = "Grace"


def _calculate_sha256(filepath: str | Path) -> str:
    """Calcola l'hash SHA256 di un file per verifiche di integrità."""
    sha256_hash = hashlib.sha256()
    with Path(filepath).open("rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def _get_license_paths() -> dict[str, Path]:
    """Restituisce la mappatura dei percorsi file per la licenza."""
    base_data_dir = Path(get_data_path())
    license_dir = base_data_dir / "Licenza"
    return {
        "dir": license_dir,
        "config": license_dir / "config.dat",
        "manifest": license_dir / "manifest.json",
    }


def _check_and_migrate_local_license(target_paths: dict[str, Any]) -> bool:
    """Migra file di licenza da posizioni legacy o portable alla directory standard in AppData."""
    if getattr(sys, "frozen", False):
        app_dir = Path(sys.executable).parent
    else:
        app_dir = Path(__file__).parent.parent.parent.resolve()

    local_appdata = Path(os.environ.get("LOCALAPPDATA", ""))
    potential_dirs = [
        app_dir / "Licenza",
        app_dir,
        PATHS_CONFIG_DIR / "Licenza",
    ]

    if local_appdata:
        for old_name in ("BotTS", "Bot TS", "SyncroJob"):
            base_dir = local_appdata / old_name
            base_author = local_appdata / "GiancarloAllegretti" / old_name
            potential_dirs.extend(
                (
                    base_dir / "Licenza",
                    base_dir / "data" / "Licenza",
                    base_author / "Licenza",
                    base_author / "data" / "Licenza",
                )
            )

    for source_dir in potential_dirs:
        if (source_dir / "config.dat").exists() and (source_dir / "manifest.json").exists():
            with suppress(Exception):
                target_paths["dir"].mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_dir / "config.dat", target_paths["config"])
                shutil.copy2(source_dir / "manifest.json", target_paths["manifest"])
                return True
    return False


def get_license_info() -> dict[str, Any] | None:
    """
    Decifra il file config.dat e restituisce i dati strutturati della licenza.

    Returns:
      dict: Metadati licenza (Cliente, Scadenza, HWID) o None se non valida.
    """
    paths = _get_license_paths()
    if not paths["config"].exists():
        _check_and_migrate_local_license(paths)
    if not paths["config"].exists():
        return None

    try:
        encrypted_data = paths["config"].read_bytes()
        key_raw = SecretsManager.get_license_key()
        if not key_raw:
            logger.error("Chiave di licenza non trovata in SecretsManager")
            return None

        cipher = Fernet(key_raw)
        try:
            decrypted = cipher.decrypt(encrypted_data).decode("utf-8")
            return json.loads(decrypted)  # type: ignore[no-any-return]
        except Exception as de:
            logger.exception("Errore decifratura config.dat", exc=de)
            return None
    except Exception:
        logger.exception("Errore caricamento licenza")
        return None


def verify_license() -> tuple[bool, str]:
    """Helper per verificare rapidamente se la licenza  valida (Boolean)."""
    status, msg = get_detailed_license_status()
    return status == LicenseStatus.VALID, msg


def get_detailed_license_status() -> tuple[LicenseStatus, str]:
    """
    Esegue una verifica completa: presenza file, integrità hash, HWID matching e scadenza temporale.

    Returns:
      tuple: (LicenseStatus, messaggio descrittivo).
    """
    paths = _get_license_paths()
    if not paths["dir"].exists():
        try:
            paths["dir"].mkdir(parents=True)
        except OSError:
            return LicenseStatus.ERROR, "Impossibile creare cartella 'Licenzà"

    if not (paths["config"].exists() and paths["manifest"].exists()):
        _check_and_migrate_local_license(paths)
    if not paths["config"].exists() or not paths["manifest"].exists():
        return LicenseStatus.MISSING, "File di licenza mancanti"

    status, msg = _check_integrity_with_manifest(paths)
    if status != LicenseStatus.VALID:
        return status, msg
    return _validate_license_data(paths)


def _check_integrity_with_manifest(paths: dict[str, Any]) -> tuple[LicenseStatus, str]:
    """Verifica che l'hash SHA256 del file config.dat corrisponda a quello dichiarato nel manifest."""
    try:
        manifest = json.loads(Path(paths["manifest"]).read_text(encoding="utf-8"))
        if _calculate_sha256(paths["config"]) != manifest.get("config.dat"):
            AuditManager.instance().log_action(
                "Violazione Licenza", category="sicurezza", status="error", severity="high"
            )
            return LicenseStatus.INVALID, "Integrità licenza compromessa (config.dat)"
    except Exception as e:
        return LicenseStatus.ERROR, f"Errore lettura manifest: {e}"
    return LicenseStatus.VALID, ""


def _validate_license_data(paths: dict[str, Any]) -> tuple[LicenseStatus, str]:
    """Confronta l'HWID e la data di scadenza contenuti nella licenza con quelli della macchina corrente."""
    try:
        payload = get_license_info()
        if not payload:
            return LicenseStatus.INVALID, "Impossibile leggere i dati della licenza"

        cur_hw = get_hardware_id().strip().rstrip(".")
        lic_hw = payload.get("Hardware ID", "").strip().rstrip(".")
        if cur_hw != lic_hw and "UNKNOWN" not in cur_hw:
            AuditManager.instance().log_action(
                "Mismatch Hardware", category="sicurezza", status="error", severity="high"
            )
            return LicenseStatus.INVALID, f"Hardware ID non valido\nAtteso: {lic_hw}\nRilevato: {cur_hw}"

        expiry_str = payload.get("Scadenza Licenza", "")
        if expiry_str:
            try:
                day, month, year = map(int, expiry_str.split("/"))
                trusted_now_dt, _ = get_trusted_time()
                if trusted_now_dt.date() > date(year, month, day):
                    return LicenseStatus.EXPIRED, f"Licenza SCADUTA il {expiry_str}"
            except ValueError:
                return LicenseStatus.INVALID, "Formato data scadenza non valido"

        return LicenseStatus.VALID, f"Licenza valida per: {payload.get('Cliente', 'Utente')}"
    except Exception as e:
        return LicenseStatus.ERROR, f"Errore validazione licenza: {e}"


def get_license_expiry() -> str:
    """Restituisce la data di scadenza come stringa (N/D se non disponibile)."""
    info = get_license_info()
    return info.get("Scadenza Licenza", "N/D") if info else "N/D"


def get_license_client() -> str:
    """Restituisce il nome del cliente assegnatario della licenza."""
    info = get_license_info()
    return info.get("Cliente", "N/D") if info else "N/D"
