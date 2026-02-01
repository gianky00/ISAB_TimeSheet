from pathlib import Path
from unittest.mock import MagicMock, patch

from src.core.backup_manager import BackupManager


class TestBackupManager:
    @patch("src.core.backup_manager.os.environ", {"OneDrive": "C:\\MockOneDrive"})
    @patch("src.core.backup_manager.Path.is_dir", return_value=True)
    def test_detect_cloud_paths(self, mock_is_dir):
        paths = BackupManager.detect_cloud_paths()
        # On Windows, OneDrive env var is common
        assert "OneDrive" in paths
        assert str(paths["OneDrive"]) == "C:\\MockOneDrive"

    @patch("src.core.backup_manager.load_config")
    @patch("src.core.backup_manager.BackupManager.detect_cloud_paths")
    def test_get_backup_dir_preferred(self, mock_detect, mock_load):
        mock_detect.return_value = {"OneDrive": Path("C:/OD")}
        mock_load.return_value = {"backup_cloud_provider": "OneDrive"}

        with patch.object(Path, "mkdir") as mock_mkdir:
            target = BackupManager.get_backup_dir()
            assert target == Path("C:/OD/SyncroJob_Backups")
            mock_mkdir.assert_called()

    @patch("src.core.backup_manager.load_config")
    @patch("src.core.backup_manager.BackupManager.detect_cloud_paths")
    def test_get_backup_dir_fallback(self, mock_detect, mock_load):
        mock_detect.return_value = {}
        mock_load.return_value = {}

        with patch.object(Path, "mkdir"):
            with patch(
                "src.core.backup_manager.Path.home", return_value=Path("C:/Users/Test")
            ):
                target = BackupManager.get_backup_dir()
                assert target == Path("C:/Users/Test/Documents/SyncroJob_Backups")

    @patch("src.core.backup_manager.os.walk")
    @patch("src.core.backup_manager.BackupManager.get_backup_dir")
    @patch("src.core.backup_manager.zipfile.ZipFile")
    @patch("src.core.backup_manager.AuditManager")
    def test_create_backup_success(self, mock_audit, mock_zip, mock_get_dir, mock_walk):
        mock_get_dir.return_value = Path("C:/Backup")
        mock_walk.return_value = [
            ("C:/Config", ["logs"], ["data.db", "config.json", "other.txt"]),
        ]
        # data.db and config.json match INCLUDE_EXT

        # Mock actual zip write behavior
        zip_inst = mock_zip.return_value.__enter__.return_value

        with patch("src.core.backup_manager.CONFIG_DIR", Path("C:/Config")):
            # Need to mock Path.stat().st_size for audit log
            with patch("src.core.backup_manager.Path.stat") as mock_stat:
                mock_stat.return_value.st_size = 1024
                success, msg = BackupManager.create_backup()

                assert success is True
                assert "SyncroJob_Backup_" in msg
                assert zip_inst.write.call_count == 2  # .db and .json

    @patch("src.core.backup_manager.BackupManager.get_backup_dir")
    @patch("src.core.backup_manager.zipfile.is_zipfile", return_value=True)
    @patch("src.core.backup_manager.zipfile.ZipFile")
    @patch("src.core.backup_manager.AuditManager")
    def test_restore_backup(self, mock_audit, mock_zip, mock_is_zip, mock_get_dir):
        mock_zip_path = "C:/back.zip"

        with patch("src.core.backup_manager.Path.exists", return_value=True):
            with patch("src.core.backup_manager.CONFIG_DIR", Path("C:/Config")):
                success, msg = BackupManager.restore_backup(mock_zip_path)
                assert success is True
                assert "Ripristino completato" in msg
                mock_zip.return_value.__enter__.return_value.extractall.assert_called_with(
                    Path("C:/Config")
                )

    def test_cleanup_old_backups(self):
        mock_dir = MagicMock(spec=Path)
        mock_files = [MagicMock(spec=Path) for _ in range(7)]
        for i, f in enumerate(mock_files):
            f.name = f"SyncroJob_Backup_{i}.zip"
            f.unlink = MagicMock()

        with patch.object(Path, "glob", return_value=mock_files):
            with patch("os.path.getmtime", side_effect=range(7)):
                BackupManager._cleanup_old_backups(mock_dir, keep=5)
                # Should delete 2 oldest
                # backups is sorted reverse=True, so [6,5,4,3,2,1,0]
                # backups[5:] is [1, 0]
                assert mock_files[0].unlink.called
                assert mock_files[1].unlink.called
                assert not mock_files[6].unlink.called
