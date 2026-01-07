"""
SyncroJob - Backup Manager
Gestisce il backup e ripristino dei dati critici su cloud locale (OneDrive/Drive).
"""

import logging
import os
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from src.core.audit_manager import AuditManager
from src.core.config_manager import CONFIG_DIR, load_config

logger = logging.getLogger(__name__)


class BackupManager:

    # Cartelle da escludere dal backup
    EXCLUDE_DIRS = ["chrome_profile", "logs", "cache"]

    # Estensioni file critici
    INCLUDE_EXT = [".db", ".json", ".dat"]

    @staticmethod
    def detect_cloud_paths() -> Dict[str, Path]:
        """Rileva le cartelle dei servizi cloud installati."""
        user_home = Path.home()
        paths = {}

        # 1. OneDrive (Priorità assoluta per Windows)
        onedrive_env = os.environ.get("OneDrive")
        if onedrive_env and os.path.isdir(onedrive_env):
            paths["OneDrive"] = Path(onedrive_env)
        elif (user_home / "OneDrive").is_dir():
            paths["OneDrive"] = user_home / "OneDrive"

        # 2. Google Drive (Virtual Drive G: or User Folder)
        # Check standard virtual drive mount points
        for drive in ["G:/Il mio Drive", "G:/My Drive", "G:/"]:
            if os.path.exists(drive):
                paths["Google Drive"] = Path(drive)
                break

        # Fallback to user folder if virtual drive not found
        if "Google Drive" not in paths and (user_home / "Google Drive").is_dir():
            paths["Google Drive"] = user_home / "Google Drive"

        # 3. Dropbox (Standard & Business/Personal variants)
        for db_path in [
            user_home / "Dropbox",
            user_home / "Dropbox (Personal)",
            user_home / "Dropbox (Business)",
        ]:
            if db_path.is_dir():
                paths["Dropbox"] = db_path
                break

        # 4. MEGA (MEGAsync)
        mega_path = user_home / "MEGAsync"
        if mega_path.is_dir():
            paths["MEGA"] = mega_path
        elif (user_home / "MEGA").is_dir():
            paths["MEGA"] = user_home / "MEGA"

        return paths

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
        if configured_path and os.path.exists(configured_path):
            return Path(configured_path)

        # 3. Auto-detect fallback (Priority: OneDrive -> Google -> Dropbox)
        if "OneDrive" in clouds:
            target = clouds["OneDrive"] / "SyncroJob_Backups"
        elif clouds:
            # Get the first available cloud provider
            target = list(clouds.values())[0] / "SyncroJob_Backups"
        else:
            # Fallback to local documents if no cloud provider found
            target = Path.home() / "Documents" / "SyncroJob_Backups"

        # Crea se non esiste
        target.mkdir(parents=True, exist_ok=True)
        return target

    @staticmethod
    def create_backup() -> Tuple[bool, str]:
        """Crea un backup completo dei dati."""
        try:
            source_dir = CONFIG_DIR
            target_dir = BackupManager.get_backup_dir()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"SyncroJob_Backup_{timestamp}.zip"
            zip_path = target_dir / zip_filename

            file_count = 0

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    # Escludi cartelle non necessarie
                    dirs[:] = [d for d in dirs if d not in BackupManager.EXCLUDE_DIRS]

                    for file in files:
                        file_path = Path(root) / file
                        if file_path.suffix in BackupManager.INCLUDE_EXT:
                            arcname = file_path.relative_to(source_dir)
                            zipf.write(file_path, arcname)
                            file_count += 1

            if file_count > 0:
                # Audit
                AuditManager().log_action(
                    action="Backup Creato",
                    category="sistema",
                    entity="BackupManager",
                    params={"file": zip_filename, "size_kb": zip_path.stat().st_size // 1024},
                    severity="low",
                )

                # Cleanup vecchi backup (mantiene ultimi 5)
                BackupManager._cleanup_old_backups(target_dir)

                return True, str(zip_path)
            else:
                if zip_path.exists():
                    zip_path.unlink()
                return False, "Nessun file da backuppare trovato."

        except Exception as e:
            logger.error(f"Backup Error: {e}")
            AuditManager().log_action(
                "Errore Backup",
                category="sistema",
                status="error",
                severity="medium",
                params={"errore": str(e)},
            )
            return False, str(e)

    @staticmethod
    def _cleanup_old_backups(target_dir: Path, keep: int = 5):
        """Mantiene solo gli ultimi N backup."""
        try:
            backups = sorted(target_dir.glob("SyncroJob_Backup_*.zip"), key=os.path.getmtime, reverse=True)
            for old_backup in backups[keep:]:
                try:
                    old_backup.unlink()
                except:
                    pass
        except:
            pass

    @staticmethod
    def list_backups() -> List[Path]:
        """Restituisce la lista dei backup disponibili ordinati per data (più recente prima)."""
        try:
            target_dir = BackupManager.get_backup_dir()
            if not target_dir.exists():
                return []
            return sorted(target_dir.glob("SyncroJob_Backup_*.zip"), key=os.path.getmtime, reverse=True)
        except Exception as e:
            logger.error(f"Error listing backups: {e}")
            return []

    @staticmethod
    def restore_backup(zip_path: str) -> Tuple[bool, str]:
        """Ripristina un backup sovrascrivendo i dati attuali."""
        try:
            if not os.path.exists(zip_path):
                return False, "File di backup non trovato."

            # Verifica validità zip
            if not zipfile.is_zipfile(zip_path):
                return False, "File non valido o corrotto."

            # Estrazione sicura
            with zipfile.ZipFile(zip_path, "r") as zipf:
                zipf.extractall(CONFIG_DIR)

            AuditManager().log_action(
                "Ripristino Backup", category="sistema", params={"file": Path(zip_path).name}, severity="high"
            )
            return True, "Ripristino completato. Riavviare l'applicazione."

        except Exception as e:
            return False, str(e)
