"""Controller per la gestione della System Tray Icon."""

from typing import Any

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_app_icon_path, get_asset_path, get_colored_icon


class TrayController:
    """Gestisce l'icona e il menu della system tray."""

    def __init__(self, main_window: Any) -> None:
        """Inizializza la classe."""
        self.mw = main_window
        self.tray_icon = QSystemTrayIcon(self.mw)
        self._setup_tray_icon()

    def _setup_tray_icon(self) -> None:
        """Configura l'icona nella system tray."""
        icon_path = get_app_icon_path()
        if icon_path:
            self.tray_icon.setIcon(QIcon(icon_path))

        # Tray Menu
        tray_menu = QMenu()
        show_action = QAction("Mostra SyncroJob", self.mw)
        show_action.setIcon(get_colored_icon(get_asset_path(Icons.HOME), COLORS["text_dark"]))
        show_action.triggered.connect(self.mw.showMaximized)
        show_action.triggered.connect(self.mw.activateWindow)
        tray_menu.addAction(show_action)

        tray_menu.addSeparator()

        def force_quit_app() -> None:
            self.mw._force_quit = True
            app = QApplication.instance()
            if app is not None:
                app.quit()

        quit_action = QAction("Esci", self.mw)
        quit_action.setIcon(get_colored_icon(get_asset_path(Icons.X_CIRCLE), COLORS["text_dark"]))
        quit_action.triggered.connect(force_quit_app)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._handle_tray_activation)
        self.tray_icon.show()

    def _handle_tray_activation(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.mw.isVisible():
                self.mw.hide()
            else:
                self.mw.showMaximized()
                self.mw.activateWindow()

    def show_message(
        self,
        title: str,
        message: str,
        icon: QSystemTrayIcon.MessageIcon = QSystemTrayIcon.MessageIcon.Information,
        timeout: int = 5000,
    ) -> None:
        """Mostra una notifica tray."""
        self.tray_icon.showMessage(title, message, icon, timeout)
