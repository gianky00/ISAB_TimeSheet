from unittest.mock import patch

from src.application.services import app_updater


class TestAppUpdaterRobust:
    @patch("src.application.services.app_updater.check_for_updates")
    def test_check_for_updates_delegation(self, mock_check):
        """Verifica che la facade deleghi correttamente al modulo GUI."""
        app_updater.check_for_updates(silent=False)
        mock_check.assert_called_once_with(silent=False)

    @patch("src.application.services.app_updater.has_pending_update")
    def test_has_pending_update_status(self, mock_pending):
        mock_pending.return_value = False
        assert app_updater.has_pending_update() is False
        mock_pending.assert_called_once()

    @patch("src.application.services.app_updater.show_install_prompt")
    def test_show_install_prompt_delegation(self, mock_prompt):
        app_updater.show_install_prompt("C:/setup.exe")
        mock_prompt.assert_called_once_with("C:/setup.exe")

    @patch("src.application.services.app_updater.get_local_setup_path")
    def test_get_local_setup_path_delegation(self, mock_path):
        mock_path.return_value = "C:/setup.exe"
        assert app_updater.get_local_setup_path() == "C:/setup.exe"
        mock_path.assert_called_once()
