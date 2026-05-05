"""
SyncroJob - Panel Factory
Componente responsabile dell'istanziazione "Lazy" dei pannelli dell'interfaccia utente.
Garantisce il disaccoppiamento tra la logica di navigazione e la creazione degli oggetti UI.
"""

import logging
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMessageBox, QWidget

from src.gui.main_window.page_index import PageIndex

if TYPE_CHECKING:
    from src.gui.controllers.navigation_controller import NavigationController
    from src.gui.main_window.main import MainWindow

logger = logging.getLogger(__name__)


class PanelFactory:
    """
    Factory per la creazione dei pannelli della MainWindow.
    Incapsula la logica di importazione dinamica e inizializzazione dei widget.
    """

    def __init__(self, navigation_controller: "NavigationController") -> None:
        """
        Inizializza la factory.

        Args:
            navigation_controller: Riferimento al controller di navigazione per l'iniezione delle dipendenze.
        """
        self.nav = navigation_controller
        self.mw: MainWindow = navigation_controller.mw

    def create_panel(self, index: int) -> QWidget | None:  # noqa: PLR0911, PLR0912
        """
        Crea un'istanza del pannello corrispondente all'indice specificato.

        Args:
            index: Indice della pagina (PageIndex).

        Returns:
            Istanza del QWidget o None in caso di errore.
        """

        try:
            if index == PageIndex.DASHBOARD:
                from src.gui.panels.dashboard_panel import DashboardPanel  # noqa: PLC0415
                return DashboardPanel()

            if index == PageIndex.AUTOMAZIONI:
                from src.gui.widgets.automazioni_widget import AutomazioniWidget  # noqa: PLC0415
                return AutomazioniWidget(main_window=self.mw)

            if index == PageIndex.RESERVED_AI:
                return QWidget()

            if index == PageIndex.TIMBRATURE:
                from src.gui.panels.timbrature_db import TimbratureDBPanel  # noqa: PLC0415
                return TimbratureDBPanel()

            if index == PageIndex.STRUMENTALE:
                from src.gui.panels.contabilita_panel import ContabilitaPanel  # noqa: PLC0415
                return ContabilitaPanel()

            if index == PageIndex.DATAEASE:
                from src.gui.panels.scarico_ore_panel import ScaricoOrePanel  # noqa: PLC0415
                return ScaricoOrePanel(controller=self.nav.scarico_ore_controller)

            if index == PageIndex.PDL_DB:
                from src.gui.panels.pdl.pdl_panel import PDLDBPanel  # noqa: PLC0415
                return PDLDBPanel(controller=self.nav.pdl_controller)

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
                return StoricoOdaPanel(controller=self.nav.oda_controller)

            if index == PageIndex.DIPENDENTI:
                from src.gui.panels.dipendenti.main_panel import DipendentiPanel  # noqa: PLC0415
                return DipendentiPanel(controller=self.nav.anagrafica_controller)

            if index == PageIndex.CONSUNTIVO:
                from src.gui.panels.consuntivo_panel import ConsuntivoPanel  # noqa: PLC0415
                return ConsuntivoPanel(controller=self.nav.consuntivo_controller)

        except Exception:
            logger.exception("Errore fatale nella creazione del pannello %s", index)
            QMessageBox.critical(
                None,
                "Errore Caricamento",
                f"Impossibile caricare il modulo {index}. Controlla i log di sistema."
            )

        return None
