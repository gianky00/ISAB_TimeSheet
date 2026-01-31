from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.gui.formatters import format_currency_smart, format_date_it


class OdaDetailView(QWidget):
    """Widget per la visualizzazione del dettaglio completo di un OdA."""

    def __init__(self, headers, parent=None):
        super().__init__(parent)
        self.headers = headers
        self.detail_labels = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)

        detail_title = QLabel("Dettaglio Completo OdA")
        detail_title.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: #2196F3; margin-bottom: 5px;"
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
            val_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            self.detail_labels[h] = val_label
            self.form_layout.addRow(f"<b>{h}:</b>", val_label)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def update_details(self, data: list):
        """Aggiorna le label con i dati della riga selezionata."""
        for i, h in enumerate(self.headers):
            if i >= len(data):
                break
            val = str(data[i])
            if val.lower() == "nan" or val == "None":
                val = ""

            # Formattazione speciale
            if "valore" in h.lower() or "prezzo" in h.lower():
                try:
                    val = format_currency_smart(float(val))
                except Exception:
                    pass
            elif "data" in h.lower() and val:
                val = format_date_it(val)

            self.detail_labels[h].setText(val)

    def clear(self):
        """Resetta i campi del dettaglio."""
        for label in self.detail_labels.values():
            label.setText("-")
