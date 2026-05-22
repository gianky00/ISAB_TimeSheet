"""Modulo Manager."""

import getpass
import json
import os
import queue
import sqlite3
import threading
import time
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Optional

from src.core.audit.database import AuditDatabase
from src.core.audit.integrity import AuditIntegrity
from src.core.audit.models import Severity, Status
from src.core.audit.signals import AuditSignals
from src.core.logging import get_context, get_logger
from src.core.notification_manager import NotificationManager

logger = get_logger(__name__)


class AuditManager:
    """Manager per l'Audit Log con meccanismi di integrità e severità.

    Implementazione rifattorizzata e modulare con supporto asincrono per evitare lag UI.

    Inizializza i componenti interni del manager (DB, Segnali, Worker).
    """

    _instance: Optional["AuditManager"] = None
    Severity = Severity
    Status = Status

    @classmethod
    def instance(cls) -> "AuditManager":
        """Restituisce l'istanza singleton della classe, creandola se necessario."""
        return cls()

    def __new__(cls) -> "AuditManager":
        """Gestisce la creazione dell'unica istanza (Singleton)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        self.db = AuditDatabase()
        self.signals = AuditSignals.instance()

        # Meccanismo Asincrono
        self._log_queue: queue.Queue[dict[str, Any] | None] = queue.Queue()
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

        self._initialized = True

    def _worker_loop(self) -> None:
        """Loop infinito del thread di background per processare i log."""
        while True:
            try:
                task = self._log_queue.get()
                if task is None:  # Sentinel
                    break

                self._execute_log_internal(**task)
                self._log_queue.task_done()
            except Exception:
                logger.exception("Audit Worker Error")
                time.sleep(1)  # Evita busy loop in caso di errore persistente

    @property
    def DB_PATH(self) -> Path:  # noqa: N802
        """Alias per compatibilità test."""
        return self.db.db_path

    @property
    def db_path(self) -> Path:
        """Compatibilità Legacy per test."""
        return self.db.db_path

    @db_path.setter
    def db_path(self, value: Path) -> None:
        self.db.db_path = value

    def _get_current_user(self) -> str:
        """Recupera l'utente corrente."""
        for env_var in ("USERNAME", "USER"):
            user = os.environ.get(env_var)
            if user and user.lower() != "none":
                return user
        try:
            return getpass.getuser()
        except Exception:
            return "unknown"

    def log_action(  # noqa: PLR0913
        self,
        action: str,
        category: str = "general",
        entity: str = "",
        params: Any = None,
        status: Any = Status.SUCCESS,
        severity: Any = Severity.LOW,
        duration_ms: int = 0,
        module: str = "",
        error_code: str | None = None,
        notify: bool = False,
        trace_id: str | None = None,
    ) -> None:
        """Inoda un'azione dettagliata nell'audit log (Asincrono)."""
        # Auto-recupera trace_id dal context SE siamo nel thread principale
        if trace_id is None:
            with suppress(Exception):
                trace_id = get_context().get("trace_id")

        task = {
            "action": action,
            "category": category,
            "entity": entity,
            "params": params,
            "status": status,
            "severity": severity,
            "duration_ms": duration_ms,
            "module": module,
            "error_code": error_code,
            "notify": notify,
            "trace_id": trace_id,
        }
        self._log_queue.put(task)

    def _execute_log_internal(  # noqa: PLR0913
        self,
        action: str,
        category: str,
        entity: str,
        params: Any,
        status: Any,
        severity: Any,
        duration_ms: int,
        module: str,
        error_code: str | None,
        notify: bool,
        trace_id: str | None,
    ) -> int | None:
        """Esecuzione effettiva della scrittura su DB (eseguita nel Worker Thread)."""
        try:
            # 1. Normalizzazione e Setup
            user_id = self._get_current_user()

            # Conversione sicura per compatibilità DB (stringhe: low, medium, high / success, error, warning)
            status_val = status.to_str() if isinstance(status, Status) else str(status)
            severity_val = severity.to_str() if isinstance(severity, Severity) else str(severity)

            # Defaults
            entity = entity or "-"
            category = category or "general"
            error_code = error_code or ""
            params_json = json.dumps(params, ensure_ascii=False) if params else "{}"
            timestamp = datetime.now(UTC).isoformat()

            # 2. Integrità(Hashing)
            row_data = {
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
            prev_hash = self.db.get_last_hash()
            data_to_hash = AuditIntegrity.build_hash_string_v2(row_data)
            current_hash = AuditIntegrity.calculate_hash(data_to_hash, prev_hash)

            # 3. Persistenza
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

            # 4. Logging Strutturato e Segnali
            self._log_structured_audit(
                action, audit_id, trace_id, category, entity, status_val, severity_val, duration_ms
            )

            row_data["id"] = audit_id  # Per compatibilità segnali
            self.signals.log_added.emit(row_data)
            self.signals.logs_updated.emit()

            if notify:
                self._generate_notification(action, entity, status_val, severity_val, params)

        except Exception as e:
            logger.exception("Audit Log Error", exc=e, action=action, category=category)
            return None
        else:
            return audit_id

    def _log_structured_audit(  # noqa: PLR0913
        self,
        action: str,
        audit_id: Any,
        trace_id: Any,
        category: str,
        entity: str,
        status: str,
        severity: str,
        duration: int,
    ) -> None:
        """Emette il log strutturato dell'audit."""
        log_level = "error" if status == "error" else "info"
        getattr(logger, log_level)(
            f"Audit: {action}",
            audit_id=audit_id,
            trace_id=trace_id,
            category=category,
            entity=entity,
            status=status,
            severity=severity,
            duration_ms=duration,
        )

    def _generate_notification(
        self,
        action: str,
        entity: str,
        status_val: str,
        severity_val: str,
        params: Any,
    ) -> None:
        """Genera una notifica utente basata sull'esito dell'azione auditata."""
        try:
            level = self._map_status_to_notif_level(status_val, severity_val)
            msg = f"Esito: {status_val.upper()}"
            if params and isinstance(params, dict) and "error_details" in params:
                msg = params["error_details"]

            NotificationManager.instance().add_notification(f"{action}: {entity}", msg, level=level)
        except Exception:
            logger.exception("Notification error in Audit")

    def _map_status_to_notif_level(self, status: str, severity: str) -> str:
        """Mappa stato e severità al livello di notifica."""
        if status == "error" or severity == "high":
            return "error"
        if status == "warning" or severity == "medium":
            return "warning"
        if status == "success":
            return "success"
        return "info"

    def verify_integrity(self) -> bool:
        """Verifica la catena di hash dell'intero database."""
        try:
            with self.db.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                rows = [dict(r) for r in conn.execute("SELECT * FROM audit_logs ORDER BY id ASC").fetchall()]

            prev_hash = "0" * 64
            for i, row in enumerate(rows):
                if i % 1000 == 0:
                    time.sleep(0.005)  # Yield

                if not row["row_hash"]:
                    continue

                if not self._check_row_integrity(row, prev_hash):
                    logger.error(f"Integrity check failed at ID {row['id']}")
                    return False

                prev_hash = row["row_hash"]
        except Exception:
            logger.exception("Integrity verification crash")
            return False
        else:
            return True

    def _check_row_integrity(self, row: dict[str, Any], prev_hash: str) -> bool:
        """Verifica la validità dell'hash di una singola riga (supporta versioni multiple)."""
        # Tentativo 1: Hash V2
        data = AuditIntegrity.build_hash_string_v2(row)
        if row["row_hash"] == AuditIntegrity.calculate_hash(data, prev_hash):
            return True

        # Tentativo 2: Hash Legacy
        data_legacy = AuditIntegrity.build_hash_string_legacy(row)
        if row["row_hash"] == AuditIntegrity.calculate_hash(data_legacy, prev_hash):
            return True

        # Tentativo 3: Hash V2 Legacy (None -> "None")
        keys = (
            "timestamp",
            "user_id",
            "action",
            "category",
            "entity",
            "params",
            "status",
            "severity",
            "duration_ms",
            "module",
            "error_code",
        )
        data_v2_old = "|".join([str(row[k]) for k in keys])
        return bool(row["row_hash"] == AuditIntegrity.calculate_hash(data_v2_old, prev_hash))

    def get_logs(self, limit: int = 200) -> list[dict[str, Any]]:
        """Recupera gli ultimi N log di audit (senza filtri avanzati)."""
        logs, _ = self.get_filtered_logs(limit=limit)
        return logs

    def get_filtered_logs(self, **kwargs: Any) -> tuple[list[dict[str, Any]], int]:
        """Interroga il database dell'audit applicando i filtri specificati."""
        return self.db.fetch_filtered(**kwargs)

    def get_categories(self) -> list[str]:
        """Restituisce l'elenco di tutte le categorie presenti nel log di audit."""
        return self.db.get_categories()

    def run_retention_policy(self, days: int = 90) -> None:
        """Elimina i log più vecchi del numero di giorni specificato."""
        cutoff = (datetime.now(UTC) - timedelta(days=days)).isoformat()
        deleted_count = self.db.delete_older_than(cutoff)
        if deleted_count > 0:
            self.log_action(
                "Pulizia Log",
                category="Sistema",
                params={"deleted_rows": deleted_count, "cutoff_date": cutoff},
                severity=Severity.LOW,
            )

    def get_stats_by_day(self, days: int = 30) -> dict[str, dict[str, int]]:
        """Calcola statistiche giornaliere (successi/errori) per l'intervallo specificato."""
        cutoff = (datetime.now(UTC) - timedelta(days=days)).strftime("%Y-%m-%d")
        stats: dict[str, dict[str, int]] = {
            (datetime.now(UTC) - timedelta(days=i)).strftime("%Y-%m-%d"): {
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
        except Exception:
            logger.exception("Stats Error")
        return dict(sorted(stats.items()))
