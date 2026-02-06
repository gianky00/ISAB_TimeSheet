import json
import os
import traceback
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from src.core.audit.database import AuditDatabase
from src.core.audit.integrity import AuditIntegrity
from src.core.audit.models import Severity, Status
from src.core.audit.signals import AuditSignals
from src.core.logging import get_context, get_logger

logger = get_logger(__name__)


class AuditManager:
    """
    Manager per l'Audit Log con meccanismi di integrità e severità.
    Implementazione rifattorizzata e modulare.
    """

    _instance = None
    Severity = Severity
    Status = Status

    @classmethod
    def instance(cls):
        return cls()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.db = AuditDatabase()
        self.signals = AuditSignals.instance()
        self._initialized = True

    @property
    def DB_PATH(self):
        """Compatibilità Legacy per test."""
        return self.db.DB_PATH

    @DB_PATH.setter
    def DB_PATH(self, value):
        self.db.DB_PATH = value

    def _get_current_user(self) -> str:
        """Recupera l'utente corrente."""
        for env_var in ("USERNAME", "USER"):
            user = os.environ.get(env_var)
            if user and user.lower() != "none":
                return user
        try:
            import getpass

            return getpass.getuser()
        except Exception:
            return "unknown"

    def log_action(
        self,
        action: str,
        category: str = "general",
        entity: str = "",
        params: Any = None,
        status: Any = Status.SUCCESS,
        severity: Any = Severity.LOW,
        duration_ms: int = 0,
        module: str = "",
        error_code: Optional[str] = None,
        notify: bool = False,
        trace_id: Optional[str] = None,
    ) -> Optional[int]:
        """
        Registra un'azione dettagliata nell'audit log.

        Args:
            action: Descrizione dell'azione
            category: Categoria (es. "bot", "sistema", "utente")
            entity: Entità coinvolta (es. nome file, cantiere)
            params: Parametri addizionali (dict convertito a JSON)
            status: Status esito (SUCCESS, ERROR, WARNING)
            severity: Gravità (LOW, MEDIUM, HIGH)
            duration_ms: Durata operazione in millisecondi
            module: Nome modulo/bot
            error_code: Codice errore opzionale
            notify: Se True, genera notifica utente
            trace_id: ID trace dal logging system (auto-recuperato se non fornito)

        Returns:
            audit_id: ID della riga inserita, o None in caso di errore
        """
        try:
            user_id = self._get_current_user()

            # Auto-recupera trace_id dal context se non fornito
            if trace_id is None:
                trace_id = get_context().get("trace_id")

            # Normalizzazione
            status_val = status.value if isinstance(status, Status) else str(status)
            severity_val = (
                severity.value if isinstance(severity, Severity) else str(severity)
            )

            # Defaults
            entity = entity or "-"
            category = category or "general"
            error_code = error_code or ""
            params_json = json.dumps(params, ensure_ascii=False) if params else "{}"
            timestamp = datetime.now().isoformat()

            prev_hash = self.db.get_last_hash()

            # Hash payload esteso
            data_to_hash = f"{timestamp}|{user_id}|{action}|{category}|{entity}|{params_json}|{status_val}|{severity_val}|{duration_ms}|{module}|{error_code}"
            current_hash = AuditIntegrity.calculate_hash(data_to_hash, prev_hash)

            audit_id = self.db.insert_log(
                (
                    timestamp,
                    user_id,
                    action,
                    category,
                    entity,
                    params_json,
                    status_val,
                    severity_val,
                    duration_ms,
                    module,
                    error_code,
                    current_hash,
                )
            )

            # Log strutturato correlato all'audit entry
            log_level = "error" if status_val == "error" else "info"
            getattr(logger, log_level)(
                f"Audit: {action}",
                audit_id=audit_id,
                trace_id=trace_id,
                category=category,
                entity=entity,
                status=status_val,
                severity=severity_val,
                duration_ms=duration_ms,
            )

            # Segnali
            log_entry = {
                "timestamp": timestamp,
                "user_id": user_id,
                "action": action,
                "category": category,
                "entity": entity,
                "params": params_json,
                "status": status_val,
                "severity": severity_val,
                "duration_ms": duration_ms,
                "module": module,
                "error_code": error_code,
            }
            self.signals.log_added.emit(log_entry)
            self.signals.logs_updated.emit()

            if notify:
                self._generate_notification(
                    action, entity, status_val, severity_val, params
                )

            return audit_id

        except Exception as e:
            logger.error("Audit Log Error", exc=e, action=action, category=category)
            traceback.print_exc()
            return None

    def _generate_notification(
        self, action: str, entity: str, status_val: str, severity_val: str, params: Any
    ):
        """Genera una notifica utente basata sull'esito dell'azione auditata."""
        try:
            from src.core.notification_manager import NotificationManager

            level = "info"
            if status_val == "error" or severity_val == "high":
                level = "error"
            elif status_val == "warning" or severity_val == "medium":
                level = "warning"
            elif status_val == "success":
                level = "success"

            msg = f"Esito: {status_val.upper()}"
            if params and isinstance(params, dict) and "error_details" in params:
                msg = params["error_details"]

            NotificationManager.instance().add_notification(
                f"{action}: {entity}", msg, level=level
            )
        except Exception as e:
            logger.error(f"Notification error in Audit: {e}")

    def verify_integrity(self) -> bool:
        """Verifica la catena di hash."""
        try:
            import sqlite3

            with self.db.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT * FROM audit_logs ORDER BY id ASC"
                ).fetchall()

                prev_hash = "0" * 64
                for row in rows:
                    if not row["row_hash"]:
                        continue

                    # Tentativo 1: Hash V2
                    data = AuditIntegrity.build_hash_string_v2(row)
                    calc_hash = AuditIntegrity.calculate_hash(data, prev_hash)

                    if row["row_hash"] != calc_hash:
                        # Tentativo 2: Hash Legacy
                        data_legacy = AuditIntegrity.build_hash_string_legacy(row)
                        calc_hash_legacy = AuditIntegrity.calculate_hash(
                            data_legacy, prev_hash
                        )

                        if row["row_hash"] != calc_hash_legacy:
                            return False

                    prev_hash = row["row_hash"]
                return True
        except Exception:
            return False

    def get_logs(self, limit: int = 200) -> List[Dict[str, Any]]:
        logs, _ = self.get_filtered_logs(limit=limit)
        return logs

    def get_filtered_logs(self, **kwargs) -> Tuple[List[Dict[str, Any]], int]:
        return self.db.fetch_filtered(**kwargs)

    def get_categories(self) -> List[str]:
        return self.db.get_categories()

    def run_retention_policy(self, days: int = 90):
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        deleted_count = self.db.delete_older_than(cutoff)
        if deleted_count > 0:
            self.log_action(
                "Pulizia Log",
                category="Sistema",
                params={"deleted_rows": deleted_count, "cutoff_date": cutoff},
                severity=Severity.LOW,
            )

    def get_stats_by_day(self, days=30) -> Dict[str, Dict[str, int]]:
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        stats = {
            (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"): {
                "success": 0,
                "error": 0,
                "warning": 0,
            }
            for i in range(days + 1)
        }

        try:
            with self.db.get_connection() as conn:
                query = """
                    SELECT date(timestamp), status, count(*)
                    FROM audit_logs
                    WHERE timestamp >= ?
                    GROUP BY date(timestamp), status
                """
                rows = conn.execute(query, (cutoff,)).fetchall()
                for r in rows:
                    day, status, count = r
                    if day in stats:
                        s_key = status.lower()
                        if s_key not in stats[day]:
                            stats[day][s_key] = 0
                        stats[day][s_key] += count
        except Exception as e:
            logger.error(f"Stats Error: {e}")
        return dict(sorted(stats.items()))
