"""
SyncroJob - Wait Helpers Coverage Boost (Final Robustness)
Test di polling con tempo incrementale automatico per evitare StopIteration.
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from src.bots.base.wait_helpers import poll_for_file, poll_for_new_file


class AutoIncrementalTime:
    def __init__(self, start=0, step=1):
        self.current = start
        self.step = step

    def __call__(self):
        self.current += self.step
        return self.current


class TestWaitHelpersCoverageFinal:
    @pytest.fixture
    def fs_setup(self, fs):
        fs.create_dir("/downloads")
        return fs

    def test_poll_for_file_with_incremental_time(self, fs_setup):
        dir_path = Path("/downloads")
        target_file = dir_path / "report.xlsx"

        # Tempo incrementale automatico
        with patch("time.time", side_effect=AutoIncrementalTime()):
            with patch("time.sleep"):
                fs_setup.create_file(target_file)
                res = poll_for_file(dir_path, pattern="*.xlsx", timeout=100)
                assert res is not None

    def test_poll_for_new_file_update_incremental(self, fs_setup):
        import os

        dir_path = Path("/downloads")
        f1 = dir_path / "report.xlsx"
        fs_setup.create_file(f1, contents="old")

        # mtime iniziale
        os.utime(str(f1), (100, 100))
        files_before = [str(f1)]

        # Mock tempo incrementale
        timer = AutoIncrementalTime(start=1000)
        with patch("time.time", side_effect=timer):
            with patch("time.sleep"):
                # Aggiorna mtime per simulare nuovo download/sovrascrittura
                os.utime(str(f1), (5000, 5000))

                res = poll_for_new_file(dir_path, files_before, pattern="*.xlsx", timeout=100)
                assert res is not None
                assert "report.xlsx" in res
