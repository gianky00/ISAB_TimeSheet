"""Modulo Pdl Timeline."""

from __future__ import annotations

from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba


class PDLTimelineWidget(QWidget):
    """Widget elegante per visualizzare la cronologia delle attività di una PDL.

    Implementa un design moderno a timeline verticale con card informative.

    Inizializza la timeline con i dati degli eventi.

    Args:
      data: Lista di dizionari, ognuno rappresentante un evento (data, tecnico, descrizione, fonte).
      parent: Widget genitore.
    """

    def __init__(self, data: list[dict[str, Any]], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.data = sorted(data, key=lambda x: str(x.get("data", "")), reverse=True)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout principale a scorrimento."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)

        if not self.data:
            empty_lbl = QLabel("Nessuna attività registrata per questa PDL.")
            empty_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-style: italic;")
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(empty_lbl)
            return

        # Popola la timeline
        for i, item in enumerate(self.data):
            is_last = i == len(self.data) - 1
            card = self._create_event_card(item, is_last)
            main_layout.addWidget(card)

        main_layout.addStretch()

    def _create_event_card(self, data: dict[str, Any], is_last: bool) -> QWidget:
        """Crea una singola card per un evento nella timeline.

        Args:
          data: Dati dell'evento.
          is_last: Se è l'ultimo evento della lista.

        Returns:
          Il widget della card creato.
        """
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        main_spacing = 15
        layout.setSpacing(main_spacing)

        # 1. Colonna Data (Sinistra)
        layout.addWidget(self._create_date_widget(data))

        # 2. Linea Temporale (Centro)
        layout.addWidget(self._create_line_widget(data, is_last))

        # 3. Contenuto Card (Destra)
        layout.addWidget(self._create_content_card(data))

        return container

    def _create_date_widget(self, data: dict[str, Any]) -> QWidget:
        """Crea il widget con giorno e mese sulla sinistra."""
        date_str = str(data.get("data", ""))
        day_num = "??"
        month_str = ""
        with suppress(Exception):
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
                try:
                    date_obj = datetime.strptime(date_str, fmt).replace(tzinfo=UTC)
                    day_num = date_obj.strftime("%d")
                    month_str = date_obj.strftime("%b").upper()
                    break
                except ValueError:
                    continue

        date_widget = QWidget()
        date_widget_width = 50
        date_widget.setFixedWidth(date_widget_width)
        date_layout = QVBoxLayout(date_widget)
        date_layout.setContentsMargins(0, 0, 0, 0)
        date_layout.setSpacing(0)

        lbl_day = QLabel(day_num)
        lbl_day.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_day.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {COLORS['text_dark']};")

        lbl_month = QLabel(month_str)
        lbl_month.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_month.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; font-weight: bold;")

        date_layout.addWidget(lbl_day)
        date_layout.addWidget(lbl_month)
        date_layout.addStretch()
        return date_widget

    def _create_line_widget(self, data: dict[str, Any], is_last: bool) -> QWidget:
        """Crea l'indicatore grafico (pallino + linea) al centro."""
        line_widget = QWidget()
        line_widget_width = 30
        line_widget.setFixedWidth(line_widget_width)
        line_layout = QVBoxLayout(line_widget)
        line_layout.setContentsMargins(0, 0, 0, 0)
        line_layout.setSpacing(0)
        line_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        dot = QLabel("  ")
        dot.setAlignment(Qt.AlignmentFlag.AlignCenter)

        fonte_text = str(data.get("fonte", "Report"))
        dot_color = self._get_status_color(fonte_text)

        dot_font_size = 12
        dot_margin_bottom = -5
        dot.setStyleSheet(
            f"color: {dot_color}; font-size: {dot_font_size}px; margin-bottom: {dot_margin_bottom}px;"
        )
        line_layout.addWidget(dot)

        line = QFrame()
        line_width = 2
        line.setFixedWidth(line_width)
        line.setStyleSheet(f"background-color: {COLORS['border_light']}; border: none;")
        if is_last:
            line.setStyleSheet(
                f"background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {COLORS['border_light']}, stop:1 transparent);"
            )

        line_layout.addWidget(line)
        return line_widget

    def _get_status_color(self, fonte_text: str) -> str:
        """Restituisce il colore basato sulla fonte."""
        if "Validato" in fonte_text:
            return COLORS["success_dark"]
        if "In Attesa" in fonte_text:
            return COLORS["warning_orange"]
        if "Relazione" in fonte_text:
            return COLORS["purple"]
        return COLORS["text_muted"]

    def _create_content_card(self, data: dict[str, Any]) -> QFrame:
        """Crea la card informativa sulla destra."""
        card_frame = QFrame()
        card_frame.setStyleSheet(f"""
      QFrame {{
        background-color: {COLORS["bg_white"]};
        border: 1px solid {COLORS["border_light"]};
        border-radius: 8px;
      }}
      QFrame:hover {{
        border-color: {COLORS["primary_blue"]};
        background-color: {COLORS["bg_white"]};
        box-shadow: 0 4px 6px {hex_to_rgba(COLORS["text_dark"], 0.1)};
      }}
    """)

        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(15, 12, 15, 12)
        card_layout.setSpacing(8)

        # Header Card: Tecnico + Badge Fonte
        card_layout.addLayout(self._create_card_header(data))

        # Descrizione
        desc_text = str(data.get("descrizione", ""))
        desc = QLabel(desc_text)
        desc.setWordWrap(True)
        desc.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-size: 12px; border: none; background: transparent;"
        )
        card_layout.addWidget(desc)

        # Ore (se presenti)
        ore = str(data.get("ore_lavoro", "")).strip()
        if ore and ore != "0" and ore.lower() != "nan":
            lbl_ore = QLabel(f"    {ore} ore")
            lbl_ore.setStyleSheet(
                f"color: {COLORS['text_muted']}; font-size: 11px; margin-top: 5px; border: none; background: transparent;"
            )
            card_layout.addWidget(lbl_ore)

        return card_frame

    def _create_card_header(self, data: dict[str, Any]) -> QHBoxLayout:
        """Crea l'header della card con tecnico e badge."""
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        tecnico_text = str(data.get("tecnico", "Tecnico Sconosciuto"))
        tecnico = QLabel(tecnico_text)
        tecnico.setStyleSheet(
            f"font-weight: bold; font-size: 13px; color: {COLORS['text_dark']}; border: none; background: transparent;"
        )
        header_layout.addWidget(tecnico)
        header_layout.addStretch()

        fonte_text = str(data.get("fonte", "Report"))
        badge_bg, badge_fg = self._get_badge_colors(fonte_text)

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
        return header_layout

    def _get_badge_colors(self, fonte_text: str) -> tuple[str, str]:
        """Restituisce i colori (sfondo, testo) per il badge della fonte."""
        if "Relazione" in fonte_text:
            return COLORS["purple"], "white"
        if "Validato" in fonte_text:
            return COLORS["success_dark"], "white"
        if "In Attesa" in fonte_text:
            return COLORS["warning_yellow"], COLORS["text_dark"]
        return COLORS["primary_dark"], "white"
