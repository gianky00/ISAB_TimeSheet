from unittest.mock import MagicMock

from src.gui.main_window.app_styler import AppStyler


class TestAppStyler:
    """Test di copertura per la configurazione dello stile globale dell'applicazione."""

    def test_setup_app_style(self, mocker):
        """Test: Configurazione stili e metadati app."""
        mock_app = MagicMock()
        mock_apply = mocker.patch("src.gui.main_window.app_styler.apply_theme")

        AppStyler.setup_app_style(mock_app)

        mock_app.setStyle.assert_called_with("Fusion")
        mock_apply.assert_called_with(mock_app, "light")
        mock_app.setApplicationName.assert_called_with("SyncroJob")
