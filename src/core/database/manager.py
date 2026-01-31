"""
SyncroJob - Database Manager
Centralized SQLite database management with Thread Safety.
"""

import logging
import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, List

from src.core.config_manager import CONFIG_DIR
from src.core.database.migrations.contabilita import (
    mig_contabilita_v1,
    mig_contabilita_v2,
    mig_contabilita_v3,
)
from src.core.database.migrations.dipendenti import (
    mig_dipendenti_v1,
    mig_dipendenti_v2,
    mig_dipendenti_v3,
)
from src.core.database.migrations.pdl import mig_pdl_v1, mig_pdl_v2
from src.core.database.migrations.storico_oda import (
    mig_storico_oda_v1,
    mig_storico_oda_v2,
)
from src.core.database.migrations.timbrature import (
    mig_timbrature_v1,
    mig_timbrature_v2,
    mig_timbrature_v3,
    mig_timbrature_v4,
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Singleton class to manage SQLite connections with thread safety and WAL mode.
    Implements a write lock to prevent contention.
    """

    _instance = None
    _write_lock = threading.Lock()

    # Predefined Paths
    DB_CONTABILITA = CONFIG_DIR / "data" / "contabilita.db"
    DB_TIMBRATURE = CONFIG_DIR / "data" / "timbrature_Isab.db"
    DB_PDL = CONFIG_DIR / "data" / "pdl.db"
    DB_STORICO_ODA = CONFIG_DIR / "data" / "storico_oda.db"
    DB_DIPENDENTI = CONFIG_DIR / "data" / "anagrafica_dipendenti.db"

    # Dizionari di Migrazione
    MIGRATIONS_CONTABILITA = {
        1: mig_contabilita_v1,
        2: mig_contabilita_v2,
        3: mig_contabilita_v3,
    }

    MIGRATIONS_TIMBRATURE = {
        1: mig_timbrature_v1,
        2: mig_timbrature_v2,
        3: mig_timbrature_v3,
        4: mig_timbrature_v4,
    }

    MIGRATIONS_PDL = {1: mig_pdl_v1, 2: mig_pdl_v2}

    MIGRATIONS_STORICO_ODA = {1: mig_storico_oda_v1, 2: mig_storico_oda_v2}

    MIGRATIONS_DIPENDENTI = {
        1: mig_dipendenti_v1,
        2: mig_dipendenti_v2,
        3: mig_dipendenti_v3,
    }

    def __new__(cls):
        """Pattern Singleton per il gestore database."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._ensure_dirs()
        return cls._instance

    def _ensure_dirs(self):
        """Ensures the data directory exists."""
        (CONFIG_DIR / "data").mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(
        self, db_path: Path, read_only: bool = False, timeout: float = 30.0
    ) -> Generator[sqlite3.Connection, None, None]:
        """
        Yields a SQLite connection with Thread Safety features.
        - WAL Mode enabled for concurrent read/write.
        - Increased timeout for locked databases.
        - Auto-commit handling via context manager.
        """
        uri = f"file:{db_path.absolute()}"
        if read_only:
            uri += "?mode=ro"

        conn = None
        try:
            # check_same_thread=False is safe when using one connection per context/thread
            conn = sqlite3.connect(
                uri, uri=True, timeout=timeout, check_same_thread=False
            )

            # Performance & Concurrency Optimizations
            if not read_only:
                conn.execute("PRAGMA journal_mode=WAL;")
                conn.execute("PRAGMA synchronous=NORMAL;")
                conn.execute(f"PRAGMA busy_timeout={int(timeout * 1000)};")

            # Enable Foreign Keys for both read and write
            conn.execute("PRAGMA foreign_keys = ON;")

            yield conn

            if not read_only and conn.in_transaction:
                conn.commit()

        except sqlite3.OperationalError as e:
            logger.error(f"Database Operational Error ({db_path.name}): {e}")
            if conn:
                conn.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected Database Error ({db_path.name}): {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    def execute_query(
        self, db_path: Path, query: str, params: tuple = (), retry_count: int = 3
    ) -> List[Any]:
        """Executes a query with automatic retries and write synchronization."""
        is_write = not query.strip().upper().startswith("SELECT")

        last_error = None
        for attempt in range(retry_count):
            try:
                # Se è una scrittura, acquisiamo il lock globale per questo processo
                if is_write:
                    self._write_lock.acquire()

                try:
                    with self.get_connection(db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute(query, params)
                        if not is_write:
                            return cursor.fetchall()
                        return []
                finally:
                    if is_write:
                        self._write_lock.release()

            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() or "busy" in str(e).lower():
                    last_error = e
                    time.sleep(0.1 * (attempt + 1))
                    continue
                raise

        logger.error(
            f"Failed to execute query after {retry_count} retries: {last_error}"
        )
        if last_error:
            raise last_error
        raise sqlite3.OperationalError(
            f"Failed to execute query after {retry_count} retries"
        )

    def init_db(self):
        """Initializes schema for all databases using the migration system."""
        self._run_migrations(
            self.DB_CONTABILITA, self.MIGRATIONS_CONTABILITA, "Contabilita"
        )
        self._run_migrations(
            self.DB_TIMBRATURE, self.MIGRATIONS_TIMBRATURE, "Timbrature"
        )
        self._run_migrations(self.DB_PDL, self.MIGRATIONS_PDL, "PDL")
        self._run_migrations(
            self.DB_STORICO_ODA, self.MIGRATIONS_STORICO_ODA, "Storico OdA"
        )
        self._run_migrations(
            self.DB_DIPENDENTI, self.MIGRATIONS_DIPENDENTI, "Dipendenti"
        )

    def _get_db_version(self, conn: sqlite3.Connection) -> int:
        try:
            return conn.execute("PRAGMA user_version").fetchone()[0]
        except Exception:
            return 0

    def _set_db_version(self, conn: sqlite3.Connection, version: int):
        conn.execute(f"PRAGMA user_version = {version}")

    def _run_migrations(self, db_path: Path, migrations: dict, db_name: str):
        """
        Executes pending migrations for a specific database.
        """
        with self.get_connection(db_path) as conn:
            current_ver = self._get_db_version(conn)
            target_ver = max(migrations.keys()) if migrations else 0

            if current_ver < target_ver:
                logger.info(
                    f"[{db_name}] Database outdated (v{current_ver}). Migrating to v{target_ver}..."
                )

                try:
                    # Apply migrations sequentially
                    for ver in range(current_ver + 1, target_ver + 1):
                        if ver in migrations:
                            logger.info(f"[{db_name}] Applying migration v{ver}...")
                            migrations[ver](conn)
                            self._set_db_version(conn, ver)
                            logger.info(f"[{db_name}] Migration v{ver} completed.")

                    logger.info(f"[{db_name}] All migrations completed successfully.")
                except Exception as e:
                    logger.critical(f"[{db_name}] Migration failed at step v{ver}: {e}")
                    raise


db_manager = DatabaseManager()
