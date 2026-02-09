from typing import Any

from PyQt6.QtCore import QObject


class TrayIconComponent(QObject):
    """
    Manages the System Tray Icon.
    """

    def __init__(self, main_window: Any) -> None:
        super().__init__(main_window)
        self.main_window = main_window
        # Lazy import to avoid circular dependencies if any, though imports should be fine
        from src.gui.controllers.tray_controller import TrayController

        self.controller = TrayController(main_window)

    def show_update_message(self, new_version: str) -> None:
        self.controller.show_message(
            "Aggiornamento Disponibile",
            f"È uscita la versione {new_version}. Clicca qui per scaricarla.",
        )

    def show_background_notification(self, title: str, message: str, is_error: bool = False) -> None:
        """
        Mostra una notifica di sistema (Toast) se l'applicazione non è attiva.
        """
        from PyQt6.QtWidgets import QApplication, QSystemTrayIcon

        is_active = self.main_window.isActiveWindow() and not self.main_window.isMinimized()

        if not is_active:
            icon = (
                QSystemTrayIcon.MessageIcon.Critical if is_error else QSystemTrayIcon.MessageIcon.Information
            )
            self.controller.show_message(title, message, icon, 5000)
            QApplication.alert(self.main_window, 0)
