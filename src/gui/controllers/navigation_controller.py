"""
SyncroJob - Navigation Controller
Gestore centrale del routing e della navigazione tra i diversi pannelli dell'interfaccia utente.
Implementa una strategia di 'Lazy Loading' (caricamento differito) per ridurre drasticamente i tempi di startup
dell'applicazione, inizializzando i moduli funzionali solo quando vengono effettivamente richiesti dall'utente.
"""

from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QStackedWidget, QWidget

from src.gui.components.popout.popout_manager import DetachedPanelWindow, PopoutPlaceholderWidget
from src.gui.main_window.page_index import PageIndex

if TYPE_CHECKING:
    from src.core.contabilita.consuntivo.consuntivo_controller import ConsuntivoController
    from src.core.contabilita.scarico_ore.controller import ScaricoOreController
    from src.core.dipendenti.anagrafica_controller import AnagraficaController
    from src.core.oda.oda_controller import ODAController
    from src.core.pdl.pdl_controller import PDLController
    from src.gui.main_window.main import MainWindow

logger = logging.getLogger(__name__)


class NavigationController(QObject):
    """
    Controller responsabile della commutazione tra le pagine nel QStackedWidget della MainWindow.
    Gestisce il ciclo di vita dei pannelli (creazione, inizializzazione segnali, visualizzazione)
    e garantisce la sincronizzazione con lo stato della Sidebar e della Command Palette.
    """

    panel_detached = pyqtSignal(int, str)  # index, title
    panel_reattached = pyqtSignal(int)  # index

    def __init__(self, main_window: MainWindow) -> None:
        """
        Inizializza il controller di navigazione e le istanze dei controller CORE.

        Args:
            main_window: Riferimento alla MainWindow dell'applicazione.
        """
        super().__init__(main_window)
        self.mw = main_window
        # Traccia i pannelli attualmente staccati (indice -> struct con panel nativo, placeholder, e finestra top-level)
        self._detached_panels: dict[int, dict[str, Any]] = {}

        # Controller attributes (inizializzati in _init_core_controllers)
        self.oda_controller: ODAController
        self.anagrafica_controller: AnagraficaController
        self.pdl_controller: PDLController
        self.scarico_ore_controller: ScaricoOreController
        self.consuntivo_controller: ConsuntivoController

        # 1. Inizializza i controller CORE
        self._init_core_controllers()

        # 2. Prepara lo stack con i segnaposto
        self._setup_stack_placeholders()

    def _init_core_controllers(self) -> None:
        """Inizializza i controller core per i dati."""
        from src.core.contabilita.consuntivo.consuntivo_controller import (  # noqa: PLC0415
            ConsuntivoController,
        )
        from src.core.contabilita.scarico_ore.controller import ScaricoOreController  # noqa: PLC0415
        from src.core.dipendenti.anagrafica_controller import AnagraficaController  # noqa: PLC0415
        from src.core.oda.oda_controller import ODAController  # noqa: PLC0415
        from src.core.pdl.pdl_controller import PDLController  # noqa: PLC0415

        self.oda_controller = ODAController()
        self.anagrafica_controller = AnagraficaController()
        self.pdl_controller = PDLController()
        self.scarico_ore_controller = ScaricoOreController()
        self.consuntivo_controller = ConsuntivoController()

    def _setup_stack_placeholders(self) -> None:
        """Popola lo stack con QWidget vuoti per supportare il lazy loading basato su indici."""
        num_pages = len(PageIndex)
        for _ in range(num_pages):
            self.stack.addWidget(QWidget())

    @property
    def stack(self) -> QStackedWidget:
        """Restituisce il widget stack della MainWindow."""
        return self.mw.stacked_widget

    def navigate_to(self, index: int, sub_index: int | None = None) -> None:
        """
        Cambia la pagina attiva nel container principale.
        Inizializza il pannello se non ancora creato.

        Args:
            index: Indice numerico della pagina (vedi PageIndex).
            sub_index: Indice opzionale per i pannelli che supportano tab interni.
        """
        if index < 0 or index >= self.stack.count():
            logger.warning("Tentativo di navigazione verso indice non valido: %s", index)
            return

        # 1. Assicurati che il pannello sia inizializzato
        self._ensure_panel_initialized(index)

        # 2. Gestione pannelli staccati (Popout)
        if index in self._detached_panels:
            self._handle_detached_navigation(index)
            return

        # 3. Cambio pagina reale nello stack
        self.stack.setCurrentIndex(index)

        # 4. Sincronizzazione Sidebar
        if hasattr(self.mw.sidebar, "set_active_button"):
            self.mw.sidebar.set_active_button(index)

        # 5. Gestione sub-index (es. per pannelli tabulati)
        panel = self.stack.widget(index)
        if panel and sub_index is not None and hasattr(panel, "set_current_tab"):
            panel.set_current_tab(sub_index)

        # 6. Notifica il pannello del focus (opzionale)
        if panel and hasattr(panel, "on_focus_received") and callable(panel.on_focus_received):
            panel.on_focus_received()

    def navigate_to_panel(self, panel_key: str) -> None:
        """Naviga verso un pannello specifico tramite chiave logica (bridge per AutomazioniWidget)."""
        mapping = {
            "scarico_ts": PageIndex.AUTOMAZIONI,
            "carico_ts": PageIndex.AUTOMAZIONI,
            "prenota_bp": PageIndex.AUTOMAZIONI,
            "dettagli_oda": PageIndex.AUTOMAZIONI,
            "scarico_pdl": PageIndex.AUTOMAZIONI,
            "ricerca_pdl": PageIndex.AUTOMAZIONI,
            "timbrature": PageIndex.AUTOMAZIONI,
        }

        # Sub-mapping per AutomazioniWidget (tab index)
        sub_mapping = {
            "scarico_ts": 0,
            "dettagli_oda": 1,
            "scarico_pdl": 2,
            "prenota_bp": 3,
            "carico_ts": 4,
            "ricerca_pdl": 5,
            "timbrature": 6,
        }

        if panel_key in mapping:
            self.navigate_to(mapping[panel_key], sub_index=sub_mapping.get(panel_key))

    def navigate_to_pdl(self, site: str | None = None, area: str | None = None) -> None:
        """Naviga alla vista PDL applicando filtri specifici."""
        self.navigate_to(PageIndex.DATAEASE)
        panel = self.get_panel(PageIndex.DATAEASE)
        if panel and hasattr(panel, "apply_external_filters"):
            panel.apply_external_filters(site=site, area=area)

    def get_panel(self, index: int) -> QWidget | None:
        """
        Restituisce l'istanza del pannello all'indice specificato.
        Inizializza il pannello se necessario.
        """
        self._ensure_panel_initialized(index)
        return self.stack.widget(index)

    def detach_panel(self, index: int) -> None:
        """
        Sposta un pannello dallo Stack principale in una finestra separata.
        Lascia un segnaposto (PopoutPlaceholderWidget) nello stack originale.
        """
        if index in self._detached_panels:
            return

        self._ensure_panel_initialized(index)
        native_panel = self.stack.widget(index)
        if not native_panel:
            return

        # Recupera il titolo dal pannello
        title = str(getattr(native_panel, "TITLE", f"Modulo {index}"))

        # Rimuovi il pannello dallo stack e inserisci il placeholder
        self.stack.removeWidget(native_panel)
        placeholder = PopoutPlaceholderWidget(
            title, on_reattach=functools.partial(self.reattach_panel, index)
        )
        self.stack.insertWidget(index, placeholder)

        # Crea e mostra la finestra esterna
        detached_window = DetachedPanelWindow(index, native_panel, title)
        detached_window.panel_closed_signal.connect(self.reattach_panel)
        detached_window.show()

        self._detached_panels[index] = {
            "panel": native_panel,
            "placeholder": placeholder,
            "window": detached_window,
        }

        self.panel_detached.emit(index, title)
        logger.info("Pannello '%s' (index %s) distaccato.", title, index)

    def reattach_panel(self, index: int) -> None:
        """Riporta un pannello distaccato nello Stack principale."""
        if index not in self._detached_panels:
            return

        data = self._detached_panels.pop(index)
        panel = data["panel"]
        placeholder = data["placeholder"]
        window = data["window"]

        # Chiudi finestra senza distruggere il pannello (già rimosso nel window.closeEvent personalizzato)
        window.close()

        # Sostituisci placeholder con pannello reale
        self.stack.removeWidget(placeholder)
        placeholder.deleteLater()
        self.stack.insertWidget(index, panel)

        # Torna al pannello
        self.navigate_to(index)
        self.panel_reattached.emit(index)
        logger.info("Pannello index %s reintegrato nello stack.", index)

    def _ensure_panel_initialized(self, index: int) -> None:
        """Strategia di Lazy Loading: crea il pannello solo alla prima richiesta."""
        panel = self.stack.widget(index)

        # Se il pannello è ancora uno QWidget base (vuoto), va inizializzato
        if type(panel) is QWidget:
            logger.info("Inizializzazione lazy del pannello indice: %s", index)
            new_panel = self._create_panel_instance(index)
            if new_panel:
                self.stack.removeWidget(panel)
                panel.deleteLater()
                self.stack.insertWidget(index, new_panel)

    def _create_panel_instance(self, index: int) -> QWidget | None:  # noqa: PLR0911, PLR0912
        """Factory interna per la creazione dei pannelli."""
        try:
            if index == PageIndex.DASHBOARD:
                from src.gui.panels.dashboard_panel import DashboardPanel  # noqa: PLC0415

                return DashboardPanel()

            if index == PageIndex.AUTOMAZIONI:
                from src.gui.widgets.automazioni_widget import AutomazioniWidget  # noqa: PLC0415

                return AutomazioniWidget(main_window=self.mw)

            if index == PageIndex.RESERVED_AI:
                # Placeholder per future espansioni
                return QWidget()

            if index == PageIndex.TIMBRATURE:
                from src.gui.panels.timbrature_db import TimbratureDBPanel  # noqa: PLC0415

                return TimbratureDBPanel()

            if index == PageIndex.STRUMENTALE:
                from src.gui.panels.contabilita_panel import ContabilitaPanel  # noqa: PLC0415

                return ContabilitaPanel()

            if index == PageIndex.DATAEASE:
                from src.gui.panels.scarico_ore_panel import ScaricoOrePanel  # noqa: PLC0415

                return ScaricoOrePanel(controller=self.scarico_ore_controller)

            if index == PageIndex.ANAGRAFICHE:
                from src.gui.panels.dipendenti.pages.anagrafica_page import AnagraficaPage  # noqa: PLC0415

                return AnagraficaPage(controller=self.anagrafica_controller)

            if index == PageIndex.SETTINGS:
                from src.gui.panels.settings.main_panel import SettingsPanel  # noqa: PLC0415

                return SettingsPanel()

            if index == PageIndex.HELP:
                from src.gui.panels.help_panel import HelpPanel  # noqa: PLC0415

                return HelpPanel()

            if index == PageIndex.NOTIFICATIONS:
                from src.gui.panels.notifications_panel import NotificationsPanel  # noqa: PLC0415

                return NotificationsPanel()

            if index == PageIndex.STORICO_ODA:
                from src.gui.panels.storico_oda import StoricoOdaPanel  # noqa: PLC0415

                return StoricoOdaPanel(controller=self.oda_controller)

            if index == PageIndex.DIPENDENTI:
                from src.gui.panels.dipendenti.main_panel import DipendentiPanel  # noqa: PLC0415

                return DipendentiPanel(controller=self.anagrafica_controller)

            if index == PageIndex.CONSUNTIVO:
                from src.gui.panels.consuntivo_panel import ConsuntivoPanel  # noqa: PLC0415

                return ConsuntivoPanel(controller=self.consuntivo_controller)

        except Exception:
            logger.exception("Errore fatale creazione pannello %s", index)
            QMessageBox.critical(
                None, "Errore Caricamento", f"Impossibile caricare il modulo {index}. Controlla i log."
            )

        return None

    def _handle_detached_navigation(self, index: int) -> None:
        """Porta in primo piano la finestra del pannello distaccato."""
        data = self._detached_panels[index]
        window = data["window"]
        window.show()
        window.raise_()
        window.activateWindow()
        # Sincronizza comunque la sidebar
        if hasattr(self.mw.sidebar, "set_active_button"):
            self.mw.sidebar.set_active_button(index)
        # Sostituisce la navigazione nello stack con il placeholder (già presente)
        self.stack.setCurrentIndex(index)
