"""
SyncroJob - App Event Handler
Controller dedicato alla gestione degli eventi globali dell'applicazione (chiusura, shortcut, backup).
"""

from PyQt6.QtCore import QObject

from src.core import config_manager
from src.core.backup_manager import BackupManager


class AppEventHandler(QObject):
    """
    Gestisce la logica di alto livello per gli eventi della MainWindow.
    Include la gestione della chiusura (nascondi vs esci), il trigger del backup automatico 
    e l'intercettazione delle scorciatoie da tastiera globali.
    """

    def __init__(self, main_window):
        """
        Inizializza l'event handler.

        Args:
            main_window: Riferimento alla MainWindow dell'applicazione.
        """
        super().__init__(main_window)
        self.main_window = main_window
        self._force_quit = False

    def quit_application(self):
        """Chiude l'applicazione completamente scavalcando la minimizzazione nel tray."""
        self._force_quit = True
        self.main_window.close()

    def handle_close_event(self, event):
        """
        Gestisce l'evento di chiusura della finestra.
        Se la chiusura non è forzata, nasconde l'applicazione nel tray invece di terminarla.
        Allo spegnimento definitivo, esegue il backup automatico e ferma i servizi.

        Args:
            event: QCloseEvent intercettato dalla MainWindow.
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
        """Gestisce il tasto F5 innescando il refresh intelligente della pagina attiva."""
        self.main_window._handle_f5_action()

    def handle_ctrl_f(self):
        """Gestisce Ctrl+F portando il focus sulla barra di ricerca globale."""
        if (
            hasattr(self.main_window, "tool_bar_component")
            and self.main_window.tool_bar_component.global_search
        ):
            search_box = self.main_window.tool_bar_component.global_search
            search_box.setFocus()
            search_box.selectAll()
