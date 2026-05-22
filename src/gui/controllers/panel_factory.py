"""SyncroJob - Panel Factory.

Componente responsabile dell'istanziazione "Lazy" dei pannelli dell'interfaccia utente.
Garantisce il disaccoppiamento tra la logica di navigazione e la creazione degli oggetti UI.
"""

import logging
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMessageBox, QWidget

from src.gui.main_window.page_index import PageIndex

if TYPE_CHECKING:
    from src.gui.controllers.navigation_controller import NavigationController
    from src.gui.main_window.main import MainWindow

logger = logging.getLogger(__name__)


class PanelFactory:
    """Factory per la creazione dei pannelli della MainWindow.

    Incapsula la logica di importazione dinamica e inizializzazione dei widget.

    Inizializza la factory.

    Args:
      navigation_controller: Riferimento al controller di navigazione per l'iniezione delle dipendenze.
    """

    def __init__(self, navigation_controller: "NavigationController") -> None:
        self.nav = navigation_controller
        self.mw: MainWindow = navigation_controller.mw

    def create_panel(self, index: PageIndex | int) -> QWidget | None:
        """Crea un'istanza del pannello corrispondente all'indice specificato.

        Args:
          index: Indice della pagina (PageIndex).

        Returns:
          Istanza del QWidget o None in caso di errore.
        """
        try:
            if index == PageIndex.RESERVED_AI:
                return QWidget()

            return self._instantiate_panel(index)

        except Exception:
            logger.exception("Errore fatale nella creazione del pannello %s", index)
            QMessageBox.critical(
                None,
                "Errore Caricamento",
                f"Impossibile caricare il modulo {index}. Controlla i log di sistema.",
            )
            return None

    def _instantiate_panel(self, index: PageIndex | int) -> QWidget | None:
        """Logica di istanziazione granulare con lazy import tramite mapping."""
        # Convert explicit int to PageIndex if possible for type safety
        target_index = PageIndex(index) if isinstance(index, int) else index
        # Mappa dei costruttori lazy per evitare catene di if-elif infinite
        registry = {
            PageIndex.DASHBOARD: self._create_dashboard,
            PageIndex.AUTOMAZIONI: self._create_automazioni,
            PageIndex.TIMBRATURE: self._create_timbrature,
            PageIndex.STRUMENTALE: self._create_contabilita,
            PageIndex.DATAEASE: self._create_scarico_ore,
            PageIndex.PDL_DB: self._create_pdl_db,
            PageIndex.SETTINGS: self._create_settings,
            PageIndex.HELP: self._create_help,
            PageIndex.NOTIFICATIONS: self._create_notifications,
            PageIndex.STORICO_ODA: self._create_oda,
            PageIndex.DIPENDENTI: self._create_dipendenti,
            PageIndex.CONSUNTIVO: self._create_consuntivo,
            PageIndex.CHANGELOG: self._create_changelog,
        }

        creator = registry.get(target_index)
        return creator() if creator else None

    # --- CREATOR HELPERS (Lazy Imports) ---

    def _create_dashboard(self) -> QWidget:
        from src.gui.panels.dashboard_panel import DashboardPanel

        return DashboardPanel()

    def _create_automazioni(self) -> QWidget:
        from src.gui.widgets.automazioni_widget import AutomazioniWidget

        return AutomazioniWidget(main_window=self.mw)

    def _create_timbrature(self) -> QWidget:
        from src.gui.panels.timbrature_db import TimbratureDBPanel

        return TimbratureDBPanel()

    def _create_contabilita(self) -> QWidget:
        from src.gui.panels.contabilita_panel import ContabilitaPanel

        return ContabilitaPanel()

    def _create_scarico_ore(self) -> QWidget:
        from src.gui.panels.scarico_ore_panel import ScaricoOrePanel

        return ScaricoOrePanel(controller=self.nav.scarico_ore_controller)

    def _create_pdl_db(self) -> QWidget:
        from src.gui.panels.pdl.pdl_panel import PDLDBPanel

        return PDLDBPanel(controller=self.nav.pdl_controller)

    def _create_settings(self) -> QWidget:
        from src.gui.panels.settings.main_panel import SettingsPanel

        return SettingsPanel()

    def _create_help(self) -> QWidget:
        from src.gui.panels.help_panel import HelpPanel

        return HelpPanel()

    def _create_notifications(self) -> QWidget:
        from src.gui.panels.notifications_panel import NotificationsPanel

        return NotificationsPanel()

    def _create_oda(self) -> QWidget:
        from src.gui.panels.storico_oda import StoricoOdaPanel

        return StoricoOdaPanel(controller=self.nav.oda_controller)

    def _create_dipendenti(self) -> QWidget:
        from src.gui.panels.dipendenti.main_panel import DipendentiPanel

        return DipendentiPanel(controller=self.nav.anagrafica_controller)

    def _create_consuntivo(self) -> QWidget:
        from src.gui.panels.consuntivo_panel import ConsuntivoPanel

        return ConsuntivoPanel(controller=self.nav.consuntivo_controller)

    def _create_changelog(self) -> QWidget:
        from src.gui.panels.changelog_panel import ChangelogPanel

        return ChangelogPanel()
