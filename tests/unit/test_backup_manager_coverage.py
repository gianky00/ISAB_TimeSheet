import os
import zipfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.core.backup_manager import BackupManager

class TestBackupManagerCoverage:

    def test_detect_cloud_paths_onedrive_env(self):
        """Test OneDrive detection via environment variable."""
        with patch.dict(os.environ, {"OneDrive": r"C:\User\OneDrive"}):
            with patch("os.path.isdir", return_value=True):
                paths = BackupManager.detect_cloud_paths()
                assert "OneDrive" in paths
                assert paths["OneDrive"] == Path(r"C:\User\OneDrive")

    def test_detect_cloud_paths_onedrive_home(self, tmp_path):
        """Test OneDrive detection in home directory."""
        with patch("pathlib.Path.home", return_value=tmp_path):
            (tmp_path / "OneDrive").mkdir()
            
            with patch.dict(os.environ, {}, clear=True): # Ensure env var not present
                paths = BackupManager.detect_cloud_paths()
                assert "OneDrive" in paths
                assert paths["OneDrive"] == tmp_path / "OneDrive"

    def test_detect_cloud_paths_google_drive(self, tmp_path):
        """Test Google Drive detection."""
        with patch("pathlib.Path.home", return_value=tmp_path):
            with patch("os.path.exists") as mock_exists:
                # Simulate G: drive existing
                mock_exists.side_effect = lambda p: p == "G:/My Drive"
                
                paths = BackupManager.detect_cloud_paths()
                assert "Google Drive" in paths
                assert str(paths["Google Drive"]) == "G:\My Drive"

    def test_detect_cloud_paths_dropbox(self, tmp_path):
        """Test Dropbox detection."""
        with patch("pathlib.Path.home", return_value=tmp_path):
            (tmp_path / "Dropbox").mkdir()
            paths = BackupManager.detect_cloud_paths()
            assert "Dropbox" in paths

    def test_get_backup_dir_preferred(self, tmp_path):
        """Test get_backup_dir with user preference."""
        clouds = {"OneDrive": tmp_path / "OneDrive"}
        
        with patch("src.core.backup_manager.BackupManager.detect_cloud_paths", return_value=clouds):
            with patch("src.core.backup_manager.load_config", return_value={"backup_cloud_provider": "OneDrive"}):
                target = BackupManager.get_backup_dir()
                assert target == clouds["OneDrive"] / "SyncroJob_Backups"

    def test_get_backup_dir_fallback_local(self, tmp_path):
        """Test get_backup_dir fallback to local Documents."""
        with patch("src.core.backup_manager.BackupManager.detect_cloud_paths", return_value={}):
            with patch("src.core.backup_manager.load_config", return_value={}):
                with patch("pathlib.Path.home", return_value=tmp_path):
                    target = BackupManager.get_backup_dir()
                    assert target == tmp_path / "Documents" / "SyncroJob_Backups"

    def test_create_backup_success(self, tmp_path):
        """Test successful backup creation."""
        # Setup source dir with files
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "data.db").write_text("content")
        (source_dir / "config.json").write_text("{}")
        (source_dir / "ignored.txt").write_text("ignore")

        target_dir = tmp_path / "backups"
        target_dir.mkdir()

        with patch("src.core.backup_manager.CONFIG_DIR", source_dir):
            with patch("src.core.backup_manager.BackupManager.get_backup_dir", return_value=target_dir):
                with patch("src.core.audit_manager.AuditManager.log_action") as mock_audit:
                    success, path = BackupManager.create_backup()
                    
                    assert success is True
                    assert "SyncroJob_Backup_" in path
                    assert Path(path).exists()
                    mock_audit.assert_called()

                    # Verify zip content
                    with zipfile.ZipFile(path, "r") as z:
                        files = z.namelist()
                        assert "data.db" in files
                        assert "config.json" in files
                        assert "ignored.txt" not in files # Not in INCLUDE_EXT

    def test_create_backup_empty(self, tmp_path):
        """Test backup with no valid files."""
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        (source_dir / "ignored.txt").write_text("ignore") # No valid extension

        target_dir = tmp_path / "backups"
        target_dir.mkdir()

        with patch("src.core.backup_manager.CONFIG_DIR", source_dir):
            with patch("src.core.backup_manager.BackupManager.get_backup_dir", return_value=target_dir):
                success, msg = BackupManager.create_backup()
                assert success is False
                assert "Nessun file" in msg
                # Should verify zip was deleted
                assert not list(target_dir.glob("*.zip"))

    def test_cleanup_old_backups(self, tmp_path):
        """Test cleanup logic."""
        # Create 10 mock backups
        for i in range(10):
            p = tmp_path / f"SyncroJob_Backup_202401{i:02d}.zip"
            p.touch()
            # Modify mtime to ensure order
            os.utime(p, (i*1000, i*1000))

        BackupManager._cleanup_old_backups(tmp_path, keep=3)
        
        files = list(tmp_path.glob("*.zip"))
        assert len(files) == 3
        # Should have kept the 3 most recent (highest timestamps)
        timestamps = sorted([p.stat().st_mtime for p in files])
        assert timestamps[0] >= 7000 # 7000, 8000, 9000 kept

    def test_list_backups(self, tmp_path):
        """Test listing backups."""
        (tmp_path / "SyncroJob_Backup_1.zip").touch()
        (tmp_path / "SyncroJob_Backup_2.zip").touch()
        
        with patch("src.core.backup_manager.BackupManager.get_backup_dir", return_value=tmp_path):
            backups = BackupManager.list_backups()
            assert len(backups) == 2

    def test_restore_backup(self, tmp_path):
        """Test backup restoration."""
        # Create a zip to restore
        zip_path = tmp_path / "restore.zip"
        with zipfile.ZipFile(zip_path, "w") as z:
            z.writestr("restored.json", "{\"restored\": true}")

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        with patch("src.core.backup_manager.CONFIG_DIR", config_dir):
             with patch("src.core.audit_manager.AuditManager.log_action"):
                success, msg = BackupManager.restore_backup(str(zip_path))
                assert success is True
                assert (config_dir / "restored.json").exists()

    def test_restore_backup_invalid(self, tmp_path):
        """Test restoring invalid file."""
        bad_zip = tmp_path / "bad.zip"
        bad_zip.write_text("Not a zip")
        
        success, msg = BackupManager.restore_backup(str(bad_zip))
        assert success is False
        assert "non valido" in msg
