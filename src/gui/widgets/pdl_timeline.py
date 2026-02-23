from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class PDLTimelineWidget(QWidget):
    """
    Widget che visualizza la cronologia degli interventi in stile Timeline verticale.
    Progettato per essere inserito in una riga espansa della tabella Programmazione.
    """

    def __init__(self, interventions: list[dict[str, Any]], parent=None):
        super().__init__(parent)
        self.interventions = interventions
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(15)
        # Background leggero per distinguere l'area espansa
        self.setStyleSheet("background-color: #f8f9fa;")

        # Titolo
        title = QLabel(f"Cronologia Interventi Recenti ({len(self.interventions)})")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #1e3a5f;")
        main_layout.addWidget(title)

        if not self.interventions:
            no_data = QLabel("Nessun intervento registrato.")
            no_data.setStyleSheet("color: #6c757d; font-style: italic; margin-left: 20px;")
            main_layout.addWidget(no_data)
            return

        # Timeline Container
        timeline_container = QWidget()
        timeline_container.setStyleSheet("background-color: transparent;")
        timeline_layout = QVBoxLayout(timeline_container)
        timeline_layout.setContentsMargins(0, 0, 0, 0)
        timeline_layout.setSpacing(0)

        for i, intervention in enumerate(self.interventions):
            # Card dell'evento
            card = self._create_event_card(intervention, is_last=(i == len(self.interventions) - 1))
            timeline_layout.addWidget(card)

        main_layout.addWidget(timeline_container)
        main_layout.addStretch()

    def _create_event_card(self, data: dict[str, Any], is_last: bool) -> QWidget:
        """Crea una singola card per un evento nella timeline."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # 1. Colonna Data (Sinistra)
        date_str = str(data.get("data", ""))
        day_num = "??"
        month_str = ""
        with suppress(Exception):
            # Tenta parsing di formati comuni
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
                try:
                    date_obj = datetime.strptime(date_str, fmt).replace(tzinfo=UTC)
                    day_num = date_obj.strftime("%d")
                    month_str = date_obj.strftime("%b").upper()
                    break
                except ValueError:
                    continue

        date_widget = QWidget()
        date_widget.setFixedWidth(50)
        date_layout = QVBoxLayout(date_widget)
        date_layout.setContentsMargins(0, 0, 0, 0)
        date_layout.setSpacing(0)

        lbl_day = QLabel(day_num)
        lbl_day.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_day.setStyleSheet("font-size: 18px; font-weight: bold; color: #212529;")

        lbl_month = QLabel(month_str)
        lbl_month.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_month.setStyleSheet("font-size: 11px; color: #6c757d; font-weight: bold;")

        date_layout.addWidget(lbl_day)
        date_layout.addWidget(lbl_month)
        date_layout.addStretch()  # Spinge in alto
        layout.addWidget(date_widget)

        # 2. Linea Temporale (Centro)
        line_widget = QWidget()
        line_widget.setFixedWidth(30)
        line_painter = QVBoxLayout(line_widget)
        line_painter.setContentsMargins(0, 0, 0, 0)
        line_painter.setSpacing(0)
        line_painter.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Pallino
        dot = QLabel("●")
        dot.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Colore pallino in base allo stato/fonte
        color = "#6c757d"  # Default Grigio
        fonte_text = str(data.get("fonte", "Report"))

        if "Validato" in fonte_text:
            color = "#198754"  # Verde
        elif "In Attesa" in fonte_text:
            color = "#ffc107"  # Giallo/Arancio
        elif "Relazione" in fonte_text:
            color = "#6f42c1"  # Viola

        dot.setStyleSheet(f"color: {color}; font-size: 12px; margin-bottom: -5px;")
        line_painter.addWidget(dot)

        # Linea verticale (sempre presente per connettere visivamente, tranne ultimo se vogliamo staccare)
        line = QFrame()
        line.setFixedWidth(2)
        line.setStyleSheet("background-color: #dee2e6; border: none;")
        if is_last:
            line.setStyleSheet(
                "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #dee2e6, stop:1 transparent);"
            )

        line_painter.addWidget(line)
        layout.addWidget(line_widget)

        # 3. Contenuto Card (Destra)
        card_frame = QFrame()
        card_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }
            QFrame:hover {
                border-color: #b6d4fe;
                background-color: #ffffff;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
        """)
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(15, 12, 15, 12)
        card_layout.setSpacing(8)

        # Header Card: Tecnico + Badge Fonte
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        tecnico_text = str(data.get("tecnico", "Tecnico Sconosciuto"))
        tecnico = QLabel(tecnico_text)
        tecnico.setStyleSheet(
            "font-weight: bold; font-size: 13px; color: #212529; border: none; background: transparent;"
        )
        header_layout.addWidget(tecnico)

        header_layout.addStretch()

        badge_bg = "#0d6efd"  # Blu default
        badge_fg = "white"
        if "Relazione" in fonte_text:
            badge_bg = "#6f42c1"  # Viola
        elif "Validato" in fonte_text:
            badge_bg = "#198754"  # Verde
        elif "In Attesa" in fonte_text:
            badge_bg = "#ffc107"
            badge_fg = "#212529"

        lbl_fonte = QLabel(f" {fonte_text} ")
        lbl_fonte.setStyleSheet(f"""
            background-color: {badge_bg};
            color: {badge_fg};
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 10px;
            font-weight: bold;
            border: none;
        """)
        header_layout.addWidget(lbl_fonte)

        card_layout.addLayout(header_layout)

        # Descrizione
        desc_text = str(data.get("descrizione", ""))
        desc = QLabel(desc_text)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #495057; font-size: 12px; border: none; background: transparent;")
        card_layout.addWidget(desc)

        # Ore (se presenti)
        ore = str(data.get("ore_lavoro", "")).strip()
        if ore and ore != "0" and ore.lower() != "nan":
            lbl_ore = QLabel(f"⏱️ {ore} ore")
            lbl_ore.setStyleSheet(
                "color: #6c757d; font-size: 11px; margin-top: 5px; border: none; background: transparent;"
            )
            card_layout.addWidget(lbl_ore)

        layout.addWidget(card_frame)

        return container
