import os
import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.core.backup_manager import BackupManager


@pytest.fixture
def mock_fs(fs: FakeFilesystem, mocker):
    """Fixture per il filesystem simulato."""
    # Importiamo qui per assicurarci di avere il valore patchato da pyfakefs
    from src.core.config_manager import CONFIG_DIR

    # Patchiamo CONFIG_DIR in backup_manager per allinearlo alla fixture
    mocker.patch("src.core.backup_manager.CONFIG_DIR", CONFIG_DIR)

    # Su Windows, Path.home() ritorna qualcosa come C:\Users\nome
    home = Path.home()
    if not fs.exists(home):
        fs.create_dir(home)
    if not fs.exists(CONFIG_DIR):
        fs.create_dir(CONFIG_DIR)

    # Crea qualche file critico per il backup
    f1 = CONFIG_DIR / "config.json"
    f2 = CONFIG_DIR / "database.db"
    fs.create_file(f1, contents='{"test": true}')
    fs.create_file(f2, contents="fake binary db")

    # Crea cartella esclusa
    logs_dir = CONFIG_DIR / "logs"
    if not fs.exists(logs_dir):
        fs.create_dir(logs_dir)
    fs.create_file(logs_dir / "app.log", contents="log data")

    return fs


@pytest.fixture
def mock_audit():
    with patch("src.core.backup_manager.AuditManager") as mock_audit_cls:
        instance = mock_audit_cls.instance.return_value
        yield instance


@pytest.fixture
def mock_config():
    with patch("src.core.backup_manager.load_config") as mock_load:
        mock_load.return_value = {}
        yield mock_load


class TestBackupManager:
    def test_detect_cloud_paths_onedrive_env(self, mock_fs):
        """Test rilevamento OneDrive tramite variabile d'ambiente."""
        od_path = Path("/mock/OneDrive")
        mock_fs.create_dir(od_path)

        with patch.dict(os.environ, {"ONEDRIVE": str(od_path)}):
            paths = BackupManager.detect_cloud_paths()
            assert "OneDrive" in paths
            assert paths["OneDrive"] == od_path

    def test_detect_cloud_paths_onedrive_home(self, mock_fs):
        """Test rilevamento OneDrive nella home utente."""
        od_path = Path.home() / "OneDrive"
        mock_fs.create_dir(od_path)

        with patch.dict(os.environ, {"ONEDRIVE": ""}):
            paths = BackupManager.detect_cloud_paths()
            assert "OneDrive" in paths
            assert paths["OneDrive"] == od_path

    def test_detect_cloud_paths_gdrive_home(self, mock_fs):
        """Test rilevamento Google Drive nella home utente."""
        gd_path = Path.home() / "Google Drive"
        mock_fs.create_dir(gd_path)

        paths = BackupManager.detect_cloud_paths()
        assert "Google Drive" in paths
        assert paths["Google Drive"] == gd_path

    def test_get_backup_dir_default_local(self, mock_fs, mock_config):
        """Test fallback su cartella Documenti locale se no cloud."""
        # Assicuriamoci che non ci siano cloud rilevati
        with patch.dict(os.environ, {"ONEDRIVE": ""}):
            # Non creiamo cartelle cloud nella home
            target = BackupManager.get_backup_dir()
            assert "SyncroJob_Backups" in str(target)
            assert "Documents" in str(target)

    def test_get_backup_dir_preferred_cloud(self, mock_fs, mock_config):
        """Test uso provider cloud preferito da config."""
        od_path = Path.home() / "OneDrive"
        mock_fs.create_dir(od_path)

        mock_config.return_value = {"backup_cloud_provider": "OneDrive"}

        target = BackupManager.get_backup_dir()
        assert target == od_path / "SyncroJob_Backups"

    def test_create_backup_success(self, mock_fs, mock_audit, mock_config):
        """Test creazione backup con successo."""
        backup_dir = Path.home() / "Documents" / "SyncroJob_Backups"
        if not mock_fs.exists(backup_dir):
            mock_fs.create_dir(backup_dir)

        success, result = BackupManager.create_backup()

        assert success is True
        assert Path(result).exists()
        assert zipfile.is_zipfile(result)

        # Verifica contenuto zip
        with zipfile.ZipFile(result, "r") as z:
            names = z.namelist()
            assert "config.json" in names
            assert "database.db" in names
            assert "logs/app.log" not in names  # Escluso

    def test_create_backup_no_files(self, mock_fs, mock_audit, mock_config):
        """Test backup fallito se non ci sono file da includere."""
        from src.core.config_manager import CONFIG_DIR

        # Rimuoviamo i file creati nella fixture
        mock_fs.remove(CONFIG_DIR / "config.json")
        mock_fs.remove(CONFIG_DIR / "database.db")

        success, message = BackupManager.create_backup()
        assert success is False
        assert "Nessun file" in message

    def test_cleanup_old_backups(self, mock_fs):
        """Test rotazione backup (mantiene solo ultimi N)."""
        backup_dir = Path("/backups")
        mock_fs.create_dir(backup_dir)

        # Crea 10 file di backup
        for i in range(10):
            name = f"SyncroJob_Backup_2024010{i}_120000.zip"
            mock_fs.create_file(backup_dir / name)
            # Simula mtime diverso
            os.utime(backup_dir / name, (1000 + i, 1000 + i))

        BackupManager._cleanup_old_backups(backup_dir, keep=5)

        remaining = list(backup_dir.glob("SyncroJob_Backup_*.zip"))
        assert len(remaining) == 5

    def test_restore_backup(self, mock_fs, mock_audit):
        """Test ripristino da file zip."""
        from src.core.config_manager import CONFIG_DIR

        # 1. Crea un file zip di test
        zip_path = Path("/tmp/restore_me.zip")
        if not mock_fs.exists("/tmp"):
            mock_fs.create_dir("/tmp")

        # Dobbiamo creare lo zip nel filesystem REALE o simulato coerentemente.
        # pyfakefs gestisce zipfile se configurato bene o se usiamo file binari.
        with zipfile.ZipFile(str(zip_path), "w") as z:
            z.writestr("restored_config.json", '{"status": "restored"}')

        # 2. Ripristina
        success, _ = BackupManager.restore_backup(str(zip_path))

        assert success is True
        assert (CONFIG_DIR / "restored_config.json").exists()

    def test_restore_backup_non_existent(self, mock_fs):
        """Test ripristino con file mancante."""
        success, message = BackupManager.restore_backup("/non/existent.zip")
        assert success is False
        assert "non trovato" in message

    def test_restore_backup_invalid_zip(self, mock_fs):
        """Test ripristino con file corrotto."""
        bad_zip = Path("/tmp/bad.zip")
        mock_fs.create_file(bad_zip, contents="not a zip")

        success, message = BackupManager.restore_backup(str(bad_zip))
        assert success is False
        assert "non valido" in message
