"""
SyncroJob - Navigation Controller
Gestore centrale del routing e della navigazione tra i diversi pannelli dell'interfaccia utente.
Implementa una strategia di 'Lazy Loading' (caricamento differito) per ridurre drasticamente i tempi di startup
dell'applicazione, inizializzando i moduli funzionali solo quando vengono effettivamente richiesti dall'utente.
"""

import logging
from typing import TYPE_CHECKING, Any

from PyQt6.QtWidgets import QMessageBox, QStackedWidget, QWidget

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


class NavigationController:
    """
    Controller responsabile della commutazione tra le pagine nel QStackedWidget della MainWindow.
    Gestisce il ciclo di vita dei pannelli (creazione, inizializzazione segnali, visualizzazione)
    e garantisce la sincronizzazione con lo stato della Sidebar e della Command Palette.
    """

    def __init__(self, main_window: Any) -> None:
        """
        Inizializza il controller di navigazione.

        Args:
            main_window: Riferimento alla MainWindow dell'applicazione.
        """
        self.mw = main_window

    def get_panel(self, index: int) -> QWidget | None:
        """
        Recupera un pannello in base al suo indice, creandolo dinamicamente se non ancora inizializzato.

        Args:
            index: Indice numerico della pagina (riferimento a PageIndex).

        Returns:
            Optional[QWidget]: L'istanza del pannello caricato o None in caso di errore.
        """
        page_stack = self.mw.page_stack
        if not isinstance(page_stack, QStackedWidget):
            return None

        panel = page_stack.widget(index)
        if getattr(self.mw, f"_panel_initialized_{index}", False):
            if isinstance(panel, QWidget):
                return panel
            return None

        logger.info(f"Lazy Loading pannello all'indice: {index}")
        try:
            new_panel = self._create_panel_by_index(index)
            if new_panel:
                self._initialize_new_panel(index, new_panel)
                return new_panel
        except Exception as e:
            self._handle_panel_error(index, e)

        if isinstance(panel, QWidget):
            return panel
        return None

    def _create_panel_by_index(self, index: int) -> QWidget | None:
        """Factory method che mappa gli indici alle funzioni di creazione dei widget pannello."""
        creators: dict[int, Callable[[], QWidget]] = {
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

    def _create_dashboard(self) -> QWidget:
        """Crea la dashboard e la collega al sistema di monitoraggio del footer."""
        from src.gui.panels import DashboardPanel

        panel = DashboardPanel()
        self.mw.dashboard_panel = panel
        if hasattr(panel, "autopilot_widget"):
            if hasattr(self.mw, "footer_left"):
                panel.autopilot_widget.set_footer_widget(self.mw.footer_left)
            if hasattr(self.mw, "status_bar_component"):
                panel.autopilot_widget.set_status_bar(self.mw.status_bar_component)
        return panel

    def _create_automazioni(self) -> QWidget:
        """Crea il selettore centralizzato per le automazioni bot."""
        from src.gui.widgets.automazioni_widget import AutomazioniWidget

        panel = AutomazioniWidget(self.mw)
        self.mw.automazioni_widget = panel
        return panel

    def _create_lyra(self) -> QWidget:
        """Inizializza l'assistente virtuale Lyra."""
        from src.gui.panels import LyraPanel

        panel = LyraPanel()
        self.mw.lyra_panel = panel
        return panel

    def _create_timbrature(self) -> QWidget:
        """Inizializza il visualizzatore del database timbrature."""
        from src.gui.panels import TimbratureDBPanel

        panel = TimbratureDBPanel()
        self.mw.timbrature_db_panel = panel
        return panel

    def _create_strumentale(self) -> QWidget:
        """Inizializza il pannello contabilità strumentale."""
        from src.gui.panels import ContabilitaPanel

        panel = ContabilitaPanel()
        self.mw.contabilita_panel = panel
        return panel

    def _create_dataease(self) -> QWidget:
        """Inizializza il visualizzatore virtualizzato Scarico Ore."""
        from src.gui.panels import ScaricoOrePanel

        panel = ScaricoOrePanel()
        self.mw.scarico_ore_panel = panel
        return panel

    def _create_anagrafiche(self) -> QWidget:
        """Inizializza il database anagrafiche PDL."""
        from src.gui.panels import PDLDBPanel

        panel = PDLDBPanel()
        self.mw.pdl_db_panel = panel
        return panel

    def _create_storico_oda(self) -> QWidget:
        """Inizializza la consultazione dello storico OdA."""
        from src.gui.panels import StoricoOdaPanel

        panel = StoricoOdaPanel()
        self.mw.storico_oda_panel = panel
        return panel

    def _create_dipendenti(self) -> QWidget:
        """Inizializza la gestione organica delle risorse umane."""
        from src.gui.panels.dipendenti.main_panel import DipendentiPanel

        panel = DipendentiPanel()
        self.mw.dipendenti_panel = panel
        return panel

    def _create_help(self) -> QWidget:
        """Inizializza il pannello di aiuto e documentazione."""
        from src.gui.panels import HelpPanel

        panel = HelpPanel()
        self.mw.help_panel = panel
        return panel

    def _create_notifications(self) -> QWidget:
        """Inizializza il centro notifiche e audit log."""
        from src.gui.panels import NotificationsPanel

        panel = NotificationsPanel()
        self.mw.notifications_panel = panel
        return panel

    def _create_settings_panel(self) -> QWidget:
        """Crea il pannello impostazioni e collega i segnali di salvataggio e aiuto contestuale."""
        from src.gui.panels import SettingsPanel

        panel = SettingsPanel()
        self.mw.settings_panel = panel
        panel.settings_saved.connect(self.mw._on_settings_saved)
        panel.request_help_section.connect(self.mw._on_help_requested)
        return panel

    def _initialize_new_panel(self, index: int, new_panel: QWidget) -> None:
        """Sostituisce il widget placeholder nello stack con l'istanza reale del pannello creato."""
        old_placeholder = self.mw.page_stack.widget(index)
        self.mw.page_stack.removeWidget(old_placeholder)
        self.mw.page_stack.insertWidget(index, new_panel)
        setattr(self.mw, f"_panel_initialized_{index}", True)
        self._try_connect_signals()

    def _handle_panel_error(self, index: int, e: Exception) -> None:
        """Notifica all'utente e logga il fallimento del caricamento di un modulo GUI."""
        import traceback

        logger.error(f"❌ Critical Error loading panel {index}: {e}")
        logger.error(traceback.format_exc())
        QMessageBox.critical(self.mw, "Errore Caricamento", f"Impossibile caricare il modulo.\nErrore: {e}")

    def _try_connect_signals(self) -> None:
        """Tenta di instaurare connessioni cross-pannello quando le dipendenze sono state caricate."""
        # Timbrature Bot -> DB & Dipendenti
        if hasattr(self.mw, "timbrature_bot_panel"):
            if hasattr(self.mw, "timbrature_db_panel") and not getattr(self.mw, "_timbrature_signals_connected", False):
                self.mw.timbrature_bot_panel.data_updated.connect(self.mw.timbrature_db_panel.refresh_data)
                self.mw._timbrature_signals_connected = True
            if hasattr(self.mw, "dipendenti_panel") and not getattr(
                self.mw, "_timbrature_dipendenti_signals_connected", False
            ):
                self.mw.timbrature_bot_panel.data_updated.connect(self.mw.dipendenti_panel.refresh_data)
                self.mw._timbrature_dipendenti_signals_connected = True

        # PDL Search -> PDL DB
        if hasattr(self.mw, "pdl_search_panel") and hasattr(self.mw, "pdl_db_panel") and not getattr(
            self.mw, "_pdl_signals_connected", False
        ):
            self.mw.pdl_search_panel.data_updated.connect(self.mw.pdl_db_panel.refresh_data)
            self.mw._pdl_signals_connected = True

    def navigate_to(self, index: int, sub_index: int | None = None) -> None:
        """
        Esegue la commutazione della pagina attiva, gestendo salvataggi pendenti e feedback della sidebar.

        Args:
            index: Indice del pannello di destinazione.
            sub_index: Eventuale indice di sottocategoria (tab interno).
        """
        if index == self.mw._current_page_index and sub_index is None:
            self.mw.sidebar.set_active_button(index)
            return

        if self.mw._current_page_index == 7 and hasattr(self.mw, "settings_panel"):
            if self.mw.settings_panel.has_unsaved_changes() and not self.mw.settings_panel.prompt_save_if_needed():
                self.mw.sidebar.set_active_button(self.mw._current_page_index)
                return

        self.get_panel(index)
        self.mw._current_page_index = index
        self.mw.page_stack.setCurrentIndex(index)
        self.mw.sidebar.set_active_button(index, sub_index)

    def navigate_to_extended(self, tab_idx: int, query: str) -> None:
        """Naviga al pannello Strumentale attivando un tab specifico e pre-compilando la ricerca."""
        self.navigate_to(4, sub_index=tab_idx)
        self.mw.contabilita_panel.main_tabs.setCurrentIndex(tab_idx)
        self.mw.contabilita_panel.set_search_query(query)

    def navigate_to_dataease(self, query: str) -> None:
        """Naviga al pannello Scarico Ore applicando un filtro immediato."""
        self.navigate_to(5)
        self.mw.scarico_ore_panel.search_input.setText(query)

    def navigate_to_timbrature(self, query: str) -> None:
        """Naviga al database timbrature applicando un filtro immediato."""
        self.navigate_to(3)
        self.mw.timbrature_db_panel.search_input.setText(query)

    def navigate_to_panel(self, panel_key: str) -> None:
        """Naviga a un pannello bot annidato partendo da una chiave identificativa."""
        bot_map = {
            "dettagli_oda": (0, 0),
            "scarico_ts": (0, 1),
            "timbrature": (0, 2),
            "prenota_bp": (0, 3),
            "carico_ts": (0, 4),
            "scarico_pdl": (1, 0),
            "ricerca_pdl": (1, 1),
        }
        if panel_key in bot_map:
            midx, sidx = bot_map[panel_key]
            self.navigate_to(1, sub_index=midx)
            if auto := getattr(self.mw, "automazioni_widget", None):
                auto.set_active_tab(midx, sidx)
            return

        db_map = {"db_timbrature": 3, "db_strumentale": 4, "db_dataease": 5, "db_dipendenti": 11, "nav_page_11": 11}
        if panel_key in db_map:
            self.navigate_to(db_map[panel_key])

    def analyze_with_lyra(self, context_text: str) -> None:
        """Naviga alla vista Lyra passando un contesto testuale per l'analisi immediata."""
        self.navigate_to(2)
        self.mw.lyra_panel.ask_lyra("Analizza questi dati e dimmi se ci sono anomalie.", context_text)
