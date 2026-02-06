from PyQt6.QtCore import QObject

from src.core import config_manager
from src.core.backup_manager import BackupManager


class AppEventHandler(QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self._force_quit = False

    def quit_application(self):
        """Chiude l'applicazione completamente (no tray)."""
        self._force_quit = True
        self.main_window.close()

    def handle_close_event(self, event):
        """
        Gestisce l'evento di chiusura della finestra.
        Se non forzata, nasconde l'applicazione nel tray.
        """
        if self._force_quit:
            # Stop Telegram Service
            if hasattr(self.main_window, "telegram") and self.main_window.telegram:
                self.main_window.telegram.stop_service()

            # Auto Backup
            config = config_manager.load_config()
            if config.get("auto_backup", True):
                BackupManager.create_backup()

            event.accept()
            return

        if self.main_window.isVisible():
            self.main_window.hide()
            event.ignore()

    def handle_f5(self):
        """Gestisce F5 tramite dispatch map delegando alla main window."""
        self.main_window._handle_f5_action()

    def handle_ctrl_f(self):
        """Gestisce Ctrl+F."""
        if (
            hasattr(self.main_window, "tool_bar_component")
            and self.main_window.tool_bar_component.global_search
        ):
            search_box = self.main_window.tool_bar_component.global_search
            search_box.setFocus()
            search_box.selectAll()
