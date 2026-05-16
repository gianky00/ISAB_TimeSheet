"""
SyncroJob - Database Manager
Centralized SQLite database management with Thread Safety.
"""

import sqlite3
import threading
import time
from collections.abc import Callable, Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, ClassVar, Optional

from src.core.constants import FileNames
from src.core.database.migrations.contabilita import (
    mig_contabilita_v1,
    mig_contabilita_v2,
    mig_contabilita_v3,
    mig_contabilita_v4,
    mig_contabilita_v5,
    mig_contabilita_v6,
    mig_contabilita_v7,
)
from src.core.database.migrations.dipendenti import (
    mig_dipendenti_v1,
    mig_dipendenti_v2,
    mig_dipendenti_v3,
)
from src.core.database.migrations.pdl import mig_pdl_v1, mig_pdl_v2, mig_pdl_v3, mig_pdl_v4, mig_pdl_v5
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
from src.core.logging import get_logger
from src.core.paths import DB_DIR

logger = get_logger(__name__)


class DatabaseManager:
    """
    Singleton class to manage SQLite connections with thread safety and WAL mode.
    Implements a write lock to prevent contention.
    """

    _instance: Optional["DatabaseManager"] = None
    _write_lock = threading.Lock()

    # Dizionari di Migrazione
    MIGRATIONS_CONTABILITA: ClassVar[dict[int, Callable[[sqlite3.Connection], None]]] = {
        1: mig_contabilita_v1,
        2: mig_contabilita_v2,
        3: mig_contabilita_v3,
        4: mig_contabilita_v4,
        5: mig_contabilita_v5,
        6: mig_contabilita_v6,
        7: mig_contabilita_v7,
    }

    MIGRATIONS_TIMBRATURE: ClassVar[dict[int, Callable[[sqlite3.Connection], None]]] = {
        1: mig_timbrature_v1,
        2: mig_timbrature_v2,
        3: mig_timbrature_v3,
        4: mig_timbrature_v4,
    }

    MIGRATIONS_PDL: ClassVar[dict[int, Callable[[sqlite3.Connection], None]]] = {
        1: mig_pdl_v1,
        2: mig_pdl_v2,
        3: mig_pdl_v3,
        4: mig_pdl_v4,
        5: mig_pdl_v5,
    }

    MIGRATIONS_STORICO_ODA: ClassVar[dict[int, Callable[[sqlite3.Connection], None]]] = {
        1: mig_storico_oda_v1,
        2: mig_storico_oda_v2,
    }

    MIGRATIONS_DIPENDENTI: ClassVar[dict[int, Callable[[sqlite3.Connection], None]]] = {
        1: mig_dipendenti_v1,
        2: mig_dipendenti_v2,
        3: mig_dipendenti_v3,
    }

    # --- DYNAMIC DATABASE PATHS ---
    DB_CONTABILITA = DB_DIR / FileNames.DB_CONTABILITA
    DB_TIMBRATURE = DB_DIR / FileNames.DB_TIMBRATURE
    DB_PDL = DB_DIR / FileNames.DB_PDL
    DB_STORICO_ODA = DB_DIR / FileNames.DB_STORICO_ODA
    DB_DIPENDENTI = DB_DIR / FileNames.DB_DIPENDENTI
    DB_CERTIFICATI = DB_DIR / FileNames.DB_CERTIFICATI
    DB_SCARICO_ORE = DB_DIR / FileNames.DB_SCARICO_ORE
    DB_GIORNALIERE = DB_DIR / FileNames.DB_GIORNALIERE
    DB_AUDIT = DB_DIR / FileNames.DB_AUDIT_LOG

    def __new__(cls) -> "DatabaseManager":
        if cls._instance is None:
            with cls._write_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @contextmanager
    def get_connection(
        self, db_path: Path, read_only: bool = False
    ) -> Generator[sqlite3.Connection, None, None]:
        """
        Provides a thread-safe connection with automatic WAL mode and transaction handling.
        """
        if read_only:
            # Per sola lettura, usiamo URI mode per garantire l'accesso se possibile
            db_uri = f"file:{db_path.as_posix()}?mode=ro"
            conn = sqlite3.connect(db_uri, timeout=30.0, uri=True)
        else:
            conn = sqlite3.connect(db_path, timeout=30.0)

        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @contextmanager
    def get_write_connection(self, db_path: Path) -> Generator[sqlite3.Connection, None, None]:
        """
        Provides a connection with an exclusive write lock to prevent 'database is locked' errors.
        """
        with self._write_lock, self.get_connection(db_path) as conn:
            yield conn

    def execute_query(
        self, db_path: Path, query: str, params: tuple[Any, ...] = (), retry_count: int = 3
    ) -> list[sqlite3.Row]:
        """
        Safely executes a read query with automatic retries on busy.
        """
        last_error = None
        for i in range(retry_count):
            try:
                with self.get_connection(db_path) as conn:
                    return conn.execute(query, params).fetchall()
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() or "busy" in str(e).lower():
                    last_error = e
                    time.sleep(0.1 * (i + 1))
                    continue
                raise
            except Exception:
                raise

        logger.error(f"Failed to execute query after {retry_count} retries: {last_error}")
        if last_error:
            raise last_error
        raise sqlite3.OperationalError(f"Failed to execute query after {retry_count} retries")

    def init_db(self) -> None:
        """Initializes schema for all databases using the migration system."""
        self._run_migrations(self.DB_CONTABILITA, self.MIGRATIONS_CONTABILITA, "Contabilita")
        self._run_migrations(self.DB_TIMBRATURE, self.MIGRATIONS_TIMBRATURE, "Timbrature")
        self._run_migrations(self.DB_PDL, self.MIGRATIONS_PDL, "PDL")
        self._run_migrations(self.DB_STORICO_ODA, self.MIGRATIONS_STORICO_ODA, "Storico OdA")
        self._run_migrations(self.DB_DIPENDENTI, self.MIGRATIONS_DIPENDENTI, "Dipendenti")

    def _get_db_version(self, conn: sqlite3.Connection) -> int:
        try:
            res = conn.execute("PRAGMA user_version").fetchone()
            return int(res[0]) if res else 0
        except Exception:
            logger.exception("Errore recupero versione database")
            return 0

    def _set_db_version(self, conn: sqlite3.Connection, version: int) -> None:
        conn.execute(f"PRAGMA user_version = {version}")  # nosec B608

    def _run_migrations(
        self, db_path: Path, migrations: dict[int, Callable[[sqlite3.Connection], None]], db_name: str
    ) -> None:
        """
        Executes pending migrations for a specific database.
        """
        # Creazione directory se non esiste
        db_path.parent.mkdir(parents=True, exist_ok=True)

        with self.get_connection(db_path) as conn:
            current_ver = self._get_db_version(conn)
            target_ver = max(migrations.keys()) if migrations else 0

            if current_ver < target_ver:
                logger.info(f"[{db_name}] Database outdated (v{current_ver}). Migrating to v{target_ver}...")

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

    def close(self) -> None:
        """Cleanup resources."""


db_manager = DatabaseManager()
