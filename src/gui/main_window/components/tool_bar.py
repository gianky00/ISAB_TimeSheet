"""
SyncroJob - ToolBar Component
Gestore degli elementi di navigazione e ricerca superiore e laterale.
Inizializza la sidebar, il banner degli aggiornamenti e la barra di ricerca globale.
"""

from typing import Any

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QLayout, QLineEdit

from src.gui.widgets.sidebar_widget import SidebarWidget
from src.gui.widgets.update_banner import UpdateBanner


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

    def setup_sidebar(self, layout: QLayout) -> SidebarWidget:
        """
        Crea e inserisce la sidebar nel layout principale.

        Args:
            layout: Il layout orizzontale della MainWindow.

        Returns:
            SidebarWidget: L'istanza creata della sidebar.
        """
        self.sidebar = SidebarWidget()
        layout.addWidget(self.sidebar)
        return self.sidebar

    def setup_content_toolbar(self, layout: QLayout) -> tuple[UpdateBanner, QLineEdit]:
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

        self.global_search = QLineEdit()
        self.global_search.setPlaceholderText("Ricerca Universale (OdA, Dipendenti, Log...) - Ctrl+F")
        self.global_search.setMinimumHeight(40)
        self.global_search.returnPressed.connect(
            lambda: self.main_window.search_controller.perform_search(
                self.global_search.text() if self.global_search else ""
            )
        )
        layout.addWidget(self.global_search)

        return self.update_banner, self.global_search
