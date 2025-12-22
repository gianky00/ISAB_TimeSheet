"""
Bot TS - Scarico Ore Panel
Pannello dedicato per lo Scarico Ore Cantiere.
Aggiornato per usare Virtual Table (130k+ righe) e Filtri Avanzati.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableView, QLineEdit, QMessageBox, QHeaderView, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QCursor, QKeySequence

from src.core.contabilita_manager import ContabilitaManager
from src.core import config_manager
from src.gui.scarico_ore_components import ScaricoOreTableModel, ScaricoOreFilterProxy, FilterHeaderView
from src.utils.parsing import parse_currency
from pathlib import Path

class ScaricoOreWorker(QThread):
    """Worker per l'importazione in background (solo Scarico Ore)."""
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def run(self):
        # Inizializza DB se necessario (sicurezza)
        ContabilitaManager.init_db()
        success, msg = ContabilitaManager.import_scarico_ore(self.file_path)
        self.finished_signal.emit(success, msg)

class ScaricoOrePanel(QWidget):
    """Pannello per la visualizzazione e gestione dello Scarico Ore Cantiere."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self._setup_ui()
        # Delay load to allow UI to show up first (optimization)
        QTimer.singleShot(100, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # --- Toolbar ---
        toolbar = QHBoxLayout()

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Filtra dati (es. scavullo 4041)... (Premi Invio)")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setFixedWidth(400)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #0d6efd;
            }
        """)
        # Ricerca su Invio
        self.search_input.returnPressed.connect(self._perform_search)

        toolbar.addWidget(self.search_input)

        toolbar.addStretch()

        # Status Label
        self.status_label = QLabel("Inizializzazione...")
        self.status_label.setStyleSheet("color: #6c757d; font-size: 13px;")
        toolbar.addWidget(self.status_label)

        toolbar.addStretch()

        # Update Button
        self.update_btn = QPushButton("🔄 Aggiorna Dati")
        self.update_btn.setToolTip("Aggiorna solo lo Scarico Ore Cantiere dal file configurato")
        self.update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        self.update_btn.clicked.connect(self._start_update)
        toolbar.addWidget(self.update_btn)

        layout.addLayout(toolbar)

        # --- Virtual Table View ---
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(False) # Colors are from Excel
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        self.table_view.setShowGrid(True)
        self.table_view.setWordWrap(False) # Optimization: Disable word wrap for 130k rows performance

        # Models
        self.source_model = ScaricoOreTableModel([])
        self.source_model.cache_loaded.connect(self._on_cache_loaded)
        self.source_model.loading_progress.connect(self._on_loading_progress)

        self.proxy_model = ScaricoOreFilterProxy(self)
        self.proxy_model.setSourceModel(self.source_model)
        self.table_view.setModel(self.proxy_model)

        # Connect signals for totals update
        self.proxy_model.layoutChanged.connect(self._update_totals)
        self.proxy_model.rowsInserted.connect(lambda p, f, l: self._update_totals())
        self.proxy_model.rowsRemoved.connect(lambda p, f, l: self._update_totals())
        self.proxy_model.modelReset.connect(self._update_totals)

        # Custom Header
        header = FilterHeaderView(Qt.Orientation.Horizontal, self.table_view)
        self.table_view.setHorizontalHeader(header)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Styles
        self.table_view.setStyleSheet("""
            QTableView {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                gridline-color: #e9ecef;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
            }
        """)

        layout.addWidget(self.table_view)

        # --- Footer Bar for Totals (Option B) ---
        self.footer_frame = QFrame()
        self.footer_frame.setStyleSheet("""
            QFrame {
                background-color: #e9ecef;
                border-top: 2px solid #dee2e6;
                border-bottom-left-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: #212529;
            }
        """)
        footer_layout = QHBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(15, 10, 15, 10)

        self.lbl_count = QLabel("Righe: 0")
        self.lbl_total_hours = QLabel("Totale Ore: 0.00")
        self.lbl_total_hours.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        footer_layout.addWidget(self.lbl_count)
        footer_layout.addStretch()
        footer_layout.addWidget(self.lbl_total_hours)

        layout.addWidget(self.footer_frame)

        # Info label
        self.info_label = QLabel("Visualizzazione completa. Clicca sulle intestazioni per filtrare. Copia con Ctrl+C.")
        self.info_label.setStyleSheet("color: #adb5bd; font-size: 11px; margin-top: 5px;")
        layout.addWidget(self.info_label)

    def _update_totals(self):
        """Calculates totals based on visible rows."""
        # This can be heavy if run on main thread for 130k rows.
        # But FilterProxy handles filtering fast.
        # We need to iterate over indices.

        # Optimization: Only count rows, and sum 'Totale Ore' (Col 7)
        row_count = self.proxy_model.rowCount()
        self.lbl_count.setText(f"Righe visibili: {row_count}")

        # Summing 130k floats in python loop might freeze GUI for 0.5s.
        # We can do it in a timer or worker if needed.
        # Let's try direct first.
        # We only need to sum if row_count < some limit? No, user wants totals.
        # Optimization: If no filter, use pre-calculated total from source?

        if row_count > 50000:
             self.lbl_total_hours.setText("Totale Ore: Calcolo... (filtrando)")
             QTimer.singleShot(100, self._calculate_sum_heavy)
        else:
             self._calculate_sum_heavy()

    def _calculate_sum_heavy(self):
        total = 0.0
        # Iterate source rows? No, filtered rows.
        # proxy.data(index) is slow.
        # Fast path: Get source rows that are accepted.

        rows = self.proxy_model.rowCount()

        # Optimization 1: if rows == source.rows (no filter), sum source data directly (fast)
        if rows == self.source_model.rowCount():
             # Sum pre-calculated floats from source model
             # Accessing _float_totals directly is faster than method call
             try:
                 total = sum(self.source_model._float_totals)
             except:
                 total = 0
        else:
             # Iterate proxy. mapToSource is the bottleneck but unavoidable if we want exact visible sum.
             # However, accessing the PRE-PARSED float is much faster than parsing string.
             proxy = self.proxy_model
             source = self.source_model

             # Optimization: Avoid dot lookup in loop
             map_to_source = proxy.mapToSource
             index_fn = proxy.index
             get_float_total = source.get_float_total

             # This loop is still O(N) but operation inside is O(1) instead of O(M)
             for r in range(rows):
                 # We only need the row index of the source
                 source_idx = map_to_source(index_fn(r, 0))
                 total += get_float_total(source_idx.row())

        self.lbl_total_hours.setText(f"Totale Ore: {total:,.2f}")

    def _start_update(self):
        """Avvia l'aggiornamento specifico per Scarico Ore."""
        config = config_manager.load_config()
        path = config.get("dataease_path", "")

        if not path:
            QMessageBox.warning(self, "Configurazione Mancante", "Configura il percorso 'File Scarico Ore' nelle Impostazioni.")
            return

        self.status_label.setText("⏳ Aggiornamento in corso (può richiedere tempo per file grandi)...")
        self.update_btn.setEnabled(False)
        self.table_view.setEnabled(False)

        self.worker = ScaricoOreWorker(path)
        self.worker.finished_signal.connect(self._on_update_finished)
        self.worker.start()

    def _on_update_finished(self, success: bool, msg: str):
        self.update_btn.setEnabled(True)
        self.table_view.setEnabled(True)

        if success:
            self.status_label.setText("✅ Aggiornato")
            # Invalidate cache by removing the file, so _load_data forces a fresh DB read
            try:
                if ScaricoOreTableModel.CACHE_PATH.exists():
                    ScaricoOreTableModel.CACHE_PATH.unlink()
            except: pass

            self._load_data() # Reload data (will rebuild cache)
            QMessageBox.information(self, "Successo", msg)
        else:
            self.status_label.setText("❌ Errore")
            QMessageBox.critical(self, "Errore Aggiornamento", msg)

    def _perform_search(self):
        """Aggiorna il filtro testuale del proxy."""
        text = self.search_input.text()
        self.proxy_model.set_filter_text(text)

        count = self.proxy_model.rowCount()
        self.status_label.setText(f"Righe visibili: {count}")

    def _set_ui_loading(self, loading: bool):
        """Disable/Enable UI during heavy loads."""
        self.search_input.setEnabled(not loading)
        self.update_btn.setEnabled(not loading)
        if loading:
            self.table_view.setDisabled(True)
            self.table_view.setStyleSheet("QTableView { background-color: #f8f9fa; }")
        else:
            self.table_view.setDisabled(False)
            self.table_view.setStyleSheet("""
            QTableView {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                gridline-color: #e9ecef;
                font-size: 13px;
            }
            """)

    def _on_loading_progress(self, msg):
        self.status_label.setText(f"⏳ {msg}")

    def _on_cache_loaded(self):
        """Called when background loading finishes."""
        count = self.source_model.rowCount()
        self.status_label.setText(f"✅ Pronti ({count} record)")
        self._set_ui_loading(False)
        self._resize_columns()
        self._update_totals()

    def _load_data(self):
        """Carica TUTTI i dati in memoria (molto veloce in RAM)."""
        if not ContabilitaManager.DB_PATH.exists():
            self.status_label.setText("Database non trovato.")
            return

        self._set_ui_loading(True)

        # ⚡ BOLT OPTIMIZATION:
        # Check if cache exists. If not, we must load from DB.
        # The Model handles both scenarios via load_data_async.

        # If cache file exists, tell model to load it async
        if ScaricoOreTableModel.CACHE_PATH.exists():
            self.source_model.load_data_async(raw_data=None)
        else:
            # If no cache, we must load from DB first (main thread DB access is fast enough usually,
            # but converting to objects is slow? DB fetch for 130k rows is 1-2s.
            # Let's fetch data here and pass to worker to build cache.
            # Ideally fetch should also be async but let's stick to fixing the "processing" lag first.
            try:
                # Fetch ALL rows (tuples) - SQLite is fast
                rows = ContabilitaManager.get_scarico_ore_data()
                # Pass rows to model to build cache in background
                self.source_model.load_data_async(raw_data=rows)
            except Exception as e:
                self.status_label.setText(f"Errore caricamento: {e}")
                self._set_ui_loading(False)

    def _resize_columns(self):
        # Reset view properties
        self.table_view.resizeColumnsToContents()

        # Adjust column widths as requested:
        # "sum of widths must equal view size" -> Stretch Last Section?
        # "Descrizione (Col 8) must be wider"

        header = self.table_view.horizontalHeader()

        # Strategy: Set interactive for most, Stretch for Description
        # Reset to interactive first
        for i in range(11):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        # DATA (0), PERS1 (1), PERS2 (2), ODC (3), POS (4), DALLE (5), ALLE (6), TOT (7) -> Fixed/Interactive
        self.table_view.setColumnWidth(0, 90)  # Data
        self.table_view.setColumnWidth(1, 130) # Pers1
        self.table_view.setColumnWidth(2, 130) # Pers2
        self.table_view.setColumnWidth(3, 80)  # ODC
        self.table_view.setColumnWidth(4, 50)  # POS
        self.table_view.setColumnWidth(5, 50)  # Dalle
        self.table_view.setColumnWidth(6, 50)  # Alle
        self.table_view.setColumnWidth(7, 80)  # Tot
        self.table_view.setColumnWidth(9, 60)  # Finito
        self.table_view.setColumnWidth(10, 100)# Commessa

        # Description (8) Stretch to fill
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)

    def keyPressEvent(self, event):
        # Implement Ctrl+C for QTableView
        if event.matches(QKeySequence.StandardKey.Copy):
            self._copy_selection()
        else:
            super().keyPressEvent(event)

    def _copy_selection(self):
        selection = self.table_view.selectionModel()
        indexes = selection.selectedIndexes()
        if not indexes: return

        # Sort by row then col
        indexes.sort(key=lambda x: (x.row(), x.column()))

        # Build text
        rows_text = {} # row_idx -> list of (col_idx, text)
        for idx in indexes:
            r = idx.row()
            c = idx.column()
            data = self.table_view.model().data(idx)
            if r not in rows_text: rows_text[r] = []
            rows_text[r].append((c, str(data)))

        # Format TSV
        tsv_lines = []
        for r in sorted(rows_text.keys()):
            # Simple approach: join by tab
            line = "\t".join([x[1] for x in sorted(rows_text[r], key=lambda y: y[0])])
            tsv_lines.append(line)

        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText("\n".join(tsv_lines))
