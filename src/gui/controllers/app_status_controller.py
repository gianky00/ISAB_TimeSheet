"""SyncroJob - App Status Controller.

Gestisce la rotazione degli account e le impostazioni del motore di automazione.
Aderisce al principio SRP separando la gestione dello stato dell'app dalla MainWindow.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.application.services import config_manager
from src.gui.widgets.toast import ToastManager

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow

logger = logging.getLogger("AppStatusController")


class AppStatusController:
    """Controller per la gestione degli stati e delle impostazioni globali dell'applicazione.

    Inizializza il controller di stato.

    Args:
        main_window: Riferimento alla finestra principale per l'aggiornamento dell'UI.
    """

    def __init__(self, main_window: MainWindow) -> None:
        self.mw = main_window

    def rotate_account(self, bot_type: str) -> None:
        """Ruota l'account attivo per il portale specificato."""
        if config_manager.switch_default_account(bot_type):
            if hasattr(self.mw, "status_bar_component"):
                self.mw.status_bar_component.show_operational_state()
                if hasattr(self.mw.status_bar_component, "footer_left") and hasattr(
                    self.mw.status_bar_component.footer_left, "refresh_accounts"
                ):
                    self.mw.status_bar_component.footer_left.refresh_accounts()
            ToastManager.instance().show(f"Account {bot_type.upper()} ruotate con successo.", "success")
        else:
            ToastManager.instance().show(f"Impossibile ruotare account {bot_type.upper()}.", "warning")

    def switch_engine(self) -> None:
        """Ruota il motore di automazione attivo tra Selenium e Playwright."""
        current = config_manager.get_config_value("automation_engine", "selenium").lower()
        new_engine = "playwright" if current == "selenium" else "selenium"

        if config_manager.set_config_value("automation_engine", new_engine):
            if hasattr(self.mw, "status_bar_component") and hasattr(
                self.mw.status_bar_component, "footer_left"
            ):
                self.mw.status_bar_component.footer_left.refresh_accounts()
            ToastManager.instance().show(f"Motore automazione: {new_engine.upper()}", "success")
        else:
            ToastManager.instance().show("Errore cambio motore.", "error")

    def switch_headless(self) -> None:
        """Ruota la modalità browser tra visibile e nascosta (headless)."""
        current = config_manager.get_config_value("browser_headless", False)
        new_state = not current

        if config_manager.set_config_value("browser_headless", new_state):
            if hasattr(self.mw, "status_bar_component") and hasattr(
                self.mw.status_bar_component, "footer_left"
            ):
                self.mw.status_bar_component.footer_left.refresh_accounts()
            mode = "NASCOSTO" if new_state else "VISIBILE"
            ToastManager.instance().show(f"Browser: {mode}", "success")
        else:
            ToastManager.instance().show("Errore cambio modalità browser.", "error")
