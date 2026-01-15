"""
Controller per la gestione della navigazione tra i pannelli della UI.
Implementa il Lazy Loading per ottimizzare le prestazioni.
"""

import logging
from typing import Optional

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
        panel = self.mw.page_stack.widget(index)

        # Se il pannello è già stato creato, lo restituiamo
        if getattr(self.mw, f"_panel_initialized_{index}", False):
            return panel

        logger.info(f"Lazy Loading pannello all'indice: {index}")

        try:
            new_panel = self._create_panel_by_index(index)
            if new_panel:
                self._initialize_new_panel(index, new_panel)
                return new_panel
        except Exception as e:
            self._handle_panel_error(index, e)

        return panel

    def _create_panel_by_index(self, index: int) -> Optional[QObject]:
        """Factory method per la creazione dei pannelli in base all'indice."""
        if index == 0:
            from src.gui.dashboard_panel import DashboardPanel

            self.mw.dashboard_panel = DashboardPanel()
            return self.mw.dashboard_panel

        if index == 1:
            from src.gui.widgets.automazioni_widget import AutomazioniWidget

            self.mw.automazioni_widget = AutomazioniWidget(self.mw)
            return self.mw.automazioni_widget

        if index == 2:
            from src.gui.lyra_panel import LyraPanel

            self.mw.lyra_panel = LyraPanel()
            return self.mw.lyra_panel

        if index == 3:
            from src.gui.widgets.database_widget import DatabaseWidget

            self.mw.database_widget = DatabaseWidget(self.mw)
            return self.mw.database_widget

        if index == 4:
            return self._create_settings_panel()

        if index == 5:
            from src.gui.help_panel import HelpPanel

            self.mw.help_panel = HelpPanel()
            return self.mw.help_panel

        if index == 6:
            from src.gui.notifications_panel import NotificationsPanel

            self.mw.notifications_panel = NotificationsPanel()
            return self.mw.notifications_panel

        return None

    def _create_settings_panel(self) -> QObject:
        """Crea e configura il pannello impostazioni."""
        from src.gui.settings_panel import SettingsPanel

        panel = SettingsPanel()
        self.mw.settings_panel = panel
        panel.settings_saved.connect(self.mw._on_settings_saved)
        panel.request_help_section.connect(self.mw._on_help_requested)
        return panel

    def _initialize_new_panel(self, index: int, new_panel: QObject):
        """Sostituisce il placeholder e inizializza lo stato del pannello."""
        old_placeholder = self.mw.page_stack.widget(index)
        self.mw.page_stack.removeWidget(old_placeholder)
        self.mw.page_stack.insertWidget(index, new_panel)
        setattr(self.mw, f"_panel_initialized_{index}", True)
        self._try_connect_signals()

    def _handle_panel_error(self, index: int, e: Exception):
        """Gestisce errori critici durante il caricamento dei moduli UI."""
        import traceback

        logger.error(f"❌ Critical Error loading panel {index}: {e}")
        logger.error(traceback.format_exc())
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.critical(
            self.mw,
            "Errore Caricamento",
            f"Impossibile caricare il modulo.\nErrore: {e}",
        )

    def _try_connect_signals(self):
        """
        Tenta di collegare i segnali tra pannelli che dipendono l'uno dall'altro
        quando entrambi sono stati inizializzati.
        """
        # Timbrature Bot -> Timbrature DB
        if (
            hasattr(self.mw, "timbrature_bot_panel")
            and hasattr(self.mw, "timbrature_db_panel")
            and not getattr(self.mw, "_timbrature_signals_connected", False)
        ):
            try:
                self.mw.timbrature_bot_panel.data_updated.connect(
                    self.mw.timbrature_db_panel.refresh_data
                )
                self.mw._timbrature_signals_connected = True
                logger.info("Signal: Timbrature Bot -> DB connected.")
            except Exception as e:
                logger.error(f"Signal Connection Failed: {e}")

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
            "prenota_bp": (0, 3),
            "carico_ts": (0, 4),
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
