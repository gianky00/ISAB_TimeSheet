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
from PyQt6.QtGui import QAction, QFont

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

        # Main Tab Container (Tabelle vs KPI)
        self.main_tabs = QTabWidget()
        self.main_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
            }
            QTabBar::tab {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                color: #495057;
                font-weight: bold;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
                color: #0d6efd;
            }
        """)

        # --- TAB 1: DATI (Years) ---
        self.year_tabs_widget = QTabWidget()
        self.year_tabs_widget.setTabPosition(QTabWidget.TabPosition.South) # Tabs at bottom for years
        self.year_tabs_widget.setStyleSheet("""
            QTabWidget::pane { border: none; }
            QTabBar::tab {
                background: #f1f3f5;
                padding: 6px 15px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background: #0d6efd;
                color: white;
            }
        """)
        self.year_tabs_widget.currentChanged.connect(self._on_tab_changed)

        self.main_tabs.addTab(self.year_tabs_widget, "📂 Dati & Tabelle")

        # --- TAB 2: KPI ---
        from src.gui.contabilita_kpi_panel import ContabilitaKPIPanel
        self.kpi_panel = ContabilitaKPIPanel()
        self.main_tabs.addTab(self.kpi_panel, "📊 Analisi KPI")

        layout.addWidget(self.main_tabs)

    def refresh_tabs(self):
        """Ricarica i tab in base agli anni nel DB."""
        # Salva l'anno corrente selezionato per ripristinarlo
        current_year = self.year_tabs_widget.tabText(self.year_tabs_widget.currentIndex())

        self.year_tabs_widget.clear()

        years = ContabilitaManager.get_available_years()
        if not years:
            no_data = QLabel("Nessun dato disponibile. Configura il file nelle impostazioni e riavvia/aggiorna.")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.year_tabs_widget.addTab(no_data, "Info")
            return

        for year in years:
            tab = ContabilitaYearTab(year)
            self.year_tabs_widget.addTab(tab, str(year))

        # Ripristina selezione
        for i in range(self.year_tabs_widget.count()):
            if self.year_tabs_widget.tabText(i) == current_year:
                self.year_tabs_widget.setCurrentIndex(i)
                break

        # Aggiorna anche i dati KPI se necessario (passando gli anni disponibili)
        if hasattr(self, 'kpi_panel'):
            self.kpi_panel.refresh_years()

    def _on_tab_changed(self, index):
        """Chiamato quando cambia la tab ANNO."""
        # Riapplica il filtro corrente alla nuova tab
        self._filter_current_tab(self.search_input.text())

    def _filter_current_tab(self, text):
        """Filtra la tabella nella tab corrente."""
        current_widget = self.year_tabs_widget.currentWidget()
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
    COL_N_PREV = 2 # Per totali
    COL_TOTALE = 3
    COL_ODC = 6
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
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Pesi/Dimensioni ideali
        self.table.setColumnWidth(self.COL_DATA, 100)      # Data
        self.table.setColumnWidth(1, 100)                  # Mese
        self.table.setColumnWidth(2, 80)                   # N Prev
        self.table.setColumnWidth(self.COL_TOTALE, 120)    # Totale
        self.table.setColumnWidth(4, 300)                  # Attivita (Large)
        self.table.setColumnWidth(5, 150)                  # TCL
        self.table.setColumnWidth(6, 120)                  # ODC
        self.table.setColumnWidth(7, 150)                  # Stato
        self.table.setColumnWidth(8, 100)                  # Tipologia
        self.table.setColumnWidth(self.COL_ORE, 80)        # Ore
        self.table.setColumnWidth(self.COL_RESA, 80)       # Resa
        header.setSectionResizeMode(11, QHeaderView.ResizeMode.Stretch) # Annotazioni

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)

        layout.addWidget(self.table)

    def _load_data(self):
        # Resetta completamente la tabella prima di popolare
        self.table.setRowCount(0)

        data = ContabilitaManager.get_data_by_year(self.year)

        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)

            # Popola colonne visibili
            for col_idx in range(len(self.COLUMNS)):
                val = row_data[col_idx]
                formatted_val = self._format_value(col_idx, val)

                item = QTableWidgetItem(formatted_val)
                # Allinea a destra i numeri
                if col_idx in [self.COL_TOTALE, self.COL_ORE, self.COL_RESA]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                self.table.setItem(row_idx, col_idx, item)

            # Salva dati nascosti (Indirizzo)
            indirizzo = row_data[self.IDX_INDIRIZZO]
            self.table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, indirizzo)

        # Aggiungi riga totali (Inizialmente vuota/calcolata su tutto)
        self._add_totals_row()
        self._update_totals()

    def _add_totals_row(self):
        """Aggiunge la riga dei totali in fondo."""
        # Se l'ultima riga è già TOTALI, non aggiungerne un'altra
        if self.table.rowCount() > 0:
            last_item = self.table.item(self.table.rowCount() - 1, 0)
            if last_item and last_item.text() == "TOTALI":
                return

        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)

        # Label "TOTALI"
        item = QTableWidgetItem("TOTALI")
        item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        item.setBackground(Qt.GlobalColor.lightGray)
        # Disabilita selezione e modifica per la label (opzionale, ma meglio lasciare select per copia)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_idx, 0, item)

        # Applica stile background grigio a tutta la riga totali
        for c in range(1, self.table.columnCount()):
            item = QTableWidgetItem("")
            item.setBackground(Qt.GlobalColor.lightGray)
            item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            # Allineamento numeri
            if c in [self.COL_TOTALE, self.COL_ORE, self.COL_RESA, self.COL_N_PREV]:
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            self.table.setItem(row_idx, c, item)

    def _update_totals(self):
        """Ricalcola e aggiorna la riga dei totali in base alle righe VISIBILI."""
        # Trova la riga totali
        total_row_idx = -1
        if self.table.rowCount() > 0:
            last_item = self.table.item(self.table.rowCount() - 1, 0)
            if last_item and last_item.text() == "TOTALI":
                total_row_idx = self.table.rowCount() - 1

        if total_row_idx == -1:
            return

        # Itera su tutte le righe tranne quella dei totali
        rows = total_row_idx

        count_prev = 0
        sum_totale_prev = 0.0
        sum_ore_sp = 0.0
        sum_resa = 0.0
        count_resa = 0 # Per media

        for r in range(rows):
            if not self.table.isRowHidden(r):
                count_prev += 1

                # Totale Prev
                t_item = self.table.item(r, self.COL_TOTALE)
                if t_item:
                    val = self._parse_currency(t_item.text())
                    sum_totale_prev += val

                # Ore Sp
                o_item = self.table.item(r, self.COL_ORE)
                if o_item:
                    val = self._parse_float(o_item.text())
                    sum_ore_sp += val

                # Resa
                r_item = self.table.item(r, self.COL_RESA)
                if r_item:
                    val = self._parse_float(r_item.text())
                    # Se vuoto o zero non contare? Assumiamo media aritmetica dei valori presenti
                    if val != 0 or r_item.text().strip() != "":
                        sum_resa += val
                        count_resa += 1

        # Aggiorna riga totali

        # N Prev (Conteggio)
        self.table.item(total_row_idx, self.COL_N_PREV).setText(str(count_prev))

        # Totale Prev (Somma)
        self.table.item(total_row_idx, self.COL_TOTALE).setText(self._format_currency(sum_totale_prev))

        # Ore SP (Somma)
        self.table.item(total_row_idx, self.COL_ORE).setText(self._format_number(sum_ore_sp))

        # Resa (Media)
        avg_resa = sum_resa / count_resa if count_resa > 0 else 0.0
        self.table.item(total_row_idx, self.COL_RESA).setText(self._format_number(avg_resa))

    def _parse_currency(self, text):
        """Converte stringa valuta (€ 1.000,00) in float."""
        try:
            clean = text.replace("€", "").replace(".", "").replace(",", ".").strip()
            return float(clean)
        except:
            return 0.0

    def _parse_float(self, text):
        """Converte stringa numero in float."""
        try:
            return float(text)
        except:
            return 0.0

    def _format_currency(self, val):
        return f"€ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _format_number(self, val):
        if val.is_integer():
            return f"{int(val)}"
        else:
            return f"{val:.2f}"

    def _format_value(self, col_idx, val):
        """Applica la formattazione specifica per colonna."""
        if not val and val != 0:
            return ""

        str_val = str(val).strip()
        if not str_val:
            return ""

        # 1. DATA
        if col_idx == self.COL_DATA:
            try:
                dt = None
                if ' ' in str_val: str_val = str_val.split(' ')[0]
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
                    try: dt = datetime.strptime(str_val, fmt); break
                    except ValueError: continue
                if dt: return dt.strftime("%d/%m/%Y")
            except: pass

        # 2. VALUTA
        elif col_idx == self.COL_TOTALE:
            try: return self._format_currency(float(str_val))
            except: pass

        # 3. NUMERI
        elif col_idx in [self.COL_ORE, self.COL_RESA]:
            try: return self._format_number(float(str_val))
            except: pass

        # 4. ODC (Replace - with /)
        elif col_idx == self.COL_ODC:
            return str_val.replace("-", "/")

        return str_val

    def filter_data(self, text):
        """Filtra le righe in base al testo e aggiorna totali."""
        # Determina quante righe di dati ci sono (esclusa totali)
        total_rows = self.table.rowCount()
        data_rows = total_rows

        if total_rows > 0:
            last_item = self.table.item(total_rows - 1, 0)
            if last_item and last_item.text() == "TOTALI":
                data_rows = total_rows - 1

        search_terms = text.lower().split()
        cols = self.table.columnCount()

        for r in range(data_rows):
            if not text:
                self.table.setRowHidden(r, False)
                continue

            row_visible = False
            for c in range(cols):
                item = self.table.item(r, c)
                if item and item.text():
                    if text.lower() in item.text().lower():
                         row_visible = True
                         break

            if not row_visible:
                row_full_text = " ".join([self.table.item(r, c).text().lower() for c in range(cols) if self.table.item(r, c)])
                if all(term in row_full_text for term in search_terms):
                    row_visible = True

            self.table.setRowHidden(r, not row_visible)

        # Assicura che la riga totali sia sempre visibile
        if data_rows < total_rows:
            self.table.setRowHidden(data_rows, False)

        # Ricalcola totali sulle righe visibili
        self._update_totals()

    def _show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if not item: return

        # Non mostrare menu sulla riga totali (ultima riga se presente)
        if item.text() == "TOTALI" or (self.table.item(item.row(), 0).text() == "TOTALI"):
            return

        row = item.row()
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
        if not path_str: return
        try: os.startfile(path_str)
        except Exception as e:
            QMessageBox.warning(self, "Errore Apertura", f"Impossibile aprire il file:\n{path_str}\n\nErrore: {e}")
