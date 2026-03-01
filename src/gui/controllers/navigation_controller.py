"""
SyncroJob - Navigation Controller
Gestore centrale del routing e della navigazione tra i diversi pannelli dell'interfaccia utente.
Implementa una strategia di 'Lazy Loading' (caricamento differito) per ridurre drasticamente i tempi di startup
dell'applicazione, inizializzando i moduli funzionali solo quando vengono effettivamente richiesti dall'utente.
"""

import logging
from typing import TYPE_CHECKING, Any

from PyQt6.QtWidgets import QMessageBox, QStackedWidget, QWidget

from src.gui.components.popout.popout_manager import DetachedPanelWindow, PopoutPlaceholderWidget

if TYPE_CHECKING:
    from collections.abc import Callable

import typing

from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)


class NavigationController(QObject):
    """
    Controller responsabile della commutazione tra le pagine nel QStackedWidget della MainWindow.
    Gestisce il ciclo di vita dei pannelli (creazione, inizializzazione segnali, visualizzazione)
    e garantisce la sincronizzazione con lo stato della Sidebar e della Command Palette.
    """

    panel_detached = pyqtSignal(int, str)  # index, title
    panel_reattached = pyqtSignal(int)  # index

    def __init__(self, main_window: Any) -> None:
        """
        Inizializza il controller di navigazione.

        Args:
            main_window: Riferimento alla MainWindow dell'applicazione.
        """
        super().__init__(main_window)
        self.mw = main_window
        # Traccia i pannelli attualmente staccati (indice -> struct con panel nativo, placeholder, e finestra top-level)
        self._detached_panels: dict[int, dict[str, Any]] = {}

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
            # Se è distaccato, restituiamo il suo placeholder al master view
            if index in self._detached_panels:
                # Ritorna il placeholder anzichè il pannello sganciato
                return typing.cast("QWidget", self._detached_panels[index]["placeholder"])

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
            12: self._create_consuntivo,
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

        # Connessione per l'aggiornamento della card moduli sganciati
        if hasattr(panel, "multi_window_card"):
            self.panel_detached.connect(
                lambda i, t: panel.multi_window_card.update_modules(self._detached_panels)
            )
            self.panel_reattached.connect(
                lambda i: panel.multi_window_card.update_modules(self._detached_panels)
            )
            panel.multi_window_card.reattach_single_requested.connect(self._on_panel_reattached)
            panel.multi_window_card.reattach_all_requested.connect(self._reattach_all_panels)

        return panel

    def _reattach_all_panels(self) -> None:
        """Riaggancia automaticamente tutti i pannelli attualmente sganciati."""
        indices = list(self._detached_panels.keys())
        for idx in indices:
            self._on_panel_reattached(idx)

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

    def _create_consuntivo(self) -> QWidget:
        """Inizializza il pannello di gestione consuntivi."""
        from src.gui.panels.consuntivo_panel import ConsuntivoPanel

        panel = ConsuntivoPanel()
        self.mw.consuntivo_panel = panel
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

    def detach_panel(self, index: int, title: str) -> None:
        """
        Stacca un modulo dall'interno della MainWindow in una finestra top-level (Pop-out).
        Al suo posto nel QStackedWidget viene inserito un placeholder.
        """
        if index in self._detached_panels:
            # È già staccato, portionalo in primo piano (Raise)
            self._detached_panels[index]["window"].raise_()
            self._detached_panels[index]["window"].activateWindow()
            return

        panel = self.mw.page_stack.widget(index)
        if not panel or not getattr(self.mw, f"_panel_initialized_{index}", False):
            # Non possiamo staccare un pannello che non è ancora stato caricato/inizializzato
            logger.warning(f"Tentato distacco di panel non init. (Index: {index})")
            return

        # Rimuoviamo il pannello originale dallo stack
        self.mw.page_stack.removeWidget(panel)

        # Creiamo un placeholder informativo col pulsante "Riaggancia"
        # Notare come il clack triggeri lo stesso riaggancio di evento chiesta OS!
        placeholder = PopoutPlaceholderWidget(title, on_reattach=lambda: self._on_panel_reattached(index))
        self.mw.page_stack.insertWidget(index, placeholder)

        # Creiamo la nuova finestra nativa PyQt passando il vero pannello
        popout_win = DetachedPanelWindow(original_index=index, panel=panel, title=title)

        # Colleghiamo il segnale emesso alla chiusura per fare il ripristino automatico
        popout_win.panel_closed_signal.connect(self._on_panel_reattached)

        # Mostriamolo fisicamente sull'OS
        popout_win.show()

        self._detached_panels[index] = {"panel": panel, "placeholder": placeholder, "window": popout_win}

        self.panel_detached.emit(index, title)

        # Facciamo scorrere lo stack sul placeholder per conferma visiva all'utente
        if self.mw._current_page_index == index:
            # Force refresh layout internal to stackedwidget since its a different instance
            self.mw.page_stack.setCurrentIndex(index)

    def _on_panel_reattached(self, index: int) -> None:
        """Riporta il pannello dentro la MainWindow e distrugge la Popout Window."""
        popout_data = self._detached_panels.pop(index, None)
        if not popout_data:
            return

        panel = popout_data["panel"]
        placeholder = popout_data["placeholder"]
        window = popout_data["window"]

        # Evita cicli chiudendola programmatticamente solo se on_reattach
        # è stato premuto. Se è stata chiusa dall'utente, il closeEvent invia già questo signal.
        if window.isVisible():
            window.panel_closed_signal.disconnect(self._on_panel_reattached)  # disconnette per no-loop
            window.close()

        # Togliamo il vecchio widget informativo "Sono in popout"
        self.mw.page_stack.removeWidget(placeholder)
        placeholder.deleteLater()

        # Rimettiamo il figlio originale (Timbrature, OdA ecc) al suo index corretto.
        # N.B. self.get_panel tornerà quello vero d'ora in poi
        self.mw.page_stack.insertWidget(index, panel)

        self.panel_reattached.emit(index)

        if self.mw._current_page_index == index:
            self.mw.page_stack.setCurrentIndex(index)

        logger.info(f"Pannello idx:{index} è stato ricollegato (reattached) regolarmente.")

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
            if hasattr(self.mw, "timbrature_db_panel") and not getattr(
                self.mw, "_timbrature_signals_connected", False
            ):
                self.mw.timbrature_bot_panel.data_updated.connect(self.mw.timbrature_db_panel.refresh_data)
                self.mw._timbrature_signals_connected = True
            if hasattr(self.mw, "dipendenti_panel") and not getattr(
                self.mw, "_timbrature_dipendenti_signals_connected", False
            ):
                self.mw.timbrature_bot_panel.data_updated.connect(self.mw.dipendenti_panel.refresh_data)
                self.mw._timbrature_dipendenti_signals_connected = True

        # PDL Search -> PDL DB
        if (
            hasattr(self.mw, "pdl_search_panel")
            and hasattr(self.mw, "pdl_db_panel")
            and not getattr(self.mw, "_pdl_signals_connected", False)
        ):
            self.mw.pdl_search_panel.data_updated.connect(self.mw.pdl_db_panel.refresh_data)
            self.mw._pdl_signals_connected = True

    def navigate_to(self, index: int, sub_index: int | None = None, bot_index: int | None = None) -> None:
        """
        Esegue la commutazione della pagina attiva, gestendo salvataggi pendenti e feedback della sidebar.

        Args:
            index: Indice del pannello di destinazione.
            sub_index: Eventuale indice di sottocategoria (tab interno).
            bot_index: Eventuale indice del bot specifico (terzo livello).
        """
        # Se sub_index è -1, lo trattiamo come None per la Sidebar
        norm_sub = None if sub_index == -1 else sub_index
        norm_bot = None if bot_index == -1 else bot_index

        if index == self.mw._current_page_index and norm_sub is norm_bot is None:
            self.mw.sidebar.set_active_button(index)
            return

        if (
            self.mw._current_page_index == 7
            and hasattr(self.mw, "settings_panel")
            and self.mw.settings_panel.has_unsaved_changes()
            and not self.mw.settings_panel.prompt_save_if_needed()
        ):
            self.mw.sidebar.set_active_button(self.mw._current_page_index)
            return

        panel = self.get_panel(index)
        self.mw._current_page_index = index
        if hasattr(self.mw.page_stack, "slide_to_index"):
            self.mw.page_stack.slide_to_index(index)
        else:
            self.mw.page_stack.setCurrentIndex(index)

        # Gestione Tab Interni (Livello 3)
        if norm_sub is not None and panel:
            if index == 1:  # Automazioni
                auto_widget = getattr(self.mw, "automazioni_widget", None)
                if auto_widget:
                    if norm_bot is not None and hasattr(auto_widget, "set_active_tab"):
                        auto_widget.set_active_tab(norm_sub, norm_bot)
                    elif hasattr(auto_widget, "setCurrentIndex"):
                        auto_widget.setCurrentIndex(norm_sub)
            elif index == 4:  # Strumentale
                if hasattr(panel, "main_tabs"):
                    panel.main_tabs.setCurrentIndex(norm_sub)
            elif index in (9, 11, 12):  # Consuntivo, Dipendenti, Monitoraggio
                if hasattr(panel, "tabs"):
                    panel.tabs.setCurrentIndex(norm_sub)

        self.mw.sidebar.set_active_button(index, norm_sub, norm_bot)

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
                # Se è un AnimatedTabWidget o QTabWidget, deve avere setCurrentIndex
                if hasattr(auto, "set_active_tab"):
                    auto.set_active_tab(midx, sidx)
                else:
                    auto.setCurrentIndex(midx)
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

    def refresh_current_page(self) -> None:
        """Esegue l'azione di refresh specifica per la pagina corrente (pattern F5)."""
        from src.gui.main_window.page_index import PageIndex

        idx = self.mw.page_stack.currentIndex()
        panel = self.mw.page_stack.currentWidget()

        if not panel or not isinstance(panel, QWidget):
            return

        # Pattern mapping per refresh
        refreshable_indices = (
            PageIndex.DASHBOARD,
            PageIndex.TIMBRATURE,
            PageIndex.ANAGRAFICHE,
            PageIndex.STORICO_ODA,
            PageIndex.DIPENDENTI,
        )

        if idx in refreshable_indices and hasattr(panel, "refresh_data"):
            panel.refresh_data()
        elif idx == PageIndex.STRUMENTALE and hasattr(panel, "refresh_tabs"):
            panel.refresh_tabs()
        elif idx == PageIndex.DATAEASE and hasattr(panel, "_start_update"):
            panel._start_update()

    def analyze_with_lyra(self, context_text: str) -> None:
        """Naviga alla vista Lyra passando un contesto testuale per l'analisi immediata."""
        self.navigate_to(2)
        self.mw.lyra_panel.ask_lyra("Analizza questi dati e dimmi se ci sono anomalie.", context_text)

    def detach_current_panel(self) -> None:
        """Sgancia il pannello attualmente visualizzato in una finestra esterna."""
        idx = self.mw.page_stack.currentIndex()
        if idx < 0:
            return

        panel = self.mw.page_stack.widget(idx)
        if not panel:
            return

        # Recupera il titolo dal pannello se disponibile, altrimenti usa un default basato sull'indice
        title = "Pannello"
        if hasattr(panel, "bot_name"):
            title = panel.bot_name
        elif hasattr(panel, "windowTitle") and panel.windowTitle():
            title = panel.windowTitle()

        # Mapping manuale se i titoli sono vuoti (Dashboard, ecc)
        from src.gui.main_window.page_index import PageIndex

        titles = {
            PageIndex.DASHBOARD: "Dashboard",
            PageIndex.AUTOMAZIONI: "Automazioni",
            PageIndex.LYRA: "Lyra AI",
            PageIndex.TIMBRATURE: "Database Timbrature",
            PageIndex.STRUMENTALE: "Contabilità Strumentale",
            PageIndex.DATAEASE: "Scarico Ore (DataEase)",
            PageIndex.ANAGRAFICHE: "Anagrafica PDL",
            PageIndex.SETTINGS: "Impostazioni",
            PageIndex.HELP: "Aiuto e Supporto",
            PageIndex.NOTIFICATIONS: "Centro Notifiche",
            PageIndex.STORICO_ODA: "Storico OdA",
            PageIndex.DIPENDENTI: "Gestione Dipendenti",
            PageIndex.CONSUNTIVO: "Consuntivo",
        }
        if title == "Pannello" or not title:
            title = titles.get(idx, f"Modulo {idx}")

        self.detach_panel(idx, title)
