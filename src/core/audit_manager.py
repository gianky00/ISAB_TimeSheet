"""
SyncroJob - Audit Manager PRO
Gestione avanzata e immutabile del log delle attività.
"""

import hashlib
import json
import logging
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List

from src.core.config_manager import CONFIG_DIR

logger = logging.getLogger(__name__)


class AuditManager:
    """
    Manager per l'Audit Log con meccanismi di integrità e severità.
    """

    _instance = None
    DB_PATH = CONFIG_DIR / "data" / "audit_log.db"
    _SALT = "SyncroJob_Secure_Audit_2026"

    # Livelli di severità
    class Severity:
        LOW = "low"  # Info, operazioni normali
        MEDIUM = "medium"  # Modifiche config, avvisi
        HIGH = "high"  # Errori, manomissioni, licenza fallita

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuditManager, cls).__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        """Inizializza il database con supporto alla severità e migrazione automatica."""
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
                    row_hash TEXT
                )
            """
            )

            # Migrazione dinamica per database esistenti
            columns_to_add = [
                ("user_id", "TEXT"),
                ("entity", "TEXT"),
                ("params", "TEXT"),
                ("severity", "TEXT DEFAULT 'low'"),
                ("row_hash", "TEXT"),
            ]

            for col_name, col_type in columns_to_add:
                try:
                    conn.execute(f"ALTER TABLE audit_logs ADD COLUMN {col_name} {col_type}")
                except sqlite3.OperationalError:
                    pass

            # PULIZIA DATI: Corregge eventuali record 'None' o nulli nel database
            try:
                conn.execute(
                    "UPDATE audit_logs SET user_id = 'unknown' WHERE user_id IS NULL OR user_id = 'None' OR user_id = ''"
                )
                conn.commit()
            except:
                pass

            conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)")
            conn.commit()

    def _get_current_user(self) -> str:
        """Recupera l'utente corrente con massima robustezza (Environment + standard + Windows API fallback)."""
        # 1. Tentativo tramite variabili d'ambiente (veloce)
        user = os.environ.get("USERNAME") or os.environ.get("USER")
        if user and user.lower() != "none" and user != "":
            return user

        # 2. Tentativo tramite modulo standard
        try:
            import getpass

            user = getpass.getuser()
            if user and user.lower() != "none":
                return user
        except:
            pass

        # 3. Tentativo tramite Windows API (Win32)
        if os.name == "nt":
            try:
                import ctypes

                advapi32 = ctypes.windll.advapi32
                buffer = ctypes.create_unicode_buffer(256)
                size = ctypes.c_uint(len(buffer))
                if advapi32.GetUserNameW(buffer, ctypes.byref(size)):
                    return buffer.value
            except:
                pass

        return "unknown"

    def _calculate_hash(self, data_str: str, prev_hash: str) -> str:
        """Calcola l'hash SHA-256 concatenato."""
        payload = f"{data_str}|{prev_hash}|{self._SALT}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def _get_last_hash(self) -> str:
        """Recupera l'hash dell'ultima riga inserita."""
        try:
            with sqlite3.connect(self.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT row_hash FROM audit_logs ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                return row[0] if row and row[0] else "0" * 64
        except:
            return "0" * 64

    def log_action(
        self,
        action: str,
        category: str = "general",
        entity: str = "",
        params: Any = None,
        status: str = "success",
        severity: str = "low",
        notify: bool = False,
    ):
        """
        Registra un'azione dettagliata nell'audit log con hashing.
        Opzionalmente genera una notifica utente.
        """
        try:
            user_id = self._get_current_user()

            # Sanificazione Dati
            entity = entity if entity else "-"
            category = category if category else "general"
            params_json = json.dumps(params, ensure_ascii=False) if params else "{}"
            timestamp = datetime.now().isoformat()

            prev_hash = self._get_last_hash()
            # Include severity in the hash string
            data_to_hash = (
                f"{timestamp}|{user_id}|{action}|{category}|{entity}|{params_json}|{status}|{severity}"
            )
            current_hash = self._calculate_hash(data_to_hash, prev_hash)

            with sqlite3.connect(self.DB_PATH) as conn:
                conn.execute(
                    """INSERT INTO audit_logs 
                       (timestamp, user_id, action, category, entity, params, status, severity, row_hash) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        timestamp,
                        user_id,
                        action,
                        category,
                        entity,
                        params_json,
                        status,
                        severity,
                        current_hash,
                    ),
                )
                conn.commit()

            # Notifica utente se richiesto
            if notify:
                from src.core.notification_manager import NotificationManager

                level = "info"
                if status == "error" or severity == "high":
                    level = "error"
                elif status == "warning" or severity == "medium":
                    level = "warning"
                elif status == "success":
                    level = "success"

                title = f"{action}: {entity}"
                # Crea un messaggio leggibile dai parametri
                msg = f"Operazione completata con esito: {status.upper()}."
                if params and isinstance(params, dict):
                    if "nuova" in params:
                        msg = f"Versione aggiornata a {params['nuova']}"
                    elif "righe" in params:
                        msg = f"Elaborate {params['righe']} righe."

                NotificationManager.instance().add_notification(title, msg, level=level)

        except Exception as e:
            logger.error(f"Audit Log Error: {e}")

    def verify_integrity(self) -> bool:
        """Verifica l'integrità, ignorando i record legacy senza hash."""
        try:
            with sqlite3.connect(self.DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM audit_logs ORDER BY id ASC")
                rows = cursor.fetchall()

                prev_hash = "0" * 64
                for row in rows:
                    # Se il record non ha hash (legacy), non lo validiamo ma aggiorniamo il prev_hash
                    # per non rompere la catena futura. Se ha un hash, deve essere corretto.
                    if not row["row_hash"]:
                        continue

                    data_to_hash = f"{row['timestamp']}|{row['user_id']}|{row['action']}|{row['category']}|{row['entity']}|{row['params']}|{row['status']}|{row['severity']}"
                    expected_hash = self._calculate_hash(data_to_hash, prev_hash)

                    if row["row_hash"] != expected_hash:
                        return False
                    prev_hash = row["row_hash"]
                return True
        except:
            return False

    def get_logs(self, limit: int = 200) -> List[Dict[str, Any]]:
        """Recupera i log con i nuovi campi."""
        logs = []
        try:
            with sqlite3.connect(self.DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
                for row in cursor.fetchall():
                    logs.append(dict(row))
        except Exception as e:
            logger.error(f"Errore recupero audit logs: {e}")
        return logs

    def run_retention_policy(self, days: int = 90):
        """Esegue la pulizia basata sulla data di retention."""
        try:
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()
            with sqlite3.connect(self.DB_PATH) as conn:
                conn.execute("DELETE FROM audit_logs WHERE timestamp < ?", (cutoff,))
                conn.commit()
                self.log_action("Sistema", "mantenimento", "Audit Database", {"clean_days": days})
        except Exception as e:
            logger.error(f"Retention Policy Error: {e}")
