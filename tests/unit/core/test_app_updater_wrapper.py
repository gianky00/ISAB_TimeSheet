from unittest.mock import patch

from src.core import app_updater


class TestAppUpdaterWrapper:
    def test_exports(self):
        # Verifica che le funzioni principali siano esportate
        assert hasattr(app_updater, "check_for_updates")
        assert hasattr(app_updater, "perform_auto_update")
        assert hasattr(app_updater, "show_install_prompt")
        assert hasattr(app_updater, "get_local_setup_path")
        assert hasattr(app_updater, "has_pending_update")

    @patch("src.core.app_updater.check_for_updates")
    def test_check_for_updates_call(self, mock_check):
        app_updater.check_for_updates(silent=True)
        mock_check.assert_called_with(silent=True)
