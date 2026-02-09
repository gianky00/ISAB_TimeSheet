from typing import Any

from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QHeaderView, QMenu, QWidgetAction

from src.gui.components.scarico_ore.filters.popup_date import DateFilterPopupWidget
from src.gui.components.scarico_ore.filters.popup_list import ListFilterPopupWidget


class FilterHeaderView(QHeaderView):
    """
    Header personalizzato con supporto per menu di filtraggio a discesa.
    Permette di cliccare sulle intestazioni per aprire popup di filtro specifici per colonna.
    """

    filterChanged = pyqtSignal(int, object)  # col, values

    def __init__(self, orientation: Qt.Orientation, parent: Any | None = None) -> None:
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setHighlightSections(True)

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        if event is not None:
            idx = self.logicalIndexAt(event.pos())
            if idx >= 0:
                self._show_filter_menu(idx, event.globalPosition().toPoint())
        super().mouseReleaseEvent(event)

    def _show_filter_menu(self, col_index: int, global_pos: QPoint) -> None:
        # Access the real model directly (ScaricoOreTableModel)
        model = self.model()
        if model is None:
            return

        # Use hasattr/getattr to access internal data if it's our custom model
        display_data = getattr(model, "_display_data", [])
        if not display_data:
            return

        # Collect unique values from ALL data (not just filtered)
        unique_values = {row[col_index] for row in display_data}

        menu = QMenu(self)

        # Determine widget type
        filter_widget: Any
        if col_index == 0:
            filter_widget = DateFilterPopupWidget(list(unique_values), None)
        else:
            sorted_values = sorted(unique_values, key=lambda x: str(x).lower())
            filter_widget = ListFilterPopupWidget(sorted_values, None)

        action = QWidgetAction(menu)
        action.setDefaultWidget(filter_widget)
        menu.addAction(action)

        menu.exec(global_pos)

        if (hasattr(filter_widget, "applied") and filter_widget.applied) or (
            isinstance(filter_widget, DateFilterPopupWidget) and filter_widget.applied
        ):
            selected = filter_widget.get_selected_values()
            self.filterChanged.emit(col_index, selected)
