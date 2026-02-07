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
    """Tab Principale Configurazione (ToolBox)."""

    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pages = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        # Search Bar
        search_layout = QHBoxLayout()
        search_icon = QLabel()
        search_icon.setPixmap(get_colored_icon(get_asset_path(Icons.SEARCH), "#6c757d").pixmap(20, 20))
        search_layout.addWidget(search_icon)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cerca impostazione...")
        self.search_bar.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 15px;
                padding: 8px 15px;
                background-color: #f8f9fa;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #0d6efd;
                background-color: white;
            }
            """
        )
        self.search_bar.textChanged.connect(self._filter_settings)
        search_layout.addWidget(self.search_bar)
        layout.addLayout(search_layout)

        # Toolbox
        self.toolbox = QToolBox()
        self.toolbox.setStyleSheet(
            """
            QToolBox::tab {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                color: #495057;
                font-weight: bold;
                padding: 5px 15px;
                min-height: 45px;
            }
            QToolBox::tab:selected {
                background: #e7f1ff;
                color: #0d6efd;
                border-color: #0d6efd;
            }
        """
        )

        # 1. Generale
        self.general_page = GeneralPage()
        self.general_page.settings_changed.connect(self.settings_changed.emit)
        self.toolbox.addItem(self.general_page, "Generale & Browser")
        self.pages.append(self.general_page)

        # 2. Liste
        self.lists_page = ListsPage()
        self.lists_page.settings_changed.connect(self.settings_changed.emit)
        self.toolbox.addItem(self.lists_page, "Liste Dati (Account, Contratti...)")
        self.pages.append(self.lists_page)

        # 3. Percorsi
        self.paths_page = PathsPage()
        self.paths_page.settings_changed.connect(self.settings_changed.emit)
        self.toolbox.addItem(self.paths_page, "Percorsi File & Integrazioni")
        self.pages.append(self.paths_page)

        # 4. Diagnostica
        self.diag_page = DiagPage()
        self.toolbox.addItem(self.diag_page, "Diagnostica")
        self.pages.append(self.diag_page)

        layout.addWidget(self.toolbox)

    def _filter_settings(self, text):
        """Filtra le pagine del toolbox (semplificato)."""
        # Implementazione base: espande tutto se c'è testo?
        # QToolBox non supporta il filtraggio interno facile.
        # Per ora lasciamo vuoto o espandiamo la pagina che matcha.

    def load_from_config(self, config):
        for page in self.pages:
            if hasattr(page, "load_from_config"):
                page.load_from_config(config)

    def save_to_config(self, config_manager):
        for page in self.pages:
            if hasattr(page, "save_to_config"):
                page.save_to_config(config_manager)
