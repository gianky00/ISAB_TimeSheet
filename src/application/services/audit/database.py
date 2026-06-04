"""Modulo Database."""

import logging
import sqlite3
from contextlib import suppress
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from src.application.services.database import db_manager

logger = logging.getLogger(__name__)


class AuditDatabase:
    """Gestisce il database SQLite per l'Audit Log.

    Inizializza il gestore del database di audit.
    """

    DB_PATH: Path = db_manager.DB_AUDIT
    _db_path_override: Path | None = None

    @property
    def db_path(self) -> Path:
        """Restituisce il percorso dinamico del database Audit."""
        if self._db_path_override is not None:
            return self._db_path_override
        return db_manager.DB_AUDIT

    @db_path.setter
    def db_path(self, value: Path) -> None:
        self._db_path_override = value

    def __init__(self) -> None:
        self._init_db()

    def _init_db(self) -> None:
        """Inizializza il database e migra lo schema se necessario."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
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
                        logger.info(f"[AUDIT DB] Migrazione: Aggiunta colonna {col_name}...")
                        conn.execute(f"ALTER TABLE audit_logs ADD COLUMN {col_name} {col_def}")  # nosec B608

            conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)")
            conn.commit()

    def get_connection(self) -> sqlite3.Connection:
        """Restituisce una nuova connessione al database dell'Audit."""
        return sqlite3.connect(self.db_path)

    def get_last_hash(self) -> str:
        """Recupera l'hash dell'ultima riga inserita per garantire l'integrità della catena."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT row_hash FROM audit_logs ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                return str(row[0]) if row and row[0] else "0" * 64
        except Exception:
            return "0" * 64

    def insert_log(self, data: tuple[Any, ...]) -> int:
        """Inserisce un nuovo record di audit.

        Args:
          data: Tupla contenente i valori per le colonne del log.

        Returns:
          int: ID della riga inserita.
        """
        query = """INSERT INTO audit_logs

          (timestamp, user_id, action, category, entity, params, status, severity,
          duration_ms, module, error_code, row_hash)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, data)
            conn.commit()
            return int(cursor.lastrowid) if cursor.lastrowid is not None else 0

    def fetch_filtered(  # noqa: PLR0913
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        levels: list[str] | None = None,
        category: str | None = None,
        search_text: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], int]:
        """Esegue una ricerca filtrata nei log di audit.

        Args:
          start_date: Data minima.
          end_date: Data massima.
          levels: Lista di severit  filtrate.
          category: Categoria specifica.
          search_text: Testo libero da cercare in più campi.
          limit: Numero massimo di risultati.
          offset: Salto per paginazione.

        Returns:
          tuple: (lista di log come dict, numero totale di match).
        """
        logs: list[dict[str, Any]] = []
        total = 0
        try:
            query = "SELECT * FROM audit_logs WHERE 1=1"
            c_query = "SELECT COUNT(*) FROM audit_logs WHERE 1=1"
            params: list[Any] = []

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
                res_count = cur.execute(c_query, params).fetchone()
                total = res_count[0] if res_count else 0

                query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
                params.extend([limit, offset])

                cur.execute(query, params)
                logs = [dict(r) for r in cur.fetchall()]
        except Exception:
            logger.exception("Audit DB Fetch Error")
        return logs, total

    def get_categories(self) -> list[str]:
        """Recupera la lista di tutte le categorie distinte presenti nei log."""
        try:
            with self.get_connection() as conn:
                res = conn.execute("SELECT DISTINCT category FROM audit_logs ORDER BY category")
                return [str(r[0]) for r in res if r[0]]
        except Exception:
            return []

    def delete_older_than(self, cutoff_iso: str) -> int:
        """Elimina i log più vecchi della data specificata.

        Args:
          cutoff_iso: Data limite in formato ISO.

        Returns:
          int: Numero di righe eliminate.
        """
        try:
            with self.get_connection() as conn:
                res = conn.execute("DELETE FROM audit_logs WHERE timestamp < ?", (cutoff_iso,))
                return int(res.rowcount)
        except Exception:
            logger.exception("Audit DB Retention Error")
            return 0
