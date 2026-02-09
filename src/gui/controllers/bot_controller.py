"""
Controller per il coordinamento dei Bot e l'aggiornamento dello stato UI.
"""

import os
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget


class BotController(QObject):
    """
    Gestisce l'interazione tra i pannelli Bot, il servizio Telegram
    e i widget di stato della UI.
    """

    def __init__(self, main_window: Any, telegram_service: Any) -> None:
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service
        self.panels: list[Any] = []

    def register_panels(self, panels: list[Any]) -> None:
        """Registra i pannelli bot per monitorarne segnali e risultati."""
        self.panels = panels
        for panel in self.panels:
            # Connessione segnali risultati (se presenti)
            if hasattr(panel, "bot_results_ready"):
                panel.bot_results_ready.connect(self._handle_bot_results)

            # Connessione segnali stato
            if hasattr(panel, "status_changed"):
                panel.status_changed.connect(self._on_panel_status_changed)

    def _handle_bot_results(self, bot_id: str, results: list[str]) -> None:
        """Gestisce i risultati prodotti dai bot e li invia a Telegram."""
        if bot_id == "scarico_pdl":
            for file_path in results:
                if Path(file_path).exists():
                    self.telegram.send_document_sync(
                        file_path,
                        caption=f"📄 **PDL Scaricato**\nFile: `{os.path.basename(file_path)}`",
                    )

    def _on_panel_status_changed(self, status: str, message: str) -> None:
        """Aggiorna la card di stato appropriata (SafeWork o Portale) in base al bot."""
        sender = self.sender()
        bot_id = getattr(sender, "bot_id", "")

        # SafeWork bots list
        safework_bots = ["scarico_pdl", "pdl_search"]

        # Update the correct status card based on bot_id
        # Note: status is the color code, message is the text
        if bot_id in safework_bots:
            if hasattr(self.mw, "status_safework"):
                self.mw.status_safework.setStatus(message, status)
        else:  # Default to Portale Fornitori bots
            if hasattr(self.mw, "status_portale"):
                self.mw.status_portale.setStatus(message, status)

    def _get_active_bot_panel(self) -> QWidget | None:
        """Determina quale pannello bot è attualmente visibile nella UI."""
        if not hasattr(self.mw, "automazioni_widget"):
            return None

        auto_widget = self.mw.automazioni_widget
        if not auto_widget:
            return None

        main_idx = auto_widget.currentIndex()
        if main_idx == 0 and hasattr(auto_widget, "tab_fornitori"):  # Portale Fornitori
            panel = auto_widget.tab_fornitori.currentWidget()
            return panel if isinstance(panel, QWidget) else None
        if main_idx == 1 and hasattr(auto_widget, "tab_safework"):  # SafeWork
            panel = auto_widget.tab_safework.currentWidget()
            return panel if isinstance(panel, QWidget) else None
        return None

    # Removed update_global_status as it's no longer relevant with separate cards
