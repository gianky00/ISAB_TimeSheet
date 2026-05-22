"""Modulo Employee Detail View."""

import logging
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.gui.panels.dipendenti.shared import create_field_row, create_info_card
from src.gui.styles import COLORS

logger = logging.getLogger(__name__)


class EmployeeDetailView(QWidget):
    """Pannello laterale per la visualizzazione dei dettagli del dipendente.

    Inizializza la classe.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(360)
        self.setStyleSheet(f"QWidget {{ background-color: {COLORS['bg_light']}; }}")

        self.detail_labels: dict[str, QLabel] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Inizializza il layout principale dei dettagli."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        self._setup_header(layout)

        detail_content = QWidget()
        detail_content.setStyleSheet("background-color: transparent;")
        detail_layout = QVBoxLayout(detail_content)
        detail_layout.setContentsMargins(0, 0, 0, 0)
        detail_layout.setSpacing(8)

        self._setup_personal_data(detail_layout)
        self._setup_work_info(detail_layout)
        self._setup_access_isab(detail_layout)
        detail_layout.addStretch()

        layout.addWidget(detail_content)
        layout.addStretch()

    def _setup_header(self, layout: QVBoxLayout) -> None:
        """Configura l'intestazione della scheda."""
        header_card = QFrame()
        header_card.setFixedHeight(70)
        header_shadow = QGraphicsDropShadowEffect()
        header_shadow.setBlurRadius(20)
        header_shadow.setYOffset(3)
        header_shadow.setColor(QColor(0, 0, 0, 60))
        header_card.setGraphicsEffect(header_shadow)
        header_card.setStyleSheet(
            f"QFrame {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 "
            f"{COLORS['primary_blue']}, stop:1 {COLORS['primary_dark']}); border-radius: 12px; }}"
        )
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(18, 12, 18, 12)

        title_label = QLabel("   SCHEDA DIPENDENTE")
        title_label.setStyleSheet(
            f"font-size: 20px; font-weight: bold; color: {COLORS['bg_white']}; letter-spacing: 1px;"
        )
        subtitle_label = QLabel("Dettagli anagrafica e accessi")
        subtitle_label.setStyleSheet("font-size: 14px; color: rgba(255, 255, 255, 0.90); margin-top: 2px;")
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        layout.addWidget(header_card)

    def _setup_personal_data(self, layout: QVBoxLayout) -> None:
        """Configura la sezione dati personali."""
        personal_card, personal_layout = create_info_card("   Dati Personali")

        row1 = QHBoxLayout()
        row1.setSpacing(10)
        row1.addWidget(self._create_detail_field("ID Risorsa"))
        row1.addWidget(self._create_detail_field("Data Nascita"))
        personal_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(10)
        row2.addWidget(self._create_detail_field("Cognome"))
        row2.addWidget(self._create_detail_field("Nome"))
        personal_layout.addLayout(row2)

        personal_layout.addWidget(self._create_detail_field("Codice Fiscale"))
        layout.addWidget(personal_card)

    def _setup_work_info(self, layout: QVBoxLayout) -> None:
        """Configura la sezione informazioni lavorative."""
        work_card, work_layout = create_info_card("   Informazioni Lavorative")
        row3 = QHBoxLayout()
        row3.setSpacing(10)
        row3.addWidget(self._create_detail_field("Badge"))
        row3.addWidget(self._create_detail_field("Data Assunzione"))
        work_layout.addLayout(row3)
        work_layout.addWidget(self._create_detail_field("Importato il"))
        layout.addWidget(work_card)

    def _setup_access_isab(self, layout: QVBoxLayout) -> None:
        """Configura la sezione ultimo accesso ISAB."""
        access_card = QFrame()
        access_shadow = QGraphicsDropShadowEffect()
        access_shadow.setBlurRadius(15)
        access_shadow.setYOffset(3)
        access_shadow.setColor(QColor(0, 0, 0, 50))
        access_card.setGraphicsEffect(access_shadow)
        access_card.setStyleSheet(
            f"QFrame {{ background: {COLORS['bg_white']}; border-radius: 10px; "
            f"border-left: 4px solid {COLORS['primary_blue']}; }}"
        )
        access_layout = QVBoxLayout(access_card)
        access_layout.setContentsMargins(15, 12, 15, 12)
        access_layout.setSpacing(6)

        access_title = QLabel("   ULTIMO ACCESSO ISAB")
        access_title.setStyleSheet(
            f"font-size: 13px; font-weight: bold; color: {COLORS['primary_blue']}; letter-spacing: 0.5px;"
        )
        self.last_access_label = QLabel("-")
        self.last_access_label.setWordWrap(True)
        self.last_access_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.last_access_label.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {COLORS['text_dark']}; padding: 5px 0;"
        )
        access_layout.addWidget(access_title)
        access_layout.addWidget(self.last_access_label)

        layout.addWidget(access_card)

    def _create_detail_field(self, label: str) -> QWidget:
        container = create_field_row(label)
        value_lbl = container.findChild(QLabel, "value_label")
        if value_lbl is not None:
            self.detail_labels[label] = value_lbl
        return container

    def update_data(self, data_dict: dict[str, Any], access_info: tuple[str, int, str] | None = None) -> None:
        """Aggiorna i campi visualizzati.

        :param data_dict: Dizionario {NomeCampo: Valore}
        :param access_info: Tupla (testo, giorni, colore) per l'ultimo accesso.
        """
        for label, widget in self.detail_labels.items():
            val = data_dict.get(label, "")
            widget.setText(str(val))

        if access_info:
            text, _, color = access_info
            self.last_access_label.setText(text)
            self.last_access_label.setStyleSheet(
                f"color: {color}; font-weight: bold; font-size: 14px; padding: 5px 0;"
            )
        else:
            self.last_access_label.setText("-")
            self.last_access_label.setStyleSheet(
                f"color: {COLORS['text_dark']}; font-weight: bold; font-size: 14px; padding: 5px 0;"
            )

    def reset(self) -> None:
        """Resetta tutti i campi."""
        for widget in self.detail_labels.values():
            widget.setText("-")
        self.last_access_label.setText("-")
        self.last_access_label.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-weight: bold; font-size: 14px; padding: 5px 0;"
        )
