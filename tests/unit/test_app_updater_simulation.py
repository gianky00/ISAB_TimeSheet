"""
Tests for AppUpdater Simulation.
Verifies version check and update notification using direct function mocking.
"""

from unittest.mock import MagicMock

import pytest

from src.core.app_updater import check_for_updates


class TestAppUpdaterSimulation:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mocker):
        # Mock della versione locale (es. v1.0.0)
        mocker.patch("src.core.updater.gui.version.__version__", "1.0.0")
        # Mock perform_auto_update per evitare download reali
        self.mock_perform = mocker.patch("src.core.updater.gui.perform_auto_update")
        # Mock HEAD request
        mock_head_resp = MagicMock()
        mock_head_resp.headers = {"content-length": "1000000"}
        mocker.patch("src.core.updater.gui.requests.head", return_value=mock_head_resp)

    def test_check_for_updates_found(self, mocker):
        """Verifica la logica quando viene trovata una nuova versione."""
        # Patch diretto delle funzioni dell'engine nel modulo GUI
        mocker.patch(
            "src.core.updater.gui.get_web_update_info",
            return_value={
                "version": "1.1.0",
                "url": "http://download.exe",
                "changelog": "Novità incredibili",
            }
        )
        mocker.patch("src.core.updater.gui.get_network_update_info", return_value=None)

        # Mock della UI
        mock_msg = mocker.patch("src.core.updater.gui.QMessageBox.question")
        from PyQt6.QtWidgets import QMessageBox
        mock_msg.return_value = QMessageBox.StandardButton.Yes

        check_for_updates(silent=False)

        # Deve aver mostrato la domanda di aggiornamento
        assert mock_msg.called
        args = mock_msg.call_args[0]
        assert "1.1.0" in str(args[2])
        # Deve aver chiamato perform_auto_update
        self.mock_perform.assert_called_once()

    def test_check_for_updates_already_updated(self, mocker):
        """Verifica che non faccia nulla se la versione locale è uguale o maggiore."""
        # Simula versione remota più vecchia
        mocker.patch(
            "src.core.updater.gui.get_web_update_info",
            return_value={"version": "0.9.0", "url": "http://old.exe"}
        )
        mocker.patch("src.core.updater.gui.get_network_update_info", return_value=None)

        mock_msg = mocker.patch("src.core.updater.gui.QMessageBox.question")

        check_for_updates(silent=True)

        # Non deve aver mostrato nulla
        assert not mock_msg.called
        assert not self.mock_perform.called

    def test_check_for_updates_http_error(self, mocker):
        """Verifica che gli errori di rete non causino crash (silent=True)."""
        # Simula errore engine che ritorna None
        mocker.patch("src.core.updater.gui.get_web_update_info", return_value=None)
        mocker.patch("src.core.updater.gui.get_network_update_info", return_value=None)

        # Non deve sollevare eccezioni
        check_for_updates(silent=True)
        assert not self.mock_perform.called
