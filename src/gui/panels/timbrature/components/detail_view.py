from collections.abc import Sequence
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFormLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from src.gui.styles import COLORS


class TimbratureDetailView(QWidget):
    """
    Componente per la visualizzazione dei dettagli di una timbratura.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.detail_labels: dict[str, QLabel] = {}
        # Mapping completo per il Dettaglio (Tutte le 18 colonne rilevate)
        self.full_headers = [
            "Data",
            "Ingresso",
            "Uscita",
            "Nome",
            "Cognome",
            "Codice Fiscale",
            "ID Dipendente",
            "Fornitore",
            "Numero Badge",
            "Reparto",
            "Cantiere",
            "Presenza TS",
            "Sito",
            "Codice RILPRES",
            "Codice Qualifica",
            "Specializzazione",
            "Società Ospitante",
            "Data Inserimento",
        ]
        self._setup_ui()

    def _setup_ui(self) -> None:
        detail_layout = QVBoxLayout(self)
        detail_layout.setContentsMargins(10, 0, 5, 0)

        detail_title = QLabel("Dettaglio Timbratura")
        detail_title.setStyleSheet(
            f"font-weight: bold; font-size: 14px; color: {COLORS['primary_blue']}; margin-bottom: 5px;"
        )
        detail_layout.addWidget(detail_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.form_layout = QFormLayout(scroll_content)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.form_layout.setSpacing(10)

        for h in self.full_headers:
            val_label = QLabel("-")
            val_label.setWordWrap(True)
            val_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.detail_labels[h] = val_label
            self.form_layout.addRow(f"<b>{h}:</b>", val_label)

        scroll.setWidget(scroll_content)
        detail_layout.addWidget(scroll)

    def display_data(self, data: Sequence[Any] | None) -> None:
        """
        Visualizza i dati passati.
        Args:
          data: Tuple o list contenente i dati grezzi della riga.
        """
        if not data:
            self.clear_fields()
            return

        # Indices source mapping (based on original file)
        mapping = {
            "Data": 0,
            "Ingresso": 1,
            "Uscita": 2,
            "Nome": 3,
            "Cognome": 4,
            "Codice Fiscale": 7,
            "ID Dipendente": 8,
            "Fornitore": 9,
            "Numero Badge": 11,
            "Reparto": 16,
            "Cantiere": 17,
            "Presenza TS": 5,
            "Sito": 6,
            "Codice RILPRES": 10,
            "Codice Qualifica": 12,
            "Specializzazione": 13,
            "Società Ospitante": 14,
            "Data Inserimento": 15,
        }

        for h in self.full_headers:
            idx = mapping.get(h)
            val = str(data[idx]) if idx is not None and idx < len(data) and data[idx] is not None else ""

            if val.lower() in ("nan", "none"):
                val = ""

            # Formattazione
            if h == "Data" and val:
                val = self._format_date(val)

            if h == "Data Inserimento" and val:
                val = self._format_date(val, strict=False)

            self.detail_labels[h].setText(val)

    def _format_date(self, val_str: str, strict: bool = True) -> str:
        """Helper per formattazione date."""
        _ = strict
        with suppress(Exception):
            # Try ISO format first
            dt = datetime.strptime(val_str, "%Y-%m-%d").replace(tzinfo=UTC)
            return dt.strftime("%d/%m/%Y")

        with suppress(Exception):
            # Try handling datetime string or other formats
            date_part = val_str.split(" ")[0]
            # If strict, we expect only date part to be valid iso or similar?
            # Original code tried flexible parsing
            for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                with suppress(ValueError):
                    dt = datetime.strptime(date_part, fmt).replace(tzinfo=UTC)
                    return dt.strftime("%d/%m/%Y")
        return val_str

    def clear_fields(self) -> None:
        """Pulisce tutti i campi."""
        for label in self.detail_labels.values():
            label.setText("-")
