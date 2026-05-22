"""Unit tests for ArchiveRotator."""

import os
from pathlib import Path

from src.core.backup.archive_rotator import ArchiveRotator


def test_rotate_backups_success(tmp_path: Path) -> None:
    """Verifica che la rotazione FIFO mantenga solo gli ultimi N backup e lasci gli altri file intatti."""
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()

    # Crea 8 file fake di backup con prefisso standard e diversi timestamp
    for i in range(8):
        f = backup_dir / f"SyncroJob_Backup_{i}.zip"
        f.touch()
        # Forza mtime crescente (più alto = più recente)
        os.utime(f, (i * 100, i * 100))

    # Crea un file con prefisso diverso (non deve essere ruotato/rimosso)
    other_file = backup_dir / "KeepMe_Other_Backup.zip"
    other_file.touch()

    # Esegui la rotazione tenendo solo gli ultimi 3
    ArchiveRotator.rotate_backups(backup_dir, keep=3)

    remaining_zips = list(backup_dir.glob("SyncroJob_Backup_*.zip"))
    assert len(remaining_zips) == 3

    # I file rimasti devono essere i più recenti (5, 6, 7)
    names = {p.name for p in remaining_zips}
    assert "SyncroJob_Backup_7.zip" in names
    assert "SyncroJob_Backup_6.zip" in names
    assert "SyncroJob_Backup_5.zip" in names
    assert "SyncroJob_Backup_0.zip" not in names

    # Verifica che il file estraneo sia rimasto intatto
    assert other_file.exists()


def test_rotate_backups_robust_with_missing_dir() -> None:
    """Verifica che non venga sollevata alcuna eccezione se la cartella non esiste."""
    non_existent = Path("non_existent_directory_xyz")
    # Non deve sollevare eccezioni
    ArchiveRotator.rotate_backups(non_existent)
