import os
import time
import zipfile
from pathlib import Path

import pytest

from src.core.backup_manager import BackupManager


class TestBackupResilience:
    @pytest.fixture
    def setup_files(self, tmp_path):
        """Prepara file finti da backuppare."""
        source_dir = tmp_path / "app_data"
        source_dir.mkdir()

        # File da includere
        (source_dir / "database.db").write_text("db data")
        (source_dir / "config.json").write_text("{}")

        # File/Cartelle da escludere
        cache_dir = source_dir / "cache"
        cache_dir.mkdir()
        (cache_dir / "temp.dat").write_text("cache data")
        (source_dir / "logs.txt").write_text("logs")  # estensione non in INCLUDE_EXT

        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        return source_dir, backup_dir

    def test_backup_creation_and_filtering(self, setup_files, mocker):
        """Test: Creazione backup con filtri corretti."""
        source_dir, backup_dir = setup_files

        # Mocking CONFIG_DIR e target backup dir
        mocker.patch("src.core.backup_manager.CONFIG_DIR", source_dir)
        mocker.patch(
            "src.core.backup_manager.BackupManager.get_backup_dir",
            return_value=backup_dir,
        )
        # Mocking AuditManager instance
        mocker.patch("src.core.backup_manager.AuditManager")

        success, zip_path = BackupManager.create_backup()

        assert success is True
        assert Path(zip_path).exists()

        # Verifica contenuto ZIP
        with zipfile.ZipFile(zip_path, "r") as zipf:
            names = zipf.namelist()
            assert "database.db" in names
            assert "config.json" in names
            assert "cache/temp.dat" not in names  # Escluso per directory
            assert "logs.txt" not in names  # Escluso per estensione

    def test_backup_retention_policy(self, setup_files, mocker):
        """Test: Mantieni solo gli ultimi N backup."""
        _, backup_dir = setup_files

        # Creiamo 7 backup finti
        for i in range(7):
            f = backup_dir / f"SyncroJob_Backup_20260101_{i}.zip"
            f.write_text("dummy")
            # Forziamo il tempo di modifica per l'ordinamento
            os.utime(f, (time.time() + i, time.time() + i))

        BackupManager._cleanup_old_backups(backup_dir, keep=5)

        remaining = list(backup_dir.glob("SyncroJob_Backup_*.zip"))
        assert len(remaining) == 5

    def test_restore_backup(self, setup_files, mocker):
        """Test: Ripristino sovrascrive i dati correnti."""
        source_dir, backup_dir = setup_files

        # Crea uno zip di backup
        zip_path = backup_dir / "test_restore.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.writestr("database.db", "restored_data")

        mocker.patch("src.core.backup_manager.CONFIG_DIR", source_dir)
        mocker.patch("src.core.backup_manager.AuditManager")

        success, _msg = BackupManager.restore_backup(str(zip_path))

        assert success is True
        assert (source_dir / "database.db").read_text() == "restored_data"

    def test_detect_cloud_paths_onedrive(self, mocker):
        """Test: Rilevamento OneDrive tramite env var."""
        mocker.patch.dict(os.environ, {"OneDrive": "C:\\Users\\Test\\OneDrive"})
        mocker.patch("pathlib.Path.is_dir", return_value=True)

        paths = BackupManager.detect_cloud_paths()
        assert "OneDrive" in paths
        assert paths["OneDrive"] == Path("C:\\Users\\Test\\OneDrive")
