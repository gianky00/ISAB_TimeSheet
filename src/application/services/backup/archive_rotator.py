"""Archive Rotator.

Gestisce la rotazione FIFO dei file di backup per non saturare lo storage locale o cloud.
"""

from contextlib import suppress
from pathlib import Path

from src.application.services.logging import get_logger

logger = get_logger("ArchiveRotator")


class ArchiveRotator:
    """Implementa algoritmi di rotazione FIFO per archivi obsoleti."""

    @staticmethod
    def rotate_backups(target_dir: Path, prefix: str = "SyncroJob_Backup_", keep: int = 5) -> None:
        """Conserva solo gli ultimi N backup ordinati per data di modifica, rimuovendo i restanti.

        La pulizia avviene in modo non bloccante ed eventuali errori vengono soppressi.

        Args:
            target_dir: Cartella contenente i file di backup.
            prefix: Prefisso dei file da considerare per la rotazione.
            keep: Numero massimo di file da conservare.
        """
        with suppress(Exception):
            backups = sorted(
                target_dir.glob(f"{prefix}*.zip"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            for old_backup in backups[keep:]:
                with suppress(Exception):
                    old_backup.unlink()
                    logger.info(f"Rimosso vecchio archivio di backup: {old_backup.name}")
