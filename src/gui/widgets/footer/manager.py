"""
SyncroJob - Footer Manager
Coordinatore della barra di stato che gestisce la transizione dalla fase di avvio (Boot) a quella operativa.
"""

from PySide6.QtWidgets import QWidget

from .business_info import FooterLeftWidget
from .components import StartupConsole
from .status_bar import FooterRightWidget


class FooterStatsManager(QWidget):
    """
    Manager centrale per il footer: gestisce la transizione tra FASE 1 (Boot) e FASE 2 (Operativa).
    Coordina i widget sinistro, centrale e destro per riflettere lo stato globale del sistema.
    """

    def __init__(
        self,
        left_widget: FooterLeftWidget,
        center_console: StartupConsole,
        right_widget: FooterRightWidget,
        parent: QWidget | None = None,
    ) -> None:
        """
        Inizializza il manager del footer.

        Args:
          left_widget: Widget per le info aziendali.
          center_console: Console per i log di avvio.
          right_widget: Widget per il progresso e lo stato bot.
          parent: Widget genitore.
        """
        super().__init__(parent)
        self.left_widget = left_widget
        self.center_console = center_console
        self.right_widget = right_widget
        self.phase = "boot"

    def transition_to_operational(
        self, client_name: str = "", expiry: str = "", last_login: str = ""
    ) -> None:
        """
        Esegue la transizione visiva alla fase operativa.
        Nasconde la telemetria di avvio e mostra gli stati dei portali.

        Args:
          client_name: Nome del cliente licenziatario.
          expiry: Data scadenza licenza.
          last_login: Data ultimo accesso.
        """
        self.phase = "operational"
        self.center_console.setText("  Sistema SyncroJob pronto.")
        self.right_widget.show_operational()
        if client_name or expiry or last_login:
            self.left_widget.update_info(client_name, expiry, last_login)

    def log_boot_message(self, message: str, is_error: bool = False) -> None:
        """
        Invia un messaggio di log alla console centrale durante il boot.

        Args:
          message: Testo del messaggio.
          is_error: Se il messaggio rappresenta un errore.
        """
        if self.phase == "boot":
            self.center_console.log(message, is_error)
