"""Modulo Oda Detail View."""

from collections.abc import Sequence
from contextlib import suppress
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.utils.formatters import format_date_it
from src.gui.formatters import format_currency_smart
from src.gui.styles import COLORS


class OdaDetailView(QWidget):
    """Widget per la visualizzazione del dettaglio completo di un OdA.

    Inizializza la classe.
    """

    def __init__(self, headers: list[str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.headers = headers
        self.detail_labels: dict[str, QLabel] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)

        detail_title = QLabel("Dettaglio Completo OdA")
        detail_title.setStyleSheet(
            f"font-weight: bold; font-size: 14px; color: {COLORS['primary_blue']}; margin-bottom: 5px;"
        )
        layout.addWidget(detail_title)

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
        layout.addWidget(scroll)

    def update_details(self, data: Sequence[Any]) -> None:
        """Aggiorna le label con i dati della riga selezionata."""
        for i, h in enumerate(self.headers):
            if i >= len(data):
                break
            val = str(data[i])
            if val.lower() == "nan" or val == "None":
                val = ""

            # Formattazione speciale
            if ("valore" in h.lower() or "prezzo" in h.lower()) and val:
                with suppress(Exception):
                    val = format_currency_smart(float(val))
            elif "data" in h.lower() and val:
                val = format_date_it(val)

            self.detail_labels[h].setText(val)

    def clear(self) -> None:
        """Resetta i campiùdel dettaglio."""
        for label in self.detail_labels.values():
            label.setText("-")
