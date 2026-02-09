import hashlib
import logging
from typing import Any

logger = logging.getLogger(__name__)


class AuditIntegrity:
    """Gestisce il calcolo degli hash e la verifica dell'integrità dei log."""

    _SALT = "SyncroJob_Secure_Audit_2026"

    @classmethod
    def calculate_hash(cls, data_str: str, prev_hash: str) -> str:
        """Calcola l'hash SHA-256 concatenato."""
        payload = f"{data_str}|{prev_hash}|{cls._SALT}"
        return hashlib.sha256(payload.encode()).hexdigest()

    @classmethod
    def build_hash_string_v2(cls, row: dict[str, Any]) -> str:
        """Costruisce la stringa di input per l'hash V2 (include tutti i campi)."""
        return f"{row['timestamp']}|{row['user_id']}|{row['action']}|{row['category']}|{row['entity']}|{row['params']}|{row['status']}|{row['severity']}|{row['duration_ms']}|{row['module']}|{row['error_code']}"

    @classmethod
    def build_hash_string_legacy(cls, row: dict[str, Any]) -> str:
        """Costruisce la stringa di input per l'hash Legacy."""
        return f"{row['timestamp']}|{row['user_id']}|{row['action']}|{row['category']}|{row['entity']}|{row['params']}|{row['status']}|{row['severity']}"
