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

from src.application.services.utils.formatters import format_date_it
from src.gui.formatters import format_currency_smart
from src.gui.styles import COLORS


class OdaDetailView(QWidget):
    """Widget per la visualizzazione del dettaglio completo di un OdA.

    Inizializza la classe.
    """

    def __init__(self, headers: list[str], parent: QWidget | None = None) -> None:
        """Inizializza il widget con la lista degli header da mostrare.

        Args:
            headers: Elenco delle intestazioni dei campi da visualizzare.
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.headers = headers
        self.detail_labels: dict[str, QLabel] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Costruisce il layout del pannello dettaglio senza bordi anti-estetici."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 8, 8)
        layout.setSpacing(8)

        detail_title = QLabel("Dettaglio Completo OdA")
        detail_title.setStyleSheet(
            f"font-weight: bold; font-size: 14px; color: {COLORS['primary_blue']}; margin-bottom: 4px;"
        )
        layout.addWidget(detail_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        # Rimuove tutti i bordi visibili dallo scroll area
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")

        self.form_layout = QFormLayout(scroll_content)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.form_layout.setSpacing(6)
        self.form_layout.setContentsMargins(0, 0, 8, 0)

        for h in self.headers:
            lbl_key = QLabel(f"<b>{h}:</b>")
            lbl_key.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px; padding: 0;")

            val_label = QLabel("-")
            val_label.setWordWrap(True)
            val_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            val_label.setStyleSheet(
                f"color: {COLORS['text_dark']}; font-size: 12px; padding: 0; border: none;"
            )
            self.detail_labels[h] = val_label
            self.form_layout.addRow(lbl_key, val_label)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def update_details(self, data: Sequence[Any]) -> None:
        """Aggiorna le label con i dati della riga selezionata.

        Args:
            data: Sequenza di valori corrispondenti agli header del dettaglio.
        """
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
        """Resetta i campi del dettaglio."""
        for label in self.detail_labels.values():
            label.setText("-")
