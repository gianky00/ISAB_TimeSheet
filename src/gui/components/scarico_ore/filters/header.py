from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHeaderView, QMenu, QWidgetAction

from src.gui.components.scarico_ore.filters.popup_date import DateFilterPopupWidget
from src.gui.components.scarico_ore.filters.popup_list import ListFilterPopupWidget


class FilterHeaderView(QHeaderView):
    """
    Header personalizzato con supporto per menu di filtraggio a discesa.
    Permette di cliccare sulle intestazioni per aprire popup di filtro specifici per colonna.
    """

    filterChanged = pyqtSignal(int, object)  # col, values

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setHighlightSections(True)

    def mouseReleaseEvent(self, event):
        idx = self.logicalIndexAt(event.pos())
        if idx >= 0:
            self._show_filter_menu(idx, event.globalPosition().toPoint())
        super().mouseReleaseEvent(event)

    def _show_filter_menu(self, col_index, global_pos):
        # Access the real model directly (ScaricoOreTableModel)
        model = self.model()

        # Collect unique values from ALL data (not just filtered)
        unique_values = {row[col_index] for row in model._display_data}

        menu = QMenu(self)

        # Determine widget type
        if col_index == 0:
            filter_widget = DateFilterPopupWidget(unique_values, None)
        else:
            sorted_values = sorted(unique_values, key=lambda x: str(x).lower())
            filter_widget = ListFilterPopupWidget(sorted_values, None)

        action = QWidgetAction(menu)
        action.setDefaultWidget(filter_widget)
        menu.addAction(action)

        menu.exec(global_pos)

        if filter_widget.applied:
            selected = filter_widget.get_selected_values()
            self.filterChanged.emit(col_index, selected)
