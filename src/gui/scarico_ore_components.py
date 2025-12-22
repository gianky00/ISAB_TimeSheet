from PyQt6.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel, pyqtSignal, QModelIndex
from PyQt6.QtGui import QColor, QBrush, QAction
from PyQt6.QtWidgets import (
    QHeaderView, QMenu, QWidgetAction, QCheckBox,
    QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QScrollArea
)
import json
from datetime import datetime

class ScaricoOreTableModel(QAbstractTableModel):
    """
    Modello virtuale per Scarico Ore Cantiere (130k+ righe).
    Gestisce dati e stili (colori) in sola lettura.
    """

    COLUMNS = [
        'DATA', 'PERS1', 'PERS2', 'ODC', 'POS', 'DALLE', 'ALLE',
        'TOTALE ORE', 'DESCRIZIONE', 'FINITO', 'COMMESSA'
    ]

    def __init__(self, data=None):
        super().__init__()
        self._data = data if data else []
        self._styles_cache = {} # Cache json parsing if needed, though raw parsing is fast enough usually

    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self._styles_cache = {}
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.COLUMNS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        # _data row structure: 0..10 are data cols, 11 is 'styles' (JSON)
        row_data = self._data[row]

        if role == Qt.ItemDataRole.DisplayRole:
            val = row_data[col]
            if val is None: return ""

            # Format Data DD/MM/YYYY for display if it's column 0
            if col == 0 and val:
                # Assuming val is YYYY-MM-DD or similar
                if '-' in str(val):
                    try:
                        # Simple string slice for speed YYYY-MM-DD
                        parts = str(val).split(' ')[0].split('-')
                        if len(parts) == 3:
                            return f"{parts[2]}/{parts[1]}/{parts[0]}"
                    except: pass

            return str(val)

        elif role == Qt.ItemDataRole.BackgroundRole:
            return self._get_style(row, col, 'bg')

        elif role == Qt.ItemDataRole.ForegroundRole:
            return self._get_style(row, col, 'fg')

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            # Numerics aligned right
            # ODC(3), POS(4), DALLE(5), ALLE(6), TOTALE(7)
            if col in [3, 4, 5, 6, 7]:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            if col == 0:
                return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.COLUMNS[section]
        return None

    def _get_style(self, row, col, style_type):
        """Helper to extract style safely."""
        # Style JSON is at index 11
        style_json = self._data[row][11]
        if not style_json:
            return None

        # Optimization: Parse once? Python's json.loads is fast enough for viewport
        # But for heavy scrolling, caching the parsed dict for the row could help.
        # Given 130k rows, we can't cache all. We rely on LRU or just parse.
        # Let's try parsing.
        try:
            styles = json.loads(style_json)
            # Keys in JSON match internal names: 'data', 'pers1', ...
            # We need to map col index to key
            keys = [
                'data', 'pers1', 'pers2', 'odc', 'pos', 'dalle', 'alle',
                'totale_ore', 'descrizione', 'finito', 'commessa'
            ]
            key = keys[col]

            if key in styles:
                color_hex = styles[key].get(style_type)
                if color_hex:
                    return QColor(color_hex)
        except:
            pass
        return None

class ScaricoOreFilterProxy(QSortFilterProxyModel):
    """
    Proxy per filtraggio avanzato:
    1. Ricerca globale (AND logic, Date parsing)
    2. Filtri per colonna (Excel style)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_text = ""
        self.column_filters = {} # {col_index: {set of allowed values}}

    def set_filter_text(self, text):
        self.filter_text = text.lower().strip()
        self.invalidateFilter()

    def set_column_filter(self, col, values):
        """
        Imposta il filtro per una colonna.
        values: set di valori ammessi. Se None o vuoto, filtro rimosso.
        """
        if not values:
            if col in self.column_filters:
                del self.column_filters[col]
        else:
            self.column_filters[col] = set(str(v).lower() for v in values)
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()

        # 1. Global Text Filter
        if self.filter_text:
            # Search logic: All terms must match at least one column
            # Wait, "scavullo 4041": Row must contain "scavullo" AND "4041" (in any column)
            terms = self.filter_text.split()

            # Retrieve all text from row for searching
            # Optimization: don't call data() for every column if not needed.
            # But we need to search everywhere.
            row_text = " ".join([str(model.data(model.index(source_row, c, source_parent))).lower() for c in range(model.columnCount())])

            # Special Date Handling: If term is DD/MM/YYYY, convert to YYYY-MM-DD
            # Or simpler: The view displays DD/MM/YYYY. The `data()` returns DD/MM/YYYY for DisplayRole.
            # The `row_text` above uses DisplayRole data.
            # So searching "11/11/2025" works naturally because `data()` converts it!
            # EXCEPT: If `data()` returns raw value, we need to handle it.
            # My `ScaricoOreTableModel.data` DOES convert to DD/MM/YYYY.
            # So "11/11/2025" in search bar will match "11/11/2025" in row text.
            # Perfect.

            for term in terms:
                if term not in row_text:
                    return False

        # 2. Column Filters
        if self.column_filters:
            for col, allowed in self.column_filters.items():
                val = model.data(model.index(source_row, col, source_parent))
                if str(val).lower() not in allowed:
                    return False

        return True


class FilterHeaderView(QHeaderView):
    """
    Header con menu a discesa per filtro valori univoci.
    """
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setHighlightSections(True)
        # Icona filtro (unicode o icona)
        # Disegnare icona filtro se colonna filtrata è complesso in Qt puro senza risorse.
        # Userò un asterisco * nel testo header o colore diverso?
        # Per ora semplice click = menu.

    def mouseReleaseEvent(self, event):
        # Handle Right Click or specific area click?
        # User asked for "apply any filter", standard is clicking an icon in header.
        # Here we override click on header section.
        idx = self.logicalIndexAt(event.pos())
        if idx >= 0:
            self._show_filter_menu(idx, event.globalPosition().toPoint())

        super().mouseReleaseEvent(event)

    def _show_filter_menu(self, col_index, global_pos):
        model = self.model() # This is the Proxy
        source_model = model.sourceModel() # The Data Model

        # Get unique values for this column from SOURCE data (all data)
        # Iterate all rows of source model
        unique_values = set()
        for r in range(source_model.rowCount()):
            val = source_model.data(source_model.index(r, col_index), Qt.ItemDataRole.DisplayRole)
            unique_values.add(val)

        sorted_values = sorted(list(unique_values), key=lambda x: str(x).lower())

        # Check currently applied filter
        current_filter = model.column_filters.get(col_index, None)

        # Build Menu
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { menu-scrollable: 1; }") # Force scrollable if huge?
        # Actually QMenu isn't scrollable by default easily.
        # If we have 1000 unique names, QMenu explodes.
        # Need a custom widget with ListWidget inside Menu.

        filter_widget = FilterPopupWidget(sorted_values, current_filter)
        action = QWidgetAction(menu)
        action.setDefaultWidget(filter_widget)
        menu.addAction(action)

        # Execute
        menu.exec(global_pos)

        # Apply Logic
        if filter_widget.applied:
            selected = filter_widget.get_selected_values()
            # If all selected, clear filter
            if len(selected) == len(sorted_values):
                model.set_column_filter(col_index, None)
            else:
                model.set_column_filter(col_index, selected)


class FilterPopupWidget(QWidget):
    """Widget contenuto nel menu filtro (ScrollArea + Checkboxes)."""
    def __init__(self, values, selected_values=None):
        super().__init__()
        self.values = values
        self.applied = False
        self._checkboxes = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Search inside filter? Optional but good for usability.
        # Skipping for now to keep it simple as per request scope "apply filters".

        # Buttons
        btn_layout = QHBoxLayout()
        btn_all = QPushButton("Tutti")
        btn_none = QPushButton("Nessuno")
        btn_ok = QPushButton("OK")

        # Stile bottoni piccoli
        for btn in [btn_all, btn_none, btn_ok]:
            btn.setStyleSheet("font-size: 11px; padding: 2px;")

        btn_all.clicked.connect(self.select_all)
        btn_none.clicked.connect(self.select_none)
        btn_ok.clicked.connect(self.apply_filter)

        btn_layout.addWidget(btn_all)
        btn_layout.addWidget(btn_none)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

        # Scroll Area for values
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(200) # Max height
        scroll.setMinimumWidth(200)

        content = QWidget()
        self.vbox = QVBoxLayout(content)
        self.vbox.setSpacing(2)
        self.vbox.setContentsMargins(2, 2, 2, 2)

        is_all_selected = (selected_values is None)

        for val in values:
            cb = QCheckBox(str(val))
            if is_all_selected or (selected_values and str(val).lower() in selected_values):
                cb.setChecked(True)
            self._checkboxes.append((cb, str(val)))
            self.vbox.addWidget(cb)

        self.vbox.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def select_all(self):
        for cb, _ in self._checkboxes:
            cb.setChecked(True)

    def select_none(self):
        for cb, _ in self._checkboxes:
            cb.setChecked(False)

    def apply_filter(self):
        self.applied = True
        # Close parent menu
        # Trick: find parent menu
        parent = self.parent()
        while parent:
            if isinstance(parent, QMenu):
                parent.close()
                break
            parent = parent.parent()

    def get_selected_values(self):
        return [val for cb, val in self._checkboxes if cb.isChecked()]
