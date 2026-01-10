"""
SyncroJob - Calendar Widgets
QDateEdit personalizzato con popup calendario.
"""

from PyQt6.QtWidgets import QDateEdit
from src.utils.helpers import get_asset_path


class CalendarDateEdit(QDateEdit):
    """QDateEdit con popup calendario e stile personalizzato."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd.MM.yyyy")
        self.setMinimumWidth(150)

        icon_path = get_asset_path("assets/icons/calendar.svg").replace("\\", "/")

        self.setStyleSheet(
            f"""
            QDateEdit {{
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px 10px;
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
                width: 34px;
                border-left-width: 1px;
                border-left-color: #ced4da;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background-color: #f8f9fa;
            }}
            QDateEdit::down-arrow {{
                image: url({icon_path});
                width: 20px;
                height: 20px;
            }}
            QDateEdit::drop-down:hover {{
                background-color: #e9ecef;
            }}
        """
        )
