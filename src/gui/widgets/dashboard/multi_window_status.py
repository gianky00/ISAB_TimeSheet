"""SyncroJob - MultiWindow Status Widget.

Visualizza nella dashboard un riepilogo delle finestre attualmente sganciate, permettendo di riagganciarle.
"""

from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS, card_style
from src.utils.helpers import get_asset_path, get_colored_icon

# Stile forzato per i tooltip in Light Mode
TOOLTIP_CSS = """
QToolTip {
  background-color: #FFFFFF;
  color: #212121;
  border: 1px solid #BBBBBB;
  border-radius: 6px;
  padding: 8px 12px;
}
"""


class DetachedModuleItem(QFrame):
    """Singola voce di un modulo sganciato nella card.

    Inizializza la classe.
    """

    reattach_requested = Signal(int)

    def __init__(self, index: int, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.index = index
        self.title = title
        self.setFixedHeight(46)

        self.setStyleSheet(f"""
      QFrame {{
        background-color: {COLORS["bg_hover"]};
        border-radius: 8px;
        border: 1px solid {COLORS["border_light"]};
      }}
      QFrame:hover {{
        background-color: #E3F2FD;
        border: 1px solid #81C784;
      }}
    """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 10, 0)

        # Icona generica
        icon_lbl = QLabel()
        icon_path = get_asset_path(Icons.SPLIT_WINDOW)
        icon_lbl.setPixmap(get_colored_icon(icon_path, COLORS["primary_blue"]).pixmap(18, 18))
        layout.addWidget(icon_lbl)

        # Titolo
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(
            f"font-weight: bold; color: {COLORS['text_dark']}; font-size: 13px; border: none; background: transparent;"
        )
        layout.addWidget(title_lbl)

        layout.addStretch()

        # Bottone Riaggancia
        self.btn = QPushButton("Riaggancia")
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setStyleSheet(f"""
      QPushButton {{
        background-color: {COLORS["bg_white"]};
        color: #2E7D32;
        border: 1px solid #A5D6A7;
        border-radius: 6px;
        padding: 4px 12px;
        font-weight: bold;
        font-size: 11px;
      }}
      QPushButton:hover {{
        background-color: #4CAF50;
        color: white;
      }}
    """)

        self.btn.clicked.connect(lambda: self.reattach_requested.emit(self.index))
        layout.addWidget(self.btn)


class MultiWindowStatusWidget(QFrame):
    """Card della Dashboard che mostra i moduli attualmente in esecuzione in finestre esterne.

    Sìnasconde automaticamente se non ci sono moduli sganciati.

    Inizializza la classe.
    """

    reattach_all_requested = Signal()
    reattach_single_requested = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("multiWindowStatusCard")
        self.setStyleSheet(card_style())

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self._setup_header()

        self.items_container = QVBoxLayout()
        self.items_container.setSpacing(8)
        self.main_layout.addLayout(self.items_container)

        self.hide()  # Nascosto di default

    def _setup_header(self) -> None:
        header_layout = QHBoxLayout()

        # Titolo e Icona
        icon_lbl = QLabel()
        icon_path = get_asset_path(Icons.SPLIT_WINDOW)
        icon_lbl.setPixmap(get_colored_icon(icon_path, COLORS["primary_blue"]).pixmap(24, 24))

        title_lbl = QLabel("Moduli in Finestre Esterne")
        title_lbl.setStyleSheet(f"font-size: 16px; font-weight: 800; color: {COLORS['text_dark']};")

        # Badge contatore
        self.count_badge = QLabel("0")
        self.count_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_badge.setFixedSize(24, 24)
        self.count_badge.setStyleSheet(f"""
      background-color: {COLORS["primary_blue"]};
      color: white;
      border-radius: 12px;
      font-weight: bold;
      font-size: 12px;
    """)

        header_layout.addWidget(icon_lbl)
        header_layout.addWidget(title_lbl)
        header_layout.addWidget(self.count_badge)
        header_layout.addStretch()

        # Bottone "Riaggancia Tutti"
        self.reattach_all_btn = QPushButton("Riaggancia Tutti")
        self.reattach_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reattach_all_btn.setStyleSheet(f"""
      QPushButton {{
        color: {COLORS["primary_blue"]};
        background: transparent;
        border: none;
        font-weight: bold;
        font-size: 12px;
        text-decoration: underline;
      }}
      QPushButton:hover {{
        color: #1976D2;
      }}
    """)

        self.reattach_all_btn.clicked.connect(lambda: self.reattach_all_requested.emit())
        header_layout.addWidget(self.reattach_all_btn)

        self.main_layout.addLayout(header_layout)

    def update_modules(self, detached_panels: dict[int, dict[str, Any]]) -> None:
        """Aggiorna la lista dei moduli sganciati. Mostra/Nasconde la card di conseguenza.

        Args:
          detached_panels: Dizionario con chiavi index e valori dict contenenti "panel", "title" o la window.
        """
        # Pulisci layout esistente
        while self.items_container.count():
            layout_item = self.items_container.takeAt(0)
            if layout_item:
                widget = layout_item.widget()
                if widget:
                    widget.deleteLater()

        count = len(detached_panels)
        self.count_badge.setText(str(count))

        if count == 0:
            self.hide()
            return

        self.show()

        for idx, data in detached_panels.items():
            # Recupera il titolo dalla window se disponibile, altrimenti usa un placeholder
            title = "Modulo Sconosciuto"
            if "window" in data and hasattr(data["window"], "windowTitle"):
                title = data["window"].windowTitle().replace(" - SyncroJob (Finestra Esterna)", "")

            module_item = DetachedModuleItem(idx, title)
            module_item.reattach_requested.connect(self.reattach_single_requested.emit)
            self.items_container.addWidget(module_item)
