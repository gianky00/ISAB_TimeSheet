import os
import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.core.backup_manager import BackupManager


class TestBackupManager:
    @pytest.fixture
    def manager(self, tmp_path, mocker):
        # Mock CONFIG_DIR
        mocker.patch("src.core.backup_manager.CONFIG_DIR", tmp_path)
        # Mock load_config
        mocker.patch("src.core.backup_manager.load_config", return_value={})
        return BackupManager

    def test_detect_cloud_paths(self, manager, tmp_path):
        with patch.dict(os.environ, {"OneDrive": str(tmp_path / "OneDrive")}):
            (tmp_path / "OneDrive").mkdir()
            paths = manager.detect_cloud_paths()
            assert "OneDrive" in paths

    def test_get_backup_dir_default(self, manager, tmp_path):
        # Ensure detect_cloud_paths returns empty
        with patch.object(manager, "detect_cloud_paths", return_value={}):
            with patch("pathlib.Path.home", return_value=tmp_path):
                target = manager.get_backup_dir()
                assert "Documents" in str(target)
                assert target.exists()

    def test_create_backup_success(self, manager, tmp_path, mocker):
        # Create dummy data in CONFIG_DIR (which is mocked to tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        (data_dir / "test.db").write_text("dummy db content")

        # Mock AuditManager
        mock_audit = mocker.patch("src.core.backup_manager.AuditManager")
        mock_audit.instance.return_value = mock_audit.return_value

        # Set backup dir to a subdirectory
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        with patch.object(manager, "get_backup_dir", return_value=backup_dir):
            success, msg = manager.create_backup()

            assert success is True
            assert ".zip" in msg
            # Check if file exists
            assert Path(msg).exists()
            mock_audit.return_value.log_action.assert_called()

    def test_create_backup_no_files(self, manager, tmp_path):
        # Empty CONFIG_DIR (tmp_path has no relevant files by default)
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        with patch.object(manager, "get_backup_dir", return_value=backup_dir):
            success, msg = manager.create_backup()
            assert success is False
            assert "Nessun file" in msg

    def test_restore_backup_success(self, manager, tmp_path, mocker):
        # Create a zip
        zip_path = tmp_path / "backup.zip"
        with zipfile.ZipFile(zip_path, "w") as z:
            z.writestr("restored.json", "{}")

        success, msg = manager.restore_backup(str(zip_path))
        assert success is True
        assert (tmp_path / "restored.json").exists()

    def test_restore_backup_invalid(self, manager, tmp_path):
        bad_zip = tmp_path / "bad.zip"
        bad_zip.write_text("not a zip")

        success, msg = manager.restore_backup(str(bad_zip))
        assert success is False
        assert "non valido" in msg

    def test_cleanup_old_backups(self, manager, tmp_path):
        # Create 10 dummy zip files
        for i in range(10):
            p = tmp_path / f"SyncroJob_Backup_{i}.zip"
            p.touch()
            # Set mtime to ensure sorting
            os.utime(p, (i * 100, i * 100))

        manager._cleanup_old_backups(tmp_path, keep=5)

        remaining = list(tmp_path.glob("*.zip"))
        assert len(remaining) == 5
        # Should be 5, 6, 7, 8, 9 (newest)
        names = [p.name for p in remaining]
        assert "SyncroJob_Backup_9.zip" in names
        assert "SyncroJob_Backup_0.zip" not in names

    def test_list_backups(self, manager, tmp_path):
        backup_dir = tmp_path / "list_test"
        backup_dir.mkdir()
        (backup_dir / "SyncroJob_Backup_A.zip").touch()

        with patch.object(manager, "get_backup_dir", return_value=backup_dir):
            backups = manager.list_backups()
            assert len(backups) == 1
            assert backups[0].name == "SyncroJob_Backup_A.zip"
