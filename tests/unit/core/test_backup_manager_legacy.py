import zipfile
from pathlib import Path
from unittest.mock import patch

from src.core.backup_manager import BackupManager


class TestBackupManager:
    @patch("src.core.backup_manager.Path.home")
    @patch("os.environ.get")
    def test_detect_onedrive_logic(self, mock_env, mock_home, tmp_path):
        """Verifica il rilevamento di OneDrive tramite ENV e home folder."""
        # 1. Tramite Variabile d'Ambiente
        mock_env.return_value = str(tmp_path / "FakeOneDrive")
        (tmp_path / "FakeOneDrive").mkdir()

        path = BackupManager._detect_onedrive()
        assert path == tmp_path / "FakeOneDrive"

        # 2. Tramite Home Folder
        mock_env.return_value = None
        mock_home.return_value = tmp_path
        (tmp_path / "OneDrive").mkdir()

        path = BackupManager._detect_onedrive()
        assert path == tmp_path / "OneDrive"

    @patch("src.core.backup_manager.load_config")
    @patch("src.core.backup_manager.BackupManager.detect_cloud_paths")
    def test_get_backup_dir_fallback(self, mock_clouds, mock_load, tmp_path):
        """Verifica il fallback alla cartella Documents se nessun cloud è trovato."""
        mock_load.return_value = {}
        mock_clouds.return_value = {}

        with patch("src.core.backup_manager.Path.home", return_value=tmp_path):
            backup_dir = BackupManager.get_backup_dir()
            assert backup_dir == tmp_path / "Documents" / "SyncroJob_Backups"
            assert backup_dir.exists()

    @patch("src.core.backup_manager.BackupManager.get_backup_dir")
    @patch("src.core.audit_manager.AuditManager.instance")
    def test_create_backup_success(self, mock_audit, mock_get_dir, tmp_path):
        """Testa il ciclo completo di creazione backup."""
        # Setup sorgenti (CONFIG_DIR reale per il test)
        src = tmp_path / "src"
        src.mkdir()
        (src / "data.db").write_text("db content")
        (src / "config.json").write_text("{}")

        # Setup target
        target = tmp_path / "backups"
        target.mkdir()
        mock_get_dir.return_value = target

        # Patch CONFIG_DIR nel modulo target con un Path reale
        with patch("src.core.backup_manager.CONFIG_DIR", src):
            with patch("os.walk", return_value=[(str(src), [], ["data.db", "config.json"])]):
                success, zip_path = BackupManager.create_backup()

                assert success is True
                assert Path(zip_path).exists()
                assert zipfile.is_zipfile(zip_path)

    def test_restore_backup_invalid_file(self, tmp_path):
        """Verifica errore se il file non è uno ZIP valido."""
        fake_file = tmp_path / "not_a_zip.txt"
        fake_file.write_text("dummy")

        success, msg = BackupManager.restore_backup(str(fake_file))
        assert success is False
        assert "non valido" in msg.lower()
