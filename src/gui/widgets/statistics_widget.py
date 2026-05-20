from datetime import datetime
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.stats_manager import StatsManager
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    PrimaryButton,
    SortableTableWidgetItem,
    StandardTable,
)
from src.utils.helpers import get_asset_path, get_colored_icon


class StatisticsWidget(QWidget):
    """Widget per visualizzare le statistiche di utilizzo."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Header
        info = QLabel("Statistiche di Utilizzo Globale")
        info.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {COLORS['text_dark']};")
        layout.addWidget(info)

        # Summary Cards Container
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(15)
        layout.addLayout(self.cards_layout)

        # Table Title
        table_title = QLabel("Dettaglio Attività")
        table_title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; margin-top: 10px; color: {COLORS['text_dark']};"
        )
        layout.addWidget(table_title)

        # Table
        self.table = StandardTable()
        v_header = self.table.verticalHeader()
        if v_header is not None:
            v_header.setVisible(False)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Bot", "Esecuzioni", "Errori", "Ultima Esecuzione"])
        h_header = self.table.horizontalHeader()
        if h_header is not None:
            h_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Stile gestito via QSS
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.table)

        # Refresh Button
        refresh_btn = PrimaryButton(" Aggiorna Statistiche")
        refresh_btn.setIcon(get_colored_icon(get_asset_path(Icons.REFRESH), COLORS["text_dark"]))
        refresh_btn.setFixedWidth(200)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet(
            f"""
      QPushButton {{
        background-color: {COLORS["bg_white"]};
        color: {COLORS["text_dark"]};
        border: 1px solid {COLORS["text_dark"]};
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
      }}
      QPushButton:hover {{ background-color: {COLORS["bg_hover"]}; }}
    """
        )
        refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(refresh_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.refresh()

    def _create_summary_card(
        self,
        title: str,
        value: Any,
        color: str,
        icon_path: str | None = None,
    ) -> QFrame:
        card = QFrame()
        card.setStyleSheet(
            f"""
      QFrame {{
        background-color: {COLORS["bg_white"]};
        border: 1px solid {COLORS["border_light"]};
        border-left: 5px solid {color};
        border-radius: 8px;
      }}
    """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)

        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)

        if icon_path:
            icon_lbl = QLabel()
            icon_lbl.setPixmap(
                get_colored_icon(get_asset_path(icon_path), COLORS["text_dark"]).pixmap(16, 16)
            )
            title_layout.addWidget(icon_lbl)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 13px; font-weight: bold; border: none;"
        )
        title_layout.addWidget(lbl_title)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        lbl_val = QLabel(str(value))
        lbl_val.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: 800; border: none;")
        layout.addWidget(lbl_val)

        return card

    def refresh(self) -> None:
        """Ricarica le statistiche."""
        stats = StatsManager().get_all_stats()
        self._refresh_summary_cards(stats)
        self._refresh_stats_table(stats)

    def _refresh_summary_cards(self, stats: dict[str, Any]) -> None:
        """Aggiorna le card di riepilogo in alto."""
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        total_runs = sum(d.get("runs", 0) for d in stats.values())
        total_errors = sum(d.get("errors", 0) for d in stats.values())

        self.cards_layout.addWidget(
            self._create_summary_card("Esecuzioni Totali", total_runs, COLORS["primary_dark"], Icons.ROCKET)
        )
        self.cards_layout.addWidget(
            self._create_summary_card("Errori Totali", total_errors, COLORS["error_red"], Icons.X_CIRCLE)
        )

    def _refresh_stats_table(self, stats: dict[str, Any]) -> None:
        """Aggiorna la tabella di dettaglio attività."""
        self.table.setRowCount(0)
        bot_names = {
            "timbrature": "Timbrature",
            "scarico_ts": "Scarico TS",
            "carico_ts": "Carico TS",
            "dettagli_oda": "Dettagli OdA",
        }

        for bot_id in sorted(stats.keys()):
            data = stats[bot_id]
            row = self.table.rowCount()
            self.table.insertRow(row)

            name = bot_names.get(bot_id, bot_id.capitalize())
            runs, errors = data.get("runs", 0), data.get("errors", 0)
            last_run = data.get("last_run", "")

            # Formattazione data
            last_run_display = "Mai"
            if last_run:
                try:
                    dt = datetime.fromisoformat(str(last_run))
                    last_run_display = dt.strftime("%d/%m/%Y %H:%M")
                except Exception:
                    last_run_display = str(last_run)

            self.table.setItem(row, 0, SortableTableWidgetItem(name))
            self.table.setItem(
                row,
                1,
                SortableTableWidgetItem(runs, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter),
            )

            err_item = SortableTableWidgetItem(
                errors, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            if errors > 0:
                err_item.setForeground(Qt.GlobalColor.red)
                err_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            self.table.setItem(row, 2, err_item)
            self.table.setItem(row, 3, SortableTableWidgetItem(last_run_display))

        self.table.setSortingEnabled(True)
