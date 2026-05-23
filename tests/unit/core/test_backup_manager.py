import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.core.backup_manager import BackupManager


class TestBackupManager:
    @pytest.fixture
    def mock_fs(self, fs):
        return fs

    @patch("src.core.backup_manager.Path.home")
    def test_detect_onedrive(self, mock_home, fs):
        home = Path("/home/user")
        mock_home.return_value = home

        # Test con variabile d'ambiente
        with patch.dict(os.environ, {"ONEDRIVE": "/fake/onedrive"}):
            fs.create_dir("/fake/onedrive")
            assert BackupManager._detect_onedrive() == Path("/fake/onedrive")

        # Test con cartella standard in home
        with patch.dict(os.environ, {"ONEDRIVE": ""}):
            fs.create_dir(str(home / "OneDrive"))
            assert BackupManager._detect_onedrive() == home / "OneDrive"

    @patch("src.core.backup_manager.Path.exists")
    def test_detect_gdrive(self, mock_exists):
        # Mocking exists to return True only for a specific path
        def side_effect(*args, **kwargs):
            # args[0] potrebbe essere self se mockato in alcuni modi,
            # ma qui patchiamo Path.exists direttamente
            return True

        mock_exists.side_effect = side_effect

        res = BackupManager._detect_gdrive()
        assert res == Path("G:/Il mio Drive")

    def test_detect_cloud_paths(self):
        with patch.object(BackupManager, "_detect_onedrive", return_value=Path("/od")):
            with patch.object(BackupManager, "_detect_gdrive", return_value=None):
                with patch.object(BackupManager, "_detect_dropbox", return_value=None):
                    with patch.object(BackupManager, "_detect_mega", return_value=None):
                        paths = BackupManager.detect_cloud_paths()
                        assert "OneDrive" in paths
                        assert paths["OneDrive"] == Path("/od")
                        assert len(paths) == 1

    @patch("src.core.backup_manager.load_config")
    def test_get_backup_dir_preferred(self, mock_config, fs):
        mock_config.return_value = {"backup_cloud_provider": "OneDrive"}
        with patch.object(BackupManager, "detect_cloud_paths", return_value={"OneDrive": Path("/od")}):
            res = BackupManager.get_backup_dir()
            assert res == Path("/od/SyncroJob_Backups")
            assert os.path.exists("/od/SyncroJob_Backups")

    @patch("src.core.backup_manager.load_config")
    def test_get_backup_dir_manual(self, mock_config, fs):
        mock_config.return_value = {"backup_path": "/manual/path"}
        fs.create_dir("/manual/path")
        res = BackupManager.get_backup_dir()
        assert res == Path("/manual/path")

    @patch("src.core.backup_manager.load_config", return_value={})
    @patch("src.core.backup_manager.ZipCompressor.compress_directory")
    @patch("src.core.backup_manager.ArchiveRotator.rotate_backups")
    @patch("src.core.backup_manager.CONFIG_DIR", Path("/src_data"))
    def test_create_backup_success(self, mock_rotate, mock_compress, mock_config, fs):
        fs.create_dir("/src_data")
        fs.create_file("/src_data/file.db")

        with patch.object(BackupManager, "get_backup_dir", return_value=Path("/backups")):
            fs.create_dir("/backups")

            def side_effect(src, dst):
                fs.create_file(str(dst), contents=b"fake zip")
                return 1

            mock_compress.side_effect = side_effect

            with patch("src.core.backup_manager.datetime") as mock_dt:
                mock_dt.now.return_value.astimezone.return_value.strftime.return_value = "test"
                with patch("src.core.backup_manager.AuditManager.instance") as mock_audit:
                    success, path = BackupManager.create_backup()
                    assert success is True
                    assert "SyncroJob_Backup_test.zip" in path

    @patch("src.core.backup_manager.ZipCompressor.compress_directory", return_value=0)
    @patch("src.core.backup_manager.get_logger")
    def test_create_backup_no_files(self, mock_get_logger, mock_compress, fs):
        with patch.object(BackupManager, "get_backup_dir", return_value=Path("/tmp/b")):
            success, msg = BackupManager.create_backup()
            assert success is False
            assert "Nessun file" in msg

    @patch("src.core.backup_manager.ZipCompressor.extract_archive")
    @patch("src.core.backup_manager.CONFIG_DIR", Path("/dst"))
    def test_restore_backup_success(self, mock_extract, fs):
        zip_path = "/fake/backup.zip"
        fs.create_file(zip_path)

        with patch("src.core.backup_manager.AuditManager.instance") as mock_audit:
            success, _msg = BackupManager.restore_backup(zip_path)
            assert success is True
            assert mock_extract.called

    def test_restore_backup_missing_file(self):
        success, msg = BackupManager.restore_backup("/non/existent.zip")
        assert success is False
        assert "non trovato" in msg

    def test_list_backups(self, fs):
        backup_dir = Path("/backups_list")
        fs.create_dir(str(backup_dir))
        fs.create_file(str(backup_dir / "SyncroJob_Backup_20230101_120000.zip"))
        fs.create_file(str(backup_dir / "SyncroJob_Backup_20230102_120000.zip"))

        with patch.object(BackupManager, "get_backup_dir", return_value=backup_dir):
            backups = BackupManager.list_backups()
            assert len(backups) == 2
