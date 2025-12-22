"""
Bot TS - Scarico Ore Panel
Pannello dedicato per lo Scarico Ore Cantiere.
Aggiornato per usare Virtual Table (130k+ righe) e Filtri Avanzati.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableView, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QCursor

from src.core.contabilita_manager import ContabilitaManager
from src.core import config_manager
from src.gui.scarico_ore_components import ScaricoOreTableModel, ScaricoOreFilterProxy, FilterHeaderView

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
        self._load_data()

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
        self.status_label = QLabel("Pronto")
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

        # Models
        self.source_model = ScaricoOreTableModel([])
        self.proxy_model = ScaricoOreFilterProxy(self)
        self.proxy_model.setSourceModel(self.source_model)
        self.table_view.setModel(self.proxy_model)

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
                /* Add a visual hint for filter? */
            }
        """)

        layout.addWidget(self.table_view)

        # Info label
        self.info_label = QLabel("Visualizzazione completa. Clicca sulle intestazioni per filtrare.")
        self.info_label.setStyleSheet("color: #adb5bd; font-size: 11px; margin-top: 5px;")
        layout.addWidget(self.info_label)

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
            self._load_data() # Reload data
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

    def _load_data(self):
        """Carica TUTTI i dati in memoria (molto veloce in RAM)."""
        if not ContabilitaManager.DB_PATH.exists():
            return

        try:
            # Fetch ALL rows (tuples)
            rows = ContabilitaManager.get_scarico_ore_data()
            self.source_model.update_data(rows)

            # Reset view properties
            self.table_view.resizeColumnsToContents()

            # Default widths adjustments
            # 'DATA'(0), 'PERS1'(1), 'PERS2'(2), 'ODC'(3), 'POS'(4), 'DALLE'(5), 'ALLE'(6),
            # 'TOTALE ORE'(7), 'DESCRIZIONE'(8), 'FINITO'(9), 'COMMESSA'(10)

            self.table_view.setColumnWidth(0, 90) # Data
            self.table_view.setColumnWidth(1, 150) # Pers1
            self.table_view.setColumnWidth(2, 150) # Pers2
            self.table_view.setColumnWidth(8, 300) # Descrizione
            self.table_view.setColumnWidth(10, 150) # Commessa

            self.status_label.setText(f"Caricati {len(rows)} record.")

        except Exception as e:
            self.status_label.setText(f"Errore caricamento: {e}")
            print(f"DB Error: {e}")

    # Context Menu for Table View is slightly different than Table Widget
    # but the generic one in Widgets uses generic events.
    # If we need context menu (Lyra, Copy), we need to implement it for QTableView.
    # Currently user didn't explicitly demand context menu for this panel,
    # but "Scarico TS" usually has it.
    # The requirement focused on Filters and View All.
    # We'll skip complex context menu re-implementation for now unless requested.
    # Standard Copy (Ctrl+C) logic needs to be added to TableView if desired.

    def keyPressEvent(self, event):
        # Implement Ctrl+C for QTableView
        if event.matches(Qt.Key.Key_Copy):
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
            # We need to handle gaps if selection is disjoint?
            # Simple approach: join by tab
            line = "\t".join([x[1] for x in sorted(rows_text[r], key=lambda y: y[0])])
            tsv_lines.append(line)

        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText("\n".join(tsv_lines))
