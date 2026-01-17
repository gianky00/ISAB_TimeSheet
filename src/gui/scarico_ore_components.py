import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QListView,
    QMenu,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
)

from src.utils.parsing import parse_currency


class CacheWorker(QThread):
    """
    ⚡ BOLT OPTIMIZATION: Background worker for heavy cache operations.
    Handles file I/O (pickle) and data processing.
    Now builds a PRE-FORMATTED display cache for max speed.
    """

    finished = pyqtSignal(
        object, object, object, object
    )  # display_data, search_index, float_totals, style_cache
    progress = pyqtSignal(str)

    def __init__(self, cache_path, data_source=None):
        super().__init__()
        self.cache_path = cache_path
        self.data_source = data_source  # If provided, we build cache from this data.

    def run(self):
        """Esegue l'operazione di caricamento o generazione della cache in background."""
        if self.data_source:
            # Build cache from raw data (e.g. from DB)
            self.progress.emit("Elaborazione dati...")
            display_data, search_index, float_totals, style_cache = self._build_caches(
                self.data_source
            )
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
                with open(self.cache_path, "rb") as f:
                    # Legacy support: check pickle structure
                    # We use pickle for local trusted cache of complex data structures.
                    loaded = pickle.load(f)  # nosec B301
                    if len(loaded) == 3:
                        # Old format: data, search, totals
                        # We must rebuild because 'data' is raw, we need 'display_data'
                        raw_data = loaded[0]
                        (
                            display_data,
                            search_index,
                            float_totals,
                            style_cache,
                        ) = self._build_caches(raw_data)
                    elif len(loaded) == 4:
                        # Version 2 format: raw_data, search, totals, style
                        # Checking if we need to rebuild (if data is not pre-formatted strings)
                        d, s, t, st = loaded
                        if (
                            d
                            and len(d) > 0
                            and (d[0][0] is None or not isinstance(d[0][0], str))
                        ):
                            # Likely raw data or None, rebuild
                            (
                                display_data,
                                search_index,
                                float_totals,
                                style_cache,
                            ) = self._build_caches(d)
                        else:
                            # Already formatted
                            display_data, search_index, float_totals, style_cache = (
                                d,
                                s,
                                t,
                                st,
                            )
                    else:
                        display_data, search_index, float_totals, style_cache = (
                            [],
                            [],
                            [],
                            [],
                        )

                self.finished.emit(
                    display_data, search_index, float_totals, style_cache
                )
            except Exception as e:
                print(f"Error loading cache: {e}")
                self.finished.emit([], [], [], [])

    def _build_style_cache_only(self, data):
        """
        Costruisce solo la cache degli stili dai dati grezzi.

        Args:
            data: Dati grezzi estratti dal database.
        Returns:
            list: Lista di dizionari di stile o None.
        """
        style_cache = []
        append_style = style_cache.append

        for row in data:
            if len(row) > 11:
                style_json = row[11]
                if style_json:
                    try:
                        append_style(json.loads(style_json))
                    except Exception:
                        append_style(None)
                else:
                    append_style(None)
            else:
                append_style(None)
        return style_cache

    def _build_caches(self, data):
        """
        Pre-computa tutto: Stringhe visualizzate, Indice ricerca, Totali, Stili.

        Args:
            data: Dati grezzi da processare.
        Returns:
            tuple: (display_data, search_index, float_totals, style_cache)
        """
        display_data, search_index, float_totals, style_cache = [], [], [], []

        for row in data:
            # 1. Date & Display Strings
            date_str = self._format_date_for_display(row[0])
            disp_row, search_parts = self._process_row_fields(row, date_str)

            display_data.append(disp_row)
            search_index.append(" ".join(search_parts).lower())

            # 2. Totals
            float_totals.append(self._parse_row_total(row[7]))

            # 3. Styles
            style_cache.append(self._parse_row_style(row))

        return display_data, search_index, float_totals, style_cache

    def _format_date_for_display(self, val) -> str:
        """
        Parsa e formatta il valore data per la visualizzazione.

        Args:
            val: Valore data (stringa o datetime).
        Returns:
            str: Data formattata dd/mm/yyyy.
        """
        if not val:
            return ""
        s_val = str(val)
        if "-" not in s_val:
            return s_val

        try:
            if len(s_val) >= 10 and s_val[4] == "-" and s_val[7] == "-":
                return f"{s_val[8:10]}/{s_val[5:7]}/{s_val[0:4]}"
            parts = s_val.split(" ")[0].split("-")
            return f"{parts[2]}/{parts[1]}/{parts[0]}" if len(parts) == 3 else s_val
        except Exception:
            return s_val

    def _process_row_fields(self, row, date_str) -> tuple[list[str], list[str]]:
        """
        Converte i campi in stringhe e prepara le parti per la ricerca.

        Args:
            row: Riga di dati grezzi.
            date_str: Data già formattata.
        Returns:
            tuple: (dati_visualizzazione, termini_ricerca)
        """
        disp_row = [date_str]
        search_parts = [date_str]
        for i in range(1, 11):
            val = row[i]
            d_val = "" if val is None else str(val)
            disp_row.append(d_val)
            if d_val:
                search_parts.append(d_val)
        return disp_row, search_parts

    def _parse_row_total(self, val) -> float:
        """
        Parsa in modo resiliente il totale ore in float.

        Args:
            val: Valore da parsare.
        Returns:
            float: Valore numerico o 0.0 in caso di errore.
        """
        try:
            if isinstance(val, (int, float)):
                return float(val)
            return parse_currency(val)
        except Exception:
            return 0.0

    def _parse_row_style(self, row) -> Optional[dict]:
        """
        Estrae e parsa il JSON degli stili se presente.

        Args:
            row: Riga di dati.
        Returns:
            dict: Dizionario degli stili o None.
        """
        if len(row) <= 11 or not row[11]:
            return None
        try:
            return json.loads(row[11])
        except Exception:
            return None

    def _save_cache(self, data, search, totals, style_cache):
        """
        Salva i dati processati nel file di cache su disco.

        Args:
            data: Dati visualizzazione.
            search: Indice ricerca.
            totals: Totali numerici.
            style_cache: Cache degli stili.
        """
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, "wb") as f:
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
        "DATA",
        "PERS1",
        "PERS2",
        "ODC",
        "POS",
        "DALLE",
        "ALLE",
        "TOTALE\nORE",
        "DESCRIZIONE",
        "FINITO",
        "COMMESSA",
    ]

    CACHE_PATH = Path("data/scarico_ore_cache.pkl")

    # ⚡ SINGLETON CACHE
    _global_cache = {
        "display_data": [],  # List[List[str]]
        "search_index": [],  # List[str]
        "totals": [],  # List[float]
        "styles": [],  # List[dict]
        "loaded": False,
    }

    cache_loaded = pyqtSignal()
    loading_progress = pyqtSignal(str)

    def __init__(self, data=None):
        """
        Inizializza il modello e collega la cache globale se già caricata.

        Args:
            data: Dati iniziali opzionali.
        """
        super().__init__()
        # Data references
        self._display_data = []
        self._search_index = []
        self._float_totals = []
        self._styles_cache = []

        # Filtering
        self._visible_indices = []  # Indices into _display_data
        self._filtered_count = 0

        self._worker = None
        self.is_loading = False

        self._current_search_terms = []
        self._current_col_filters = {}

        # If global cache is loaded, use it immediately
        if self._global_cache["loaded"]:
            self._display_data = self._global_cache["display_data"]
            self._search_index = self._global_cache["search_index"]
            self._float_totals = self._global_cache["totals"]
            self._styles_cache = self._global_cache["styles"]
            # Reset filter (show all)
            self._visible_indices = list(range(len(self._display_data)))
            self._filtered_count = len(self._visible_indices)

        if data:
            self.update_data(data)

    def load_data_async(self, raw_data=None):
        """
        Avvia il caricamento asincrono dei dati.

        Args:
            raw_data: Dati grezzi da processare, se None carica dalla cache su disco.
        """
        if self._global_cache["loaded"] and raw_data is None:
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
        """Callback eseguito al termine del caricamento asincrono."""
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
        self._global_cache["display_data"] = display_data
        self._global_cache["search_index"] = search
        self._global_cache["totals"] = totals
        self._global_cache["styles"] = style_cache
        self._global_cache["loaded"] = True

        self.is_loading = False
        self._worker = None
        self.cache_loaded.emit()

    def update_data(self, new_data):
        """Aggiorna i dati del modello in modo asincrono."""
        self.load_data_async(new_data)

    def set_data(self, data):
        """Aggiornamento dati sincrono (principalmente per test)."""
        worker = CacheWorker(self.CACHE_PATH)
        display_data, search, totals, style_cache = worker._build_caches(data)
        self._on_worker_finished(display_data, search, totals, style_cache)

    def set_filter(self, text, col_filters=None):
        """
        Applica filtri (testo globale e colonne) e aggiorna _visible_indices.
        Operazione pura Python ottimizzata per grandi dataset.
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
                    i for i in indices if all(t in s_idx[i] for t in search_terms)
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
                    indices = [i for i in indices if d_data[i][col].lower() in allowed]

            self._visible_indices = indices

        self._filtered_count = len(self._visible_indices)
        self.endResetModel()

    def get_float_total_for_visible(self):
        """Calcola la somma dei totali per le righe attualmente visibili."""
        # This is fast: sum(list comprehension)
        # accessing _float_totals via index
        if not self._float_totals:
            return 0.0

        # Direct index access
        # Optimization: use numpy if available? No, stick to stdlib.
        # map is fast.
        total = sum(self._float_totals[i] for i in self._visible_indices)
        return total

    def rowCount(self, parent=None):
        """Restituisce il numero di righe filtrate."""
        if parent is None:
            parent = QModelIndex()
        return self._filtered_count

    def columnCount(self, parent=None):
        """Restituisce il numero di colonne del modello."""
        if parent is None:
            parent = QModelIndex()
        return len(self.COLUMNS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """Restituisce il dato per l'indice e il ruolo richiesto."""
        if not index.isValid():
            return None

        # ⚡ FAST PATH ⚡
        # Map visual row to real row
        row = index.row()
        if row >= self._filtered_count:
            return None

        real_row_idx = self._visible_indices[row]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            # Direct string access
            return self._display_data[real_row_idx][col]

        elif role == Qt.ItemDataRole.BackgroundRole:
            return self._get_style(real_row_idx, col, "bg")

        elif role == Qt.ItemDataRole.ForegroundRole:
            return self._get_style(real_row_idx, col, "fg")

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if col in [3, 4, 5, 6, 7]:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            if col == 0:
                return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        """Restituisce l'intestazione per la sezione e il ruolo richiesto."""
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self.COLUMNS[section]
        return None

    def _get_style(self, real_row, col, style_type):
        """Recupera lo stile (colore hex) dalla cache degli stili."""
        try:
            if real_row >= len(self._styles_cache):
                return None
            styles = self._styles_cache[real_row]
            if not styles:
                return None

            # Keys mapping (same as before)
            keys = [
                "data",
                "pers1",
                "pers2",
                "odc",
                "pos",
                "dalle",
                "alle",
                "totale_ore",
                "descrizione",
                "finito",
                "commessa",
            ]
            key = keys[col]
            if key in styles:
                color_hex = styles[key].get(style_type)
                if color_hex:
                    return QColor(color_hex)
        except Exception:
            pass
        return None


class FilterHeaderView(QHeaderView):
    """
    Header personalizzato con supporto per menu di filtraggio a discesa.
    Permette di cliccare sulle intestazioni per aprire popup di filtro specifici per colonna.
    """

    def __init__(self, orientation, parent=None):
        """
        Inizializza l'header e abilita il click sulle sezioni.

        Args:
            orientation: Orientamento (Qt.Orientation.Horizontal).
            parent: Widget genitore.
        """
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setHighlightSections(True)

    def mouseReleaseEvent(self, event):
        """Gestisce il rilascio del mouse per mostrare il menu di filtro."""
        idx = self.logicalIndexAt(event.pos())
        if idx >= 0:
            self._show_filter_menu(idx, event.globalPosition().toPoint())
        super().mouseReleaseEvent(event)

    def _show_filter_menu(self, col_index, global_pos):
        """
        Crea e visualizza il menu di filtraggio per la colonna specificata.

        Args:
            col_index: Indice della colonna.
            global_pos: Posizione globale dove visualizzare il menu.
        """
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
            sorted_values = sorted(unique_values, key=lambda x: str(x).lower())
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

    filterChanged = pyqtSignal(int, object)  # col, values


# ... (ListFilterPopupWidget and DateFilterPopupWidget remain mostly same,
# just ensure they handle strings correctly, which they do)


class ListFilterPopupWidget(QWidget):
    """
    Widget di popup per il filtraggio di liste di valori unici.
    Include una barra di ricerca e opzioni di selezione rapida.
    """

    def __init__(self, values, selected_values=None):
        """
        Inizializza il widget con i valori disponibili.

        Args:
            values: Lista di valori unici.
            selected_values: Set di valori già selezionati (opzionale).
        """
        super().__init__()
        self.values = values
        self.all_values = {str(v).lower() for v in values}
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
        is_all_selected = selected_values is None
        selected_set = set()
        if selected_values:
            selected_set = {v.lower() for v in selected_values}

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
        """Filtra la lista in base al testo inserito."""
        text = text.lower()
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if text in item.text().lower():
                self.list_view.setRowHidden(i, False)
            else:
                self.list_view.setRowHidden(i, True)

    def select_all(self):
        """Seleziona tutti i valori visibili nella lista."""
        self.model.blockSignals(True)
        for i in range(self.model.rowCount()):
            if not self.list_view.isRowHidden(i):
                self.model.item(i).setCheckState(Qt.CheckState.Checked)
        self.model.blockSignals(False)
        self.model.layoutChanged.emit()

    def select_none(self):
        """Deseleziona tutti i valori visibili nella lista."""
        self.model.blockSignals(True)
        for i in range(self.model.rowCount()):
            if not self.list_view.isRowHidden(i):
                self.model.item(i).setCheckState(Qt.CheckState.Unchecked)
        self.model.blockSignals(False)
        self.model.layoutChanged.emit()

    def _on_item_changed(self, item):
        """Callback eseguito al cambio di stato di un elemento."""
        pass

    def apply_filter(self):
        """Segnala l'applicazione del filtro e chiude il menu."""
        self.applied = True
        self._close_menu()

    def get_selected_values(self):
        """Restituisce la lista dei valori attualmente selezionati."""
        # Scan all items
        selected = []
        all_checked = True

        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected.append(item.text())
            else:
                all_checked = False

        if all_checked:
            return None
        return selected

    def _close_menu(self):
        """Chiude ricorsivamente i menu QMenu genitori."""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMenu):
                parent.close()
                break
            parent = parent.parent()


class DateFilterPopupWidget(QWidget):
    """Widget filtro gerarchico per date (Anno -> Mese -> Giorno)."""

    def __init__(self, values, selected_values=None):
        """
        Inizializza il widget con le date disponibili.

        Args:
            values: Lista di stringhe data (dd/mm/yyyy).
            selected_values: Lista di date già selezionate (opzionale).
        """
        super().__init__()
        self.values = values  # list of "DD/MM/YYYY" strings
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
        """Costruisce la struttura ad albero Anno -> Mese -> Giorno."""
        self.raw_dates = set(values)
        structure: Dict[str, Dict[str, List[str]]] = self._group_dates_by_hierarchy(
            values
        )

        is_all_selected = selected_values is None
        selected_set = set(selected_values) if selected_values else set()

        for y in sorted(structure.keys(), reverse=True):
            y_item = self._create_year_item(
                y, structure[y], selected_set, is_all_selected
            )
            self.model.appendRow(y_item)

    def _group_dates_by_hierarchy(
        self, values: list
    ) -> Dict[str, Dict[str, List[str]]]:
        """Organizza le date in un dizionario Anno -> Mese -> [Date]."""
        structure: Dict[str, Dict[str, List[str]]] = {}
        for v in values:
            if not v:
                continue
            try:
                parts = v.split("/")
                if len(parts) != 3:
                    continue
                _, m, y = parts
                if y not in structure:
                    structure[y] = {}
                if m not in structure[y]:
                    structure[y][m] = []
                structure[y][m].append(v)
            except Exception:
                continue
        return structure

    def _create_year_item(
        self, year, months_map, selected_set, is_all
    ) -> QStandardItem:
        """Crea il nodo anno e popola i mesi."""
        y_item = QStandardItem(year)
        y_item.setCheckable(True)
        y_item.setEditable(False)

        checked_months = 0
        for m in sorted(months_map.keys()):
            m_item = self._create_month_item(m, months_map[m], selected_set, is_all)
            y_item.appendRow(m_item)
            if m_item.checkState() == Qt.CheckState.Checked:
                checked_months += 1

        # Stato Anno
        if checked_months == len(months_map):
            y_item.setCheckState(Qt.CheckState.Checked)
        elif checked_months > 0 or self._has_any_child_checked(y_item):
            y_item.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            y_item.setCheckState(Qt.CheckState.Unchecked)

        return y_item

    def _create_month_item(
        self, month_code, days, selected_set, is_all
    ) -> QStandardItem:
        """Crea il nodo mese e popola i giorni."""
        m_name = self._get_month_name(month_code)
        m_item = QStandardItem(f"{m_name} ({month_code})")
        m_item.setCheckable(True)
        m_item.setEditable(False)

        checked_days = 0
        for date_str in sorted(days):
            day_part = date_str.split("/")[0]
            d_item = QStandardItem(day_part)
            d_item.setCheckable(True)
            d_item.setEditable(False)
            d_item.setData(date_str, Qt.ItemDataRole.UserRole)

            state = (
                Qt.CheckState.Checked
                if (is_all or date_str in selected_set)
                else Qt.CheckState.Unchecked
            )
            d_item.setCheckState(state)
            if state == Qt.CheckState.Checked:
                checked_days += 1
            m_item.appendRow(d_item)

        # Stato Mese
        if checked_days == len(days):
            m_item.setCheckState(Qt.CheckState.Checked)
        elif checked_days > 0:
            m_item.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            m_item.setCheckState(Qt.CheckState.Unchecked)
        return m_item

    def _has_any_child_checked(self, item: QStandardItem) -> bool:
        """Verifica ricorsiva se almeno un figlio è selezionato."""
        for r in range(item.rowCount()):
            child = item.child(r)
            if child and child.checkState() != Qt.CheckState.Unchecked:
                return True
        return False

    def _get_month_name(self, m_str):
        """Converte il codice mese nel nome esteso in italiano."""
        names = {
            "01": "Gennaio",
            "02": "Febbraio",
            "03": "Marzo",
            "04": "Aprile",
            "05": "Maggio",
            "06": "Giugno",
            "07": "Luglio",
            "08": "Agosto",
            "09": "Settembre",
            "10": "Ottobre",
            "11": "Novembre",
            "12": "Dicembre",
        }
        return names.get(m_str, m_str)

    def _on_item_changed(self, item):
        """Gestisce i cambiamenti di stato ricorsivamente (su e giù nell'albero)."""
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
        """Imposta lo stato di tutti i discendenti in modo ricorsivo."""
        for i in range(item.rowCount()):
            child = item.child(i)
            child.setCheckState(state)
            self._set_children_state(child, state)

    def _update_parent_state(self, item):
        """Aggiorna lo stato del genitore in base ai suoi figli."""
        parent = item.parent()
        if not parent:
            return

        checked = 0
        partial = 0
        count = parent.rowCount()

        for i in range(count):
            s = parent.child(i).checkState()
            if s == Qt.CheckState.Checked:
                checked += 1
            elif s == Qt.CheckState.PartiallyChecked:
                partial += 1

        if checked == count:
            parent.setCheckState(Qt.CheckState.Checked)
        elif checked > 0 or partial > 0:
            parent.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            parent.setCheckState(Qt.CheckState.Unchecked)

        self._update_parent_state(parent)

    def select_all(self):
        """Seleziona ricorsivamente tutte le date nell'albero."""
        self.model.blockSignals(True)
        root = self.model.invisibleRootItem()
        self._set_children_state(root, Qt.CheckState.Checked)
        self.model.blockSignals(False)
        self.model.layoutChanged.emit()

    def select_none(self):
        """Deseleziona ricorsivamente tutte le date nell'albero."""
        self.model.blockSignals(True)
        root = self.model.invisibleRootItem()
        self._set_children_state(root, Qt.CheckState.Unchecked)
        self.model.blockSignals(False)
        self.model.layoutChanged.emit()

    def apply_filter(self):
        """Segnala l'applicazione del filtro e chiude il menu."""
        self.applied = True
        self._close_menu()

    def get_selected_values(self):
        """Traversa l'albero per trovare tutte le foglie (date) selezionate."""
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

        if all_checked:
            return None
        return selected

    def _close_menu(self):
        """Chiude ricorsivamente i menu QMenu genitori."""
        parent = self.parent()
        while parent:
            if isinstance(parent, QMenu):
                parent.close()
                break
            parent = parent.parent()
