"""
Bot TS - Scarico Ore Panel
Pannello dedicato per lo Scarico Ore Cantiere.
Aggiornato per usare Virtual Table (130k+ righe) e Filtri Avanzati.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableView, QLineEdit, QMessageBox, QHeaderView, QFrame, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QCursor, QKeySequence

from src.core.contabilita_manager import ContabilitaManager
from src.core import config_manager
from src.gui.scarico_ore_components import ScaricoOreTableModel, FilterHeaderView
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
        # ⚡ BOLT: Set loading text immediately before first paint
        self.search_input.setPlaceholderText("⏳ Inizializzazione dati... attendere")
        self.search_input.setEnabled(False)
        QTimer.singleShot(50, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # --- Toolbar ---
        toolbar = QHBoxLayout()

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("⏳ Inizializzazione...")
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
        # Also search on text changed? For 130k rows, Enter is safer, but let's see.
        # Ideally debounce. But Virtual Model is fast enough for per-char?
        # Let's stick to Enter for "MAXIMUM" responsiveness unless requested.
        # Actually user said "Cold Start Lag" on search.
        # Let's enable real-time search if it's fast (< 50ms).
        # We'll stick to Enter to be safe for now as requested by previous logic.

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
        # ⚡ BOLT: Use Virtual Model directly, no Proxy
        self.source_model = ScaricoOreTableModel([])
        self.source_model.cache_loaded.connect(self._on_cache_loaded)
        self.source_model.loading_progress.connect(self._on_loading_progress)

        self.table_view.setModel(self.source_model)

        # Custom Header
        header = FilterHeaderView(Qt.Orientation.Horizontal, self.table_view)
        self.table_view.setHorizontalHeader(header)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Connect Header Filters
        header.filterChanged.connect(self._on_header_filter_changed)

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
        # ⚡ BOLT: Use Model's fast counter
        row_count = self.source_model.rowCount()
        self.lbl_count.setText(f"Righe visibili: {row_count}")

        if row_count > 0:
             # Use the model's optimized sum (it uses indices)
             # Ideally run in background if > 50k rows?
             # Python sum of 130k floats is ~5ms. Safe for main thread.
             total = self.source_model.get_float_total_for_visible()
             self.lbl_total_hours.setText(f"Totale Ore: {total:,.2f}")
        else:
             self.lbl_total_hours.setText("Totale Ore: 0.00")

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
            # Invalidate cache by removing the file
            try:
                if ScaricoOreTableModel.CACHE_PATH.exists():
                    ScaricoOreTableModel.CACHE_PATH.unlink()
            except: pass

            # Reset global cache to force reload
            ScaricoOreTableModel._global_cache['loaded'] = False

            self._load_data() # Reload data
            QMessageBox.information(self, "Successo", msg)
        else:
            self.status_label.setText("❌ Errore")
            QMessageBox.critical(self, "Errore Aggiornamento", msg)

    def _perform_search(self):
        """Aggiorna il filtro testuale."""
        text = self.search_input.text()
        # Pass current column filters? No, we need to store them in panel.
        # Actually Model handles combination logic if we pass them.
        # Let's store col filters in panel state.
        if not hasattr(self, '_current_col_filters'):
            self._current_col_filters = {}

        self.source_model.set_filter(text, self._current_col_filters)
        self._update_totals()

    def _on_header_filter_changed(self, col, values):
        """Handle column filter changes from header."""
        if not hasattr(self, '_current_col_filters'):
            self._current_col_filters = {}

        if not values:
            if col in self._current_col_filters:
                del self._current_col_filters[col]
        else:
            # Store as set of lowercase for model optimization
            self._current_col_filters[col] = set(str(v).lower() for v in values)

        # Re-apply filters
        text = self.search_input.text()
        self.source_model.set_filter(text, self._current_col_filters)
        self._update_totals()

    def _set_ui_loading(self, loading: bool):
        """Disable/Enable UI during heavy loads."""
        self.search_input.setEnabled(not loading)
        self.update_btn.setEnabled(not loading)

        if loading:
            self.search_input.setPlaceholderText("⏳ Caricamento in corso... attendere")
            self.table_view.setDisabled(True)
            self.table_view.setStyleSheet("QTableView { background-color: #f8f9fa; }")
            # ⚡ BOLT: Force paint to show loading text immediately
            QApplication.processEvents()
        else:
            self.search_input.setPlaceholderText("🔍 Filtra dati (es. scavullo 4041)... (Premi Invio)")
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
        QApplication.processEvents() # Ensure progress updates are seen

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
        if ScaricoOreTableModel.CACHE_PATH.exists():
            self.source_model.load_data_async(raw_data=None)
        else:
            try:
                # Fetch ALL rows (tuples) - SQLite is fast
                rows = ContabilitaManager.get_scarico_ore_data()
                self.source_model.load_data_async(raw_data=rows)
            except Exception as e:
                self.status_label.setText(f"Errore caricamento: {e}")
                self._set_ui_loading(False)

    def _resize_columns(self):
        # ⚡ BOLT OPTIMIZATION: REMOVED resizeColumnsToContents()

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
