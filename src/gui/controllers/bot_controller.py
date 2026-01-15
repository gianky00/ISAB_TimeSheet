"""
Controller per il coordinamento dei Bot e l'aggiornamento dello stato UI.
"""

import os

from PyQt6.QtCore import QObject


class BotController(QObject):
    """
    Gestisce l'interazione tra i pannelli Bot, il servizio Telegram
    e i widget di stato della UI.
    """

    def __init__(self, main_window, telegram_service):
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service
        self.panels = []

    def register_panels(self, panels: list):
        """Registra i pannelli bot per monitorarne segnali e risultati."""
        self.panels = panels
        for panel in self.panels:
            # Connessione segnali risultati (se presenti)
            if hasattr(panel, "bot_results_ready"):
                panel.bot_results_ready.connect(self._handle_bot_results)

            # Connessione segnali stato
            if hasattr(panel, "status_changed"):
                panel.status_changed.connect(self._on_panel_status_changed)

    def _handle_bot_results(self, bot_id, results):
        """Gestisce i risultati prodotti dai bot e li invia a Telegram."""
        if bot_id == "scarico_pdl":
            for file_path in results:
                if os.path.exists(file_path):
                    self.telegram.send_document_sync(
                        file_path,
                        caption=f"📄 **PDL Scaricato**\nFile: `{os.path.basename(file_path)}`",
                    )

    def _on_panel_status_changed(self, status, message):
        """Aggiorna la card di stato appropriata (SafeWork o Portale) in base al bot."""
        sender = self.sender()
        bot_id = getattr(sender, "bot_id", "")

        # Update the correct status card based on bot_id
        if bot_id in ["scarico_pdl"]:  # SafeWork bots
            if hasattr(self.mw, "status_safework"):
                self.mw.status_safework.setStatus(status, message)
        else:  # Default to Portale Fornitori bots
            if hasattr(self.mw, "status_portale"):
                self.mw.status_portale.setStatus(status, message)

    def _get_active_bot_panel(self):
        """Determina quale pannello bot è attualmente visibile nella UI."""
        if not hasattr(self.mw, "automazioni_widget") or not self.mw.automazioni_widget:
            return None

        main_idx = self.mw.automazioni_widget.currentIndex()
        if main_idx == 0:  # Portale Fornitori
            return self.mw.tab_fornitori.currentWidget()
        elif main_idx == 1:  # SafeWork
            return self.mw.tab_safework.currentWidget()
        return None

    # Removed update_global_status as it's no longer relevant with separate cards
