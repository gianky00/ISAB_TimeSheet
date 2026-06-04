"""SyncroJob - Backup Manager.

Gestisce il backup e ripristino dei dati critici su cloud locale (OneDrive/Drive).
"""

import os
from datetime import UTC, datetime
from pathlib import Path

from src.application.services.audit_manager import AuditManager
from src.application.services.backup.archive_rotator import ArchiveRotator
from src.application.services.backup.zip_compressor import ZipCompressor
from src.application.services.config_manager import load_config
from src.application.services.logging import get_logger
from src.application.services.paths import CONFIG_DIR

logger = get_logger(__name__)


class BackupManager:
    """Manager specializzato nella creazione e ripristino di backup dell'applicazione.

    Agisce come facciata ad alto livello (Facade) e supporta il rilevamento
    automatico dei percorsi OneDrive, Google Drive, Dropbox e MEGA.
    """

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

            file_count = ZipCompressor.compress_directory(source_dir, zip_path)

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
                ArchiveRotator.rotate_backups(target_dir)

                return True, str(zip_path)

            if zip_path.exists():
                zip_path.unlink()
            success, msg = False, "Nessun file da backuppare trovato."

        except Exception as e:
            logger.exception("Backup Error")
            AuditManager.instance().log_action(
                "Errore Backup",
                category="sistema",
                status="error",
                severity="medium",
                params={"errore": str(e)},
            )
            return False, str(e)
        else:
            return success, msg

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
        except Exception:
            logger.exception("Error listing backups")
            return []

    @staticmethod
    def restore_backup(zip_path: str) -> tuple[bool, str]:
        """Ripristina un backup sovrascrivendo i dati attuali."""
        try:
            zip_p = Path(zip_path)
            if not zip_p.exists():
                return False, "File di backup non trovato."

            # Estrazione delegata sicura
            ZipCompressor.extract_archive(zip_p, CONFIG_DIR)

            AuditManager.instance().log_action(
                "Ripristino Backup",
                category="sistema",
                params={"file": zip_p.name},
                severity="high",
            )
        except Exception as e:
            return False, str(e)
        else:
            return True, "Ripristino completato. Riavviare l'applicazione."
