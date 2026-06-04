import os
import zipfile
from pathlib import Path
from unittest.mock import ANY, patch

import pytest

from src.application.services.backup_manager import BackupManager


class TestBackupManagerRobust:
    @pytest.fixture
    def mock_config_dir(self, tmp_path):
        """Mocka CONFIG_DIR con una directory temporanea."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Crea file fake
        (config_dir / "data.db").write_text("DB Content")
        (config_dir / "settings.json").write_text("{}")
        (config_dir / "ignored.txt").write_text("Ignore me")

        # Mocka la variabile globale in backup_manager
        with patch("src.application.services.backup_manager.CONFIG_DIR", config_dir):
            yield config_dir

    @pytest.fixture
    def mock_audit(self):
        """Mocka AuditManager per evitare scritture su DB reale."""
        with patch("src.application.services.backup_manager.AuditManager") as mock:
            yield mock.instance.return_value

    @pytest.fixture
    def mock_cloud_env(self, tmp_path):
        """Simula ambiente con OneDrive."""
        onedrive_path = tmp_path / "OneDrive"
        onedrive_path.mkdir()

        with patch.dict(os.environ, {"OneDrive": str(onedrive_path)}):
            yield onedrive_path

    def test_detect_cloud_paths(self, mock_cloud_env, tmp_path):
        """Test rilevamento percorsi cloud."""
        paths = BackupManager.detect_cloud_paths()
        assert "OneDrive" in paths
        assert paths["OneDrive"] == mock_cloud_env

    def test_get_backup_dir_onedrive(self, mock_cloud_env):
        """Test selezione automatica directory backup."""
        with patch("src.application.services.backup_manager.load_config", return_value={}):
            backup_dir = BackupManager.get_backup_dir()
            assert backup_dir == mock_cloud_env / "SyncroJob_Backups"
            assert backup_dir.exists()

    def test_create_backup_success(self, mock_config_dir, mock_cloud_env, mock_audit):
        """Test creazione backup zip."""
        with patch("src.application.services.backup_manager.load_config", return_value={}):
            success, path_str = BackupManager.create_backup()

            assert success is True
            assert path_str.endswith(".zip")
            zip_path = Path(path_str)
            assert zip_path.exists()

            # Verifica contenuto zip
            with zipfile.ZipFile(zip_path, "r") as z:
                files = z.namelist()
                assert "data.db" in files
                assert "settings.json" in files
                assert "ignored.txt" not in files  # Estensione non inclusa in INCLUDE_EXT

            mock_audit.log_action.assert_called_with(
                action="Backup Creato",
                category="sistema",
                entity="BackupManager",
                params=ANY,
                severity="low",
            )

    def test_create_backup_empty(self, tmp_path, mock_audit):
        """Test backup senza file validi."""
        empty_conf = tmp_path / "empty_conf"
        empty_conf.mkdir()

        with (
            patch("src.application.services.backup_manager.CONFIG_DIR", empty_conf),
            patch(
                "src.application.services.backup_manager.BackupManager.get_backup_dir",
                return_value=tmp_path,
            ),
        ):
            success, msg = BackupManager.create_backup()
            assert success is False
            assert "Nessun file" in msg

    def test_cleanup_old_backups(self, tmp_path):
        """Test rotazione backup (keep=5)."""
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        # Crea 10 file fake con timestamp diversi
        for i in range(10):
            f = backup_dir / f"SyncroJob_Backup_2023010{i}_000000.zip"
            f.touch()
            # Forza mtime per ordine
            os.utime(f, (i * 1000, i * 1000))

        from src.application.services.backup.archive_rotator import ArchiveRotator

        ArchiveRotator.rotate_backups(backup_dir, keep=5)

        files = list(backup_dir.glob("*.zip"))
        assert len(files) == 5
        # I file rimasti devono essere quelli con i > 4 (i più recenti)
        dates = sorted([f.name for f in files])
        assert "20230109" in dates[-1]  # Il più recente

    def test_restore_backup_success(self, mock_config_dir, tmp_path, mock_audit):
        """Test ripristino backup."""
        # 1. Crea uno zip valido
        zip_path = tmp_path / "restore_test.zip"
        with zipfile.ZipFile(zip_path, "w") as z:
            z.writestr("restored_file.db", "Restored Content")

        # 2. Esegui restore
        success, _msg = BackupManager.restore_backup(str(zip_path))

        assert success is True
        assert (mock_config_dir / "restored_file.db").exists()
        assert (mock_config_dir / "restored_file.db").read_text() == "Restored Content"

        mock_audit.log_action.assert_called()

    def test_restore_backup_invalid(self, tmp_path):
        """Test ripristino file non valido."""
        bad_zip = tmp_path / "bad.zip"
        bad_zip.write_text("Not a zip")

        success, msg = BackupManager.restore_backup(str(bad_zip))
        assert success is False
        assert "non valido" in msg

    def test_list_backups(self, tmp_path):
        """Test listaggio backup."""
        with patch(
            "src.application.services.backup_manager.BackupManager.get_backup_dir",
            return_value=tmp_path,
        ):
            (tmp_path / "SyncroJob_Backup_A.zip").touch()
            (tmp_path / "OtherFile.txt").touch()

            backups = BackupManager.list_backups()
            assert len(backups) == 1
            assert backups[0].name == "SyncroJob_Backup_A.zip"
