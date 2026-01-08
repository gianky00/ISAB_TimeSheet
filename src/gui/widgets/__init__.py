"""
SyncroJob - GUI Widgets
Widget personalizzati riutilizzabili.
Esporta le nuove classi e mantiene quelle legacy se necessario.
"""

# Re-export new widgets
# Import and re-export old widgets for compatibility during migration
# (Assuming old_widgets.py contains the original implementation of other widgets like CalendarDateEdit, etc.)
from src.gui.old_widgets import (
    CalendarDateEdit,
    DetailedInfoDialog,
    EditableDataTable,
    ExcelTableWidget,
    HorizontalLogItem,
    HorizontalTimelineContainer,
    HorizontalTimelineWidget,
    InfoLabel,
    KPIBigCard,
    LogWidget,
    MissionReportCard,
    StatusIndicator,
)

from .bot_parameters import BotParametersWidget
from .data_table import DataTable
from .modern_button import ModernButton
from .notification_item import NotificationItem
from .status_card import StatusCard
from .toast import Toast, ToastManager

__all__ = [
    "BotParametersWidget",
    "CalendarDateEdit",
    "DetailedInfoDialog",
    "EditableDataTable",
    "ExcelTableWidget",
    "HorizontalLogItem",
    "HorizontalTimelineContainer",
    "HorizontalTimelineWidget",
    "InfoLabel",
    "KPIBigCard",
    "LogWidget",
    "MissionReportCard",
    "StatusIndicator",
    "DataTable",
    "ModernButton",
    "NotificationItem",
    "StatusCard",
    "Toast",
    "ToastManager",
]
