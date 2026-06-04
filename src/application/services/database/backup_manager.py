"""SyncroJob - Database Backup Manager.

Specializzato nella protezione dei database SQLite tramite backup periodici e rotazione.
"""

import shutil
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from src.application.services.audit_manager import AuditManager
from src.application.services.logging import get_logger
from src.application.services.paths import DB_DIR

logger = get_logger(__name__)


class DatabaseBackupManager:
    """Gestisce il backup dei database SQLite in una cartella locale dedicata.

    Implementa la rotazione dei file per evitare eccessivo consumo di disco.
    """

    BACKUP_DIR: Path = DB_DIR / "backups"
    MAX_BACKUPS: int = 10

    @classmethod
    def execute_backup(cls) -> bool:
        """Esegue il backup di tutti i database attivi.

        Utilizza il comando VACUUM INTO di SQLite per backup consistenti a caldo.
        """
        try:
            cls.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            # Formato richiesto: GG_MM_AAAA alle HH_MM (es. 12_05_2026 alle 07_52)
            timestamp = datetime.now(UTC).astimezone().strftime("%d_%m_%Y alle %H_%M")
            session_dir = cls.BACKUP_DIR / timestamp
            session_dir.mkdir(exist_ok=True)

            db_files = list(DB_DIR.glob("*.db"))
            if not db_files:
                logger.warning(f"Nessun database trovato per il backup in {DB_DIR}")
                return False

            success_count = 0
            for db_path in db_files:
                backup_path = session_dir / db_path.name
                if cls._safe_copy(db_path, backup_path):
                    success_count += 1

            if success_count > 0:
                logger.info(f"Backup database completato: {success_count} file salvati in {session_dir}")
                cls._rotate_backups()

                AuditManager.instance().log_action(
                    action="Database Backup",
                    category="sistema",
                    entity="DatabaseBackupManager",
                    params={"count": success_count, "path": str(session_dir)},
                    severity="low",
                )
                return True

            # Se non ha salvato nulla, rimuove la cartella di sessione vuota
            if session_dir.exists() and not list(session_dir.iterdir()):
                session_dir.rmdir()
        except Exception:
            logger.exception("Errore critico durante il backup dei database")
        return False

    @classmethod
    def _safe_copy(cls, src: Path, dst: Path) -> bool:
        """Esegue una copia sicura del database.

        Prova a usare SQLite per un backup consistente, altrimenti fallback su shutil.
        """
        try:
            # Metodo 1: SQLite Online Backup (consistente anche se il DB è aperto)
            with sqlite3.connect(src) as conn:
                conn.execute(f"VACUUM INTO '{dst.as_posix()}'")
        except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
            # Fallback se VACUUM INTO non è supportato o fallisce (es. db molto vecchio o corrotto)
            logger.warning(f"VACUUM INTO fallito per {src.name} ({e}), provo copia standard")
            try:
                shutil.copy2(src, dst)
            except Exception:
                logger.exception(f"Copia fallita per {src.name}")
                return False
            else:
                return True
        except Exception:
            logger.exception(f"Errore copia database {src.name}")
            return False
        else:
            return True

    @classmethod
    def _rotate_backups(cls) -> None:
        """Mantiene solo gli ultimi MAX_BACKUPS basandosi sulla data di modifica."""
        try:
            backups = sorted(
                [d for d in cls.BACKUP_DIR.iterdir() if d.is_dir()],
                key=lambda d: d.stat().st_mtime,
                reverse=True,
            )

            if len(backups) > cls.MAX_BACKUPS:
                for old_dir in backups[cls.MAX_BACKUPS :]:
                    logger.info(f"Rimozione vecchio backup database: {old_dir}")
                    shutil.rmtree(old_dir, ignore_errors=True)
        except Exception:
            logger.exception("Errore durante la rotazione dei backup database")

    @classmethod
    def list_backups(cls) -> list[Path]:
        """Restituisce la lista delle cartelle di backup disponibili ordinate per data."""
        if not cls.BACKUP_DIR.exists():
            return []
        return sorted(
            [d for d in cls.BACKUP_DIR.iterdir() if d.is_dir()], key=lambda d: d.stat().st_mtime, reverse=True
        )
