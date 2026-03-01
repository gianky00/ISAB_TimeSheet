"""
SyncroJob - ToolBar Component
Gestore degli elementi di navigazione e ricerca superiore e laterale.
Inizializza la sidebar, il banner degli aggiornamenti e la barra di ricerca globale.
"""

from typing import Any

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QLineEdit, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.widgets.core_widgets import (
    SearchInput,
)
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.sidebar_widget import SidebarWidget
from src.gui.widgets.update_banner import UpdateBanner
from src.utils.helpers import get_asset_path


class ToolBarComponent(QObject):
    """
    Coordina la creazione e il posizionamento dei componenti di navigazione principali.
    Gestisce la comunicazione tra la barra di ricerca globale e il SearchController.
    """

    def __init__(self, main_window: Any) -> None:
        """
        Inizializza il componente ToolBar.

        Args:
            main_window: Riferimento alla MainWindow dell'applicazione.
        """
        super().__init__(main_window)
        self.main_window = main_window
        self.sidebar: SidebarWidget | None = None
        self.update_banner: UpdateBanner | None = None
        self.global_search: QLineEdit | None = None

    def setup_sidebar(self, parent_widget: QWidget) -> SidebarWidget:
        """
        Crea la sidebar per l'uso come overlay.

        Args:
            parent_widget: Il widget genitore.

        Returns:
            SidebarWidget: L'istanza creata della sidebar.
        """
        self.sidebar = SidebarWidget(parent_widget)
        return self.sidebar

    def setup_content_toolbar(self, layout: QVBoxLayout) -> tuple[UpdateBanner, QLineEdit]:
        """
        Crea la barra superiore nell'area dei contenuti (Banner + Ricerca).

        Args:
            layout: Il layout verticale dell'area centrale.

        Returns:
            tuple: (Istanza UpdateBanner, Istanza QLineEdit della ricerca).
        """
        self.update_banner = UpdateBanner()
        self.update_banner.download_requested.connect(self.main_window._on_download_update_clicked)
        layout.addWidget(self.update_banner)

        # Wrap search bar in a horizontal layout to add margin for floating logo
        from PyQt6.QtWidgets import QHBoxLayout

        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(75, 0, 0, 0)  # Spazio per il logo fluttuante

        self.global_search = SearchInput()
        self.global_search.setPlaceholderText("Ricerca Universale (OdA, Dipendenti, Log...) - Ctrl+F")
        self.global_search.setMinimumHeight(40)
        self.global_search.returnPressed.connect(
            lambda: self.main_window.search_controller.perform_search(
                self.global_search.text() if self.global_search else ""
            )
        )
        search_layout.addWidget(self.global_search)

        # Pulsante Split Window (Vista Esterna) Universale
        self.detach_btn = ModernButton(
            "",
            variant=ModernButton.Variant.SECONDARY,
            size=ModernButton.Size.MEDIUM,
            icon=get_asset_path(Icons.SPLIT_WINDOW),
        )
        self.detach_btn.setToolTip("Sgancia la vista corrente in una finestra esterna (Multi-Window)")
        self.detach_btn.setFixedWidth(45)
        self.detach_btn.clicked.connect(self.main_window.navigation_controller.detach_current_panel)
        search_layout.addWidget(self.detach_btn)

        layout.addLayout(search_layout)

        return self.update_banner, self.global_search
