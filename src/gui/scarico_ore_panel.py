"""
Bot TS - Scarico Ore Panel
Pannello dedicato per lo Scarico Ore Cantiere.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidgetItem, QHeaderView, QMenu, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QFont, QCursor

from src.gui.widgets import ExcelTableWidget, StatusIndicator
from src.core.contabilita_manager import ContabilitaManager
from src.core import config_manager
from datetime import datetime
from src.utils.parsing import parse_currency

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

    COLUMNS = [
        'DATA', 'PERS1', 'PERS2', 'ODC', 'POS', 'DALLE', 'ALLE',
        'TOTALE ORE', 'DESCRIZIONE', 'FINITO', 'COMMESSA'
    ]

    # Mappatura indici colonne (0-based)
    COL_DATA = 0
    COL_ODC = 3
    COL_POS = 4
    COL_DALLE = 5
    COL_ALLE = 6
    COL_TOTALE_ORE = 7
    COL_DESCRIZIONE = 8

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self._setup_ui()
        # Initial load limited for speed
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # --- Toolbar ---
        toolbar = QHBoxLayout()

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Cerca (es. ODC, Commessa, Data)...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setFixedWidth(300)
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
        # Usa returnPressed per evitare freeze durante digitazione veloce su 130k righe
        # O un timer. Per ora usiamo returnPressed per SQL search.
        self.search_input.returnPressed.connect(self._perform_search)
        # Aggiungi bottone cerca per chiarezza
        search_btn = QPushButton("Cerca")
        search_btn.clicked.connect(self._perform_search)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        toolbar.addWidget(self.search_input)
        toolbar.addWidget(search_btn)

        toolbar.addStretch()

        # Status Label
        self.status_label = QLabel("Pronto")
        self.status_label.setStyleSheet("color: #6c757d; font-size: 13px;")
        toolbar.addWidget(self.status_label)

        toolbar.addStretch()

        # Update Button
        self.update_btn = QPushButton("🔄 Aggiorna")
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

        # --- Table ---
        self.table = ExcelTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.setWordWrap(True) # Multiline support

        # Stile tabella
        self.table.setStyleSheet("""
            QTableWidget {
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

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(self.COL_DESCRIZIONE, QHeaderView.ResizeMode.Stretch) # Descrizione elastica

        # Default widths
        self.table.setColumnWidth(self.COL_DATA, 100)
        self.table.setColumnWidth(1, 150) # PERS1
        self.table.setColumnWidth(2, 150) # PERS2
        self.table.setColumnWidth(self.COL_ODC, 100)
        self.table.setColumnWidth(self.COL_POS, 60)
        self.table.setColumnWidth(self.COL_DALLE, 60)
        self.table.setColumnWidth(self.COL_ALLE, 60)
        self.table.setColumnWidth(self.COL_TOTALE_ORE, 100)

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)

        layout.addWidget(self.table)

        # Info label for limited view
        self.info_label = QLabel("Visualizzazione limitata alle prime 500 righe. Usa la ricerca per trovare dati specifici.")
        self.info_label.setStyleSheet("color: #adb5bd; font-size: 11px; margin-top: 5px;")
        layout.addWidget(self.info_label)

    def _start_update(self):
        """Avvia l'aggiornamento specifico per Scarico Ore."""
        config = config_manager.load_config()
        path = config.get("dataease_path", "") # Usa la chiave per Scarico Ore

        if not path:
            QMessageBox.warning(self, "Configurazione Mancante", "Configura il percorso 'File Scarico Ore' nelle Impostazioni.")
            return

        self.status_label.setText("⏳ Aggiornamento in corso...")
        self.update_btn.setEnabled(False)
        self.table.setEnabled(False)

        self.worker = ScaricoOreWorker(path)
        self.worker.finished_signal.connect(self._on_update_finished)
        self.worker.start()

    def _on_update_finished(self, success: bool, msg: str):
        self.update_btn.setEnabled(True)
        self.table.setEnabled(True)

        if success:
            self.status_label.setText("✅ Aggiornato")
            self._load_data() # Reload data
            QMessageBox.information(self, "Successo", msg)
        else:
            self.status_label.setText("❌ Errore")
            QMessageBox.critical(self, "Errore Aggiornamento", msg)

    def _perform_search(self):
        """Esegue la ricerca tramite query SQL per velocità."""
        text = self.search_input.text().strip()
        self._load_data(filter_text=text)

    def _load_data(self, filter_text: str = ""):
        """Carica i dati dal DB con limite e filtro opzionale."""
        # Usa il manager per ottenere i dati (ma dobbiamo aggiungere supporto filtro/limit al manager o farlo qui)
        # Per performance su 130k righe, meglio farlo in SQL.
        # Estendiamo la logica qui accedendo al DB direttamente o aggiungendo metodo al manager.
        # Per pulizia, meglio aggiungere metodo al manager. Ma per rapidità (piano step 5), facciamo una query diretta qui o chiamiamo un nuovo metodo manager.
        # Creiamo un metodo ad-hoc nel manager è meglio. Ma ContabilitaManager è in `src/core`.
        # Per ora userò `ContabilitaManager.get_scarico_ore_data` che ritorna TUTTO, il che è male.
        # Modifichiamo il Manager per supportare limit e search.

        # Tuttavia, per ora simuliamo accesso diretto ottimizzato o limitato.
        # Se chiamo get_scarico_ore_data() scarica 130k righe in RAM (ok per python) ma poi inserirle in QTable è lento.
        # Quindi slice in Python prima di UI update.

        import sqlite3
        from src.core.contabilita_manager import ContabilitaManager

        if not ContabilitaManager.DB_PATH.exists():
            return

        try:
            conn = sqlite3.connect(ContabilitaManager.DB_PATH)
            cursor = conn.cursor()

            cols = ['data', 'pers1', 'pers2', 'odc', 'pos', 'dalle', 'alle', 'totale_ore', 'descrizione', 'finito', 'commessa']
            query = f"SELECT {', '.join(cols)} FROM scarico_ore"
            params = []

            if filter_text:
                # Basic search on multiple columns
                conditions = []
                # Cerca su Data, Pers1, ODC, Descrizione, Commessa
                for col in ['data', 'pers1', 'odc', 'descrizione', 'commessa']:
                    conditions.append(f"{col} LIKE ?")
                    params.append(f"%{filter_text}%")
                query += " WHERE " + " OR ".join(conditions)

            query += " ORDER BY id DESC LIMIT 500" # Hard limit for UI performance

            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()

            self._update_table(rows)

            if filter_text and len(rows) == 0:
                self.status_label.setText("Nessun risultato trovato.")
            elif filter_text:
                self.status_label.setText(f"Trovati {len(rows)} risultati (limitati a 500).")
            else:
                self.status_label.setText("Pronto (Ultimi 500 record).")

        except Exception as e:
            self.status_label.setText(f"Errore caricamento: {e}")
            print(f"DB Error: {e}")

    def _update_table(self, rows):
        """Aggiorna la UI con i dati raw dal DB."""
        self.table.setSortingEnabled(False)
        self.table.blockSignals(True)
        self.table.setRowCount(0) # Clear

        align_right = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        align_center = Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter

        # Setup row count
        self.table.setRowCount(len(rows))

        # Colonne numeriche da formattare e allineare
        numeric_cols = [self.COL_ODC, self.COL_POS, self.COL_DALLE, self.COL_ALLE, self.COL_TOTALE_ORE]

        total_ore_sum = 0.0

        for r, row_data in enumerate(rows):
            # row_data: tuple of strings
            for c, val in enumerate(row_data):
                str_val = str(val) if val is not None else ""

                # Formatting
                if c == self.COL_DATA:
                    # Input YYYY-MM-DD -> DD/MM/YYYY
                    if '-' in str_val:
                        try:
                            dt = datetime.strptime(str_val.split()[0], "%Y-%m-%d")
                            str_val = dt.strftime("%d/%m/%Y")
                        except: pass

                elif c in numeric_cols:
                    # Int/Float formatting
                    try:
                        f_val = parse_currency(str_val)
                        if c == self.COL_TOTALE_ORE:
                            total_ore_sum += f_val

                        # "Se interi senza decimale, altrimenti max 2"
                        if f_val.is_integer():
                            str_val = str(int(f_val))
                        else:
                            str_val = f"{f_val:.2f}".replace('.', ',')
                    except:
                        pass

                item = QTableWidgetItem(str_val)

                # Alignment
                if c in numeric_cols:
                    item.setTextAlignment(align_right)
                elif c == self.COL_DATA:
                    item.setTextAlignment(align_center)

                self.table.setItem(r, c, item)

        self.table.resizeRowsToContents()
        self.table.blockSignals(False)
        self.table.setSortingEnabled(True)

        # Add Footer Total Row
        self._add_total_row(total_ore_sum)

    def _add_total_row(self, total_ore):
        row = self.table.rowCount()
        self.table.insertRow(row)

        lbl_item = QTableWidgetItem("TOTALI (Visibili)")
        lbl_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        lbl_item.setBackground(Qt.GlobalColor.lightGray)
        lbl_item.setFlags(Qt.ItemFlag.NoItemFlags)
        self.table.setItem(row, 0, lbl_item)

        # Fill grey
        for c in range(1, self.table.columnCount()):
            item = QTableWidgetItem("")
            item.setBackground(Qt.GlobalColor.lightGray)
            item.setFlags(Qt.ItemFlag.NoItemFlags)

            if c == self.COL_TOTALE_ORE:
                # Format total
                val_str = f"{total_ore:.2f}".replace('.', ',')
                if total_ore.is_integer():
                    val_str = str(int(total_ore))

                item.setText(val_str)
                item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            self.table.setItem(row, c, item)

    def _show_context_menu(self, pos):
        self.table.contextMenuEvent(type('DummyEvent', (object,), {'globalPos': lambda: self.table.viewport().mapToGlobal(pos), 'pos': lambda: pos})())
