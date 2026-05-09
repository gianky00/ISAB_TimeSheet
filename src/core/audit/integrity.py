import hashlib
import logging
from typing import Any

logger = logging.getLogger(__name__)


class AuditIntegrity:
    """Gestisce il calcolo degli hash e la verifica dell'integrita' dei log."""

    _SALT = "SyncroJob_Secure_Audit_2026"

    @classmethod
    def _n(cls, val: Any) -> str:
        """Normalizza un valore in stringa, gestendo i None come stringa vuota."""
        if val is None:
            return ""
        return str(val)

    @classmethod
    def calculate_hash(cls, data_str: str, prev_hash: str) -> str:
        """Calcola l'hash SHA-256 concatenato."""
        payload = f"{data_str}|{prev_hash}|{cls._SALT}"
        return hashlib.sha256(payload.encode()).hexdigest()

    @classmethod
    def build_hash_string_v2(cls, row: dict[str, Any]) -> str:
        """Costruisce la stringa di input per l'hash V2 (include tutti i campi)."""
        return (
            f"{cls._n(row['timestamp'])}|{cls._n(row['user_id'])}|{cls._n(row['action'])}|"
            f"{cls._n(row['category'])}|{cls._n(row['entity'])}|{cls._n(row['params'])}|"
            f"{cls._n(row['status'])}|{cls._n(row['severity'])}|{cls._n(row['duration_ms'])}|"
            f"{cls._n(row['module'])}|{cls._n(row['error_code'])}"
        )

    @classmethod
    def build_hash_string_legacy(cls, row: dict[str, Any]) -> str:
        """Costruisce la stringa di input per l'hash Legacy."""
        return (
            f"{cls._n(row['timestamp'])}|{cls._n(row['user_id'])}|{cls._n(row['action'])}|"
            f"{cls._n(row['category'])}|{cls._n(row['entity'])}|{cls._n(row['params'])}|"
            f"{cls._n(row['status'])}|{cls._n(row['severity'])}"
        )
