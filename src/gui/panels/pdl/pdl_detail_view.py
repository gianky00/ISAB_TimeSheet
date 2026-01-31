from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class PDLDetailView(QWidget):
    """Widget per la visualizzazione del dettaglio completo di un PDL."""

    def __init__(self, headers, parent=None):
        super().__init__(parent)
        self.headers = headers
        self.detail_labels = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)

        detail_title = QLabel("Dettaglio Completo PDL")
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

        scroll.set(scroll_content)
        layout.addWidget(scroll)

    def set(self, scroll_content):
        # Fix per errore di battitura nel codice sopra se necessario,
        # ma meglio usare il metodo corretto di QScrollArea
        pass

    # Sovrascrivo setup_ui per correggere l'errore di battitura 'set' vs 'setWidget'
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)

        detail_title = QLabel("Dettaglio Completo PDL")
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

    def update_details(self, data):
        """Aggiorna le label con i dati forniti (lista ordinata come headers)."""
        for i, h in enumerate(self.headers):
            if i >= len(data):
                break
            val = str(data[i])
            if val.lower() == "nan" or val == "None":
                val = ""

            # Formattazione "Importato il"
            if h == "Importato il" and val:
                try:
                    dt = datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
                    val = dt.strftime("%d/%m/%Y %H:%M:%S")
                except Exception:
                    pass

            self.detail_labels[h].setText(val)

    def clear(self):
        """Resetta i campi del dettaglio."""
        for label in self.detail_labels.values():
            label.setText("-")
