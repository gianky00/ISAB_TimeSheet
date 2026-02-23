"""
SyncroJob - Tray Icon Component
Gestore dell'icona nell'area di notifica (System Tray).
Permette all'applicazione di restare attiva in background e di inviare notifiche push di sistema.
"""

from typing import Any

from PyQt6.QtCore import QObject


class TrayIconComponent(QObject):
    """
    Componente responsabile dell'integrazione con la System Tray.
    Inizializza il TrayController e fornisce metodi di alto livello per l'invio di messaggi balloon.
    """

    def __init__(self, main_window: Any) -> None:
        """
        Inizializza il componente Tray.

        Args:
            main_window: Riferimento alla MainWindow dell'applicazione.
        """
        super().__init__(main_window)
        self.main_window = main_window
        from src.gui.controllers.tray_controller import TrayController

        self.controller = TrayController(main_window)

    def show_update_message(self, new_version: str) -> None:
        """
        Mostra una notifica di sistema per segnalare la disponibilità di una nuova versione.

        Args:
            new_version: Stringa della versione rilevata (es. '2.1.0').
        """
        self.controller.show_message(
            "Aggiornamento Disponibile",
            f"È uscita la versione {new_version}. Clicca qui per scaricarla.",
        )

    def show_background_notification(self, title: str, message: str, is_error: bool = False) -> None:
        """
        Invia una notifica balloon di sistema se l'applicazione è in background o minimizzata.
        Attiva inoltre l'alert visivo sulla taskbar (lampeggiamento).

        Args:
            title: Titolo della notifica.
            message: Contenuto testuale della notifica.
            is_error: Se True, utilizza l'icona di errore critico.
        """
        from PyQt6.QtWidgets import QApplication, QSystemTrayIcon

        is_active = self.main_window.isActiveWindow() and not self.main_window.isMinimized()

        if not is_active:
            icon = (
                QSystemTrayIcon.MessageIcon.Critical if is_error else QSystemTrayIcon.MessageIcon.Information
            )
            self.controller.show_message(title, message, icon, 5000)
            QApplication.alert(self.main_window, 0)
