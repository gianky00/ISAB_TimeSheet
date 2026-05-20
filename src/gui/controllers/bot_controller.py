"""
SyncroJob - Bot Controller
Orchestratore per il coordinamento delle attività dei bot Selenium e l'aggiornamento dinamico della UI.
Gestisce il bridge tra i segnali emessi dai pannelli bot, il servizio di messaggistica Telegram
e le card di stato globali presenti nel footer della MainWindow.
"""

import os
from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget


class BotController(QObject):
    """
    Controller centrale per il monitoraggio e la notifica dello stato delle automazioni.
    Si occupa di:
    - Collegare i segnali di stato di ogni pannello bot alle card informative (Portale/SafeWork).
    - Inoltrare i file prodotti dai bot (es. PDF dei PDL) direttamente sul canale Telegram.
    - Identificare il pannello bot attualmente attivo per operazioni contestuali.
    """

    def __init__(self, main_window: Any, telegram_service: Any) -> None:
        """
        Inizializza il bot controller.

        Args:
          main_window: Riferimento alla MainWindow (per accesso alle status card).
          telegram_service: Istanza del TelegramService per l'invio di notifiche e file.
        """
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service
        self.panels: list[Any] = []

    def register_panels(self, panels: list[Any]) -> None:
        """
        Sottoscrive il controller ai segnali di ogni pannello bot registrato.

        Args:
          panels: Lista di widget bot (che ereditano tipicamente da BaseBotPanel).
        """
        self.panels = panels
        for panel in self.panels:
            if hasattr(panel, "bot_results_ready"):
                panel.bot_results_ready.connect(self._handle_bot_results)
            if hasattr(panel, "status_changed"):
                panel.status_changed.connect(self._on_panel_status_changed)
            if hasattr(panel, "autopilot_changed"):
                panel.autopilot_changed.connect(self._on_autopilot_trigger)

    def _handle_bot_results(self, bot_id: str, results: list[str]) -> None:
        """
        Reagisce al completamento di un bot inviando i file prodotti a Telegram.
        Specializzato per lo scarico PDL.

        Args:
          bot_id: Identificatore del bot che ha prodotto i risultati.
          results: Lista di percorsi file generati.
        """
        if bot_id == "scarico_pdl":
            for file_path in results:
                if Path(file_path).exists():
                    self.telegram.send_document_sync(
                        file_path,
                        caption=f"   **PDL Scaricato**\nFile: `{os.path.basename(file_path)}`",
                    )

    def _on_panel_status_changed(self, status: str, message: str) -> None:
        """
        Aggiorna le card di stato nel footer in base all'appartenenza del bot (Portale o SafeWork).

        Args:
          status: Codice colore HEX per l'indicatore visuale.
          message: Testo descrittivo dello stato (es. 'Esecuzione in corso...').
        """
        sender = self.sender()
        bot_id = getattr(sender, "bot_id", "")
        safework_bots = ["scarico_pdl", "ricerca_pdl"]

        if bot_id in safework_bots:
            if hasattr(self.mw, "status_safework"):
                self.mw.status_safework.setStatus(message, status)
        elif hasattr(self.mw, "status_portale"):
            self.mw.status_portale.setStatus(message, status)

    def _on_autopilot_trigger(self) -> None:
        """Aggiorna globalmente la UI dell'Autopilot (Barra di stato e Dashboard)."""
        # 1. Update StatusBar indicators
        if hasattr(self.mw, "status_bar_component"):
            self.mw.status_bar_component.update_autopilot_ui()

        # 2. Update Dashboard cards if visible
        if hasattr(self.mw, "dashboard_panel"):
            self.mw.dashboard_panel.refresh_live_data()

    def _get_active_bot_panel(self) -> QWidget | None:
        """
        Individua il pannello bot attualmente visualizzato dall'utente navigando tra i tab.

        Returns:
          Optional[QWidget]: Il pannello attivo o None se non identificato.
        """
        if not hasattr(self.mw, "automazioni_widget") or not self.mw.automazioni_widget:
            return None

        auto_widget = self.mw.automazioni_widget
        main_idx = auto_widget.currentIndex()

        tab_fornitori_idx = 0
        tab_safework_idx = 1

        if main_idx == tab_fornitori_idx and hasattr(auto_widget, "tab_fornitori"):
            panel = auto_widget.tab_fornitori.currentWidget()
            return panel if isinstance(panel, QWidget) else None
        if main_idx == tab_safework_idx and hasattr(auto_widget, "tab_safework"):
            panel = auto_widget.tab_safework.currentWidget()
            return panel if isinstance(panel, QWidget) else None
        return None
