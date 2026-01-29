import logging

from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.panels.dipendenti.pages.anagrafica_page import AnagraficaPage
from src.gui.panels.dipendenti_manager_panel import DipendentiManagerPanel
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class DipendentiPanel(QWidget):
    """
    Pannello principale Dipendenti.
    Facade che orchestra i sotto-pannelli (Tabs).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.tabs = QTabWidget()
        self.tabs.setProperty("class", "Level2Tabs")  # Stile Tab secondari

        # Tab 1: Monitoraggio (Vecchia interfaccia)
        self.anagrafica_page = AnagraficaPage()
        self.tabs.addTab(
            self.anagrafica_page,
            get_colored_icon(get_asset_path(Icons.ACTIVITY), "#0d6efd"),
            "Monitoraggio",
        )

        # Tab 2: Configurazione (Nuova interfaccia CRUD)
        self.manager_page = DipendentiManagerPanel()
        self.tabs.addTab(
            self.manager_page,
            get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), "#6c757d"),
            "Configurazione",
        )

        # AGGIORNAMENTO AUTOMATICO TRA TAB
        self.manager_page.data_changed.connect(self.anagrafica_page.refresh_data)

        main_layout.addWidget(self.tabs)

    def refresh_data(self):
        """Metodo pubblico chiamato dal controller per aggiornare i dati."""
        # Aggiorna il tab attivo
        current = self.tabs.currentWidget()
        if hasattr(current, "refresh_data"):
            current.refresh_data()

        # Opzionale: aggiorna anche l'altro in background se necessario
        if current == self.anagrafica_page and hasattr(self.manager_page, "refresh_data"):
            # Non forziamo il refresh grafico se non visibile, ma magari ricarica dati
            pass
