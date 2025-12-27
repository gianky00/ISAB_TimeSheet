"""
Bot TS - GUI Widgets
Widget personalizzati riutilizzabili.
Esporta le nuove classi e mantiene quelle legacy se necessario.
"""

# Re-export new widgets
from .data_table import DataTable
from .modern_button import ModernButton
from .status_card import StatusCard
from .toast import Toast, ToastManager

# Import and re-export old widgets for compatibility during migration
# (Assuming old_widgets.py contains the original implementation of other widgets like CalendarDateEdit, etc.)
from src.gui.old_widgets import (
    HorizontalLogItem, HorizontalTimelineContainer, HorizontalTimelineWidget,
    StatusIndicator, CalendarDateEdit, ExcelTableWidget, EditableDataTable,
    LogWidget, DetailedInfoDialog, InfoLabel, KPIBigCard, MissionReportCard
)

# If any widgets were replaced, ensure they are not imported twice or decide which one to use.
# `Toast` is in both? Yes, `toast.py` was overwritten in plan step 2 with new Toast.
# `old_widgets.py` has old `Toast`? No, `toast.py` was a separate file before?
# Wait, `src/gui/widgets.py` was moved to `src/gui/old_widgets.py`.
# `old_widgets.py` contains `LogWidget`, `EditableDataTable`, `ExcelTableWidget` etc.
# The new `src/gui/widgets/toast.py` is the new toast.

# So this __init__.py aggregates everything for cleaner imports.
