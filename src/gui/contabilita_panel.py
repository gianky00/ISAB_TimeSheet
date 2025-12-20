"""
Bot TS - Contabilita Panel
Pannello per la visualizzazione della Contabilità Strumentale.
"""
import os
import re
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QMessageBox, QMenu, QTableWidget,
    QHeaderView, QTableWidgetItem, QLabel, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QAction

from src.core.contabilita_manager import ContabilitaManager
from src.core import config_manager
from src.gui.widgets import ExcelTableWidget, StatusIndicator


class ContabilitaWorker(QThread):
    """Worker per l'importazione in background."""
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def run(self):
        # Inizializza DB se necessario
        ContabilitaManager.init_db()
        success, msg = ContabilitaManager.import_data_from_excel(self.file_path)
        self.finished_signal.emit(success, msg)


class ContabilitaPanel(QWidget):
    """Pannello principale Contabilità Strumentale."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self._setup_ui()

        # Carica i dati iniziali
        self.refresh_tabs()

    def _setup_ui(self):
        """Configura l'interfaccia."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # Header / Status / Search
        top_layout = QHBoxLayout()

        self.status_label = QLabel("Pronto")
        self.status_label.setStyleSheet("color: #6c757d; font-size: 13px;")
        top_layout.addWidget(self.status_label)

        top_layout.addStretch()

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Cerca in questa tabella...")
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
        self.search_input.textChanged.connect(self._filter_current_tab)
        top_layout.addWidget(self.search_input)

        layout.addLayout(top_layout)

        # Tab Widget per gli anni
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
            }
            QTabBar::tab {
                background: #f1f3f5;
                border: 1px solid #dee2e6;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                color: #495057;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
                color: #0d6efd;
            }
        """)
        self.tabs.currentChanged.connect(self._on_tab_changed)
        layout.addWidget(self.tabs)

    def refresh_tabs(self):
        """Ricarica i tab in base agli anni nel DB."""
        # Salva l'anno corrente selezionato per ripristinarlo
        current_year = self.tabs.tabText(self.tabs.currentIndex())

        self.tabs.clear()

        years = ContabilitaManager.get_available_years()
        if not years:
            # Se non ci sono dati, mostra un tab placeholder o vuoto
            no_data = QLabel("Nessun dato disponibile. Configura il file nelle impostazioni e riavvia/aggiorna.")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabs.addTab(no_data, "Info")
            return

        for year in years:
            tab = ContabilitaYearTab(year)
            self.tabs.addTab(tab, str(year))

        # Ripristina selezione
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == current_year:
                self.tabs.setCurrentIndex(i)
                break

    def _on_tab_changed(self, index):
        """Chiamato quando cambia la tab."""
        # Riapplica il filtro corrente alla nuova tab
        self._filter_current_tab(self.search_input.text())

    def _filter_current_tab(self, text):
        """Filtra la tabella nella tab corrente."""
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, ContabilitaYearTab):
            current_widget.filter_data(text)

    def start_import_process(self):
        """Avvia il processo di importazione (chiamato dall'esterno o init)."""
        config = config_manager.load_config()
        path = config.get("contabilita_file_path", "")

        if not path or not os.path.exists(path):
            self.status_label.setText("⚠️ File contabilità non configurato o non trovato.")
            return

        self.status_label.setText("🔄 Aggiornamento contabilità in corso...")

        self.worker = ContabilitaWorker(path)
        self.worker.finished_signal.connect(self._on_import_finished)
        self.worker.start()

    def _on_import_finished(self, success: bool, msg: str):
        if success:
            self.status_label.setText(f"✅ Aggiornamento completato: {msg}")
            self.refresh_tabs()
        else:
            self.status_label.setText(f"❌ Errore aggiornamento: {msg}")

        self.worker = None


class ContabilitaYearTab(QWidget):
    """Tab per un singolo anno."""

    COLUMNS = [
        'DATA PREV.', 'MESE', 'N°PREV.', 'TOTALE PREV.', "ATTIVITA'",
        'TCL', 'ODC', "STATO ATTIVITA'", 'TIPOLOGIA', 'ORE SP', 'RESA', 'ANNOTAZIONI'
    ]

    # Indici colonne nascoste nei dati ritornati dal manager
    # I dati dal manager sono: [Visible Cols...] + [Indirizzo, NomeFile]
    IDX_INDIRIZZO = 12
    IDX_NOMEFILE = 13

    # Indici colonne per formattazione (basati su COLUMNS)
    COL_DATA = 0
    COL_TOTALE = 3
    COL_ORE = 9
    COL_RESA = 10

    def __init__(self, year: int, parent=None):
        super().__init__(parent)
        self.year = year
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        self.table = ExcelTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)

        header = self.table.horizontalHeader()

        # Imposta larghezze specifiche per migliorare la leggibilità
        # ResizeMode: Interactive allows user resizing, but we set initial sizes
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Pesi/Dimensioni ideali
        self.table.setColumnWidth(self.COL_DATA, 100)      # Data
        self.table.setColumnWidth(1, 100)                  # Mese
        self.table.setColumnWidth(2, 80)                   # N Prev
        self.table.setColumnWidth(self.COL_TOTALE, 120)    # Totale
        self.table.setColumnWidth(4, 300)                  # Attivita (Large)
        self.table.setColumnWidth(5, 150)                  # TCL
        self.table.setColumnWidth(6, 100)                  # ODC
        self.table.setColumnWidth(7, 150)                  # Stato
        self.table.setColumnWidth(8, 100)                  # Tipologia
        self.table.setColumnWidth(self.COL_ORE, 80)        # Ore
        self.table.setColumnWidth(self.COL_RESA, 80)       # Resa
        header.setSectionResizeMode(11, QHeaderView.ResizeMode.Stretch) # Annotazioni (Stretch)

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)

        layout.addWidget(self.table)

    def _load_data(self):
        data = ContabilitaManager.get_data_by_year(self.year)
        self.table.setRowCount(0)

        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)

            # Popola colonne visibili con formattazione
            for col_idx in range(len(self.COLUMNS)):
                val = row_data[col_idx]
                formatted_val = self._format_value(col_idx, val)

                item = QTableWidgetItem(formatted_val)
                # Allinea a destra i numeri
                if col_idx in [self.COL_TOTALE, self.COL_ORE, self.COL_RESA]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                self.table.setItem(row_idx, col_idx, item)

            # Salva dati nascosti (Indirizzo, Nome File) come UserData nel primo item della riga
            indirizzo = row_data[self.IDX_INDIRIZZO]
            self.table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, indirizzo)

    def _format_value(self, col_idx, val):
        """Applica la formattazione specifica per colonna."""
        if not val and val != 0:
            return ""

        str_val = str(val).strip()
        if not str_val:
            return ""

        # 1. DATA (GG/MM/AAAA)
        if col_idx == self.COL_DATA:
            try:
                # Prova diversi formati in ingresso
                # Excel spesso salva come YYYY-MM-DD HH:MM:SS
                dt = None
                if ' ' in str_val:
                    str_val = str_val.split(' ')[0]

                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
                    try:
                        dt = datetime.strptime(str_val, fmt)
                        break
                    except ValueError:
                        continue

                if dt:
                    return dt.strftime("%d/%m/%Y")
            except:
                pass # Return original if parse fails

        # 2. VALUTA (Totale Prev)
        elif col_idx == self.COL_TOTALE:
            try:
                f_val = float(str_val)
                # Formato: € 1.234,56
                return f"€ {f_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            except:
                pass

        # 3. NUMERI (Ore, Resa)
        elif col_idx in [self.COL_ORE, self.COL_RESA]:
            try:
                f_val = float(str_val)
                # Rimuovi decimali se intero
                if f_val.is_integer():
                    return f"{int(f_val)}"
                else:
                    # Max 2 decimali
                    return f"{f_val:.2f}"
            except:
                pass

        return str_val

    def filter_data(self, text):
        """Filtra le righe in base al testo."""
        rows = self.table.rowCount()
        cols = self.table.columnCount()

        search_terms = text.lower().split()

        for r in range(rows):
            if not text:
                self.table.setRowHidden(r, False)
                continue

            row_visible = False
            # Cerca in tutte le colonne
            for c in range(cols):
                item = self.table.item(r, c)
                if item and item.text():
                    cell_text = item.text().lower()
                    # Verifica se TUTTI i termini sono presenti nella riga (in qualsiasi cella)
                    # Qui facciamo un controllo più semplice: se ALMENO UNA cella contiene ALMENO UN termine?
                    # Solitamente search bar filtra se la riga matcha la query.
                    # Se ci sono più termini ("maggio 2024"), cerchiamo che la riga li contenga tutti?
                    # Facciamo match semplice: se la stringa di ricerca è contenuta nella riga (concatenata o check any cell)
                    if text.lower() in cell_text:
                         row_visible = True
                         break

            # Miglioramento: Ricerca multi-termine (AND) su tutta la riga
            if not row_visible:
                # Unisci tutto il testo della riga per cercare
                row_full_text = " ".join([self.table.item(r, c).text().lower() for c in range(cols) if self.table.item(r, c)])
                if all(term in row_full_text for term in search_terms):
                    row_visible = True

            self.table.setRowHidden(r, not row_visible)

    def _show_context_menu(self, pos):
        """Mostra menu contestuale."""
        item = self.table.itemAt(pos)
        if not item:
            return

        row = item.row()
        # Recupera il path dal primo item della riga
        first_item = self.table.item(row, 0)
        file_path = first_item.data(Qt.ItemDataRole.UserRole)

        menu = QMenu(self)

        action_open = QAction("📂 Apri File", self)

        if file_path:
             action_open.triggered.connect(lambda: self._open_file(file_path))
        else:
            action_open.setEnabled(False)
            action_open.setText("📂 Apri File (Percorso non disponibile)")

        menu.addAction(action_open)
        menu.exec(self.table.viewport().mapToGlobal(pos))

    def _open_file(self, path_str):
        """Apre il file con l'applicazione di default."""
        if not path_str:
            return

        try:
            os.startfile(path_str)
        except Exception as e:
            QMessageBox.warning(self, "Errore Apertura", f"Impossibile aprire il file:\n{path_str}\n\nErrore: {e}")
