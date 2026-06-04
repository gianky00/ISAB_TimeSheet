from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.infrastructure.utils.browser_diagnostics import (
    _check_filesystem,
    _check_processes,
    emergency_profile_reset,
    run_browser_diagnostic,
)


class TestBrowserDiagnostics:
    @pytest.fixture(autouse=True)
    def setup_fs(self, fs):
        self.user_data_dir = Path("/profile")
        fs.create_dir(str(self.user_data_dir))

        # Patch CONFIG_DIR per salvataggio report
        self.config_dir = Path("/config")
        fs.create_dir(str(self.config_dir))
        with patch("src.application.services.config_manager.CONFIG_DIR", self.config_dir):
            yield

    def test_check_filesystem_success(self, fs):
        res = _check_filesystem(self.user_data_dir)
        assert res["status"] == "PASS"
        assert "OK" in res["details"][0]

    def test_check_filesystem_fail_write(self, fs):
        # Simula errore scrittura rendendo la cartella read-only o inesistente
        path = Path("/nonexistent")
        # pyfakefs handles nonexistent path
        res = _check_filesystem(path)
        # La logica del codice tenta di creare la dir se non esiste
        # Se non può crearla (es. permessi root), fallisce
        # Ma qui in fakefs la crea.

        # Test con file di lock
        fs.create_file(str(self.user_data_dir / "SingletonLock"))
        res = _check_filesystem(self.user_data_dir)
        assert any("SingletonLock" in d for d in res["details"])

    @patch("src.infrastructure.utils.browser_diagnostics.psutil.process_iter")
    def test_check_processes(self, mock_iter):
        mock_proc = MagicMock()
        # Assicuriamoci che il cmdline contenga il percorso della directory come stringa
        path_str = str(self.user_data_dir)
        mock_proc.info = {"name": "chrome.exe", "cmdline": [f"--user-data-dir={path_str}"]}
        mock_proc.pid = 123
        mock_iter.return_value = [mock_proc]

        res = _check_processes(self.user_data_dir)
        assert res["status"] == "WARNING"
        assert "PID: 123" in res["details"][0]

    @patch("src.infrastructure.utils.browser_diagnostics.sync_playwright")
    @patch("src.infrastructure.utils.browser_diagnostics._check_processes")
    @patch("src.infrastructure.utils.browser_diagnostics._check_filesystem")
    def test_run_browser_diagnostic(self, mock_fs, mock_proc, mock_pw, fs):
        mock_fs.return_value = {"status": "PASS", "details": []}
        mock_proc.return_value = {"status": "PASS", "details": []}

        # Mock Playwright Context Manager
        mock_pw_instance = mock_pw.return_value.__enter__.return_value
        mock_browser = mock_pw_instance.chromium.launch.return_value

        report = run_browser_diagnostic(self.user_data_dir)

        assert report["overall_status"] == "PASS"
        assert (self.config_dir / "logs" / "browser_debug.json").exists()

    @patch("src.infrastructure.utils.browser_diagnostics.cleanup_bot_processes")
    @patch("src.infrastructure.utils.browser_diagnostics.shutil.move")
    def test_emergency_profile_reset(self, mock_move, mock_cleanup, fs):
        assert emergency_profile_reset(self.user_data_dir) is True
        assert mock_cleanup.called
        assert mock_move.called

        # Se non esiste
        assert emergency_profile_reset(Path("/missing")) is False
