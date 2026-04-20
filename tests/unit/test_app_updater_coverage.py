from unittest.mock import patch

from src.core import app_updater


class TestAppUpdater:
    @patch("src.core.app_updater.check_for_updates")
    def test_check_for_updates_delegation(self, mock_check):
        """Verifica che la facade deleghi correttamente."""
        app_updater.check_for_updates(silent=True)
        mock_check.assert_called_once_with(silent=True)

    @patch("src.core.app_updater.has_pending_update")
    def test_has_pending_update_delegation(self, mock_pending):
        mock_pending.return_value = True
        assert app_updater.has_pending_update() is True
        mock_pending.assert_called_once()

    @patch("src.core.app_updater.perform_auto_update")
    def test_perform_auto_update_delegation(self, mock_auto):
        app_updater.perform_auto_update()
        mock_auto.assert_called_once()

    @patch("src.core.app_updater.run_pending_installer")
    def test_run_pending_installer_delegation(self, mock_run):
        app_updater.run_pending_installer()
        mock_run.assert_called_once()
