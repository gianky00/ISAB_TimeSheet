"""
SyncroJob - GUI Widgets Registry
"""

from .activity_timeline import ActivityTimelineWidget
from .bot_parameters import BotParametersWidget
from .core_widgets import (
    FilterComboBox,
    IconButton,
    PrimaryButton,
    SearchInput,
    StandardCheckBox,
)
from .data_table import EditableDataTable
from .editable_data_table import EditableDataTable as LegacyEditableDataTable
from .excel_table import ExcelTableWidget
from .loading_overlay import LoadingOverlay
from .modern_button import ModernButton
from .modern_card import ModernCard, ModernContentCard
from .status_card import StatusCard
from .timeline_widget import TimelineWidget
from .toast import ToastManager, toast_error, toast_info, toast_success, toast_warning

__all__ = [
    "ActivityTimelineWidget",
    "BotParametersWidget",
    "EditableDataTable",
    "ExcelTableWidget",
    "FilterComboBox",
    "IconButton",
    "LoadingOverlay",
    "ModernButton",
    "ModernCard",
    "ModernContentCard",
    "PrimaryButton",
    "SearchInput",
    "StandardCheckBox",
    "StatusCard",
    "TimelineWidget",
    "ToastManager",
    "toast_error",
    "toast_info",
    "toast_success",
    "toast_warning",
]
