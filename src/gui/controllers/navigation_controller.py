"""
Controller per la gestione della navigazione tra i pannelli della UI.
Implementa il Lazy Loading per ottimizzare le prestazioni.
"""

import logging
from typing import Optional

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QMessageBox

# Importiamo PageIndex localmente o usiamo interi per evitare circular imports
# PageIndex mappa:
# 0: DASHBOARD
# 1: AUTOMAZIONI
# 2: LYRA
# 3: TIMBRATURE
# 4: STRUMENTALE
# 5: DATAEASE
# 6: ANAGRAFICHE
# 7: SETTINGS
# 8: HELP
# 9: NOTIFICATIONS
# 10: STORICO_ODA
# 11: DIPENDENTI

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
        creators = {
            0: self._create_dashboard,
            1: self._create_automazioni,
            2: self._create_lyra,
            3: self._create_timbrature,
            4: self._create_strumentale,
            5: self._create_dataease,
            6: self._create_anagrafiche,
            7: self._create_settings_panel,
            8: self._create_help,
            9: self._create_notifications,
            10: self._create_storico_oda,
            11: self._create_dipendenti,
        }

        if creator := creators.get(index):
            return creator()
        return None

    def _create_dashboard(self):
        from src.gui.panels import DashboardPanel

        self.mw.dashboard_panel = DashboardPanel()

        # Connetti AutopilotWidget al footer per aggiornamenti in tempo reale
        if hasattr(self.mw.dashboard_panel, "autopilot_widget"):
            # Aggiornamento Login Accounts
            if hasattr(self.mw, "footer_left"):
                self.mw.dashboard_panel.autopilot_widget.set_footer_widget(
                    self.mw.footer_left
                )

            # Aggiornamento Status Cards (Autopilot UI)
            if hasattr(self.mw, "status_bar_component"):
                self.mw.dashboard_panel.autopilot_widget.set_status_bar(
                    self.mw.status_bar_component
                )

        return self.mw.dashboard_panel

    def _create_automazioni(self):
        from src.gui.widgets.automazioni_widget import AutomazioniWidget

        self.mw.automazioni_widget = AutomazioniWidget(self.mw)
        return self.mw.automazioni_widget

    def _create_lyra(self):
        from src.gui.panels import LyraPanel

        self.mw.lyra_panel = LyraPanel()
        return self.mw.lyra_panel

    def _create_timbrature(self):
        from src.gui.panels import TimbratureDBPanel

        self.mw.timbrature_db_panel = TimbratureDBPanel()
        return self.mw.timbrature_db_panel

    def _create_strumentale(self):
        from src.gui.panels import ContabilitaPanel

        self.mw.contabilita_panel = ContabilitaPanel()
        return self.mw.contabilita_panel

    def _create_dataease(self):
        from src.gui.panels import ScaricoOrePanel

        self.mw.scarico_ore_panel = ScaricoOrePanel()
        return self.mw.scarico_ore_panel

    def _create_anagrafiche(self):
        from src.gui.panels import PDLDBPanel

        self.mw.pdl_db_panel = PDLDBPanel()
        return self.mw.pdl_db_panel

    def _create_storico_oda(self):
        from src.gui.panels import StoricoOdaPanel

        self.mw.storico_oda_panel = StoricoOdaPanel()
        return self.mw.storico_oda_panel

    def _create_dipendenti(self):
        from src.gui.panels.dipendenti.main_panel import DipendentiPanel

        self.mw.dipendenti_panel = DipendentiPanel()
        return self.mw.dipendenti_panel

    def _create_help(self):
        from src.gui.panels import HelpPanel

        self.mw.help_panel = HelpPanel()
        return self.mw.help_panel

    def _create_notifications(self):
        from src.gui.panels import NotificationsPanel

        self.mw.notifications_panel = NotificationsPanel()
        return self.mw.notifications_panel

    def _create_settings_panel(self) -> QObject:
        """Crea e configura il pannello impostazioni."""
        from src.gui.panels import SettingsPanel

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

        # Timbrature Bot -> Dipendenti (Anagrafica)
        if (
            hasattr(self.mw, "timbrature_bot_panel")
            and hasattr(self.mw, "dipendenti_panel")
            and not getattr(self.mw, "_timbrature_dipendenti_signals_connected", False)
        ):
            try:
                self.mw.timbrature_bot_panel.data_updated.connect(
                    self.mw.dipendenti_panel.refresh_data
                )
                self.mw._timbrature_dipendenti_signals_connected = True
                logger.info("Signal: Timbrature Bot -> Dipendenti connected.")
            except Exception as e:
                logger.error(f"Signal Timbrature -> Dipendenti Connection Failed: {e}")

        # PDL Search -> PDL DB
        if (
            hasattr(self.mw, "pdl_search_panel")
            and hasattr(self.mw, "pdl_db_panel")
            and not getattr(self.mw, "_pdl_signals_connected", False)
        ):
            try:
                self.mw.pdl_search_panel.data_updated.connect(
                    self.mw.pdl_db_panel.refresh_data
                )
                self.mw._pdl_signals_connected = True
                logger.info("Signal: PDL Search -> DB connected.")
            except Exception as e:
                logger.error(f"Signal: PDL Search Connection Failed: {e}")

    def navigate_to(self, index: int, sub_index: Optional[int] = None):
        """Navigazione con Lazy Loading."""
        if index == self.mw._current_page_index and sub_index is None:
            self.mw.sidebar.set_active_button(index)
            return

        # Controllo salvataggio impostazioni se stiamo lasciando il pannello SETTINGS (7)
        if self.mw._current_page_index == 7 and hasattr(self.mw, "settings_panel"):
            if self.mw.settings_panel.has_unsaved_changes():
                if not self.mw.settings_panel.prompt_save_if_needed():
                    self.mw.sidebar.set_active_button(self.mw._current_page_index)
                    return

        # Assicurati che il pannello di destinazione sia caricato
        self.get_panel(index)

        self.mw._current_page_index = index
        self.mw.page_stack.setCurrentIndex(index)
        self.mw.sidebar.set_active_button(index, sub_index)

    def navigate_to_extended(self, tab_idx, query):
        """Naviga a un tab specifico di Contabilità."""
        self.navigate_to(4, sub_index=tab_idx)  # STRUMENTALE
        self.mw.contabilita_panel.main_tabs.setCurrentIndex(tab_idx)
        self.mw.contabilita_panel.set_search_query(query)

    def navigate_to_dataease(self, query):
        """Naviga a Scarico Ore (DataEase)."""
        self.navigate_to(5)  # DATAEASE
        self.mw.scarico_ore_panel.search_input.setText(query)

    def navigate_to_timbrature(self, query):
        """Naviga a Timbrature DB."""
        self.navigate_to(3)  # TIMBRATURE
        self.mw.timbrature_db_panel.search_input.setText(query)

    def navigate_to_panel(self, panel_key: str):
        """Navigazione verso pannelli annidati."""
        bot_map = {
            # Portale Fornitori (main_idx=0)
            "dettagli_oda": (0, 0),
            "scarico_ts": (0, 1),
            "timbrature": (0, 2),
            "prenota_bp": (0, 3),
            "carico_ts": (0, 4),
            # SafeWork (main_idx=1)
            "scarico_pdl": (1, 0),
            "ricerca_pdl": (1, 1),
        }

        if panel_key in bot_map:
            main_idx, sub_idx = bot_map[panel_key]
            self.navigate_to(1, sub_index=main_idx)  # AUTOMAZIONI

            # Recupera il widget automazioni (ora dovrebbe essere inizializzato)
            auto_widget = getattr(self.mw, "automazioni_widget", None)

            if auto_widget:
                # Usa il metodo dedicato che include logging e refresh
                auto_widget.set_active_tab(main_idx, sub_idx)
            return

        db_map = {
            "db_timbrature": 3,
            "db_strumentale": 4,
            "db_dataease": 5,
            "db_dipendenti": 11,
            "nav_page_11": 11,
        }
        if panel_key in db_map:
            self.navigate_to(db_map[panel_key])
            return

    def analyze_with_lyra(self, context_text: str):
        """Passa alla vista Lyra."""
        self.navigate_to(2)  # LYRA
        self.mw.lyra_panel.ask_lyra(
            "Analizza questi dati e dimmi se ci sono anomalie.", context_text
        )
