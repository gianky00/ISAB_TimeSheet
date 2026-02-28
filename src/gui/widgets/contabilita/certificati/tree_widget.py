"""
SyncroJob - Certificati Tree Widget
Componente specializzato per la visualizzazione gerarchica dei certificati campione.
"""

from typing import ClassVar

from PyQt6.QtGui import QBrush, QColor, QIcon
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.contabilita.helpers import SortableTreeWidgetItem
from src.gui.widgets.core_widgets import StandardTreeWidget
from src.utils.helpers import get_asset_path


class CertificatiTreeWidget(StandardTreeWidget):
    """Tree Widget specializzato per la gestione dei certificati."""

    HEADERS: ClassVar[list[str]] = [
        "Modello /\nTipo",
        "Costruttore",
        "Matricola",
        "Range\nStrumento",
        "Errore\nmax %",
        "Certificato\nTaratura",
        "Scadenza\nCertificato",
        "Emissione\nCertificato",
        "ID-COEMI",
        "Stato\nCertificato",
    ]

    (
        IDX_MODELLO,
        IDX_COSTRUTTORE,
        IDX_MATRICOLA,
        IDX_RANGE,
        IDX_ERRORE,
        IDX_CERTIFICATO,
        IDX_SCADENZA,
        IDX_EMISSIONE,
        IDX_ID,
        IDX_STATO,
    ) = range(10)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setHeaderLabels(self.HEADERS)
        self.setWordWrap(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setAnimated(True)

        h = self.header()
        if h:
            for col in range(10):
                h.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
            h.setStretchLastSection(True)

        self.setStyleSheet(f"""
            QTreeWidget {{
                border: 1px solid {COLORS["border_light"]};
                border-radius: 8px;
                background-color: {COLORS["bg_white"]};
                outline: none;
            }}
            QTreeWidget::item {{
                padding: 8px 4px;
                border-bottom: 1px solid {COLORS["bg_alt"]};
            }}
            QTreeWidget::item:hover {{ background-color: {COLORS["bg_light"]}; }}
            QTreeWidget::item:selected {{
                background-color: {COLORS["bg_info_pastel"]};
                color: {COLORS["primary_dark"]};
            }}
            QHeaderView::section {{
                background-color: {COLORS["bg_light"]};
                padding: 10px 8px;
                border: none;
                border-bottom: 2px solid {COLORS["border_light"]};
                border-right: 1px solid {COLORS["border_light"]};
                font-weight: bold;
                color: {COLORS["text_muted"]};
            }}
        """)

    def apply_current_certificate_styling(
        self, item: SortableTreeWidgetItem, days_to_expiry: int | None, status_dot_icon: str
    ):
        """Applica lo styling specifico per il certificato più recente."""
        if days_to_expiry is None:
            status_text, bg_color, text_color = "N/D", COLORS["bg_alt"], COLORS["text_muted"]
        elif days_to_expiry < 0:
            status_text, bg_color, text_color = (
                f"Scaduto da {abs(days_to_expiry)} giorni",
                COLORS["bg_error_pastel"],
                COLORS["error_red"],
            )
        elif 0 <= days_to_expiry <= 15:
            status_text, bg_color, text_color = (
                f"Scade tra {days_to_expiry} giorni",
                COLORS["bg_warning_pastel"],
                COLORS["warning_orange"],
            )
        elif 16 <= days_to_expiry <= 30:
            status_text, bg_color, text_color = (
                f"Scade tra {days_to_expiry} giorni",
                COLORS["bg_attention_pastel"],
                COLORS["warning_yellow"],
            )
        else:
            status_text, bg_color, text_color = (
                f"Attivo ({days_to_expiry} giorni rimanenti)",
                COLORS["bg_success_pastel"],
                COLORS["success_dark"],
            )

        for col in range(self.columnCount()):
            item.setBackground(col, QBrush(QColor(bg_color)))

        item.setIcon(self.IDX_STATO, QIcon(get_asset_path(status_dot_icon)))
        item.setText(self.IDX_STATO, status_text)
        item.setForeground(self.IDX_STATO, QBrush(QColor(text_color)))

        font = item.font(self.IDX_STATO)
        font.setBold(True)
        item.setFont(self.IDX_STATO, font)

    def apply_historical_certificate_styling(self, item: SortableTreeWidgetItem):
        """Applica lo styling per i certificati storici."""
        bg_color = QColor(COLORS["bg_alt"])
        for col in range(self.columnCount()):
            item.setBackground(col, QBrush(bg_color))

        item.setIcon(self.IDX_STATO, QIcon(get_asset_path(Icons.STATUS_DOT_GRAY)))
        item.setText(self.IDX_STATO, "STORICO")
        item.setForeground(self.IDX_STATO, QBrush(QColor(COLORS["text_light"])))
        item.setToolTip(self.IDX_STATO, "Certificato storico - Esiste un certificato più recente")
