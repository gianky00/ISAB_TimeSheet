"""
SyncroJob - SafeWork Status List Widget
Widget per visualizzare lo stato di elaborazione riga per riga per i bot SafeWork.
"""

from typing import cast

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QLabel, QListWidget, QListWidgetItem, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon


class StatusListWidget(QListWidget):
    """Widget per visualizzare lo stato di elaborazione riga per riga della tabella bot."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza la lista degli stati."""
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet("""
      QListWidget { background: transparent; border: none; outline: none; }
      QListWidget::item { padding: 0px; margin: 0px; border: none; }
    """)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def initialize_rows(self, count: int, row_height: int = 30) -> None:
        """Prepara n righe con stato 'Pending' (pallino grigio)."""
        # Ottimizzazione: Se il numero di righe  lo stesso, resetta solo le icone esistenti
        if self.count() == count:
            for i in range(count):
                self._reset_row_icon(i)
            return

        self.clear()
        self.setUpdatesEnabled(False)
        try:
            for _ in range(count):
                item = QListWidgetItem()
                item.setSizeHint(QSize(40, row_height))

                icon_label = QLabel()
                icon_label.setFixedSize(24, 24)
                icon_label.setStyleSheet(
                    f"background-color: {COLORS['border_light']}; border-radius: 12px; border: 1px solid {COLORS['border_medium']};"
                )

                container = QWidget()
                layout = QVBoxLayout(container)
                layout.setContentsMargins(0, 3, 0, 3)
                layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignCenter)

                self.addItem(item)
                self.setItemWidget(item, container)
        finally:
            self.setUpdatesEnabled(True)

    def _reset_row_icon(self, index: int) -> None:
        """Ripristina l'icona di una riga allo stato 'Pending'."""
        item = self.item(index)
        widget = self.itemWidget(item)
        if widget:
            icon_label = widget.findChild(QLabel)
            if icon_label:
                icon_label.clear()
                icon_label.setStyleSheet(
                    f"background-color: {COLORS['border_light']}; border-radius: 12px; border: 1px solid {COLORS['border_medium']};"
                )

    def update_status(self, index: int, success: bool) -> None:
        """Aggiorna l'icona della riga specificata (Verde successo, Rosso errore)."""
        if index < 0 or index >= self.count():
            return
        item = self.item(index)
        widget = self.itemWidget(item)
        if not widget:
            return

        icon_label = cast("QLabel", widget.findChild(QLabel))
        if not icon_label:
            return

        if success:
            icon_path, color = get_asset_path(Icons.CHECK), COLORS["success_dark"]
            bg = COLORS["table_success_bg"]
        else:
            icon_path, color = get_asset_path(Icons.X_CIRCLE), COLORS["error_red"]
            bg = COLORS["table_error_bg"]

        pixmap = get_colored_icon(icon_path, color).pixmap(16, 16)
        icon_label.setPixmap(pixmap)
        icon_label.setStyleSheet(f"background-color: {bg}; border-radius: 12px; border: 1px solid {color};")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
