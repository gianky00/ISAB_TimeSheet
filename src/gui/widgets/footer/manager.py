from PyQt6.QtWidgets import QWidget

from .business_info import FooterLeftWidget
from .components import StartupConsole
from .status_bar import FooterRightWidget


class FooterStatsManager(QWidget):
    """Manager centrale per il footer: gestisce la transizione tra FASE 1 e FASE 2."""

    def __init__(
        self,
        left_widget: FooterLeftWidget,
        center_console: StartupConsole,
        right_widget: FooterRightWidget,
        parent=None,
    ):
        super().__init__(parent)
        self.left_widget = left_widget
        self.center_console = center_console
        self.right_widget = right_widget
        self.phase = "boot"

    def transition_to_operational(
        self, client_name: str = "", expiry: str = "", last_login: str = ""
    ):
        self.phase = "operational"
        self.center_console.setText("✓ Sistema SyncroJob pronto.")
        self.right_widget.show_operational()
        if client_name or expiry or last_login:
            self.left_widget.update_info(client_name, expiry, last_login)

    def log_boot_message(self, message: str, is_error: bool = False):
        if self.phase == "boot":
            self.center_console.log(message, is_error)
