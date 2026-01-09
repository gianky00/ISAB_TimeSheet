"""
Controller per la gestione della navigazione tra i pannelli della UI.
"""

from PyQt6.QtCore import QObject

class NavigationController(QObject):
    """
    Gestisce il routing interno dell'applicazione, permettendo 
    di passare da una pagina all'altra con filtri specifici.
    """

    def __init__(self, main_window):
        super().__init__(main_window)
        self.mw = main_window

    def navigate_to(self, index: int):
        """Navigazione base con controllo salvataggio."""
        # Se stiamo già sulla pagina richiesta, non fare nulla
        if index == self.mw._current_page_index:
            self.mw.sidebar.set_active_button(index)
            return

        # Se stiamo lasciando la pagina delle impostazioni, controlla le modifiche
        if self.mw._current_page_index == 4:
            if self.mw.settings_panel.has_unsaved_changes():
                if not self.mw.settings_panel.prompt_save_if_needed():
                    self.mw.sidebar.set_active_button(self.mw._current_page_index)
                    return

        self.mw._current_page_index = index
        self.mw.page_stack.setCurrentIndex(index)
        self.mw.sidebar.set_active_button(index)

    def navigate_to_extended(self, tab_idx, query):
        """Naviga a un tab specifico di Contabilità e imposta il filtro."""
        self.navigate_to(3)  # Database
        self.mw.database_widget.setCurrentIndex(1)  # Contabilità
        self.mw.contabilita_panel.main_tabs.setCurrentIndex(tab_idx)
        self.mw.contabilita_panel.set_search_query(query)

    def navigate_to_dataease(self, query):
        """Naviga a Scarico Ore (DataEase)."""
        self.navigate_to(3)
        self.mw.database_widget.setCurrentIndex(2)  # DataEase
        self.mw.scarico_ore_panel.search_input.setText(query)

    def navigate_to_timbrature(self, query):
        """Naviga a Timbrature DB."""
        self.navigate_to(3)
        self.mw.database_widget.setCurrentIndex(0)  # Timbrature
        self.mw.timbrature_db_panel.search_input.setText(query)

    def navigate_to_panel(self, panel_key: str):
        """
        Naviga a un pannello specifico (usato dalla Dashboard).
        Keys: 'dettagli_oda', 'scarico_ts', 'timbrature', 'carico_ts'
              'db_timbrature', 'db_strumentale', 'db_dataease'
        """
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
        """Passa alla vista Lyra e analizza il contesto fornito."""
        self.navigate_to(2)  # Switch to Lyra
        self.mw.lyra_panel.ask_lyra(
            "Analizza questi dati e dimmi se ci sono anomalie o punti di attenzione.", context_text
        )
