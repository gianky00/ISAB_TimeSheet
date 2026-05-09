"""
SyncroJob - Signal Connector
Controller responsabile del cablaggio dei segnali tra i diversi moduli dell'applicazione.
Mantiene disaccoppiata la logica dei servizi dalla visualizzazione della MainWindow.
"""

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject

from src.core.notification_manager import NotificationManager
from src.gui.widgets.toast import ToastManager

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow


class SignalConnector(QObject):
    """
    Gestisce la connessione dei segnali PySide6 tra i Singleton Manager e la UI.
    Sìoccupa di aggiornare badge, mostrare toast e gestire la navigazione dalla sidebar.
    """

    def __init__(self, main_window: "MainWindow") -> None:
        """
        Inizializza il connettore di segnali.

        Args:
          main_window: Riferimento alla MainWindow dell'applicazione.
        """
        super().__init__(main_window)
        self.main_window = main_window

    def connect_all(self) -> None:
        """Esegue tutte le connessioni dei segnali."""
        self.connect_global_signals()
        self.connect_sidebar_signals()

    def connect_global_signals(self) -> None:
        """
        Collega i segnali globali dei servizi core.
        - Notifiche -> Toast Manager & Tray Icon
        - Conteggio notifiche -> Badge Sidebar
        """
        # Toast Manager (In-app notification)
        NotificationManager.instance().request_toast.connect(
            lambda msg, t, d: ToastManager.instance().show(
                msg, t, d, is_rich_text=("<" in msg and ">" in msg)
            )
        )

        # Tray Icon (System notification)
        if hasattr(self.main_window, "tray_icon_component"):
            from PySide6.QtWidgets import QSystemTrayIcon  # noqa: PLC0415

            icon_map = {
                "info": QSystemTrayIcon.MessageIcon.Information,
                "success": QSystemTrayIcon.MessageIcon.Information,
                "warning": QSystemTrayIcon.MessageIcon.Warning,
                "error": QSystemTrayIcon.MessageIcon.Critical,
            }

            def show_tray_msg(msg: str, level: str, duration: int) -> None:
                """Formatta e mostra un messaggio nella tray icon di sistema."""
                title = "SyncroJob"
                if ":" in msg:
                    title, msg = msg.split(":", 1)
                self.main_window.tray_icon_component.show_message(
                    title.strip(),
                    msg.strip(),
                    icon_map.get(level, QSystemTrayIcon.MessageIcon.Information),
                    duration,
                )

            NotificationManager.instance().request_toast.connect(show_tray_msg)

        # Notification Badge on Sidebar
        sidebar = getattr(self.main_window, "sidebar", None)
        if sidebar:
            NotificationManager.instance().unread_count_changed.connect(
                sidebar.group_notifiche.header_btn.set_badge
            )
            sidebar.group_notifiche.header_btn.set_badge(NotificationManager.instance().get_unread_count())

    def connect_sidebar_signals(self) -> None:
        """
        Collega i segnali di interazione della barra laterale ai controller di navigazione.
        Gestisce i cambi pagina, l'apertura di tab specifici e la Command Palette.
        """
        sidebar = getattr(self.main_window, "sidebar", None)
        if not sidebar:
            return

        # La navigazione a 3 livelli  ora gestita centralmente dal NavigationController
        sidebar.navigation_requested.connect(self.main_window.navigation_controller.navigate_to)

        # Command Palette integration (MenuBarComponent handles the palette)
        if hasattr(self.main_window, "menu_bar_component"):
            sidebar.palette_requested.connect(self.main_window.menu_bar_component.open_command_palette)
