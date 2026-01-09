"""
Controller per la gestione della navigazione tra i pannelli della UI.
Implementa il Lazy Loading per ottimizzare le prestazioni.
"""

import logging

from PyQt6.QtCore import QObject

logger = logging.getLogger(__name__)


class NavigationController(QObject):
    """
    Gestisce il routing interno dell'applicazione.
    Carica i pannelli "on-demand" quando richiesto.
    """

    def __init__(self, main_window):
        super().__init__(main_window)
        self.mw = main_window

    def get_panel(self, index: int):
        """Restituisce il pannello all'indice specificato, creandolo se necessario."""
        # Se il pannello è già stato creato, lo restituiamo
        panel = self.mw.page_stack.widget(index)

        # Se il widget è un placeholder (o se vogliamo essere sicuri tramite attributo)
        if hasattr(self.mw, f"_panel_initialized_{index}") and getattr(
            self.mw, f"_panel_initialized_{index}"
        ):
            return panel

        logger.info(f"Lazy Loading pannello all'indice: {index}")

        # Creazione dinamica in base all'indice
        new_panel = None

        if index == 0:
            from src.gui.dashboard_panel import DashboardPanel

            new_panel = DashboardPanel()
            self.mw.dashboard_panel = new_panel
        elif index == 1:
            from src.gui.main_window import AutomazioniWidget

            new_panel = AutomazioniWidget(self.mw)
            self.mw.automazioni_widget = new_panel
        elif index == 2:
            from src.gui.lyra_panel import LyraPanel

            new_panel = LyraPanel()
            self.mw.lyra_panel = new_panel
        elif index == 3:
            from src.gui.main_window import DatabaseWidget

            new_panel = DatabaseWidget(self.mw)
            self.mw.database_widget = new_panel
        elif index == 4:
            from src.gui.settings_panel import SettingsPanel

            new_panel = SettingsPanel()
            self.mw.settings_panel = new_panel
            # Connetti segnali vitali delle impostazioni
            new_panel.settings_saved.connect(self.mw._on_settings_saved)
            new_panel.request_help_section.connect(self.mw._on_help_requested)
        elif index == 5:
            from src.gui.help_panel import HelpPanel

            new_panel = HelpPanel()
            self.mw.help_panel = new_panel
        elif index == 6:
            from src.gui.notifications_panel import NotificationsPanel

            new_panel = NotificationsPanel()
            self.mw.notifications_panel = new_panel

        if new_panel:
            # Rimpiazza il placeholder nello stack
            old_placeholder = self.mw.page_stack.widget(index)
            self.mw.page_stack.removeWidget(old_placeholder)
            self.mw.page_stack.insertWidget(index, new_panel)
            setattr(self.mw, f"_panel_initialized_{index}", True)

            return new_panel

        return panel

    def navigate_to(self, index: int):
        """Navigazione con Lazy Loading."""
        if index == self.mw._current_page_index:
            self.mw.sidebar.set_active_button(index)
            return

        # Controllo salvataggio impostazioni se stiamo lasciando il pannello 4
        if self.mw._current_page_index == 4 and hasattr(self.mw, "settings_panel"):
            if self.mw.settings_panel.has_unsaved_changes():
                if not self.mw.settings_panel.prompt_save_if_needed():
                    self.mw.sidebar.set_active_button(self.mw._current_page_index)
                    return

        # Assicurati che il pannello di destinazione sia caricato
        self.get_panel(index)

        self.mw._current_page_index = index
        self.mw.page_stack.setCurrentIndex(index)
        self.mw.sidebar.set_active_button(index)

    def navigate_to_extended(self, tab_idx, query):
        """Naviga a un tab specifico di Contabilità."""
        self.navigate_to(3)  # Assicura caricamento DatabaseWidget
        self.mw.database_widget.setCurrentIndex(1)  # Contabilità
        self.mw.contabilita_panel.main_tabs.setCurrentIndex(tab_idx)
        self.mw.contabilita_panel.set_search_query(query)

    def navigate_to_dataease(self, query):
        """Naviga a Scarico Ore (DataEase)."""
        self.navigate_to(3)
        self.mw.database_widget.setCurrentIndex(2)
        self.mw.scarico_ore_panel.search_input.setText(query)

    def navigate_to_timbrature(self, query):
        """Naviga a Timbrature DB."""
        self.navigate_to(3)
        self.mw.database_widget.setCurrentIndex(0)
        self.mw.timbrature_db_panel.search_input.setText(query)

    def navigate_to_panel(self, panel_key: str):
        """Navigazione verso pannelli annidati."""
        bot_map = {
            "dettagli_oda": (0, 0),
            "scarico_ts": (0, 1),
            "timbrature": (0, 2),
            "carico_ts": (0, 3),
            "scarico_pdl": (1, 0),
        }

        if panel_key in bot_map:
            main_idx, sub_idx = bot_map[panel_key]
            self.navigate_to(1)
            self.mw.automazioni_widget.setCurrentIndex(main_idx)
            if main_idx == 0:
                self.mw.tab_fornitori.setCurrentIndex(sub_idx)
            elif main_idx == 1:
                self.mw.tab_safework.setCurrentIndex(sub_idx)
            return

        db_map = {"db_timbrature": 0, "db_strumentale": 1, "db_dataease": 2}
        if panel_key in db_map:
            self.navigate_to(3)
            self.mw.database_widget.setCurrentIndex(db_map[panel_key])
            return

    def analyze_with_lyra(self, context_text: str):
        """Passa alla vista Lyra."""
        self.navigate_to(2)
        self.mw.lyra_panel.ask_lyra(
            "Analizza questi dati e dimmi se ci sono anomalie.", context_text
        )
