"""
SyncroJob - Config Tab
Organizzatore della configurazione principale strutturato in un QToolBox.
Contiene le pagine per impostazioni generali, gestione liste, percorsi e diagnostica.
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QToolBox,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.panels.settings.pages.diag_page import DiagPage
from src.gui.panels.settings.pages.general_page import GeneralPage
from src.gui.panels.settings.pages.lists_page import ListsPage
from src.gui.panels.settings.pages.paths_page import PathsPage
from src.utils.helpers import get_asset_path, get_colored_icon


class ConfigTab(QWidget):
    """
    Tab contenitore che raggruppa le diverse pagine di configurazione.
    Fornisce una barra di ricerca per filtrare le impostazioni e delega il caricamento/salvataggio alle singole pagine.
    """

    settings_changed = pyqtSignal()
    """Segnale emesso quando una qualsiasi impostazione nelle pagine figlie cambia."""

    def __init__(self, parent=None):
        """
        Inizializza il tab di configurazione.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.pages = []
        self._setup_ui()

    def _setup_ui(self):
        """Configura la barra di ricerca e il componente QToolBox con le pagine tematiche."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        # Search Bar Area
        search_layout = QHBoxLayout()
        search_icon = QLabel()
        search_icon.setPixmap(get_colored_icon(get_asset_path(Icons.SEARCH), "#6c757d").pixmap(20, 20))
        search_layout.addWidget(search_icon)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cerca impostazione...")
        self.search_bar.setStyleSheet(
            "QLineEdit { border: 1px solid #ced4da; border-radius: 15px; padding: 8px 15px; background-color: #f8f9fa; font-size: 14px; }"
        )
        self.search_bar.textChanged.connect(self._filter_settings)
        search_layout.addWidget(self.search_bar)
        layout.addLayout(search_layout)

        # Toolbox Setup
        self.toolbox = QToolBox()
        self.toolbox.setStyleSheet(
            "QToolBox::tab { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 5px 15px; min-height: 45px; } QToolBox::tab:selected { background: #e7f1ff; color: #0d6efd; border-color: #0d6efd; }"
        )

        # Inizializzazione Pagine
        self.general_page = GeneralPage()
        self.general_page.settings_changed.connect(self.settings_changed.emit)
        self.toolbox.addItem(self.general_page, "Generale & Browser")
        self.pages.append(self.general_page)

        self.lists_page = ListsPage()
        self.lists_page.settings_changed.connect(self.settings_changed.emit)
        self.toolbox.addItem(self.lists_page, "Liste Dati (Account, Contratti...)")
        self.pages.append(self.lists_page)

        self.paths_page = PathsPage()
        self.paths_page.settings_changed.connect(self.settings_changed.emit)
        self.toolbox.addItem(self.paths_page, "Percorsi File & Integrazioni")
        self.pages.append(self.paths_page)

        self.diag_page = DiagPage()
        self.toolbox.addItem(self.diag_page, "Diagnostica")
        self.pages.append(self.diag_page)

        layout.addWidget(self.toolbox)

    def _filter_settings(self, text):
        """Metodo placeholder per il filtraggio futuro dei widget all'interno del toolbox."""

    def load_from_config(self, config):
        """
        Delega il caricamento delle impostazioni a tutte le pagine registrate.

        Args:
            config: Dizionario di configurazione caricato.
        """
        for page in self.pages:
            if hasattr(page, "load_from_config"):
                page.load_from_config(config)

    def save_to_config(self, config_manager):
        """
        Delega il salvataggio dei dati correnti a tutte le pagine registrate.

        Args:
            config_manager: Riferimento al modulo o all'istanza del gestore configurazione.
        """
        for page in self.pages:
            if hasattr(page, "save_to_config"):
                page.save_to_config(config_manager)
