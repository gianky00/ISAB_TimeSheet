from unittest.mock import patch

from src.core import app_updater


class TestAppUpdater:
    @patch("src.gui.dialogs.updater_dialog.check_for_updates")
    def test_check_for_updates_delegation(self, mock_check):  # noqa: ANN001
        """Verifica che la facade deleghi correttamente al modulo GUI."""
        app_updater.check_for_updates(silent=True)
        mock_check.assert_called_once_with(silent=True)

    @patch("src.core.updater.engine.has_pending_update")
    def test_has_pending_update_delegation(self, mock_pending):  # noqa: ANN001
        mock_pending.return_value = True
        assert app_updater.has_pending_update() is True
        mock_pending.assert_called_once()

    @patch("src.gui.dialogs.updater_dialog.perform_auto_update")
    def test_perform_auto_update_delegation(self, mock_auto):  # noqa: ANN001
        app_updater.perform_auto_update()
        mock_auto.assert_called_once()

    @patch("src.core.updater.engine.run_pending_installer")
    def test_run_pending_installer_delegation(self, mock_run):  # noqa: ANN001
        app_updater.run_pending_installer()
        mock_run.assert_called_once()
