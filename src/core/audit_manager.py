"""
SyncroJob - Audit Manager PRO
Gestione avanzata e immutabile del log delle attività.
"""

import hashlib
import json
import logging
import os
import sqlite3
import time
import traceback
from contextlib import suppress
from datetime import datetime, timedelta
from enum import Enum
from types import TracebackType
from typing import Any, Dict, List, Optional, Type

from src.core.config_manager import CONFIG_DIR

logger = logging.getLogger(__name__)


class AuditSignals:
    """Singleton per i segnali di AuditManager (compatibile con PyQt6)."""

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            from PyQt6.QtCore import QObject, pyqtSignal

            class _Signals(QObject):
                log_added = pyqtSignal(dict)
                logs_updated = pyqtSignal()

            cls._instance = _Signals()
        return cls._instance


class AuditTimer:
    """
    Context Manager per misurare la durata delle operazioni e
    catturare automaticamente eccezioni per l'audit log.
    """

    def __init__(
        self,
        action: str,
        category: str = "general",
        entity: str = "",
        module: str = "",
        notify: bool = False,
    ):
        self.action = action
        self.category = category
        self.entity = entity
        self.module = module
        self.notify = notify
        self.start_time = 0.0
        self.audit_manager = AuditManager.instance()

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        duration_ms = int((time.time() - self.start_time) * 1000)
        status = AuditManager.Status.SUCCESS
        severity = AuditManager.Severity.LOW
        error_code = None
        params = {"duration_str": f"{duration_ms}ms"}

        if exc_type:
            status = AuditManager.Status.ERROR
            severity = AuditManager.Severity.HIGH
            error_code = exc_type.__name__
            params["error_details"] = str(exc_val)
            params["traceback"] = "".join(traceback.format_tb(exc_tb))

        self.audit_manager.log_action(
            action=self.action,
            category=self.category,
            entity=self.entity,
            params=params,
            status=status,
            severity=severity,
            duration_ms=duration_ms,
            module=self.module,
            error_code=error_code,
            notify=self.notify,
        )
        # Non sopprimiamo l'eccezione, la lasciamo propagare
        return False


class AuditManager:
    """
    Manager per l'Audit Log con meccanismi di integrità e severità.
    """

    _instance = None
    DB_PATH = CONFIG_DIR / "data" / "audit_log.db"
    _SALT = "SyncroJob_Secure_Audit_2026"

    class Severity(Enum):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    class Status(Enum):
        SUCCESS = "success"
        ERROR = "error"
        WARNING = "warning"

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
        self._init_db()
        self.signals = AuditSignals.instance()
        self._initialized = True

    def _init_db(self):
        """Inizializza il database e migra lo schema se necessario."""
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.DB_PATH) as conn:
            # Creazione Tabella Base
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    category TEXT,
                    entity TEXT,
                    params TEXT,
                    status TEXT DEFAULT 'success',
                    severity TEXT DEFAULT 'low',
                    row_hash TEXT,
                    duration_ms INTEGER DEFAULT 0,
                    module TEXT DEFAULT '',
                    error_code TEXT DEFAULT ''
                )
            """
            )

            # --- MIGRAZIONE AUTOMATICA ---
            # Verifica colonne esistenti
            cursor = conn.execute("PRAGMA table_info(audit_logs)")
            existing_cols = {row[1] for row in cursor.fetchall()}

            # Colonne da aggiungere se mancano
            new_columns = {
                "duration_ms": "INTEGER DEFAULT 0",
                "module": "TEXT DEFAULT ''",
                "error_code": "TEXT DEFAULT ''",
                "user_id": "TEXT",  # Legacy checks
                "entity": "TEXT",
                "params": "TEXT",
                "severity": "TEXT DEFAULT 'low'",
                "row_hash": "TEXT",
            }

            for col_name, col_def in new_columns.items():
                if col_name not in existing_cols:
                    with suppress(sqlite3.OperationalError):
                        print(f"[AUDIT] Migrazione: Aggiunta colonna {col_name}...")
                        conn.execute(
                            f"ALTER TABLE audit_logs ADD COLUMN {col_name} {col_def}"
                        )

            # Indici
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)"
            )
            conn.commit()

    def _get_current_user(self) -> str:
        """Recupera l'utente corrente."""
        for env_var in ("USERNAME", "USER"):
            user = os.environ.get(env_var)
            if user and user.lower() != "none":
                return user
        with suppress(Exception):
            import getpass

            return getpass.getuser()
        return "unknown"

    def _calculate_hash(self, data_str: str, prev_hash: str) -> str:
        """Calcola l'hash SHA-256 concatenato."""
        payload = f"{data_str}|{prev_hash}|{self._SALT}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def _get_last_hash(self) -> str:
        try:
            with sqlite3.connect(self.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT row_hash FROM audit_logs ORDER BY id DESC LIMIT 1"
                )
                row = cursor.fetchone()
                return row[0] if row and row[0] else "0" * 64
        except Exception:
            return "0" * 64

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
    ):
        """
        Registra un'azione dettagliata nell'audit log.
        """
        try:
            user_id = self._get_current_user()

            # Normalizzazione
            status_val = (
                status.value if isinstance(status, self.Status) else str(status)
            )
            severity_val = (
                severity.value if isinstance(severity, self.Severity) else str(severity)
            )

            # Defaults
            entity = entity or "-"
            category = category or "general"
            module = module or ""
            error_code = error_code or ""
            params_json = json.dumps(params, ensure_ascii=False) if params else "{}"
            timestamp = datetime.now().isoformat()

            prev_hash = self._get_last_hash()

            # Hash payload esteso
            data_to_hash = f"{timestamp}|{user_id}|{action}|{category}|{entity}|{params_json}|{status_val}|{severity_val}|{duration_ms}|{module}|{error_code}"
            current_hash = self._calculate_hash(data_to_hash, prev_hash)

            with sqlite3.connect(self.DB_PATH) as conn:
                conn.execute(
                    """INSERT INTO audit_logs
                       (timestamp, user_id, action, category, entity, params, status, severity,
                        duration_ms, module, error_code, row_hash)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
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
                    ),
                )
                conn.commit()

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

        except Exception as e:
            logger.error(f"Audit Log Error: {e}")
            traceback.print_exc()

    def _generate_notification(self, action, entity, status_val, severity_val, params):
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

    def verify_integrity(self) -> bool:
        """Verifica la catena di hash."""
        try:
            with sqlite3.connect(self.DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT * FROM audit_logs ORDER BY id ASC"
                ).fetchall()

                prev_hash = "0" * 64
                for row in rows:
                    if not row["row_hash"]:
                        continue

                    # NOTA: Per i record vecchi (migrati), i campi nuovi saranno DEFAULT (0 o "").
                    # Se l'hash originale non li includeva, questo controllo fallirà per i vecchi record.
                    # Questo è inevitabile in una migrazione sicura a meno di ricalcolare gli hash (che è illegale per l'audit).
                    # Accettiamo che i log pre-migrazione possano fallire la verifica in questa versione V2.

                    # Costruiamo stringa hash V2
                    # Se il DB ha colonne aggiunte con default, sqlite le restituisce.
                    data = f"{row['timestamp']}|{row['user_id']}|{row['action']}|{row['category']}|{row['entity']}|{row['params']}|{row['status']}|{row['severity']}|{row['duration_ms']}|{row['module']}|{row['error_code']}"

                    # Tentativo 1: Hash V2
                    calc_hash = self._calculate_hash(data, prev_hash)

                    if row["row_hash"] != calc_hash:
                        # Tentativo 2: Hash Legacy (senza nuovi campi) per retrocompatibilità
                        data_legacy = f"{row['timestamp']}|{row['user_id']}|{row['action']}|{row['category']}|{row['entity']}|{row['params']}|{row['status']}|{row['severity']}"
                        calc_hash_legacy = self._calculate_hash(data_legacy, prev_hash)

                        if row["row_hash"] != calc_hash_legacy:
                            return False  # Hash non valido né V2 né Legacy

                    prev_hash = row["row_hash"]
                return True
        except Exception:
            return False

    def get_logs(self, limit: int = 200) -> List[Dict[str, Any]]:
        """Recupera i log recenti (Compatibilità Legacy)."""
        logs, _ = self.get_filtered_logs(limit=limit)
        return logs

    def get_filtered_logs(
        self,
        start_date=None,
        end_date=None,
        levels=None,
        category=None,
        search_text=None,
        limit=50,
        offset=0,
    ):
        logs = []
        total = 0
        try:
            query = "SELECT * FROM audit_logs WHERE 1=1"
            c_query = "SELECT COUNT(*) FROM audit_logs WHERE 1=1"
            params = []

            if start_date:
                query += " AND timestamp >= ?"
                c_query += " AND timestamp >= ?"
                params.append(start_date.isoformat())
            if end_date:
                e_date = end_date + timedelta(days=1)
                query += " AND timestamp < ?"
                c_query += " AND timestamp < ?"
                params.append(e_date.isoformat())
            if levels and "ALL" not in levels:
                pl = ",".join(["?"] * len(levels))
                query += f" AND severity IN ({pl})"
                c_query += f" AND severity IN ({pl})"
                params.extend(levels)
            if category and category != "Tutte":
                query += " AND category = ?"
                c_query += " AND category = ?"
                params.append(category)
            if search_text:
                sp = f"%{search_text}%"
                clause = " AND (action LIKE ? OR entity LIKE ? OR params LIKE ? OR error_code LIKE ? OR module LIKE ?)"
                query += clause
                c_query += clause
                params.extend([sp] * 5)

            with sqlite3.connect(self.DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                total = cur.execute(c_query, params).fetchone()[0]

                query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
                params.extend([limit, offset])

                cur.execute(query, params)
                logs = [dict(r) for r in cur.fetchall()]

        except Exception as e:
            logger.error(f"Filter Error: {e}")

        return logs, total

    def get_categories(self):
        try:
            with sqlite3.connect(self.DB_PATH) as conn:
                res = conn.execute(
                    "SELECT DISTINCT category FROM audit_logs ORDER BY category"
                )
                return [r[0] for r in res if r[0]]
        except Exception:
            return []

    def run_retention_policy(self, days=90):
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        try:
            with sqlite3.connect(self.DB_PATH) as conn:
                res = conn.execute(
                    "DELETE FROM audit_logs WHERE timestamp < ?", (cutoff,)
                )
                deleted_count = res.rowcount

            if deleted_count > 0:
                self.log_action(
                    "Pulizia Log",
                    category="Sistema",
                    params={"deleted_rows": deleted_count, "cutoff_date": cutoff},
                    severity="low",
                )
        except Exception as e:
            logger.error(f"Retention Policy Error: {e}")

    def get_stats_by_day(self, days=30) -> Dict[str, Dict[str, int]]:
        """
        Restituisce statistiche aggregate per giorno.
        Return format: {'2023-10-01': {'success': 10, 'error': 2, 'warning': 1}, ...}
        """
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        stats = {}

        # Pre-fill dates
        for i in range(days + 1):
            d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            stats[d] = {"success": 0, "error": 0, "warning": 0}

        try:
            with sqlite3.connect(self.DB_PATH) as conn:
                # SQLite 'date' function extracts YYYY-MM-DD from ISO string
                query = """
                    SELECT date(timestamp), status, count(*)
                    FROM audit_logs
                    WHERE timestamp >= ?
                    GROUP BY date(timestamp), status
                """
                rows = conn.execute(query, (cutoff,)).fetchall()

                for r in rows:
                    day = r[0]
                    status = r[1]
                    count = r[2]

                    if day in stats:
                        # Normalize status
                        s_key = status.lower()
                        if s_key not in stats[day]:
                            stats[day][s_key] = 0
                        stats[day][s_key] += count

        except Exception as e:
            logger.error(f"Stats Error: {e}")

        # Filter out empty future dates if any and sort
        return dict(sorted(stats.items()))
