"""
SyncroJob - SafeWork Status List Widget
Widget per visualizzare lo stato di elaborazione riga per riga per i bot SafeWork.
"""

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QLabel, QListWidget, QListWidgetItem, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon


class StatusListWidget(QListWidget):
    """Widget per visualizzare lo stato di elaborazione riga per riga della tabella bot."""

    def __init__(self, parent=None):
        """Inizializza la lista degli stati."""
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet("""
            QListWidget { background: transparent; border: none; outline: none; }
            QListWidget::item { padding: 0px; margin: 0px; border: none; }
        """)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def initialize_rows(self, count: int, row_height: int = 30):
        """Prepara n righe con stato 'Pending' (pallino grigio)."""
        self.clear()
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

    def update_status(self, index: int, success: bool):
        """Aggiorna l'icona della riga specificata (Verde successo, Rosso errore)."""
        if index < 0 or index >= self.count():
            return
        item = self.item(index)
        widget = self.itemWidget(item)
        if not widget:
            return
        icon_label: QLabel = widget.findChild(QLabel)
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
