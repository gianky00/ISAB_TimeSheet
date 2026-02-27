"""
SyncroJob - Dashboard Stat Card
Card elegante per la visualizzazione di metriche rapide in home page.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.gui.styles import COLORS
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon


class DashboardStatCard(ModernCard):
    """
    Card informativa per la Dashboard.
    Mostra un valore, un'etichetta e un'icona tematica.
    """

    def __init__(
        self,
        title: str,
        value: str,
        icon_key: str,
        color: str = COLORS["primary_blue"],
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent, elevation=12)
        self.setMinimumHeight(100)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # Icona Badge
        self.icon_container = QWidget()
        self.icon_container.setFixedSize(50, 50)
        self.icon_container.setStyleSheet(f"""
            background-color: {color}20; /* 20% opacity */
            border-radius: 25px;
        """)
        icon_layout = QVBoxLayout(self.icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(get_colored_icon(get_asset_path(icon_key), color).pixmap(24, 24))
        icon_layout.addWidget(icon_lbl)
        layout.addWidget(self.icon_container)

        # Testi
        text_v = QVBoxLayout()
        text_v.setSpacing(2)
        text_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.val_lbl = QLabel(value)
        self.val_lbl.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 900;
            color: {COLORS["text_dark"]};
            background: transparent;
        """)

        self.title_lbl = QLabel(title.upper())
        self.title_lbl.setStyleSheet(f"""
            font-size: 10px;
            font-weight: 800;
            color: {COLORS["text_muted"]};
            letter-spacing: 1.5px;
            background: transparent;
        """)

        self.detail_lbl = QLabel("")
        self.detail_lbl.setStyleSheet(f"""
            font-size: 11px;
            font-weight: 600;
            color: {COLORS["text_dark"]};
            background: transparent;
            margin-top: 4px;
        """)
        
        self.meta_lbl = QLabel("")
        self.meta_lbl.setStyleSheet(f"""
            font-size: 10px;
            color: {COLORS["text_muted"]};
            background: transparent;
            font-style: italic;
        """)

        text_v.addWidget(self.val_lbl)
        text_v.addWidget(self.title_lbl)
        text_v.addWidget(self.detail_lbl)
        text_v.addWidget(self.meta_lbl)
        layout.addLayout(text_v)

        layout.addStretch()

    def update_value(self, new_value: str, details: str = "", meta: str = "") -> None:
        self.val_lbl.setText(new_value)
        if details:
            self.detail_lbl.setText(details)
            self.detail_lbl.show()
        else:
            self.detail_lbl.hide()
            
        if meta:
            self.meta_lbl.setText(meta)
            self.meta_lbl.show()
        else:
            self.meta_lbl.hide()
