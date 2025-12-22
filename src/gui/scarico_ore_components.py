from PyQt6.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel, pyqtSignal, QModelIndex, QSortFilterProxyModel
from PyQt6.QtGui import QColor, QBrush, QAction, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (
    QHeaderView, QMenu, QWidgetAction, QCheckBox,
    QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QScrollArea, QListView, QLineEdit, QTreeView
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

    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
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
        style_json = self._data[row][11]
        if not style_json:
            return None
        try:
            styles = json.loads(style_json)
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
            terms = self.filter_text.split()
            row_text = " ".join([str(model.data(model.index(source_row, c, source_parent))).lower() for c in range(model.columnCount())])

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
    """Header con menu a discesa ottimizzato."""
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
        model = self.model() # Proxy
        source_model = model.sourceModel() # Data Model

        # Collect unique values
        unique_values = set()
        for r in range(source_model.rowCount()):
            val = source_model.data(source_model.index(r, col_index), Qt.ItemDataRole.DisplayRole)
            unique_values.add(val)

        # Check applied filter
        current_filter = model.column_filters.get(col_index, None)

        menu = QMenu(self)

        # Determine widget type based on column
        # Col 0 is 'DATA'
        if col_index == 0:
            filter_widget = DateFilterPopupWidget(unique_values, current_filter)
        else:
            sorted_values = sorted(list(unique_values), key=lambda x: str(x).lower())
            filter_widget = ListFilterPopupWidget(sorted_values, current_filter)

        action = QWidgetAction(menu)
        action.setDefaultWidget(filter_widget)
        menu.addAction(action)

        menu.exec(global_pos)

        if filter_widget.applied:
            selected = filter_widget.get_selected_values()
            # If everything selected (or effectively all), clear filter
            # Optimization: pass None if selection count == total count
            # But specific widget logic handles what "selected" means
            model.set_column_filter(col_index, selected)


class ListFilterPopupWidget(QWidget):
    """Widget filtro con QListView e Search Bar per alte performance."""
    def __init__(self, values, selected_values=None):
        super().__init__()
        self.values = values
        self.all_values = set(str(v).lower() for v in values)
        self.applied = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Search Bar
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Cerca...")
        self.search_edit.textChanged.connect(self._filter_list)
        layout.addWidget(self.search_edit)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_all = QPushButton("Tutti")
        btn_none = QPushButton("Nessuno")
        btn_ok = QPushButton("OK")
        for btn in [btn_all, btn_none, btn_ok]:
            btn.setStyleSheet("font-size: 11px; padding: 2px;")

        btn_all.clicked.connect(self.select_all)
        btn_none.clicked.connect(self.select_none)
        btn_ok.clicked.connect(self.apply_filter)

        btn_layout.addWidget(btn_all)
        btn_layout.addWidget(btn_none)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

        # List View with Standard Item Model
        self.list_view = QListView()
        self.model = QStandardItemModel()
        self.model.itemChanged.connect(self._on_item_changed)

        # Populate efficiently
        is_all_selected = (selected_values is None)
        selected_set = set()
        if selected_values:
            selected_set = set(v.lower() for v in selected_values)

        for val in values:
            item = QStandardItem(str(val))
            item.setCheckable(True)
            if is_all_selected or (str(val).lower() in selected_set):
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.model.appendRow(item)

        self.list_view.setModel(self.model)
        self.list_view.setFixedHeight(250)
        self.list_view.setMinimumWidth(250)
        layout.addWidget(self.list_view)

        self.original_rows = [self.model.item(i) for i in range(self.model.rowCount())]

    def _filter_list(self, text):
        text = text.lower()
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if text in item.text().lower():
                self.list_view.setRowHidden(i, False)
            else:
                self.list_view.setRowHidden(i, True)

    def select_all(self):
        self.model.blockSignals(True)
        for i in range(self.model.rowCount()):
            if not self.list_view.isRowHidden(i):
                self.model.item(i).setCheckState(Qt.CheckState.Checked)
        self.model.blockSignals(False)

    def select_none(self):
        self.model.blockSignals(True)
        for i in range(self.model.rowCount()):
            if not self.list_view.isRowHidden(i):
                self.model.item(i).setCheckState(Qt.CheckState.Unchecked)
        self.model.blockSignals(False)

    def _on_item_changed(self, item):
        pass

    def apply_filter(self):
        self.applied = True
        self._close_menu()

    def get_selected_values(self):
        # Scan all items
        selected = []
        all_checked = True

        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected.append(item.text())
            else:
                all_checked = False

        if all_checked: return None
        return selected

    def _close_menu(self):
        parent = self.parent()
        while parent:
            if isinstance(parent, QMenu):
                parent.close()
                break
            parent = parent.parent()


class DateFilterPopupWidget(QWidget):
    """Widget filtro gerarchico per date (Anno -> Mese -> Giorno)."""
    def __init__(self, values, selected_values=None):
        super().__init__()
        self.values = values # list of "DD/MM/YYYY" strings
        self.applied = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_all = QPushButton("Tutti")
        btn_none = QPushButton("Nessuno")
        btn_ok = QPushButton("OK")
        for btn in [btn_all, btn_none, btn_ok]:
            btn.setStyleSheet("font-size: 11px; padding: 2px;")

        btn_all.clicked.connect(self.select_all)
        btn_none.clicked.connect(self.select_none)
        btn_ok.clicked.connect(self.apply_filter)

        btn_layout.addWidget(btn_all)
        btn_layout.addWidget(btn_none)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

        # Tree View
        self.tree = QTreeView()
        self.tree.setHeaderHidden(True)
        self.model = QStandardItemModel()
        self.tree.setModel(self.model)
        self.tree.setFixedHeight(300)
        self.tree.setMinimumWidth(250)

        # Connect logic for recursive check
        self.model.itemChanged.connect(self._on_item_changed)

        layout.addWidget(self.tree)

        # Process dates
        self._build_tree(values, selected_values)

    def _build_tree(self, values, selected_values):
        # Structure: {Year: {Month: [Day, Day]}}
        structure = {}
        self.raw_dates = set(values)

        for v in values:
            if not v: continue
            try:
                # v is DD/MM/YYYY
                parts = v.split('/')
                if len(parts) != 3: continue
                d, m, y = parts[0], parts[1], parts[2]

                if y not in structure: structure[y] = {}
                if m not in structure[y]: structure[y][m] = []
                structure[y][m].append(v) # Store full string in leaf
            except: continue

        is_all_selected = (selected_values is None)
        selected_set = set(selected_values) if selected_values else set()

        sorted_years = sorted(structure.keys(), reverse=True)

        for y in sorted_years:
            y_item = QStandardItem(y)
            y_item.setCheckable(True)
            y_item.setEditable(False)

            months = structure[y]
            y_checked_count = 0

            for m in sorted(months.keys()):
                m_name = self._get_month_name(m)
                m_item = QStandardItem(f"{m_name} ({m})")
                m_item.setCheckable(True)
                m_item.setEditable(False)

                days_list = months[m]
                m_checked_count = 0

                for date_str in sorted(days_list):
                    # Display just the day part? Or date_str?
                    # Let's display date_str but cleaner
                    day_part = date_str.split('/')[0]
                    d_item = QStandardItem(day_part)
                    d_item.setCheckable(True)
                    d_item.setEditable(False)
                    d_item.setData(date_str, Qt.ItemDataRole.UserRole) # Store value

                    if is_all_selected or (date_str in selected_set):
                        d_item.setCheckState(Qt.CheckState.Checked)
                        m_checked_count += 1
                    else:
                        d_item.setCheckState(Qt.CheckState.Unchecked)

                    m_item.appendRow(d_item)

                # Set Month State
                if m_checked_count == len(days_list):
                    m_item.setCheckState(Qt.CheckState.Checked)
                    y_checked_count += 1
                elif m_checked_count > 0:
                    m_item.setCheckState(Qt.CheckState.PartiallyChecked)
                else:
                    m_item.setCheckState(Qt.CheckState.Unchecked)

                y_item.appendRow(m_item)

            # Set Year State
            if y_checked_count == len(months):
                y_item.setCheckState(Qt.CheckState.Checked)
            elif y_checked_count > 0: # This logic is simple, ideally we check partial
                # If any child is partial or checked, we are partial
                y_item.setCheckState(Qt.CheckState.PartiallyChecked)
            else:
                # Check for deeper partials
                has_partial = False
                for r in range(y_item.rowCount()):
                    if y_item.child(r).checkState() != Qt.CheckState.Unchecked:
                        has_partial = True; break
                y_item.setCheckState(Qt.CheckState.PartiallyChecked if has_partial else Qt.CheckState.Unchecked)

            self.model.appendRow(y_item)

    def _get_month_name(self, m_str):
        names = {
            "01": "Gennaio", "02": "Febbraio", "03": "Marzo", "04": "Aprile",
            "05": "Maggio", "06": "Giugno", "07": "Luglio", "08": "Agosto",
            "09": "Settembre", "10": "Ottobre", "11": "Novembre", "12": "Dicembre"
        }
        return names.get(m_str, m_str)

    def _on_item_changed(self, item):
        # Propagate changes down and up
        # Prevent recursion loops
        self.model.blockSignals(True)

        state = item.checkState()

        # Down: Set all children to same state (if Checked or Unchecked)
        if state != Qt.CheckState.PartiallyChecked:
            self._set_children_state(item, state)

        # Up: Update parent state based on siblings
        self._update_parent_state(item)

        self.model.blockSignals(False)

    def _set_children_state(self, item, state):
        for i in range(item.rowCount()):
            child = item.child(i)
            child.setCheckState(state)
            self._set_children_state(child, state)

    def _update_parent_state(self, item):
        parent = item.parent()
        if not parent: return

        checked = 0
        partial = 0
        count = parent.rowCount()

        for i in range(count):
            s = parent.child(i).checkState()
            if s == Qt.CheckState.Checked: checked += 1
            elif s == Qt.CheckState.PartiallyChecked: partial += 1

        if checked == count:
            parent.setCheckState(Qt.CheckState.Checked)
        elif checked > 0 or partial > 0:
            parent.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            parent.setCheckState(Qt.CheckState.Unchecked)

        self._update_parent_state(parent)

    def select_all(self):
        self.model.blockSignals(True)
        root = self.model.invisibleRootItem()
        self._set_children_state(root, Qt.CheckState.Checked)
        self.model.blockSignals(False)

    def select_none(self):
        self.model.blockSignals(True)
        root = self.model.invisibleRootItem()
        self._set_children_state(root, Qt.CheckState.Unchecked)
        self.model.blockSignals(False)

    def apply_filter(self):
        self.applied = True
        self._close_menu()

    def get_selected_values(self):
        # Traverse tree to find selected leaves
        selected = []
        root = self.model.invisibleRootItem()

        all_checked = True

        # Helper to traverse
        stack = [root.child(i) for i in range(root.rowCount())]
        while stack:
            item = stack.pop()
            if item.rowCount() > 0:
                # Node
                if item.checkState() != Qt.CheckState.Checked:
                    all_checked = False
                stack.extend([item.child(i) for i in range(item.rowCount())])
            else:
                # Leaf (Day)
                if item.checkState() == Qt.CheckState.Checked:
                    val = item.data(Qt.ItemDataRole.UserRole)
                    selected.append(val)
                else:
                    all_checked = False

        if all_checked: return None
        return selected

    def _close_menu(self):
        parent = self.parent()
        while parent:
            if isinstance(parent, QMenu):
                parent.close()
                break
            parent = parent.parent()
