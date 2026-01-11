import pytest
import os
import shutil
from pathlib import Path
from src.core.backup_manager import BackupManager
from src.core.audit_manager import AuditManager
from src.core.contabilita_stats import ContabilitaStats
from unittest.mock import patch, MagicMock
import sqlite3

class TestCoreLogicBoost:
    def test_backup_manager_full_flow(self, tmp_path):
        # Setup source and backup dirs
        src = tmp_path / "src"
        src.mkdir()
        (src / "test.db").write_text("data")
        
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()
        
        bm = BackupManager(str(src), str(backup_dir))
        success, b_path = bm.create_backup("test.db")
        
        assert success is True
        assert Path(b_path).exists()
        
        # Test listing and cleaning
        backups = bm.list_backups()
        assert len(backups) >= 1
        
        bm.cleanup_old_backups(max_backups=0)
        assert len(bm.list_backups()) == 0

    def test_audit_manager_rotation(self, tmp_path):
        with patch("src.core.config_manager.CONFIG_DIR", tmp_path):
            am = AuditManager()
            # Log multiple entries
            for i in range(10):
                am.log_action(f"Action {i}", "User")
            
            # Verify file exists
            log_file = tmp_path / "logs" / "audit.log"
            assert log_file.exists()

    def test_contabilita_stats_calculation(self, tmp_path):
        db_path = tmp_path / "stats.db"
        # Setup table
        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE contabilita (year INTEGER, tcl TEXT, importo_pos REAL, ore REAL)")
            conn.execute("INSERT INTO contabilita VALUES (2024, 'T1', 1000.0, 10.0)")
            conn.execute("INSERT INTO contabilita VALUES (2024, 'T1', 500.0, 5.0)")
        
        stats = ContabilitaStats.get_year_stats(db_path, 2024)
        assert stats["total_pos"] == 1500.0
        assert stats["total_ore"] == 15.0
        assert len(stats["by_tcl"]) == 1
