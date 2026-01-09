"""
Bot TS - Scarico Ore Panel
Pannello dedicato per lo Scarico Ore Cantiere.
Aggiornato per usare Virtual Table (130k+ righe) e Filtri Avanzati.
"""

import time
from datetime import datetime

from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableView,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.contabilita_manager import ContabilitaManager
from src.gui.scarico_ore_components import FilterHeaderView, ScaricoOreTableModel


class ScaricoOreWorker(QThread):
    """Worker per l'importazione in background (solo Scarico Ore)."""

    finished_signal = pyqtSignal(bool, str, int, int, float)  # Added float duration
    progress_signal = pyqtSignal(str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.start_time = 0

    def run(self):
        # Inizializza DB se necessario (sicurezza)
        ContabilitaManager.init_db()
        self.start_time = time.time()

        # Pre-scan for total rows to enable accurate progress/ETA
        # We need to open the file to count rows first.
        # This adds a small overhead but allows for the requested feature.
        try:
            total_rows = ContabilitaManager.scan_scarico_ore_rows(self.file_path)
        except Exception:
            total_rows = 1000  # Fallback

        def progress_cb(current, total):
            # If total passed by callback is widely different (e.g. chunk based), ignore or adapt.
            # But import_scarico_ore passes row_idx vs total_rows (if known)

            # Use the more accurate total from scan if available
            real_total = total if total > 0 else total_rows
            if current > real_total:
                real_total = current  # Dynamic update to prevent > 100%

            elapsed = time.time() - self.start_time
            if current > 0 and elapsed > 0:
                rate = current / elapsed
                remaining = real_total - current
                eta_seconds = remaining / rate if rate > 0 else 0

                m, s = divmod(int(eta_seconds), 60)
                percent = int((current / real_total) * 100) if real_total > 0 else 0
                if percent > 99:
                    percent = 99  # Cap until actually finished

                self.progress_signal.emit(
                    f"⏳ Importazione: {percent}% completato ({current}/{real_total}) • Tempo stimato: {m}m {s}s"
                )

        success, msg, added, removed = ContabilitaManager.import_scarico_ore(
            self.file_path, progress_callback=progress_cb
        )
        total_duration = time.time() - self.start_time
        self.finished_signal.emit(success, msg, added, removed, total_duration)


class ScaricoOrePanel(QWidget):
    """Pannello per la visualizzazione e gestione dello Scarico Ore Cantiere."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self._last_update_status = (
            None  # Store the status string to persist after reload
        )
        self._setup_ui()
        # Delay load to allow UI to show up first (optimization)
        # ⚡ BOLT: Set loading text immediately before first paint
        self.search_input.setPlaceholderText("⏳ Inizializzazione dati... attendere")
        self.search_input.setEnabled(False)
        QTimer.singleShot(50, self._load_data)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # 1. Create Tabs (DataEase Wrapper)
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            """
            QTabWidget::pane { border: 1px solid #dee2e6; border-radius: 6px; background-color: white; }
            QTabBar::tab {
                background: #f1f3f5;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                color: #495057;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: white;
                color: #0d6efd;
                border-bottom: 2px solid #0d6efd;
            }
        """
        )
        main_layout.addWidget(self.tabs)

        # 2. "Scarico Ore" Tab
        self.scarico_tab = QWidget()
        scarico_layout = QVBoxLayout(self.scarico_tab)
        scarico_layout.setContentsMargins(10, 10, 10, 10)

        # --- Toolbar ---
        toolbar = QHBoxLayout()

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("⏳ Inizializzazione...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setFixedWidth(400)
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                background-color: white;
                color: black;
            }
            QLineEdit:focus {
                border-color: #0d6efd;
            }
        """
        )
        # Ricerca su Invio
        self.search_input.returnPressed.connect(self._perform_search)

        toolbar.addWidget(self.search_input)

        toolbar.addStretch()

        # Status Label
        self.status_label = QLabel("Inizializzazione...")
        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #495057;
                font-size: 14px;
                font-weight: 500;
                padding: 5px 10px;
                background-color: #f8f9fa;
                border-radius: 4px;
                border: 1px solid #dee2e6;
            }
        """
        )
        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Center alignment as requested
        toolbar.addWidget(self.status_label)

        toolbar.addStretch()

        # Update Button
        self.update_btn = QPushButton("🔄 Aggiorna Dati")
        self.update_btn.setToolTip(
            "Aggiorna solo lo Scarico Ore Cantiere dal file configurato"
        )
        self.update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_btn.setStyleSheet(
            """
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
        """
        )
        self.update_btn.clicked.connect(self._start_update)
        toolbar.addWidget(self.update_btn)

        scarico_layout.addLayout(toolbar)

        # --- Virtual Table View ---
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(False)  # Colors are from Excel
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        self.table_view.setShowGrid(True)
        self.table_view.setWordWrap(True)  # Enabled word wrap
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

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
        # Enable Word Wrap via Alignment (Corrected Flags)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap
        )

        # Connect Header Filters
        header.filterChanged.connect(self._on_header_filter_changed)

        # Disable Vertical Header (Row Numbers) as requested
        self.table_view.verticalHeader().setVisible(False)

        # Styles
        self.table_view.setStyleSheet(
            """
            QTableView {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                color: black;  /* Force black text */
                gridline-color: #e9ecef;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #E1F5FE;
                color: #333333;
                padding: 5px;
                border: none;
                border-right: 1px solid #B3E5FC;
                border-bottom: 3px solid #81D4FA;
                font-weight: bold;
                text-transform: uppercase;
                font-size: 11px;
            }
            QHeaderView::section:vertical {
                font-size: 11px;
                font-weight: bold;
                color: #495057;
                background-color: #F5F5F5;
                padding: 0px 8px;
                border-right: 1px solid #dee2e6;
                border-bottom: 1px solid #dee2e6;
            }
        """
        )

        scarico_layout.addWidget(self.table_view)

        # --- Footer Bar for Totals (Option B) ---
        self.footer_frame = QFrame()
        self.footer_frame.setStyleSheet(
            """
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
        """
        )
        footer_layout = QHBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(15, 10, 15, 10)

        self.lbl_count = QLabel("Righe: 0")
        self.lbl_count.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #0d6efd;"
        )
        self.lbl_total_hours = QLabel("Totale Ore: 0")
        self.lbl_total_hours.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        # New Selection Label
        self.lbl_selection_total = QLabel("Totale selezionato: 0")
        self.lbl_selection_total.setStyleSheet("color: #0d6efd;")
        self.lbl_selection_total.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        footer_layout.addWidget(self.lbl_count)
        footer_layout.addStretch()
        footer_layout.addWidget(self.lbl_selection_total)
        footer_layout.addSpacing(20)
        footer_layout.addWidget(self.lbl_total_hours)

        scarico_layout.addWidget(self.footer_frame)

        # Info label
        self.info_label = QLabel(
            "Visualizzazione completa. Clicca sulle intestazioni per filtrare. Copia con Ctrl+C."
        )
        self.info_label.setStyleSheet(
            "color: #adb5bd; font-size: 11px; margin-top: 5px;"
        )
        scarico_layout.addWidget(self.info_label)

        # Add Tab
        self.tabs.addTab(self.scarico_tab, "Scarico Ore")

        # Connect selection changes
        self.table_view.selectionModel().selectionChanged.connect(
            self._update_selection_totals
        )

    def _format_number(self, value: float) -> str:
        """Formats number: integer if no decimals, else 2 decimals."""
        if value % 1 == 0:
            return f"{int(value)}"
        return f"{value:.2f}"

    def _update_totals(self):
        """Calculates totals based on visible rows."""
        # ⚡ BOLT: Use Model's fast counter
        row_count = self.source_model.rowCount()
        self.lbl_count.setText(f"Righe visibili: {row_count}")

        if row_count > 0:
            total = self.source_model.get_float_total_for_visible()
            formatted = self._format_number(total)
            self.lbl_total_hours.setText(f"Totale Ore: {formatted}")
        else:
            self.lbl_total_hours.setText("Totale Ore: 0")

    def _update_selection_totals(self):
        """Calculates total of selected 'TOTALE ORE' cells."""
        try:
            indexes = self.table_view.selectionModel().selectedIndexes()
            if not indexes:
                self.lbl_selection_total.setText("Totale selezionato: 0")
                return

            total_selected = 0.0
            # Column 7 is 'TOTALE ORE'
            target_col = 7

            # Optimization: Filter indexes for col 7 only
            for idx in indexes:
                if idx.column() == target_col:
                    try:
                        val_str = str(idx.data(Qt.ItemDataRole.DisplayRole))
                        # Parse float (handles comma/dot via parse_currency or float)
                        if val_str:
                            # Handle comma just in case
                            val_str = val_str.replace(",", ".")
                            total_selected += float(val_str)
                    except ValueError:
                        pass  # Ignore parsing errors

            formatted = self._format_number(total_selected)
            self.lbl_selection_total.setText(f"Totale selezionato: {formatted}")
        except Exception as e:
            print(f"Errore selezione: {e}")

    def _start_update(self):
        """Avvia l'aggiornamento specifico per Scarico Ore."""
        config = config_manager.load_config()
        path = config.get("dataease_path", "")

        if not path:
            QMessageBox.warning(
                self,
                "Configurazione Mancante",
                "Configura il percorso 'File Scarico Ore' nelle Impostazioni.",
            )
            return

        self.status_label.setText("⏳ Calcolo stima tempi...")
        self.update_btn.setEnabled(False)
        self.table_view.setEnabled(False)

        self.worker = ScaricoOreWorker(path)
        self.worker.finished_signal.connect(self._on_update_finished)
        # Connect to _on_loading_progress to handle the message format correctly if needed,
        # but ScaricoOreWorker emits the full formatted string now.
        # Direct connection to setText is fine as worker formats it.
        self.worker.progress_signal.connect(self.status_label.setText)
        self.worker.start()

    def _on_update_finished(
        self,
        success: bool,
        msg: str,
        added: int = 0,
        removed: int = 0,
        duration: float = 0.0,
    ):
        self.update_btn.setEnabled(True)
        self.table_view.setEnabled(True)

        if success:
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            # Match exact format from ContabilitaPanel
            # Always color
            added_str = f"<font color='green'><b>+{added}</b></font>"
            removed_str = f"<font color='red'><b>-{removed}</b></font>"

            # Format duration
            if duration < 60:
                time_str = f"{duration:.1f}s"
            else:
                m, s = divmod(int(duration), 60)
                time_str = f"{m}m {s}s"

            final_status = (
                f"✅ {timestamp} {added_str} {removed_str} (Tempo: {time_str})"
            )
            self.status_label.setText(final_status)
            self._last_update_status = final_status  # Store to persist after reload

            # Invalidate cache by removing the file
            try:
                if ScaricoOreTableModel.CACHE_PATH.exists():
                    ScaricoOreTableModel.CACHE_PATH.unlink()
            except Exception:
                pass

            # Reset global cache to force reload
            ScaricoOreTableModel._global_cache["loaded"] = False

            self._load_data()  # Reload data
            # REMOVED: QMessageBox.information(self, "Successo", msg)
        else:
            self.status_label.setText("❌ Errore")
            QMessageBox.critical(self, "Errore Aggiornamento", msg)

    def _perform_search(self):
        """Aggiorna il filtro testuale."""
        text = self.search_input.text()
        # Pass current column filters? No, we need to store them in panel.
        # Actually Model handles combination logic if we pass them.
        # Let's store col filters in panel state.
        if not hasattr(self, "_current_col_filters"):
            self._current_col_filters = {}

        self.source_model.set_filter(text, self._current_col_filters)
        self._update_totals()

    def _on_header_filter_changed(self, col, values):
        """Handle column filter changes from header."""
        if not hasattr(self, "_current_col_filters"):
            self._current_col_filters = {}

        if not values:
            if col in self._current_col_filters:
                del self._current_col_filters[col]
        else:
            # Store as set of lowercase for model optimization
            self._current_col_filters[col] = {str(v).lower() for v in values}

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
            self.search_input.setPlaceholderText(
                "🔍 Filtra dati (es. scavullo 4041)... (Premi Invio)"
            )
            self.table_view.setDisabled(False)
            self.table_view.setStyleSheet(
                """
            QTableView {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                gridline-color: #e9ecef;
                font-size: 13px;
            }
            """
            )

    def _on_loading_progress(self, msg):
        # Update text. If format matches worker (contains "Tempo stimato"), it's handled.
        # Ensure we don't have "Inizializzazione..." stuck if progress message comes.
        self.status_label.setText(
            f"{msg}"
        )  # Worker sends full formatted string with icon
        QApplication.processEvents()  # Ensure progress updates are seen

    def _on_cache_loaded(self):
        """Called when background loading finishes."""
        self.source_model.rowCount()

        # Restore last update status if exists, otherwise show default "Pronto"
        if self._last_update_status:
            self.status_label.setText(self._last_update_status)
        else:
            # Only set if not already set by something else (unlikely in this flow, but safe)
            current_text = self.status_label.text()
            if "ultimo aggiornamento" not in current_text:
                self.status_label.setText("Pronto")

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
        # Enable multiline by setting height
        header.setMinimumHeight(80)

        # Strategy: Most columns are fixed/interactive. DESCRIPTION stretches to fill space.
        header.setStretchLastSection(False)

        # Reset to interactive first
        for i in range(11):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        # DATA (0), PERS1 (1), PERS2 (2), ODC (3), POS (4), DALLE (5), ALLE (6), TOT (7) -> Fixed/Interactive
        self.table_view.setColumnWidth(0, 100)  # Data
        self.table_view.setColumnWidth(1, 150)  # Pers1
        self.table_view.setColumnWidth(2, 150)  # Pers2
        self.table_view.setColumnWidth(3, 100)  # ODC
        self.table_view.setColumnWidth(4, 60)  # POS
        self.table_view.setColumnWidth(5, 75)  # Dalle
        self.table_view.setColumnWidth(6, 75)  # Alle
        self.table_view.setColumnWidth(7, 90)  # Totale Ore

        # DESCRIZIONE (8) -> STRETCH (Fills all remaining space)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)

        self.table_view.setColumnWidth(9, 80)  # Finito
        self.table_view.setColumnWidth(10, 100)  # Commessa

    def keyPressEvent(self, event):
        # Implement Ctrl+C for QTableView
        if event.matches(QKeySequence.StandardKey.Copy):
            self._copy_selection()
        else:
            super().keyPressEvent(event)

    def _copy_selection(self):
        selection = self.table_view.selectionModel()
        indexes = selection.selectedIndexes()
        if not indexes:
            return

        # Sort by row then col
        indexes.sort(key=lambda x: (x.row(), x.column()))

        # Build text
        rows_text = {}  # row_idx -> list of (col_idx, text)
        for idx in indexes:
            r = idx.row()
            c = idx.column()
            data = self.table_view.model().data(idx)
            if r not in rows_text:
                rows_text[r] = []
            rows_text[r].append((c, str(data)))

        # Format TSV
        tsv_lines = []
        for r in sorted(rows_text.keys()):
            # Simple approach: join by tab
            line = "\t".join([x[1] for x in sorted(rows_text[r], key=lambda y: y[0])])
            tsv_lines.append(line)

        from PyQt6.QtWidgets import QApplication

        QApplication.clipboard().setText("\n".join(tsv_lines))
