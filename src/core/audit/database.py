import logging
import sqlite3
from contextlib import suppress
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from src.core.config_manager import CONFIG_DIR

logger = logging.getLogger(__name__)


class AuditDatabase:
    """Gestisce il database SQLite per l'Audit Log."""

    DB_PATH = CONFIG_DIR / "data" / "audit_log.db"

    def __init__(self):
        self._init_db()

    def _init_db(self):
        """Inizializza il database e migra lo schema se necessario."""
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.DB_PATH) as conn:
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
            cursor = conn.execute("PRAGMA table_info(audit_logs)")
            existing_cols = {row[1] for row in cursor.fetchall()}

            new_columns = {
                "duration_ms": "INTEGER DEFAULT 0",
                "module": "TEXT DEFAULT ''",
                "error_code": "TEXT DEFAULT ''",
                "user_id": "TEXT",
                "entity": "TEXT",
                "params": "TEXT",
                "severity": "TEXT DEFAULT 'low'",
                "row_hash": "TEXT",
            }

            for col_name, col_def in new_columns.items():
                if col_name not in existing_cols:
                    with suppress(sqlite3.OperationalError):
                        logger.info(
                            f"[AUDIT DB] Migrazione: Aggiunta colonna {col_name}..."
                        )
                        conn.execute(
                            f"ALTER TABLE audit_logs ADD COLUMN {col_name} {col_def}"
                        )

            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)"
            )
            conn.commit()

    def get_connection(self):
        return sqlite3.connect(self.DB_PATH)

    def get_last_hash(self) -> str:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT row_hash FROM audit_logs ORDER BY id DESC LIMIT 1"
                )
                row = cursor.fetchone()
                return row[0] if row and row[0] else "0" * 64
        except Exception:
            return "0" * 64

    def insert_log(self, data: tuple):
        query = """INSERT INTO audit_logs
                   (timestamp, user_id, action, category, entity, params, status, severity,
                    duration_ms, module, error_code, row_hash)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        with self.get_connection() as conn:
            conn.execute(query, data)
            conn.commit()

    def fetch_filtered(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        levels: Optional[List[str]] = None,
        category: Optional[str] = None,
        search_text: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[Dict[str, Any]], int]:
        logs = []
        total = 0
        try:
            query = "SELECT * FROM audit_logs WHERE 1=1"
            c_query = "SELECT COUNT(*) FROM audit_logs WHERE 1=1"
            params: List[Any] = []

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

            with self.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                total = cur.execute(c_query, params).fetchone()[0]

                query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
                params.extend([limit, offset])

                cur.execute(query, params)
                logs = [dict(r) for r in cur.fetchall()]
        except Exception as e:
            logger.error(f"Audit DB Fetch Error: {e}")
        return logs, total

    def get_categories(self) -> List[str]:
        try:
            with self.get_connection() as conn:
                res = conn.execute(
                    "SELECT DISTINCT category FROM audit_logs ORDER BY category"
                )
                return [r[0] for r in res if r[0]]
        except Exception:
            return []

    def delete_older_than(self, cutoff_iso: str) -> int:
        try:
            with self.get_connection() as conn:
                res = conn.execute(
                    "DELETE FROM audit_logs WHERE timestamp < ?", (cutoff_iso,)
                )
                return res.rowcount
        except Exception as e:
            logger.error(f"Audit DB Retention Error: {e}")
            return 0
