"""
Tests per DatabaseBackupManager.
"""

import sqlite3

import pytest

from src.core.database.backup_manager import DatabaseBackupManager


@pytest.fixture
def temp_db_dir(tmp_path):
    """Crea una directory DB temporanea."""
    db_dir = tmp_path / "data"
    db_dir.mkdir()

    # Crea un DB finto
    db_file = db_dir / "test.db"
    with sqlite3.connect(db_file) as conn:
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
        conn.execute("INSERT INTO test VALUES (1)")

    # Mock dei percorsi nel manager
    original_db_dir = DatabaseBackupManager.BACKUP_DIR.parent
    DatabaseBackupManager.BACKUP_DIR = db_dir / "backups"

    # Salviamo i percorsi originali per ripristinarli (anche se in pytest è meglio usare monkeypatch)
    yield db_dir, db_file

def test_execute_backup(temp_db_dir, monkeypatch):
    """Verifica che il backup venga creato correttamente con il nuovo formato."""
    db_dir, _db_file = temp_db_dir

    monkeypatch.setattr("src.core.database.backup_manager.DB_DIR", db_dir)
    monkeypatch.setattr("src.core.database.backup_manager.DatabaseBackupManager.BACKUP_DIR", db_dir / "backups")

    success = DatabaseBackupManager.execute_backup()
    assert success is True

    backup_root = db_dir / "backups"
    assert backup_root.exists()

    # Verifica il formato: GG_MM_AAAA alle HH_MM
    sessions = list(backup_root.iterdir())
    assert len(sessions) == 1
    folder_name = sessions[0].name
    assert " alle " in folder_name
    assert len(folder_name.split("_")) >= 4 # GG, MM, AAAA, HH, MM

    # Verifica che il file DB sia all'interno
    backup_file = sessions[0] / "test.db"
    assert backup_file.exists()

def test_rotation(temp_db_dir, monkeypatch):
    """Verifica la rotazione dei backup basata su mtime."""
    db_dir, _ = temp_db_dir
    backup_root = db_dir / "backups"

    monkeypatch.setattr("src.core.database.backup_manager.DB_DIR", db_dir)
    monkeypatch.setattr("src.core.database.backup_manager.DatabaseBackupManager.BACKUP_DIR", backup_root)
    monkeypatch.setattr("src.core.database.backup_manager.DatabaseBackupManager.MAX_BACKUPS", 2)

    # Mock del tempo per generare nomi diversi se necessario (anche se usiamo mtime)
    # Creiamo manualmente 3 cartelle con mtime diversi per testare la rotazione
    (backup_root / "cartella_1").mkdir(parents=True)
    (backup_root / "cartella_2").mkdir(parents=True)
    (backup_root / "cartella_3").mkdir(parents=True)

    import os
    import time

    # Impostiamo mtime crescenti
    now = time.time()
    os.utime(backup_root / "cartella_1", (now - 100, now - 100))
    os.utime(backup_root / "cartella_2", (now - 50, now - 50))
    os.utime(backup_root / "cartella_3", (now, now))

    # Chiamiamo la rotazione (interna o via execute_backup che la chiama)
    DatabaseBackupManager._rotate_backups()

    backups = DatabaseBackupManager.list_backups()
    assert len(backups) == 2
    # Deve aver rimosso cartella_1 (la più vecchia per mtime)
    names = [b.name for b in backups]
    assert "cartella_1" not in names
    assert "cartella_2" in names
    assert "cartella_3" in names
