"""SyncroJob - ToolBar Component.

Gestore degli elementi di navigazione e ricerca superiore e laterale.
Inizializza la sidebar, il banner degli aggiornamenti e la barra di ricerca globale.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QEasingCurve, QEvent, QObject, QPropertyAnimation, QSize, Qt
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.widgets.core_widgets import (
    SearchInput,
)
from src.gui.widgets.sidebar_widget import SidebarWidget
from src.gui.widgets.update_banner import UpdateBanner
from src.utils.helpers import get_asset_path, get_colored_icon

if TYPE_CHECKING:
    from PySide6.QtGui import QEnterEvent

    from src.gui.main_window.main import MainWindow


class AnimatedSplitButton(QPushButton):
    """Pulsante Split personalizzato con sfondo bianco, massimo contrasto e animazione al passaggio del mouse."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza la classe."""
        super().__init__(parent)
        self.setFixedWidth(45)
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.is_detached_mode = False

        # Setup Animazione (Bounce sull'icon size)
        self.anim = QPropertyAnimation(self, b"iconSize")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.Type.OutBack)

        self.set_state(False)

    def set_state(self, is_detached: bool) -> None:
        """Aggiorna l'aspetto del pulsante in base allo stato del pannello corrente."""
        self.is_detached_mode = is_detached
        if is_detached:
            self.setToolTip("Riaggancia la vista corrente alla finestra principale")
            self.setStyleSheet("""
        QPushButton {
          background-color: #E8F5E9;
          border: 2px solid #2E7D32;
          border-radius: 8px;
        }
        QPushButton:hover {
          background-color: #C8E6C9;
          border: 2px solid #1B5E20;
        }
        QPushButton:pressed {
          background-color: #A5D6A7;
          padding-top: 2px;
        }
      """)

            icon_path = get_asset_path(Icons.CHEVRON_DOWN)
            self.setIcon(get_colored_icon(icon_path, "#1B5E20"))
        else:
            self.setToolTip("Sgancia la vista corrente in una finestra esterna (Multi-Window)")
            self.setStyleSheet("""
        QPushButton {
          background-color: #FFFFFF;
          border: 2px solid #2C3E50;
          border-radius: 8px;
        }
        QPushButton:hover {
          background-color: #F0F4F8;
          border: 2px solid #3498DB;
        }
        QPushButton:pressed {
          background-color: #E2E8F0;
          padding-top: 2px;
        }
      """)

            icon_path = get_asset_path(Icons.SPLIT_WINDOW)
            self.setIcon(get_colored_icon(icon_path, "#212121"))

        self.setIconSize(QSize(20, 20))

    def enterEvent(self, event: QEnterEvent) -> None:
        """Animazione di ingrandimento dell'icona al passaggio del mouse."""
        self.anim.stop()
        self.anim.setStartValue(QSize(20, 20))
        self.anim.setEndValue(QSize(26, 26))
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        """Ritorno alla dimensione normale."""
        self.anim.stop()
        self.anim.setStartValue(self.iconSize())
        self.anim.setEndValue(QSize(20, 20))
        self.anim.start()
        super().leaveEvent(event)


class ToolBarComponent(QObject):
    """Coordina la creazione e il posizionamento dei componenti di navigazione principali.

    Gestisce la comunicazione tra la barra di ricerca globale e il SearchController.
    """

    def __init__(self, main_window: MainWindow) -> None:
        """Inizializza il componente ToolBar.

        Args:
          main_window: Riferimento alla MainWindow dell'applicazione.
        """
        super().__init__(main_window)
        self.main_window = main_window
        self.sidebar: SidebarWidget | None = None
        self.update_banner: UpdateBanner | None = None
        self.global_search: QLineEdit | None = None
        self.detach_btn: AnimatedSplitButton | None = None

    def setup_sidebar(self, parent_widget: QWidget) -> SidebarWidget:
        """Crea la sidebar per l'uso come overlay.

        Args:
          parent_widget: Il widget genitore.

        Returns:
          SidebarWidget: L'istanza creata della sidebar.
        """
        self.sidebar = SidebarWidget(parent_widget)
        return self.sidebar

    def setup_content_toolbar(self, layout: QVBoxLayout) -> tuple[UpdateBanner, QLineEdit]:
        """Crea la barra superiore nell'area dei contenuti (Banner + Ricerca).

        Args:
          layout: Il layout verticale dell'area centrale.

        Returns:
          tuple: (Istanza UpdateBanner, Istanza QLineEdit della ricerca).
        """
        self.update_banner = UpdateBanner()
        self.update_banner.download_requested.connect(self.main_window._on_download_update_clicked)
        layout.addWidget(self.update_banner)

        # Wrap search bar in a horizontal layout to add margin for floating logo
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

        # Pulsante Split Window (Vista Esterna) Universale con animazione
        self.detach_btn = AnimatedSplitButton()
        self.detach_btn.clicked.connect(self._handle_split_click)
        search_layout.addWidget(self.detach_btn)

        layout.addLayout(search_layout)

        # Connessione ai segnali per mantenere aggiornato il pulsante
        self.main_window.stacked_widget.currentChanged.connect(self._update_split_button_state)
        self.main_window.navigation_controller.panel_detached.connect(self._update_split_button_state)
        self.main_window.navigation_controller.panel_reattached.connect(self._update_split_button_state)

        return self.update_banner, self.global_search

    def _handle_split_click(self) -> None:
        """Gestisce il click sul pulsante split, eseguendo detach o reattach in base allo stato."""
        idx = self.main_window.stacked_widget.currentIndex()
        if self.detach_btn and self.detach_btn.is_detached_mode:
            self.main_window.navigation_controller.reattach_panel(idx)
        else:
            self.main_window.navigation_controller.detach_panel(idx)

    def _update_split_button_state(self, *args: object) -> None:
        """Aggiorna lo stile e l'azione del pulsante split verificando se il pannello corrente  sganciato."""
        idx = self.main_window.stacked_widget.currentIndex()
        is_detached = idx in self.main_window.navigation_controller._detached_panels
        if self.detach_btn:
            self.detach_btn.set_state(is_detached)
