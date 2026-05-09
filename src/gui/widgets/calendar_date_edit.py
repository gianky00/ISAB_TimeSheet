"""
SyncroJob - Calendar Widgets
QDateEdit personalizzato con popup calendario.
"""

from PySide6.QtWidgets import QCalendarWidget, QDateEdit, QWidget

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path


class CalendarDateEdit(QDateEdit):
    """QDateEdit con popup calendario e stile personalizzato."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd.MM.yyyy")
        self.setMinimumWidth(220)  # Aumentato per evitare troncamento data

        # Configura il widget calendario interno per evitare i "..."
        calendar = self.calendarWidget()
        if calendar:
            calendar.setMinimumWidth(450)  # Ancora più largo
            calendar.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.ShortDayNames)
            calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

            calendar.setStyleSheet(
                f"""
      QCalendarWidget QWidget {{
        alternate-background-color: {COLORS["bg_light"]};
        color: {COLORS["text_dark"]};
      }}
      QCalendarWidget QTableView {{
        selection-background-color: {COLORS["primary_dark"]};
        selection-color: white;
        font-size: 14px;
        outline: 0;
      }}
      /* Intestazione giorni (L, M, M...) */
      QCalendarWidget QHeaderView {{
        background-color: {COLORS["bg_light"]};
      }}
      QCalendarWidget QHeaderView::section {{
        background-color: {COLORS["bg_light"]};
        color: {COLORS["text_muted"]};
        padding: 5px;
        font-weight: bold;
        font-size: 13px;
        border: none;
      }}
      QCalendarWidget QToolButton {{
        color: {COLORS["text_dark"]};
        icon-size: 28px;
        background-color: transparent;
        margin: 5px;
        font-weight: bold;
      }}
      QCalendarWidget QToolButton:hover {{
        background-color: {COLORS["bg_hover"]};
        border-radius: 4px;
      }}
      QCalendarWidget QSpinBox {{
        width: 50px;
        font-size: 14px;
        color: {COLORS["text_dark"]};
        background-color: {COLORS["bg_white"]};
        selection-background-color: {COLORS["primary_dark"]};
        selection-color: white;
      }}
      """
            )

        icon_path = get_asset_path(Icons.CALENDAR).replace("\\", "/")

        self.setStyleSheet(
            f"""
      QDateEdit {{
        border: 1px solid {COLORS["border_medium"]};
        border-radius: 4px;
        padding: 5px 45px 5px 10px;
        font-size: 14px;
        background-color: {COLORS["bg_white"]};
        color: {COLORS["text_dark"]};
      }}
      QDateEdit:focus {{
        border-color: {COLORS["primary_dark"]};
      }}
      QDateEdit::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 40px;
        border-left-width: 1px;
        border-left-color: {COLORS["border_medium"]};
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
        background-color: {COLORS["bg_light"]};
      }}
      QDateEdit::down-arrow {{
        image: url({icon_path});
        width: 18px;
        height: 18px;
      }}
      QDateEdit::drop-down:hover {{
        background-color: {COLORS["bg_hover"]};
      }}
    """
        )
