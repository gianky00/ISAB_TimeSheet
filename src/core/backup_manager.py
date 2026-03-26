"""
SyncroJob - Backup Manager
Gestisce il backup e ripristino dei dati critici su cloud locale (OneDrive/Drive).
"""

import logging
import os
import zipfile
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import ClassVar

from src.core.audit_manager import AuditManager
from src.core.config_manager import load_config
from src.core.paths import CONFIG_DIR

logger = logging.getLogger(__name__)


class BackupManager:
    """
    Manager specializzato nella creazione e ripristino di backup dell'applicazione.
    Supporta il rilevamento automatico dei percorsi OneDrive e Google Drive.
    """

    # Cartelle da escludere dal backup
    EXCLUDE_DIRS: ClassVar[list[str]] = ["chrome_profile", "logs", "cache"]

    # Estensioni file critici
    INCLUDE_EXT: ClassVar[list[str]] = [".db", ".json", ".dat"]

    @staticmethod
    def detect_cloud_paths() -> dict[str, Path]:
        """Rileva le cartelle dei servizi cloud installati."""
        paths = {}

        # Sequenza di rilevamento
        if onedrive := BackupManager._detect_onedrive():
            paths["OneDrive"] = onedrive

        if gdrive := BackupManager._detect_gdrive():
            paths["Google Drive"] = gdrive

        if dropbox := BackupManager._detect_dropbox():
            paths["Dropbox"] = dropbox

        if mega := BackupManager._detect_mega():
            paths["MEGA"] = mega

        return paths

    @staticmethod
    def _detect_onedrive() -> Path | None:
        """Rileva percorso OneDrive."""
        user_home = Path.home()
        onedrive_env = os.environ.get("ONEDRIVE")
        if onedrive_env and Path(onedrive_env).is_dir():
            return Path(onedrive_env)
        if (user_home / "OneDrive").is_dir():
            return user_home / "OneDrive"
        return None

    @staticmethod
    def _detect_gdrive() -> Path | None:
        """Rileva percorso Google Drive."""
        for drive in ("G:/Il mio Drive", "G:/My Drive", "G:/"):
            if Path(drive).exists():
                return Path(drive)
        user_home = Path.home()
        if (user_home / "Google Drive").is_dir():
            return user_home / "Google Drive"
        return None

    @staticmethod
    def _detect_dropbox() -> Path | None:
        """Rileva percorso Dropbox."""
        user_home = Path.home()
        for db_path in (
            user_home / "Dropbox",
            user_home / "Dropbox (Personal)",
            user_home / "Dropbox (Business)",
        ):
            if db_path.is_dir():
                return db_path
        return None

    @staticmethod
    def _detect_mega() -> Path | None:
        """Rileva percorso MEGA."""
        user_home = Path.home()
        mega_path = user_home / "MEGAsync"
        if mega_path.is_dir():
            return mega_path
        if (user_home / "MEGA").is_dir():
            return user_home / "MEGA"
        return None

    @staticmethod
    def get_backup_dir() -> Path:
        """Restituisce la cartella di destinazione backup (da config o auto-detect)."""
        config = load_config()
        clouds = BackupManager.detect_cloud_paths()

        # 1. Check user preference first
        preferred = config.get("backup_cloud_provider")  # e.g. "OneDrive", "Google Drive", "Local"

        if preferred and preferred in clouds:
            target = clouds[preferred] / "SyncroJob_Backups"
            target.mkdir(parents=True, exist_ok=True)
            return target

        # 2. Check manual path override
        configured_path = config.get("backup_path")
        if configured_path and Path(configured_path).exists():
            return Path(configured_path)

        # 3. Auto-detect fallback (Priority: OneDrive -> Google -> Dropbox)
        if "OneDrive" in clouds:
            target = clouds["OneDrive"] / "SyncroJob_Backups"
        elif clouds:
            # Get the first available cloud provider
            target = next(iter(clouds.values())) / "SyncroJob_Backups"
        else:
            # Fallback to local documents if no cloud provider found
            target = Path.home() / "Documents" / "SyncroJob_Backups"

        # Crea se non esiste
        target.mkdir(parents=True, exist_ok=True)
        return target

    @staticmethod
    def create_backup() -> tuple[bool, str]:
        """Crea un backup completo dei dati."""
        try:
            source_dir = CONFIG_DIR
            target_dir = BackupManager.get_backup_dir()

            timestamp = datetime.now(UTC).astimezone().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"SyncroJob_Backup_{timestamp}.zip"
            zip_path = target_dir / zip_filename

            file_count = 0

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Usiamo os.walk per massima compatibilità con filesystem simulati e reali
                for root, dirs, files in os.walk(source_dir):
                    # Filtra directory escluse
                    dirs[:] = [d for d in dirs if d not in BackupManager.EXCLUDE_DIRS]

                    for file in files:
                        file_path = Path(root) / file
                        if file_path.suffix in BackupManager.INCLUDE_EXT:
                            arcname = file_path.relative_to(source_dir)
                            zipf.write(file_path, arcname)
                            file_count += 1

            if file_count > 0:
                # Audit
                AuditManager.instance().log_action(
                    action="Backup Creato",
                    category="sistema",
                    entity="BackupManager",
                    params={
                        "file": zip_filename,
                        "size_kb": zip_path.stat().st_size // 1024,
                    },
                    severity="low",
                )

                # Cleanup vecchi backup (mantiene ultimi 5)
                BackupManager._cleanup_old_backups(target_dir)

                return True, str(zip_path)

            if zip_path.exists():
                zip_path.unlink()
            return False, "Nessun file da backuppare trovato."  # noqa: TRY300

        except Exception as e:
            logger.error(f"Backup Error: {e}")  # noqa: TRY400
            AuditManager.instance().log_action(
                "Errore Backup",
                category="sistema",
                status="error",
                severity="medium",
                params={"errore": str(e)},
            )
            return False, str(e)

    @staticmethod
    def _cleanup_old_backups(target_dir: Path, keep: int = 5) -> None:
        """
        Mantiene solo gli ultimi N backup nel database, eliminando i più vecchi.

        Args:
            target_dir: Cartella dove risiedono i backup.
            keep: Numero di backup da conservare (default 5).
        """
        with suppress(Exception):
            backups = sorted(
                target_dir.glob("SyncroJob_Backup_*.zip"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            for old_backup in backups[keep:]:
                with suppress(Exception):
                    old_backup.unlink()

    @staticmethod
    def list_backups() -> list[Path]:
        """Restituisce la lista dei backup disponibili ordinati per data (più recente prima)."""
        try:
            target_dir = BackupManager.get_backup_dir()
            if not target_dir.exists():
                return []
            return sorted(
                target_dir.glob("SyncroJob_Backup_*.zip"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
        except Exception as e:
            logger.error(f"Error listing backups: {e}")  # noqa: TRY400
            return []

    @staticmethod
    def restore_backup(zip_path: str) -> tuple[bool, str]:
        """Ripristina un backup sovrascrivendo i dati attuali."""
        try:
            zip_p = Path(zip_path)
            if not zip_p.exists():
                return False, "File di backup non trovato."

            # Verifica validità zip
            if not zipfile.is_zipfile(zip_p):
                return False, "File non valido o corrotto."

            # Estrazione sicura
            with zipfile.ZipFile(zip_p, "r") as zipf:
                zipf.extractall(CONFIG_DIR)

            AuditManager.instance().log_action(
                "Ripristino Backup",
                category="sistema",
                params={"file": zip_p.name},
                severity="high",
            )
            return True, "Ripristino completato. Riavviare l'applicazione."  # noqa: TRY300

        except Exception as e:
            return False, str(e)
