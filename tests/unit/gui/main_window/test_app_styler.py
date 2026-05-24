from unittest.mock import patch

from PySide6.QtWidgets import QApplication

from src.gui.main_window.app_styler import AppStyler


def test_setup_app_style(qtbot):
    # Dobbiamo usare il QApplication reale fornito da pytest-qt (tramite qapp) o crearne un mock
    # Per essere sicuri, mockiamo apply_theme in modo da non sporcare lo stato globale
    app = QApplication.instance()

    with patch("src.gui.main_window.app_styler.apply_theme") as mock_apply_theme:
        AppStyler.setup_app_style(app)

        # apply_theme è stata chiamata
        mock_apply_theme.assert_called_once_with(app, "light")

        # check che setApplicationName è stato impostato
        assert app.applicationName() == "SyncroJob"
