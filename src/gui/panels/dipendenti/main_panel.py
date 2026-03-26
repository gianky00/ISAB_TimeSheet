# mypy: disable-error-code="no-untyped-def, no-untyped-call, arg-type, attr-defined, misc, no-redef"
"""
SyncroJob - Employees Main Panel
Pannello principale per la gestione del personale che orchestra i tab di monitoraggio e configurazione.
Funge da punto di ingresso unico per tutte le funzionalità relative ai dipendenti.
"""

import logging
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QVBoxLayout, QWidget

if TYPE_CHECKING:
    from src.core.dipendenti.anagrafica_controller import AnagraficaController

from src.core.constants import Icons
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.panels.dipendenti.pages.anagrafica_page import AnagraficaPage
from src.gui.panels.dipendenti_manager_panel import DipendentiManagerPanel
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class DipendentiPanel(QWidget):
    """
    Pannello principale Dipendenti (Facade).
    Coordina i sotto-pannelli organizzati in tab:
    - Monitoraggio: Analisi abilitazioni e accessi.
    - Configurazione: Gestione anagrafica (CRUD).
    """

    def __init__(self, controller: "AnagraficaController", parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello dipendenti con iniezione del controller.

        Args:
            controller: Istanza del controller per la logica di business.
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout principale e inizializza i widget dei tab."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.tabs = AnimatedTabWidget()

        # Tab 1: Monitoraggio
        self.anagrafica_page = AnagraficaPage(controller=self.controller)
        self.tabs.addTab(
            self.anagrafica_page,
            get_colored_icon(get_asset_path(Icons.ACTIVITY), COLORS["primary_dark"]),
            "Monitoraggio",
        )

        # Tab 2: Configurazione
        self.manager_page = DipendentiManagerPanel()
        self.tabs.addTab(
            self.manager_page,
            get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), COLORS["text_muted"]),
            "Configurazione",
        )

        # Sincronizzazione dati tra tab
        self.manager_page.data_changed.connect(self.anagrafica_page.refresh_data)

        main_layout.addWidget(self.tabs)

    def set_current_tab(self, index: int | None = None) -> None:
        """Cambia il tab visualizzato in base all'indice fornito."""
        if index is not None and 0 <= index < self.tabs.count():
            self.tabs.setCurrentIndex(index)

    def refresh_data(self) -> None:
        """
        Aggiorna i dati del pannello.
        Metodo pubblico chiamato dal NavigationController o in risposta ad eventi globali.
        Innesca il refresh sul widget del tab attualmente attivo.
        """
        # Aggiorna il tab attivo
        current = self.tabs.currentWidget()
        if current and hasattr(current, "refresh_data") and callable(current.refresh_data):
            current.refresh_data()
