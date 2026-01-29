"""
SyncroJob - Calendar Widgets
QDateEdit personalizzato con popup calendario.
"""

from PyQt6.QtWidgets import QCalendarWidget, QDateEdit

from src.core.constants import Icons
from src.utils.helpers import get_asset_path


class CalendarDateEdit(QDateEdit):
    """QDateEdit con popup calendario e stile personalizzato."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd.MM.yyyy")
        self.setMinimumWidth(220)  # Aumentato per evitare troncamento data

        # Configura il widget calendario interno per evitare i "..."
        calendar = self.calendarWidget()
        calendar.setMinimumWidth(450)  # Ancora più largo
        calendar.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.ShortDayNames)
        calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

        calendar.setStyleSheet(
            """
            QCalendarWidget QWidget {
                alternate-background-color: #f8f9fa;
                color: black;
            }
            QCalendarWidget QTableView {
                selection-background-color: #0d6efd;
                selection-color: white;
                font-size: 14px;
                outline: 0;
            }
            /* Intestazione giorni (L, M, M...) */
            QCalendarWidget QHeaderView {
                background-color: #f8f9fa;
            }
            QCalendarWidget QHeaderView::section {
                background-color: #f8f9fa;
                color: #555;
                padding: 5px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }
            QCalendarWidget QToolButton {
                color: black;
                icon-size: 28px;
                background-color: transparent;
                margin: 5px;
                font-weight: bold;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #e9ecef;
                border-radius: 4px;
            }
            QCalendarWidget QSpinBox {
                width: 50px;
                font-size: 14px;
                color: black;
                background-color: white;
                selection-background-color: #0d6efd;
                selection-color: white;
            }
            """
        )

        icon_path = get_asset_path(Icons.CALENDAR).replace("\\", "/")

        self.setStyleSheet(
            f"""
            QDateEdit {{
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px 45px 5px 10px;
                font-size: 14px;
                background-color: white;
                color: black;
            }}
            QDateEdit:focus {{
                border-color: #0d6efd;
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 40px;
                border-left-width: 1px;
                border-left-color: #ced4da;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background-color: #f8f9fa;
            }}
            QDateEdit::down-arrow {{
                image: url({icon_path});
                width: 18px;
                height: 18px;
            }}
            QDateEdit::drop-down:hover {{
                background-color: #e9ecef;
            }}
        """
        )
