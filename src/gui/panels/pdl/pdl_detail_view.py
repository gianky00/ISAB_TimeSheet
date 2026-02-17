from collections.abc import Sequence
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFormLayout,
    QHeaderView,
    QLabel,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class PDLDetailView(QWidget):
    """Widget per la visualizzazione del dettaglio completo di un PDL."""

    def __init__(self, headers: list[str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.headers = headers
        self.detail_labels: dict[str, QLabel] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(10)

        detail_title = QLabel("Dettaglio Completo PDL")
        detail_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #2196F3; margin-bottom: 5px;")
        layout.addWidget(detail_title)

        # Sezione Dati Generali (Scrollabile)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.form_layout = QFormLayout(scroll_content)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.form_layout.setSpacing(10)

        for h in self.headers:
            val_label = QLabel("-")
            val_label.setWordWrap(True)
            val_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.detail_labels[h] = val_label
            self.form_layout.addRow(f"<b>{h}:</b>", val_label)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, 2)  # Stretch factor 2

        # Sezione Cronologia Interventi
        cron_label = QLabel("Cronologia Interventi (Report Attività)")
        cron_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #4CAF50; margin-top: 10px;")
        layout.addWidget(cron_label)

        self.cron_table = QTableWidget()
        self.cron_table.setColumnCount(5)
        self.cron_table.setHorizontalHeaderLabels(["Data", "Fonte", "Tecnico", "Ore", "Descrizione"])
        self.cron_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.cron_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.cron_table.setAlternatingRowColors(True)
        self.cron_table.setStyleSheet("QTableWidget { font-size: 11px; }")
        layout.addWidget(self.cron_table, 1)  # Stretch factor 1

    def update_details(self, data: Sequence[Any], interventions: list[dict[str, Any]] | None = None) -> None:
        """Aggiorna le label con i dati forniti e popola la cronologia."""
        for i, h in enumerate(self.headers):
            if i >= len(data):
                break
            val = str(data[i])
            if val.lower() == "nan" or val == "None":
                val = ""

            # Formattazione "Importato il"
            if h == "Importato il" and val:
                with suppress(Exception):
                    dt = datetime.strptime(val, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
                    val = dt.strftime("%d/%m/%Y %H:%M:%S")

            self.detail_labels[h].setText(val)

        # Aggiorna Cronologia
        self.cron_table.setRowCount(0)
        if interventions:
            self.cron_table.setRowCount(len(interventions))
            for row_idx, inv in enumerate(interventions):
                self.cron_table.setItem(row_idx, 0, QTableWidgetItem(inv.get("data", "")))

                fonte_item = QTableWidgetItem(inv.get("fonte", ""))
                # Colora in base alla fonte per visibilità
                if "In Attesa" in inv.get("fonte", ""):
                    fonte_item.setForeground(QColor("#f39c12"))  # Arancione
                elif "Validato" in inv.get("fonte", ""):
                    fonte_item.setForeground(QColor("#198754"))  # Verde

                self.cron_table.setItem(row_idx, 1, fonte_item)
                self.cron_table.setItem(row_idx, 2, QTableWidgetItem(inv.get("tecnico", "")))
                self.cron_table.setItem(row_idx, 3, QTableWidgetItem(str(inv.get("ore_lavoro", ""))))
                desc_item = QTableWidgetItem(inv.get("descrizione", ""))
                desc_item.setToolTip(inv.get("descrizione", ""))
                self.cron_table.setItem(row_idx, 4, desc_item)

    def clear(self) -> None:
        """Resetta i campi del dettaglio e la cronologia."""
        for label in self.detail_labels.values():
            label.setText("-")
        self.cron_table.setRowCount(0)
