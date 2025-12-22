"""
Bot TS - Contabilita Panel
Pannello per la visualizzazione della Contabilità Strumentale.
"""
import os
import re
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QMessageBox, QMenu, QTableWidget,
    QHeaderView, QTableWidgetItem, QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QAction, QFont
import time

from src.core.contabilita_manager import ContabilitaManager
from src.core import config_manager
from src.gui.widgets import ExcelTableWidget, StatusIndicator


class ContabilitaWorker(QThread):
    """Worker per l'importazione in background."""
    finished_signal = pyqtSignal(bool, str)
    progress_signal = pyqtSignal(str)

    def __init__(self, file_path: str, giornaliere_path: str = ""):
        super().__init__()
        self.file_path = file_path
        self.giornaliere_path = giornaliere_path
        self.start_time = 0

    def run(self):
        # Inizializza DB se necessario
        ContabilitaManager.init_db()

        self.progress_signal.emit("⏳ Analisi carico di lavoro...")

        # Scan workload for Global ETA
        sheets, files = ContabilitaManager.scan_workload(self.file_path, self.giornaliere_path)
        total_ops = sheets + files
        if total_ops == 0: total_ops = 1

        self.start_time = time.time()

        def global_progress(processed_in_phase, phase_offset, phase_name):
            current_total = phase_offset + processed_in_phase
            elapsed = time.time() - self.start_time

            if current_total > 0 and elapsed > 0:
                rate = current_total / elapsed
                remaining = total_ops - current_total
                eta_seconds = remaining / rate if rate > 0 else 0

                m, s = divmod(int(eta_seconds), 60)
                percent = int((current_total / total_ops) * 100)

                self.progress_signal.emit(f"⏳ {phase_name}: {percent}% - {current_total}/{total_ops} - ETA: {m}m {s}s")

        # 1. Import Contabilità (Dati)
        dati_cb = lambda c, t: global_progress(c, 0, "Contabilità")
        success, msg = ContabilitaManager.import_data_from_excel(self.file_path, progress_callback=dati_cb)

        # 2. Import Giornaliere (se configurato)
        msg_giornaliere = ""
        if success and self.giornaliere_path:
            giorn_cb = lambda c, t: global_progress(c, sheets, "Giornaliere")

            g_success, g_msg = ContabilitaManager.import_giornaliere(self.giornaliere_path, progress_callback=giorn_cb)
            msg_giornaliere = f" | Giornaliere: {g_msg}" if g_success else f" | Err Giornaliere: {g_msg}"

        # Nota: Scarico Ore Cantiere ora è gestito separatamente nel suo pannello dedicato.

        self.finished_signal.emit(success, msg + msg_giornaliere)


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

        # 1. Search Bar (Left)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Cerca in questa tabella...")
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
        self.search_input.textChanged.connect(self._filter_current_tab)
        top_layout.addWidget(self.search_input)

        top_layout.addStretch()

        # 2. Status Label (Center)
        self.status_label = QLabel("Pronto")
        self.status_label.setStyleSheet("color: #6c757d; font-size: 13px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.status_label)

        top_layout.addStretch()

        # 3. Refresh Button (Right)
        self.refresh_btn = QPushButton("🔄 Aggiorna")
        self.refresh_btn.setToolTip("Aggiorna solo Contabilità e Giornaliere")
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.setStyleSheet("""
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
        self.refresh_btn.clicked.connect(self.start_import_process)
        top_layout.addWidget(self.refresh_btn)

        layout.addLayout(top_layout)

        # Main Tab Container (Tabelle vs KPI)
        self.main_tabs = QTabWidget()
        self.main_tabs.currentChanged.connect(self._on_main_tab_changed) # Connect tab change
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
        self.year_tabs_widget.setStyleSheet(self._get_subtab_style())
        self.year_tabs_widget.currentChanged.connect(self._on_tab_changed)

        self.main_tabs.addTab(self.year_tabs_widget, "📂 Dati")

        # --- TAB 2: GIORNALIERE (Years) ---
        self.giornaliere_tabs_widget = QTabWidget()
        self.giornaliere_tabs_widget.setTabPosition(QTabWidget.TabPosition.South)
        self.giornaliere_tabs_widget.setStyleSheet(self._get_subtab_style())
        self.giornaliere_tabs_widget.currentChanged.connect(self._on_tab_changed)

        self.main_tabs.addTab(self.giornaliere_tabs_widget, "📂 Giornaliere")

        # --- TAB 3: KPI ---
        from src.gui.contabilita_kpi_panel import ContabilitaKPIPanel
        self.kpi_panel = ContabilitaKPIPanel()
        self.main_tabs.addTab(self.kpi_panel, "📊 Analisi KPI")

        layout.addWidget(self.main_tabs)

    def _get_subtab_style(self):
        return """
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
        """

    def _on_main_tab_changed(self, index):
        """Handle visibility of search bar based on main tab."""
        tab_text = self.main_tabs.tabText(index)
        if "Analisi KPI" in tab_text:
            self.search_input.hide()
        else:
            self.search_input.show()
            # Trigger filter update for the new active tab
            self._filter_current_tab(self.search_input.text())

    def refresh_tabs(self):
        """Ricarica i tab in base agli anni nel DB."""
        # Salva l'anno corrente selezionato per ripristinarlo
        current_year_dati = self.year_tabs_widget.tabText(self.year_tabs_widget.currentIndex())
        current_year_giorn = self.giornaliere_tabs_widget.tabText(self.giornaliere_tabs_widget.currentIndex())

        self.year_tabs_widget.clear()
        self.giornaliere_tabs_widget.clear()

        years = ContabilitaManager.get_available_years()
        if not years:
            no_data = QLabel("Nessun dato disponibile. Configura il file nelle impostazioni e riavvia/aggiorna.")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.year_tabs_widget.addTab(no_data, "Info")
            return

        # Popola tab Dati e Giornaliere
        for year in years:
            # Dati
            tab_dati = ContabilitaYearTab(year)
            self.year_tabs_widget.addTab(tab_dati, str(year))

            # Giornaliere
            tab_giorn = GiornaliereYearTab(year)
            self.giornaliere_tabs_widget.addTab(tab_giorn, str(year))

        # Ripristina selezione Dati
        for i in range(self.year_tabs_widget.count()):
            if self.year_tabs_widget.tabText(i) == current_year_dati:
                self.year_tabs_widget.setCurrentIndex(i)
                break

        # Ripristina selezione Giornaliere
        for i in range(self.giornaliere_tabs_widget.count()):
            if self.giornaliere_tabs_widget.tabText(i) == current_year_giorn:
                self.giornaliere_tabs_widget.setCurrentIndex(i)
                break

        # Aggiorna anche i dati KPI
        if hasattr(self, 'kpi_panel'):
            self.kpi_panel.refresh_years()

    def _on_tab_changed(self, index):
        """Chiamato quando cambia la tab ANNO (in uno dei sub-tabwidget)."""
        self._filter_current_tab(self.search_input.text())

    def _filter_current_tab(self, text):
        """Filtra la tabella nella tab corrente attiva."""
        # Trova quale sub-tabwidget è visibile
        current_main_idx = self.main_tabs.currentIndex()
        current_main_widget = self.main_tabs.widget(current_main_idx)

        target_widget = None

        if current_main_widget == self.year_tabs_widget:
            target_widget = self.year_tabs_widget.currentWidget()
        elif current_main_widget == self.giornaliere_tabs_widget:
            target_widget = self.giornaliere_tabs_widget.currentWidget()

        if target_widget and hasattr(target_widget, 'filter_data'):
            target_widget.filter_data(text)

    def start_import_process(self):
        """Avvia il processo di importazione (chiamato dall'esterno o init)."""
        config = config_manager.load_config()
        path = config.get("contabilita_file_path", "")
        giornaliere_path = config.get("giornaliere_path", "")

        if not path or not os.path.exists(path):
            self.status_label.setText("⚠️ File contabilità non configurato o non trovato.")
            return

        self.status_label.setText("🔄 Aggiornamento in corso (Contabilità, Giornaliere)...")
        self.refresh_btn.setDisabled(True) # Disable button during update

        self.worker = ContabilitaWorker(path, giornaliere_path)
        self.worker.finished_signal.connect(self._on_import_finished)
        self.worker.progress_signal.connect(self.status_label.setText)
        self.worker.start()

    def _on_import_finished(self, success: bool, msg: str):
        if success:
            self.status_label.setText(f"✅ Aggiornamento completato")
            self.refresh_tabs()
        else:
            self.status_label.setText(f"❌ Errore aggiornamento: {msg}")
            QMessageBox.warning(self, "Esito Importazione", msg) # Show details in popup if error

        self.worker = None
        self.refresh_btn.setDisabled(False) # Re-enable button


class ContabilitaYearTab(QWidget):
    """Tab per un singolo anno (Tabella Dati)."""

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
        self.table.setWordWrap(True)  # Enable word wrap for multiline text

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
        data = ContabilitaManager.get_data_by_year(self.year)
        
        self.table.setSortingEnabled(False)
        self.table.blockSignals(True)
        
        try:
            self.table.setRowCount(len(data))
            
            align_right_flags = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            right_aligned_cols = {self.COL_TOTALE, self.COL_ORE, self.COL_RESA}
            columns_count = len(self.COLUMNS)

            for row_idx, row_data in enumerate(data):
                for col_idx in range(columns_count):
                    val = row_data[col_idx]
                    formatted_val = self._format_value(col_idx, val)

                    item = QTableWidgetItem(formatted_val)
                    if col_idx in right_aligned_cols:
                        item.setTextAlignment(align_right_flags)

                    self.table.setItem(row_idx, col_idx, item)

                indirizzo = row_data[self.IDX_INDIRIZZO]
                if self.table.item(row_idx, 0):
                    self.table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, indirizzo)

            self.table.resizeRowsToContents()  # Ensure full content is visible

            self._add_totals_row()
            self._update_totals()

        finally:
            self.table.blockSignals(False)
            self.table.setSortingEnabled(True)

    def _add_totals_row(self):
        if self.table.rowCount() > 0:
            last_item = self.table.item(self.table.rowCount() - 1, 0)
            if last_item and last_item.text() == "TOTALI":
                return

        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)

        item = QTableWidgetItem("TOTALI")
        item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        item.setBackground(Qt.GlobalColor.lightGray)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_idx, 0, item)

        for c in range(1, self.table.columnCount()):
            item = QTableWidgetItem("")
            item.setBackground(Qt.GlobalColor.lightGray)
            item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            if c in [self.COL_TOTALE, self.COL_ORE, self.COL_RESA, self.COL_N_PREV]:
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            self.table.setItem(row_idx, c, item)

    def _update_totals(self):
        total_row_idx = -1
        if self.table.rowCount() > 0:
            last_item = self.table.item(self.table.rowCount() - 1, 0)
            if last_item and last_item.text() == "TOTALI":
                total_row_idx = self.table.rowCount() - 1

        if total_row_idx == -1: return

        rows = total_row_idx
        count_prev = 0
        sum_totale_prev = 0.0
        sum_ore_sp = 0.0
        sum_resa = 0.0
        count_resa = 0

        for r in range(rows):
            if not self.table.isRowHidden(r):
                count_prev += 1
                is_excluded = False
                r_item = self.table.item(r, self.COL_RESA)
                if r_item:
                    resa_text = r_item.text().strip()
                    if "INS.ORE SP" in resa_text.upper():
                        is_excluded = True

                if not is_excluded:
                    t_item = self.table.item(r, self.COL_TOTALE)
                    if t_item:
                        sum_totale_prev += self._parse_currency(t_item.text())

                o_item = self.table.item(r, self.COL_ORE)
                if o_item:
                    sum_ore_sp += self._parse_float(o_item.text())

                if not is_excluded and r_item:
                    val = self._parse_float(r_item.text())
                    if val != 0 or r_item.text().strip() != "":
                        sum_resa += val
                        count_resa += 1

        self.table.item(total_row_idx, self.COL_N_PREV).setText(str(count_prev))
        self.table.item(total_row_idx, self.COL_TOTALE).setText(self._format_currency(sum_totale_prev))
        self.table.item(total_row_idx, self.COL_ORE).setText(self._format_number(sum_ore_sp))
        avg_resa = sum_resa / count_resa if count_resa > 0 else 0.0
        self.table.item(total_row_idx, self.COL_RESA).setText(self._format_number(avg_resa))

    def _parse_currency(self, text):
        try:
            clean = text.replace("€", "").replace(".", "").replace(",", ".").strip()
            return float(clean)
        except: return 0.0

    def _parse_float(self, text):
        try: return float(text)
        except: return 0.0

    def _format_currency(self, val):
        return f"€ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _format_number(self, val):
        if val.is_integer(): return f"{int(val)}"
        else: return f"{val:.2f}"

    def _format_value(self, col_idx, val):
        if not val and val != 0: return ""
        str_val = str(val).strip()
        if not str_val: return ""

        if col_idx == self.COL_DATA:
            try:
                dt = None
                if ' ' in str_val: str_val = str_val.split(' ')[0]
                try: dt = datetime.strptime(str_val, "%Y-%m-%d")
                except ValueError:
                    for fmt in ("%d/%m/%Y", "%Y/%m/%d"):
                        try: dt = datetime.strptime(str_val, fmt); break
                        except ValueError: continue
                if dt: return dt.strftime("%d/%m/%Y")
            except: pass
        elif col_idx == self.COL_TOTALE:
            try: return self._format_currency(float(str_val))
            except: pass
        elif col_idx in [self.COL_ORE, self.COL_RESA]:
            try: return self._format_number(float(str_val))
            except: pass
        elif col_idx == self.COL_ODC:
            return str_val.replace("-", "/")

        return str_val

    def filter_data(self, text):
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

        if data_rows < total_rows:
            self.table.setRowHidden(data_rows, False)
        self._update_totals()

    def _show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if not item: return
        if item.text() == "TOTALI" or (self.table.item(item.row(), 0).text() == "TOTALI"): return

        row = item.row()
        first_item = self.table.item(row, 0)
        file_path = first_item.data(Qt.ItemDataRole.UserRole)

        menu = QMenu(self)

        # Lyra Action
        lyra_action = QAction("✨ Analizza Riga con Lyra", self)
        lyra_action.triggered.connect(lambda: self.table._analyze_row_at(pos))
        menu.addAction(lyra_action)

        menu.addSeparator()

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


class GiornaliereYearTab(QWidget):
    """Tab per un singolo anno (Giornaliere)."""

    # data, personale, tcl, descrizione, n_prev, odc, pdl, inizio, fine, ore
    COLUMNS = [
        'DATA', 'PERSONALE', 'TCL', 'DESCRIZIONE ATTIVITA', 'N°PREV.', 'ODC',
        'PDL', 'INIZIO', 'FINE', 'ORE'
    ]

    # Mappatura indici basata sulla query get_giornaliere_by_year
    # Query: data, personale, tcl, descrizione, n_prev, odc, pdl, inizio, fine, ore, nome_file

    COL_DATA = 0
    COL_ORE = 9
    IDX_NOMEFILE = 10

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
        self.table.setWordWrap(True) # Abilita testo a capo

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Dimensioni
        self.table.setColumnWidth(0, 100)  # Data
        self.table.setColumnWidth(1, 200)  # Personale
        self.table.setColumnWidth(2, 100)  # TCL (added)
        self.table.setColumnWidth(3, 300)  # Descrizione
        self.table.setColumnWidth(4, 80)   # N Prev
        self.table.setColumnWidth(5, 120)  # ODC
        self.table.setColumnWidth(6, 80)   # PDL
        self.table.setColumnWidth(7, 80)   # Inizio
        self.table.setColumnWidth(8, 80)   # Fine
        self.table.setColumnWidth(9, 80)   # Ore

        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # Descrizione elastica

        # Context Menu
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)

        layout.addWidget(self.table)

    def _load_data(self):
        data = ContabilitaManager.get_giornaliere_by_year(self.year)

        self.table.setSortingEnabled(False)
        self.table.blockSignals(True)

        try:
            self.table.setRowCount(len(data))
            align_right_flags = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

            # Ore a destra
            right_cols = {self.COL_ORE}

            for row_idx, row_data in enumerate(data):
                # row_data includes all columns + nome_file
                for col_idx in range(len(self.COLUMNS)):
                    val = row_data[col_idx]
                    formatted_val = self._format_value(col_idx, val)

                    item = QTableWidgetItem(formatted_val)
                    if col_idx in right_cols:
                        item.setTextAlignment(align_right_flags)

                    self.table.setItem(row_idx, col_idx, item)

                # Store filename in first column's user data
                if len(row_data) > self.IDX_NOMEFILE:
                    filename = row_data[self.IDX_NOMEFILE]
                    if self.table.item(row_idx, 0):
                        self.table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, filename)

            # Resize per contenuto multiriga
            self.table.resizeRowsToContents()

            # Totali
            self._add_totals_row()
            self._update_totals()

        finally:
            self.table.blockSignals(False)
            self.table.setSortingEnabled(True)

    def _add_totals_row(self):
        """Aggiunge la riga dei totali in fondo."""
        if self.table.rowCount() > 0:
            last_item = self.table.item(self.table.rowCount() - 1, 0)
            if last_item and last_item.text() == "TOTALI":
                return

        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)

        item = QTableWidgetItem("TOTALI")
        item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        item.setBackground(Qt.GlobalColor.lightGray)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_idx, 0, item)

        for c in range(1, self.table.columnCount()):
            item = QTableWidgetItem("")
            item.setBackground(Qt.GlobalColor.lightGray)
            item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            if c == self.COL_ORE:
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            self.table.setItem(row_idx, c, item)

    def _update_totals(self):
        """Ricalcola totali sulle righe visibili."""
        total_row_idx = -1
        if self.table.rowCount() > 0:
            last_item = self.table.item(self.table.rowCount() - 1, 0)
            if last_item and last_item.text() == "TOTALI":
                total_row_idx = self.table.rowCount() - 1

        if total_row_idx == -1: return

        rows = total_row_idx
        sum_ore = 0.0

        for r in range(rows):
            if not self.table.isRowHidden(r):
                item = self.table.item(r, self.COL_ORE)
                if item:
                    # Parse localizing the comma back to dot for float calc
                    text_val = item.text().replace(',', '.')
                    sum_ore += self._parse_float(text_val)

        # Format total with the same helper
        self.table.item(total_row_idx, self.COL_ORE).setText(self._format_number(sum_ore))

    def _parse_float(self, text):
        try: return float(text)
        except: return 0.0

    def _format_number(self, val):
        """Formatta ORE: max 2 decimali, virgola, niente .0 finale."""
        try:
            val_f = float(val)
            val_f = round(val_f, 2)
            if val_f.is_integer():
                return f"{int(val_f)}"
            else:
                return f"{val_f}".replace('.', ',')
        except:
            return str(val)

    def _format_value(self, col_idx, val):
        if not val: return ""
        str_val = str(val).strip()
        if str_val.lower() == 'nan': return ""

        # Data
        if col_idx == self.COL_DATA:
            try:
                dt = None
                if ' ' in str_val: str_val = str_val.split(' ')[0]
                try: dt = datetime.strptime(str_val, "%Y-%m-%d")
                except ValueError:
                    for fmt in ("%d/%m/%Y", "%Y/%m/%d"):
                        try: dt = datetime.strptime(str_val, fmt); break
                        except ValueError: continue
                if dt: return dt.strftime("%d/%m/%Y")
            except: pass

        # Ore formatting
        if col_idx == self.COL_ORE:
            return self._format_number(val)

        return str_val

    def filter_data(self, text):
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

        if data_rows < total_rows:
            self.table.setRowHidden(data_rows, False)
        self._update_totals()

    def _show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if not item: return
        if item.text() == "TOTALI" or (self.table.item(item.row(), 0).text() == "TOTALI"): return

        row = item.row()
        first_item = self.table.item(row, 0)
        filename = first_item.data(Qt.ItemDataRole.UserRole)

        menu = QMenu(self)

        # Lyra Action
        lyra_action = QAction("✨ Analizza Riga con Lyra", self)
        lyra_action.triggered.connect(lambda: self.table._analyze_row_at(pos))
        menu.addAction(lyra_action)

        menu.addSeparator()

        if filename:
             action_open = QAction(f"📂 Apri {filename}", self)
             action_open.triggered.connect(lambda: self._open_giornaliera(filename))
             menu.addAction(action_open)
        else:
            action_dummy = QAction("Nessun file associato", self)
            action_dummy.setEnabled(False)
            menu.addAction(action_dummy)

        menu.exec(self.table.viewport().mapToGlobal(pos))

    def _open_giornaliera(self, filename):
        """Tenta di aprire la giornaliera cercando nella root configurata."""
        config = config_manager.load_config()
        root_path = config.get("giornaliere_path", "")
        if not root_path:
            QMessageBox.warning(self, "Attenzione", "Cartella Giornaliere non configurata o non trovata.")
            return

        # Normalize the root path to handle mixed slashes
        root_path = os.path.normpath(root_path)

        # Ricerca ricorsiva del file
        # Ottimizzazione: Cerca in "Giornaliere YYYY"
        found_path = None

        # Cerca prima nella cartella dell'anno specifico
        year_folder = os.path.join(root_path, f"Giornaliere {self.year}")
        if os.path.exists(year_folder):
             potential_path = os.path.join(year_folder, filename)
             if os.path.exists(potential_path):
                 found_path = potential_path

        # Se non trovato, cerca ovunque
        if not found_path:
            for root, dirs, files in os.walk(root_path):
                if filename in files:
                    found_path = os.path.join(root, filename)
                    break

        if found_path:
            # Ensure final path is strictly Windows-compliant for os.startfile
            found_path = os.path.normpath(found_path)
            try:
                os.startfile(found_path)
            except Exception as e:
                QMessageBox.warning(self, "Errore", f"Impossibile aprire il file: {e}\nPath: {found_path}")
        else:
            QMessageBox.warning(self, "File non trovato", f"Non riesco a trovare '{filename}' nella cartella giornaliere.")
