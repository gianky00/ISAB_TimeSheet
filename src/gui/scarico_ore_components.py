from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSignal, QModelIndex, QThread
from PyQt6.QtGui import QColor, QBrush, QAction, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (
    QHeaderView, QMenu, QWidgetAction, QCheckBox,
    QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QScrollArea, QListView, QLineEdit, QTreeView
)
import json
import pickle
from pathlib import Path
from datetime import datetime
from src.utils.parsing import parse_currency

class CacheWorker(QThread):
    """
    ⚡ BOLT OPTIMIZATION: Background worker for heavy cache operations.
    Handles file I/O (pickle) and data processing.
    Now builds a PRE-FORMATTED display cache for max speed.
    """
    finished = pyqtSignal(object, object, object, object) # display_data, search_index, float_totals, style_cache
    progress = pyqtSignal(str)

    def __init__(self, cache_path, data_source=None):
        super().__init__()
        self.cache_path = cache_path
        self.data_source = data_source # If provided, we build cache from this data.

    def run(self):
        if self.data_source:
            # Build cache from raw data (e.g. from DB)
            self.progress.emit("Elaborazione dati...")
            display_data, search_index, float_totals, style_cache = self._build_caches(self.data_source)
            # Save to disk
            self.progress.emit("Salvataggio cache...")
            self._save_cache(display_data, search_index, float_totals, style_cache)
            self.finished.emit(display_data, search_index, float_totals, style_cache)
        else:
            # Load from file
            if not self.cache_path.exists():
                self.finished.emit([], [], [], [])
                return

            try:
                self.progress.emit("Caricamento cache...")
                with open(self.cache_path, 'rb') as f:
                    # Legacy support: check pickle structure
                    loaded = pickle.load(f)
                    if len(loaded) == 3:
                        # Old format: data, search, totals
                        # We must rebuild because 'data' is raw, we need 'display_data'
                        raw_data = loaded[0]
                        display_data, search_index, float_totals, style_cache = self._build_caches(raw_data)
                    elif len(loaded) == 4:
                        # Version 2 format: raw_data, search, totals, style
                        # Checking if we need to rebuild (if data is not pre-formatted strings)
                        d, s, t, st = loaded
                        if d and len(d) > 0 and (d[0][0] is None or not isinstance(d[0][0], str)):
                             # Likely raw data or None, rebuild
                             display_data, search_index, float_totals, style_cache = self._build_caches(d)
                        else:
                             # Already formatted
                             display_data, search_index, float_totals, style_cache = d, s, t, st
                    else:
                        display_data, search_index, float_totals, style_cache = [], [], [], []

                self.finished.emit(display_data, search_index, float_totals, style_cache)
            except Exception as e:
                print(f"Error loading cache: {e}")
                self.finished.emit([], [], [], [])

    def _build_style_cache_only(self, data):
        """Helper to build only style cache from data."""
        style_cache = []
        append_style = style_cache.append

        for row in data:
            if len(row) > 11:
                style_json = row[11]
                if style_json:
                    try:
                        append_style(json.loads(style_json))
                    except:
                        append_style(None)
                else:
                    append_style(None)
            else:
                append_style(None)
        return style_cache

    def _build_caches(self, data):
        """
        Pre-computa tutto: Stringhe visualizzate, Indice ricerca, Totali, Stili.
        Optimized for speed.
        """
        display_data = [] # List of list of strings
        search_index = []
        float_totals = []
        style_cache = []

        append_display = display_data.append
        append_search = search_index.append
        append_total = float_totals.append
        append_style = style_cache.append

        str_converter = str

        for row in data:
            # --- 1. Display Strings & Search Index ---
            # We want to format everything ONCE here.

            # Date (Col 0)
            val_0 = row[0]
            str_0 = ""
            if val_0:
                s_val = str_converter(val_0)
                if '-' in s_val:
                    try:
                        if len(s_val) >= 10 and s_val[4] == '-' and s_val[7] == '-':
                             str_0 = f"{s_val[8:10]}/{s_val[5:7]}/{s_val[0:4]}"
                        else:
                             parts = s_val.split(' ')[0].split('-')
                             if len(parts) == 3:
                                 str_0 = f"{parts[2]}/{parts[1]}/{parts[0]}"
                             else:
                                 str_0 = s_val
                    except:
                        str_0 = s_val
                else:
                    str_0 = s_val

            # Build Display Row (Cols 0-10)
            display_row = [str_0]
            search_parts = [str_0]

            for i in range(1, 11):
                val = row[i]
                if val is None:
                    d_val = ""
                else:
                    d_val = str_converter(val)

                display_row.append(d_val)
                if d_val:
                    search_parts.append(d_val)

            # Append full raw row just in case we need it? No, keep memory low.
            # But wait, if we rebuild cache next time, do we have raw data?
            # If we save PRE-FORMATTED data to disk, we lose raw data (e.g. floats are now strings).
            # This means we CANNOT rebuild totals/styles correctly if we rely on raw types later?
            # Float totals are stored separately. Styles are stored separately.
            # So display_data being strings is fine for display and search.
            # What if we need to export to Excel later with real types?
            # The export usually uses the DB or the Table Model.
            # If Table Model only has strings, export will have strings.
            # User might want numbers.
            # However, for PERFORMANCE of the VIEW, strings are key.
            # If export is needed, we can load from DB again or keep raw data in memory (doubles RAM).
            # For 130k rows, RAM is cheap (100MB).
            # Let's keep display_data as the main source for the View.
            # If needed, we can add raw_data later.

            append_display(display_row)

            # Search Index (lowercase joined)
            append_search(" ".join(search_parts).lower())

            # --- 2. Float Totals (Col 7) ---
            val_7 = row[7]
            try:
                if isinstance(val_7, (int, float)):
                    append_total(float(val_7))
                else:
                    append_total(parse_currency(val_7))
            except:
                append_total(0.0)

            # --- 3. Style Cache (Pre-parse JSON) ---
            if len(row) > 11:
                style_json = row[11]
                if style_json:
                    try:
                        append_style(json.loads(style_json))
                    except:
                        append_style(None)
                else:
                    append_style(None)
            else:
                append_style(None)

        return display_data, search_index, float_totals, style_cache

    def _save_cache(self, data, search, totals, style_cache):
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, 'wb') as f:
                pickle.dump((data, search, totals, style_cache), f)
        except Exception as e:
            print(f"Error saving cache: {e}")

class ScaricoOreTableModel(QAbstractTableModel):
    """
    Modello virtuale ULTRA-RAPIDO per Scarico Ore (130k+ righe).
    Integra la logica di filtraggio per evitare l'overhead di QSortFilterProxyModel.
    Usa dati pre-formattati per rendering O(1).
    """

    COLUMNS = [
        'DATA', 'PERS1', 'PERS2', 'ODC', 'POS', 'DALLE', 'ALLE',
        'TOTALE ORE', 'DESCRIZIONE', 'FINITO', 'COMMESSA'
    ]

    CACHE_PATH = Path("data/scarico_ore_cache.pkl")

    # ⚡ SINGLETON CACHE
    _global_cache = {
        'display_data': [], # List[List[str]]
        'search_index': [], # List[str]
        'totals': [],       # List[float]
        'styles': [],       # List[dict]
        'loaded': False
    }

    cache_loaded = pyqtSignal()
    loading_progress = pyqtSignal(str)

    def __init__(self, data=None):
        super().__init__()
        # Data references
        self._display_data = []
        self._search_index = []
        self._float_totals = []
        self._styles_cache = []

        # Filtering
        self._visible_indices = [] # Indices into _display_data
        self._filtered_count = 0

        self._worker = None
        self.is_loading = False

        self._current_search_terms = []
        self._current_col_filters = {}

        # If global cache is loaded, use it immediately
        if self._global_cache['loaded']:
            self._display_data = self._global_cache['display_data']
            self._search_index = self._global_cache['search_index']
            self._float_totals = self._global_cache['totals']
            self._styles_cache = self._global_cache['styles']
            # Reset filter (show all)
            self._visible_indices = list(range(len(self._display_data)))
            self._filtered_count = len(self._visible_indices)

        if data:
            self.update_data(data)

    def load_data_async(self, raw_data=None):
        if self._global_cache['loaded'] and raw_data is None:
            self.cache_loaded.emit()
            return

        if self.is_loading:
            return

        self.is_loading = True
        self.loading_progress.emit("Avvio..." if raw_data else "Caricamento Cache...")

        self._worker = CacheWorker(self.CACHE_PATH, raw_data)
        self._worker.progress.connect(self.loading_progress.emit)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.start()

    def _on_worker_finished(self, display_data, search, totals, style_cache):
        self.beginResetModel()
        self._display_data = display_data
        self._search_index = search
        self._float_totals = totals
        self._styles_cache = style_cache

        # Reset filters
        self._visible_indices = list(range(len(display_data)))
        self._filtered_count = len(self._visible_indices)

        self.endResetModel()

        # Update Singleton
        self._global_cache['display_data'] = display_data
        self._global_cache['search_index'] = search
        self._global_cache['totals'] = totals
        self._global_cache['styles'] = style_cache
        self._global_cache['loaded'] = True

        self.is_loading = False
        self._worker = None
        self.cache_loaded.emit()

    def update_data(self, new_data):
        self.load_data_async(new_data)

    def set_filter(self, text, col_filters=None):
        """
        Applica filtri (testo globale e colonne) e aggiorna _visible_indices.
        Operazione pura Python ottimizzata.
        """
        text = text.lower().strip()
        search_terms = text.split() if text else []

        self.beginResetModel()

        # Optimize: if no filters, just range
        if not search_terms and not col_filters:
            self._visible_indices = list(range(len(self._display_data)))
        else:
            # Filter Logic
            # We use list comprehension for speed
            indices = range(len(self._display_data))

            # 1. Global Search
            if search_terms:
                # Pre-bind
                s_idx = self._search_index
                # Efficient intersection
                indices = [
                    i for i in indices
                    if all(t in s_idx[i] for t in search_terms)
                ]

            # 2. Column Filters
            if col_filters:
                # col_filters: {col_idx: set(lowercase_values)}
                for col, allowed in col_filters.items():
                    # allowed is a set of lowercase strings
                    # Data is in self._display_data[i][col] (string)
                    # We need to lower it? Yes.
                    # This part is slower, O(N).
                    d_data = self._display_data
                    indices = [
                        i for i in indices
                        if d_data[i][col].lower() in allowed
                    ]

            self._visible_indices = indices

        self._filtered_count = len(self._visible_indices)
        self.endResetModel()

    def get_float_total_for_visible(self):
        """Sum totals for visible rows."""
        # This is fast: sum(list comprehension)
        # accessing _float_totals via index
        if not self._float_totals: return 0.0

        # Direct index access
        # Optimization: use numpy if available? No, stick to stdlib.
        # map is fast.
        total = sum(self._float_totals[i] for i in self._visible_indices)
        return total

    def rowCount(self, parent=QModelIndex()):
        return self._filtered_count

    def columnCount(self, parent=QModelIndex()):
        return len(self.COLUMNS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        # ⚡ FAST PATH ⚡
        # Map visual row to real row
        row = index.row()
        if row >= self._filtered_count: return None

        real_row_idx = self._visible_indices[row]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            # Direct string access
            return self._display_data[real_row_idx][col]

        elif role == Qt.ItemDataRole.BackgroundRole:
            return self._get_style(real_row_idx, col, 'bg')

        elif role == Qt.ItemDataRole.ForegroundRole:
            return self._get_style(real_row_idx, col, 'fg')

        elif role == Qt.ItemDataRole.TextAlignmentRole:
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

    def _get_style(self, real_row, col, style_type):
        try:
            if real_row >= len(self._styles_cache): return None
            styles = self._styles_cache[real_row]
            if not styles: return None

            # Keys mapping (same as before)
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
        # Access the real model directly
        # The view's model is now ScaricoOreTableModel (no proxy)
        model = self.model()

        # Collect unique values from ALL data (not just filtered)
        # Optimization: Use set comprehension on _display_data
        unique_values = {row[col_index] for row in model._display_data}

        # Check applied filter
        # We need to access current filters from panel?
        # Or store them in model? The model receives them in set_filter.
        # Let's say we pass current applied filters to the menu.
        # Ideally model should store current column filters state.
        # But for now, we can pass empty or manage it in the panel.
        # Actually, let's assume no pre-selection for simplicity or TODO.
        # Better: The panel manages the state.

        menu = QMenu(self)

        # Determine widget type
        if col_index == 0:
            filter_widget = DateFilterPopupWidget(unique_values, None)
        else:
            sorted_values = sorted(list(unique_values), key=lambda x: str(x).lower())
            filter_widget = ListFilterPopupWidget(sorted_values, None)

        action = QWidgetAction(menu)
        action.setDefaultWidget(filter_widget)
        menu.addAction(action)

        menu.exec(global_pos)

        if filter_widget.applied:
            selected = filter_widget.get_selected_values()
            # Signal the panel to update filters
            # Since header doesn't know panel, we use a signal or direct model update
            # But the model needs ALL filters (text + cols).
            # So we emit a custom signal from Header?
            # Or just call a method on the parent widget if possible?
            # Creating a signal here is best practice.
            self.filterChanged.emit(col_index, selected)

    filterChanged = pyqtSignal(int, object) # col, values

# ... (ListFilterPopupWidget and DateFilterPopupWidget remain mostly same,
# just ensure they handle strings correctly, which they do)

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
