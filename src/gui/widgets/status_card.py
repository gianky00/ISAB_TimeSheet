"""
SyncroJob - Status Card (Modern)
Card per la status bar che mostra lo stato di un servizio con ombre morbide.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.design.colors import get_palette
from src.gui.styles import COLORS
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon


class StatusCard(ModernCard):
    """
    Card per la status bar che mostra lo stato di un servizio.
    Eredita da ModernCard per ombre e hover premium.
    """

    clicked = Signal()

    def __init__(self, title: str, status: str = "In attesa", parent: QWidget | None = None) -> None:
        super().__init__(parent, elevation=8)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Override base style for status bar context
        self.setStyleSheet(f"""
      QFrame#modernCard {{
        background-color: {COLORS["bg_white"]};
        border: 1px solid {COLORS["border_light"]};
        border-radius: 8px;
      }}
    """)

        self._palette = get_palette()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 4, 12, 4)
        layout.setSpacing(12)

        # 1. Icona colorata (Barra verticale decorativa)
        self._icon_bar = QFrame()
        self._icon_bar.setFixedWidth(4)
        self._icon_bar.setStyleSheet(f"background-color: {self._palette.primary}; border-radius: 2px;")
        layout.addWidget(self._icon_bar)

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(20, 20)
        icon_lbl.setScaledContents(True)
        icon_lbl.setPixmap(
            get_colored_icon(get_asset_path(Icons.CLOCK), self._palette.on_surface).pixmap(20, 20)
        )
        layout.addWidget(icon_lbl)

        # 2. Colonna Centrale: Titolo e Stato
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._title_label = QLabel(title)
        self._title_label.setStyleSheet(
            f"font-weight: 700; font-size: 13px; color: {self._palette.on_surface}; border: none; background: transparent;"
        )
        text_layout.addWidget(self._title_label)

        self._status = status
        self._status_label = QLabel(status)
        self._status_label.setStyleSheet(
            f"font-size: 11px; color: {self._palette.on_surface}; opacity: 0.8; border: none; background: transparent;"
        )
        text_layout.addWidget(self._status_label)

        layout.addLayout(text_layout)

        # 3. Spacer elastico
        layout.addStretch()

        # 4. Badge Autopilot
        self._meta_label = QLabel()
        self._meta_label.setVisible(False)
        self._meta_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._meta_label)

    def setStatus(self, message: str, status_id: str | None = None) -> None:
        """Aggiorna il messaggio di stato e il colore della barra laterale."""
        self._status_label.setText(message)
        if status_id:
            self._status = status_id
            self._icon_bar.setStyleSheet(
                f"background-color: {status_id if status_id.startswith('#') else self._palette.primary}; border-radius: 2px;"
            )

    def setAutopilot(self, active: bool, text: str = "") -> None:
        """Mostra o nasconde l'indicatore Autopilot."""
        if active:
            self._meta_label.setText(text.upper() or "AUTO")
            self._meta_label.setVisible(True)
            self._meta_label.setStyleSheet(
                f"""
        font-size: 11px;
        font-weight: 800;
        color: {COLORS["success_material"]};
        background-color: {COLORS["table_success_bg"]};
        border-radius: 6px;
        padding: 6px 10px;
        border: 1px solid {COLORS["success_green"]};
        """
            )
        else:
            self._meta_label.setVisible(False)

    def _update_status_display(self, message: str) -> None:
        """Metodo di compatibilit  per l'aggiornamento rapido dello stato."""
        self._status_label.setText(message)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Emette il segnale di click."""
        self.clicked.emit()
        super().mousePressEvent(event)
