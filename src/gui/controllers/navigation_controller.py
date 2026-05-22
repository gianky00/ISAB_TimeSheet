"""SyncroJob - Navigation Controller.

Gestore centrale del routing e della navigazione tra i diversi pannelli dell'interfaccia utente.
Implementa una strategiàdi 'Lazy Loading' (caricamento differito) per ridurre drasticamente i tempi di startup
dell'applicazione, inizializzando i moduli funzionali solo quando vengono effettivamente richiesti dall'utente.
"""

from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QStackedWidget, QWidget

from src.gui.components.popout.popout_manager import DetachedPanelWindow, PopoutPlaceholderWidget
from src.gui.controllers.panel_factory import PanelFactory
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
    """Controller responsabile della commutazione tra le pagine nel QStackedWidget della MainWindow.

    Gestisce il routing e delega la creazione dei pannelli alla PanelFactory.
    """

    panel_detached = Signal(int, str)  # index, title
    panel_reattached = Signal(int)  # index

    def __init__(self, main_window: MainWindow) -> None:
        """Inizializza il controller di navigazione e i componenti associati.

        Args:
          main_window: Riferimento alla MainWindow dell'applicazione.
        """
        super().__init__(main_window)
        self.mw = main_window

        # Inizializza la factory per i pannelli (SRP)
        self.panel_factory = PanelFactory(self)

        # Traccia i pannelli attualmente staccati
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
        from src.core.contabilita.consuntivo.consuntivo_controller import (
            ConsuntivoController,
        )
        from src.core.contabilita.scarico_ore.controller import ScaricoOreController
        from src.core.dipendenti.anagrafica_controller import AnagraficaController
        from src.core.oda.oda_controller import ODAController
        from src.core.pdl.pdl_controller import PDLController

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

    def navigate_to(self, index: int, sub_index: int | None = None, bot_index: int | None = None) -> None:
        """Cambia la pagina attiva nel container principale.

        Inizializza il pannello se non ancora creato.
        """
        if index < 0 or index >= self.stack.count():
            logger.warning("Tentativo di navigazione verso indice non valido: %s", index)
            return

        # 1. Assicurati che il pannello sia inizializzato via Factory
        self._ensure_panel_initialized(index)

        # 2. Gestione pannelli staccati (Popout)
        if index in self._detached_panels:
            self._handle_detached_navigation(index)
            return

        # 3. Cambio pagina reale nello stack
        if hasattr(self.stack, "slide_to_index"):
            self.stack.slide_to_index(index)
        else:
            self.stack.setCurrentIndex(index)

        # 4. Sincronizzazione Sidebar
        if hasattr(self.mw.sidebar, "set_active_button"):
            self.mw.sidebar.set_active_button(index, sub_index, bot_index)

        # 5. Gestione sub-index (es. per pannelli tabulati)
        panel = self.stack.widget(index)
        if panel and hasattr(panel, "set_current_tab"):
            try:
                panel.set_current_tab(sub_index, bot_index)
            except TypeError:
                panel.set_current_tab(sub_index)

        # 6. Notifica il pannello del focus
        if panel and hasattr(panel, "on_focus_received") and callable(panel.on_focus_received):
            panel.on_focus_received()

    def navigate_to_panel(self, panel_key: str) -> None:
        """Naviga verso un pannello specifico tramite chiave logica."""
        automation_sub_mapping = {
            "dettagli_oda": (0, 0),
            "scarico_ts": (0, 1),
            "timbrature": (0, 2),
            "prenota_bp": (0, 3),
            "carico_ts": (0, 4),
            "scarico_pdl": (1, 0),
            "ricerca_pdl": (1, 1),
        }

        if panel_key in automation_sub_mapping:
            portal_idx, bot_idx = automation_sub_mapping[panel_key]
            self.navigate_to(PageIndex.AUTOMAZIONI, sub_index=portal_idx, bot_index=bot_idx)
        else:
            logger.debug("Tentativo di navigazione diretta non mappata: %s", panel_key)

    def navigate_to_pdl(self, site: str | None = None, area: str | None = None) -> None:
        """Naviga alla vista PDL applicando filtri specifici."""
        self.navigate_to(PageIndex.PDL_DB)
        panel = self.get_panel(PageIndex.PDL_DB)
        if panel and hasattr(panel, "apply_external_filters"):
            panel.apply_external_filters(site=site, area=area)

    def get_panel(self, index: int) -> QWidget | None:
        """Restituisce l'istanza del pannello, inizializzandolo se necessario."""
        self._ensure_panel_initialized(index)
        return self.stack.widget(index)

    def detach_panel(self, index: int) -> None:
        """Sposta un pannello dallo Stack principale in una finestra separata."""
        if index in self._detached_panels:
            return

        self._ensure_panel_initialized(index)
        native_panel = self.stack.widget(index)
        if not native_panel:
            return

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
        """Strategiàdi Lazy Loading basata sulla PanelFactory."""
        try:
            panel = self.stack.widget(index)

            # Se il pannello  ancora uno QWidget base (vuoto), delega alla factory
            if type(panel) is QWidget:
                logger.info("Inizializzazione lazy del pannello indice: %s", index)
                new_panel = self.panel_factory.create_panel(index)
                if new_panel:
                    self.stack.removeWidget(panel)
                    panel.deleteLater()
                    self.stack.insertWidget(index, new_panel)
        except Exception:
            logger.exception("Errore imprevisto durante inizializzazione pannello %s", index)

    def _handle_detached_navigation(self, index: int) -> None:
        """Porta in primo piano la finestra del pannello distaccato."""
        data = self._detached_panels[index]
        window = data["window"]
        window.show()
        window.raise_()
        window.activateWindow()
        if hasattr(self.mw.sidebar, "set_active_button"):
            self.mw.sidebar.set_active_button(index)
        self.stack.setCurrentIndex(index)
