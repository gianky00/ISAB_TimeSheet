import os
import zipfile
from pathlib import Path

import pytest

from src.core.backup.archive_rotator import ArchiveRotator
from src.core.backup_manager import BackupManager


class TestBackupFeatures:
    @pytest.fixture
    def mock_dirs(self, tmp_path):
        """Prepara directory sorgente e destinazione per i test."""
        source = tmp_path / "source"
        source.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        # Crea file critici
        (source / "data.db").write_text("db content")
        (source / "config.json").write_text("{}")

        # Crea cartella da escludere
        (source / "cache").mkdir()
        (source / "cache" / "trash.tmp").write_text("junk")

        return source, target

    def test_detect_cloud_paths_onedrive(self, mocker):
        """Verifica rilevamento OneDrive tramite variabile d'ambiente."""
        # Setup: Mock Path.home() per restituire un oggetto Path che si comporta bene
        fake_home = Path("/home/user")
        mocker.patch("pathlib.Path.home", return_value=fake_home)

        # Mock os.environ.get
        mocker.patch("os.environ.get", return_value="/cloud/onedrive")

        # Mock Path.is_dir per entrambe le chiamate (env var check e home check)
        mocker.patch("pathlib.Path.is_dir", return_value=True)
        # Mantieni anche os.path per sicurezza se misto
        mocker.patch("os.path.isdir", return_value=True)

        paths = BackupManager.detect_cloud_paths()
        assert "OneDrive" in paths
        # Su Windows i percorsi potrebbero venire normalizzati
        assert "/cloud/onedrive" in str(paths["OneDrive"]).replace("\\", "/")

    def test_create_backup_logic(self, mock_dirs, mocker):
        """Verifica che il backup contenga solo i file corretti."""
        source, target = mock_dirs
        mocker.patch("src.core.backup_manager.CONFIG_DIR", source)
        mocker.patch("src.core.backup_manager.BackupManager.get_backup_dir", return_value=target)

        # Esegui backup
        success, zip_path = BackupManager.create_backup()

        assert success is True
        assert Path(zip_path).exists()

        # Ispezione ZIP
        with zipfile.ZipFile(zip_path, "r") as z:
            names = z.namelist()
            assert "data.db" in names
            assert "config.json" in names
            # Cache esclusa
            assert not any("cache" in n for n in names)

    def test_cleanup_old_backups(self, mock_dirs):
        """Verifica che vengano mantenuti solo gli ultimi N backup."""
        _, target = mock_dirs

        # Crea 7 finti backup
        for i in range(7):
            p = target / f"SyncroJob_Backup_2026010{i}_000000.zip"
            p.write_text("zip data")
            # Forza tempi di modifica diversi
            os.utime(p, (1000 + i, 1000 + i))

        # SRP: ArchiveRotator gestisce la rotazione
        ArchiveRotator.rotate_backups(target, keep=5)

        remaining = list(target.glob("*.zip"))
        assert len(remaining) == 5

    def test_restore_backup_safe_extraction(self, mock_dirs, mocker):
        """Verifica che il restore sovrascriva i dati nella sorgente."""
        source, target = mock_dirs
        mocker.patch("src.core.backup_manager.CONFIG_DIR", source)

        # Crea uno zip di backup
        zip_path = target / "test_restore.zip"
        with zipfile.ZipFile(zip_path, "w") as z:
            z.writestr("new_data.db", "restored content")

        success, _msg = BackupManager.restore_backup(str(zip_path))

        assert success is True
        assert (source / "new_data.db").exists()
        assert (source / "new_data.db").read_text() == "restored content"

    def test_restore_invalid_zip(self, tmp_path):
        """Verifica errore in caso di file non zip."""
        bad_file = tmp_path / "fake.zip"
        bad_file.write_text("not a zip")

        success, msg = BackupManager.restore_backup(str(bad_file))
        assert success is False
        assert "non valido" in msg
