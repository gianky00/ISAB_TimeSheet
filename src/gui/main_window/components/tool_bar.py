from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QLineEdit

from src.gui.widgets.sidebar_widget import SidebarWidget
from src.gui.widgets.update_banner import UpdateBanner


class ToolBarComponent(QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.sidebar = None
        self.update_banner = None
        self.global_search = None

    def setup_sidebar(self, layout):
        """Creates the sidebar in the main layout (horizontal)."""
        self.sidebar = SidebarWidget()
        # Signals will be connected by Controller
        layout.addWidget(self.sidebar)
        return self.sidebar

    def setup_content_toolbar(self, layout):
        """Creates the top toolbar in the content area (vertical layout)."""
        self.update_banner = UpdateBanner()
        # Connect internally if possible, or expose signal
        self.update_banner.download_requested.connect(
            self.main_window._on_download_update_clicked
        )
        layout.addWidget(self.update_banner)

        self.global_search = QLineEdit()
        self.global_search.setPlaceholderText(
            "Ricerca Universale (OdA, Dipendenti, Log...) - Ctrl+F"
        )
        self.global_search.setMinimumHeight(40)
        # Assuming search_controller is available on main_window
        self.global_search.returnPressed.connect(
            lambda: self.main_window.search_controller.perform_search(
                self.global_search.text()
            )
        )
        layout.addWidget(self.global_search)

        return self.update_banner, self.global_search
