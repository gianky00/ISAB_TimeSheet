"""
SyncroJob - Navigation Controller
Gestore centrale del routing e della navigazione tra i diversi pannelli dell'interfaccia utente.
Implementa una strategia di 'Lazy Loading' (caricamento differito) per ridurre drasticamente i tempi di startup
dell'applicazione, inizializzando i moduli funzionali solo quando vengono effettivamente richiesti dall'utente.
"""

import functools
import logging
from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QStackedWidget, QWidget

from src.gui.components.popout.popout_manager import DetachedPanelWindow, PopoutPlaceholderWidget
from src.gui.main_window.page_index import PageIndex

if TYPE_CHECKING:
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

    def __init__(self, main_window: "MainWindow") -> None:
        """
        Inizializza il controller di navigazione e le istanze dei controller CORE.

        Args:
            main_window: Riferimento alla MainWindow dell'applicazione.
        """
        super().__init__(main_window)
        self.mw = main_window
        # Traccia i pannelli attualmente staccati (indice -> struct con panel nativo, placeholder, e finestra top-level)
        self._detached_panels: dict[int, dict[str, Any]] = {}

        # === CORE CONTROLLERS (Singleton-like for UI context) ===
        from src.core.contabilita.consuntivo.consuntivo_controller import (  # noqa: PLC0415
            ConsuntivoController,
        )
        from src.core.dipendenti.anagrafica_controller import AnagraficaController  # noqa: PLC0415
        from src.core.oda.oda_controller import ODAController  # noqa: PLC0415
        from src.core.pdl.pdl_controller import PDLController  # noqa: PLC0415
        from src.core.scarico_ore.controller import ScaricoOreController  # noqa: PLC0415

        self.oda_controller = ODAController()
        self.anagrafica_controller = AnagraficaController()
        self.pdl_controller = PDLController()
        self.scarico_ore_controller = ScaricoOreController()
        self.consuntivo_controller = ConsuntivoController()

    @property
    def stack(self) -> QStackedWidget:
        """Restituisce il widget stack della MainWindow."""
        return self.mw.stacked_widget

    def navigate_to(self, index: int) -> None:
        """
        Cambia la pagina attiva nel container principale.
        Inizializza il pannello se non ancora creato.

        Args:
            index: Indice numerico della pagina (vedi PageIndex).
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
        self.mw.sidebar.set_active_index(index)

        # 5. Notifica il pannello del focus (opzionale)
        panel = self.stack.widget(index)
        if hasattr(panel, "on_focus_received") and callable(panel.on_focus_received):
            panel.on_focus_received()

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
        title = getattr(native_panel, "TITLE", f"Modulo {index}")

        # Rimuovi il pannello dallo stack e inserisci il placeholder
        self.stack.removeWidget(native_panel)
        placeholder = PopoutPlaceholderWidget(
            title, on_reattach=functools.partial(self.reattach_panel, index)
        )
        self.stack.insertWidget(index, placeholder)

        # Crea e mostra la finestra esterna
        detached_window = DetachedPanelWindow(native_panel, title)
        detached_window.reattach_requested.connect(functools.partial(self.reattach_panel, index))
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
                from src.gui.panels.automazioni_panel import AutomazioniPanel  # noqa: PLC0415

                return AutomazioniPanel()

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

                return ScaricoOrePanel()

            if index == PageIndex.ANAGRAFICHE:
                from src.gui.panels.anagrafica_page import AnagraficaPage  # noqa: PLC0415

                return AnagraficaPage()

            if index == PageIndex.SETTINGS:
                from src.gui.panels.settings_panel import SettingsPanel  # noqa: PLC0415

                return SettingsPanel()

            if index == PageIndex.HELP:
                from src.gui.panels.help_panel import HelpPanel  # noqa: PLC0415

                return HelpPanel()

            if index == PageIndex.NOTIFICATIONS:
                from src.gui.panels.notifications_panel import NotificationsPanel  # noqa: PLC0415

                return NotificationsPanel()

            if index == PageIndex.STORICO_ODA:
                from src.gui.panels.storico_oda_panel import StoricoOdaPanel  # noqa: PLC0415

                return StoricoOdaPanel()

            if index == PageIndex.DIPENDENTI:
                from src.gui.panels.dipendenti_manager_panel import DipendentiManagerPanel  # noqa: PLC0415

                return DipendentiManagerPanel()

            if index == PageIndex.CONSUNTIVO:
                from src.gui.panels.consuntivo_panel import ConsuntivoPanel  # noqa: PLC0415

                return ConsuntivoPanel()

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
        self.mw.sidebar.set_active_index(index)
        # Sostituisce la navigazione nello stack con il placeholder (già presente)
        self.stack.setCurrentIndex(index)
