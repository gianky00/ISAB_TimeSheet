"""
Unit Tests for Backup Features
Tests cloud detection and backup creation logic.
"""
import pytest
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.core.backup_manager import BackupManager
from src.core import config_manager

@pytest.fixture
def mock_home(tmp_path):
    """Mocks user home directory with fake cloud folders."""
    home = tmp_path / "home"
    home.mkdir()
    
    # Create fake cloud dirs
    (home / "OneDrive").mkdir()
    (home / "Google Drive").mkdir()
    
    return home

def test_detect_cloud_paths(mock_home):
    """Test detection of cloud services."""
    with patch("pathlib.Path.home", return_value=mock_home):
        # Clear env var to test folder detection
        with patch.dict(os.environ, {"OneDrive": ""}):
            paths = BackupManager.detect_cloud_paths()
            assert "OneDrive" in paths
            assert "Google Drive" in paths
            assert paths["OneDrive"] == mock_home / "OneDrive"

def test_get_backup_dir_onedrive_priority(mock_home):
    """Test that OneDrive is prioritized by default."""
    with patch("pathlib.Path.home", return_value=mock_home), \
         patch.dict(os.environ, {"OneDrive": str(mock_home / "OneDrive")}):
        
        # Mock config to empty
        with patch("src.core.backup_manager.load_config", return_value={}):
            backup_dir = BackupManager.get_backup_dir()
            expected = mock_home / "OneDrive" / "BotTS_Backups"
            assert backup_dir == expected

def test_get_backup_dir_user_preference(mock_home):
    """Test user preference override."""
    with patch("pathlib.Path.home", return_value=mock_home):
        # User prefers Google Drive
        # MOCK detect_cloud_paths to return only our mocked paths, preventing real G: drive detection
        mock_clouds = {"Google Drive": mock_home / "Google Drive"}
        
        with patch("src.core.backup_manager.load_config", return_value={"backup_cloud_provider": "Google Drive"}), \
             patch("src.core.backup_manager.BackupManager.detect_cloud_paths", return_value=mock_clouds):
            
            backup_dir = BackupManager.get_backup_dir()
            expected = mock_home / "Google Drive" / "BotTS_Backups"
            assert backup_dir == expected

def test_get_backup_dir_local_fallback(tmp_path):
    """Test fallback to Documents if no cloud found."""
    # Empty home
    empty_home = tmp_path / "empty_home"
    empty_home.mkdir()
    
    with patch("pathlib.Path.home", return_value=empty_home), \
         patch.dict(os.environ, {"OneDrive": ""}):
         
        # Ensure detect_cloud_paths finds nothing
        with patch("src.core.backup_manager.load_config", return_value={}), \
             patch("src.core.backup_manager.BackupManager.detect_cloud_paths", return_value={}):
             
            backup_dir = BackupManager.get_backup_dir()
            expected = empty_home / "Documents" / "BotTS_Backups"
            assert backup_dir == expected

def test_create_backup_success(tmp_path):
    """Test creation of ZIP backup."""
    # Mock source config dir
    fake_config_dir = tmp_path / "config"
    fake_config_dir.mkdir()
    (fake_config_dir / "test.db").touch()
    (fake_config_dir / "config.json").touch()
    
    # Mock target dir
    target_dir = tmp_path / "backups"
    target_dir.mkdir()
    
    with patch("src.core.backup_manager.CONFIG_DIR", fake_config_dir), \
         patch("src.core.backup_manager.BackupManager.get_backup_dir", return_value=target_dir), \
         patch("src.core.audit_manager.AuditManager.log_action") as mock_audit:
         
        success, msg = BackupManager.create_backup()
        
        assert success is True
        assert "BotTS_Backup_" in msg
        assert len(list(target_dir.glob("*.zip"))) == 1
        mock_audit.assert_called()

def test_cleanup_old_backups(tmp_path):
    """Test rotation of old backups."""
    target_dir = tmp_path / "rotation"
    target_dir.mkdir()
    
    # Create 10 dummy backups with DIFFERENT mtimes
    import time
    for i in range(10):
        p = target_dir / f"BotTS_Backup_2025010{i}.zip"
        p.touch()
        # Set mtime explicitly (files created earlier have smaller timestamp)
        # We want 09 to be newest -> highest timestamp
        os.utime(p, (time.time() + i*10, time.time() + i*10))
        
    BackupManager._cleanup_old_backups(target_dir, keep=5)
    
    remaining = list(target_dir.glob("*.zip"))
    assert len(remaining) == 5
    # Ensure newest remains (09 has highest mtime)
    assert (target_dir / "BotTS_Backup_20250109.zip").exists()
