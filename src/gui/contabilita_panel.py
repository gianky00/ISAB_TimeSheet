"""
Bot TS - Contabilita Panel
Pannello per la visualizzazione della Contabilità Strumentale.
"""
import os
import re
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QMessageBox, QMenu, QTableWidget,
    QHeaderView, QTableWidgetItem, QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QAbstractItemView
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QAction, QFont
import time

from src.core.contabilita_manager import ContabilitaManager
from src.core import config_manager
from src.gui.widgets import ExcelTableWidget, StatusIndicator


class ContabilitaWorker(QThread):
    """Worker per l'importazione in background."""
    finished_signal = pyqtSignal(bool, str, int, int)
    progress_signal = pyqtSignal(str)

    def __init__(self, file_path: str, giornaliere_path: str = "", attivita_path: str = ""):
        super().__init__()
        self.file_path = file_path
        self.giornaliere_path = giornaliere_path
        self.attivita_path = attivita_path
        self.start_time = 0

    def run(self):
        # Inizializza DB se necessario
        ContabilitaManager.init_db()

        self.progress_signal.emit("⏳ Analisi carico di lavoro...")

        # Scan workload for Global ETA
        sheets, files = ContabilitaManager.scan_workload(self.file_path, self.giornaliere_path)

        # Attività Programmate counts as 1 task if configured
        attivita_task = 1 if self.attivita_path and os.path.exists(self.attivita_path) else 0

        total_ops = sheets + files + attivita_task
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

                self.progress_signal.emit(f"⏳ Importazione: {percent}% completato ({current_total}/{total_ops}) • Tempo stimato: {m}m {s}s")

        total_added = 0
        total_removed = 0

        # 1. Import Contabilità (Dati)
        dati_cb = lambda c, t: global_progress(c, 0, "Contabilità")
        success, msg, added, removed = ContabilitaManager.import_data_from_excel(self.file_path, progress_callback=dati_cb)
        total_added += added
        total_removed += removed

        # 2. Import Giornaliere (se configurato)
        msg_giornaliere = ""
        if success and self.giornaliere_path:
            giorn_cb = lambda c, t: global_progress(c, sheets, "Giornaliere")
            g_success, g_msg, g_added, g_removed = ContabilitaManager.import_giornaliere(self.giornaliere_path, progress_callback=giorn_cb)
            msg_giornaliere = f" | Giornaliere: {g_msg}" if g_success else f" | Err Giornaliere: {g_msg}"
            total_added += g_added
            total_removed += g_removed

        # 3. Import Attività Programmate (se configurato)
        msg_attivita = ""
        if success and self.attivita_path:
            att_cb = lambda c, t: global_progress(c, sheets + files, "Attività Programmate")
            att_success, att_msg, att_added, att_removed = ContabilitaManager.import_attivita_programmate(self.attivita_path)
            # Call progress once
            att_cb(1, 1)
            msg_attivita = f" | Att. Prog: {att_msg}" if att_success else f" | Err Att. Prog: {att_msg}"
            total_added += att_added
            total_removed += att_removed

        self.finished_signal.emit(success, msg + msg_giornaliere + msg_attivita, total_added, total_removed)


class ContabilitaPanel(QWidget):
    """Pannello principale Strumentale."""

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
                background-color: white;
                color: black;
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
        self.status_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 14px;
                font-weight: 500;
                padding: 5px 10px;
                background-color: #f8f9fa;
                border-radius: 4px;
                border: 1px solid #dee2e6;
            }
        """)
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

        # --- Totale Selezionato Label (Global for this panel) ---
        self.selection_container = QWidget()
        selection_layout = QHBoxLayout(self.selection_container)
        selection_layout.setContentsMargins(0, 0, 0, 5)
        selection_layout.addStretch() # Push to right

        self.selection_count_label = QLabel("Righe: 0")
        self.selection_count_label.setStyleSheet("color: #6c757d; font-weight: bold; margin-right: 15px;")

        self.selection_sum_label = QLabel("Totale ORE SP: 0")
        self.selection_sum_label.setStyleSheet("color: #0d6efd; font-weight: bold;")

        selection_layout.addWidget(self.selection_count_label)
        selection_layout.addWidget(self.selection_sum_label)

        layout.addWidget(self.selection_container)

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

        self.main_tabs.addTab(self.year_tabs_widget, "📂 Preventivi")

        # --- TAB 2: GIORNALIERE (Years) ---
        self.giornaliere_tabs_widget = QTabWidget()
        self.giornaliere_tabs_widget.setTabPosition(QTabWidget.TabPosition.South)
        self.giornaliere_tabs_widget.setStyleSheet(self._get_subtab_style())
        self.giornaliere_tabs_widget.currentChanged.connect(self._on_tab_changed)

        self.main_tabs.addTab(self.giornaliere_tabs_widget, "📂 Giornaliere")

        # --- TAB 3: Attività Programmate ---
        self.attivita_widget = AttivitaProgrammateTab()
        self.main_tabs.addTab(self.attivita_widget, "📅 Attività Programmate")

        # --- TAB 4: KPI ---
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
            self.selection_container.hide()
        else:
            self.search_input.show()
            self.selection_container.show()
            # Trigger filter update for the new active tab
            self._filter_current_tab(self.search_input.text())
            self._connect_selection_signal()

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

        # Connect signals for initial tabs
        self._connect_selection_signal()

        # Aggiorna anche i dati KPI
        if hasattr(self, 'kpi_panel'):
            self.kpi_panel.refresh_years()

        # Aggiorna Attività Programmate
        if hasattr(self, 'attivita_widget'):
            self.attivita_widget.refresh_data()

    def _on_tab_changed(self, index):
        """Chiamato quando cambia la tab ANNO (in uno dei sub-tabwidget)."""
        self._filter_current_tab(self.search_input.text())
        self._connect_selection_signal() # Connect new tab table

    def _connect_selection_signal(self):
        """Connects the selection change signal of the current table to update totals."""
        current_main_idx = self.main_tabs.currentIndex()
        current_main_widget = self.main_tabs.widget(current_main_idx)

        target_widget = None
        if current_main_widget == self.year_tabs_widget:
            target_widget = self.year_tabs_widget.currentWidget()
        elif current_main_widget == self.giornaliere_tabs_widget:
            target_widget = self.giornaliere_tabs_widget.currentWidget()
        elif current_main_widget == getattr(self, 'attivita_widget', None):
            target_widget = self.attivita_widget

        if target_widget and hasattr(target_widget, 'table'):
            try:
                # Disconnect all first to avoid duplicates (safe pattern)
                try: target_widget.table.selectionModel().selectionChanged.disconnect()
                except Exception: pass

                target_widget.table.selectionModel().selectionChanged.connect(
                    lambda s, d: self._update_selection_total(target_widget.table)
                )
            except Exception as e:
                print(f"Errore connessione segnali selezione: {e}")

    def _update_selection_total(self, table_widget):
        """Calculates total of selected ORE SP column and row count."""
        try:
            selection_model = table_widget.selectionModel()
            indexes = selection_model.selectedIndexes()

            if not indexes:
                self.selection_count_label.setText("Righe: 0")
                self.selection_sum_label.setText("Totale ORE SP: 0")
                return

            # Identifica la colonna "ORE" o "ORE SP" per la tabella corrente
            target_col_idx = -1
            # Controlla header per trovare la colonna corretta dinamicamente
            for c in range(table_widget.columnCount()):
                header_item = table_widget.horizontalHeaderItem(c)
                if header_item:
                    header_text = header_item.text().upper()
                    if "ORE SP" in header_text or header_text == "ORE":
                        target_col_idx = c
                        break

            selected_rows = set()
            total_ore = 0.0

            for idx in indexes:
                row = idx.row()

                # Skip se la riga è nascosta (filtrata)
                if table_widget.isRowHidden(row):
                    continue

                # Skip se è la riga TOTALI
                item_first = table_widget.item(row, 0)
                if item_first and item_first.text() == "TOTALI":
                    continue

                selected_rows.add(row)

            # Calcola somma Ore solo per le righe uniche selezionate
            for row in selected_rows:
                if target_col_idx != -1:
                    item = table_widget.item(row, target_col_idx)
                    if item:
                        text = item.text()
                        try:
                            # Clean number format (Italian)
                            clean = str(text).replace(".", "").replace(",", ".").strip()
                            if clean:
                                val = float(clean)
                                total_ore += val
                        except ValueError:
                            pass # Ignora errori di parsing numerico (es. celle vuote)

            # Format
            if total_ore % 1 == 0:
                fmt_ore = f"{int(total_ore)}"
            else:
                fmt_ore = f"{total_ore:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            self.selection_count_label.setText(f"Righe: {len(selected_rows)}")
            self.selection_sum_label.setText(f"Totale ORE SP: {fmt_ore}")
        except Exception as e:
            print(f"Errore calcolo selezione: {e}")

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
        elif current_main_widget == getattr(self, 'attivita_widget', None):
            target_widget = self.attivita_widget

        if target_widget and hasattr(target_widget, 'filter_data'):
            target_widget.filter_data(text)

    def start_import_process(self):
        """Avvia il processo di importazione (chiamato dall'esterno o init)."""
        config = config_manager.load_config()
        path = config.get("contabilita_file_path", "")
        giornaliere_path = config.get("giornaliere_path", "")
        attivita_path = config.get("attivita_programmate_path", "")

        if not path or not os.path.exists(path):
            self.status_label.setText("⚠️ File contabilità non configurato o non trovato.")
            return

        self.status_label.setText("🔄 Aggiornamento in corso...")
        self.refresh_btn.setDisabled(True) # Disable button during update

        self.worker = ContabilitaWorker(path, giornaliere_path, attivita_path)
        self.worker.finished_signal.connect(self._on_import_finished)
        self.worker.progress_signal.connect(self.status_label.setText)
        self.worker.start()

    def _on_import_finished(self, success: bool, msg: str, added: int, removed: int):
        if success:
            now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            # Format text with colors
            added_text = f"<font color='green'><b>+{added}</b></font>"
            removed_text = f"<font color='red'><b>-{removed}</b></font>"
            status_html = f"Pronto, ultimo aggiornamento: {now_str} {added_text} {removed_text}"

            self.status_label.setText(status_html)
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

        # Force text color for Dark Mode compatibility
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #e9ecef;
                font-size: 13px;
                border: 1px solid #dee2e6;
                selection-background-color: #e7f1ff;
                selection-color: #0d6efd;
            }
            QTableWidget::item {
                color: black;
            }
            QTableWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
            }
            QTableWidget::item:focus {
                background-color: #e7f1ff;
                color: #0d6efd;
                border: none;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: black;
                padding: 4px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)

        self.table.auto_copy_headers = True

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
        # Variabili per calcolo media (ora usate solo per compatibilità futura se richiesto)
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

                # Totale Prev (solo righe valide)
                if not is_excluded:
                    t_item = self.table.item(r, self.COL_TOTALE)
                    if t_item:
                        sum_totale_prev += self._parse_currency(t_item.text())

                # Ore Spese (TUTTE le righe, incluse INS.ORE SP per il costo totale)
                o_item = self.table.item(r, self.COL_ORE)
                if o_item:
                    sum_ore_sp += self._parse_float(o_item.text())

        self.table.item(total_row_idx, self.COL_N_PREV).setText(str(count_prev))
        self.table.item(total_row_idx, self.COL_TOTALE).setText(self._format_currency(sum_totale_prev))
        self.table.item(total_row_idx, self.COL_ORE).setText(self._format_number(sum_ore_sp))

        # Calcolo Resa Ponderata (Globale): Totale Preventivato / Ore Spese Totali
        # Sostituisce la media aritmetica precedente
        weighted_resa = 0.0
        if sum_ore_sp > 0:
            weighted_resa = sum_totale_prev / sum_ore_sp

        self.table.item(total_row_idx, self.COL_RESA).setText(self._format_number(weighted_resa))

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
        """Formatta ORE: max 2 decimali, virgola, niente .0 finale (Italiano)."""
        try:
            val_f = float(val)
            val_f = round(val_f, 2)
            if val_f.is_integer():
                return f"{int(val_f)}"
            else:
                return f"{val_f:.2f}".replace('.', ',')
        except:
            return str(val)

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
            except Exception: pass
        elif col_idx == self.COL_TOTALE:
            try: return self._format_currency(float(str_val))
            except Exception: pass
        elif col_idx in [self.COL_ORE, self.COL_RESA]:
            try: return self._format_number(float(str_val))
            except Exception: pass
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

        # Force text color for Dark Mode compatibility
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #e9ecef;
                font-size: 13px;
                border: 1px solid #dee2e6;
                selection-background-color: #e7f1ff;
                selection-color: #0d6efd;
            }
            QTableWidget::item {
                color: black;
            }
            QTableWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
            }
            QTableWidget::item:focus {
                background-color: #e7f1ff;
                color: #0d6efd;
                border: none;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: black;
                padding: 4px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)

        self.table.auto_copy_headers = True

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


class AttivitaProgrammateTab(QWidget):
    """Tab per Attività Programmate."""

    COLUMNS = [
        'PS', 'AREA', 'PdL', 'IMP.', 'DESCRIZIONE ATTIVITA', 'LUN', 'MAR', 'MER',
        'GIO', 'VEN', 'STATO PdL', 'STATO ATTIVITA', 'DATA CONTROLLO',
        'PERSONALE IMPIEGATO', 'PO', 'AVVISO'
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        # --- Filter Bar ---
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(5, 0, 5, 5)

        # PS Flag
        self.chk_ps = QCheckBox("Filtra PS")
        self.chk_ps.setStyleSheet("font-weight: bold; color: #495057;")
        self.chk_ps.stateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.chk_ps)

        # PO Flag
        self.chk_po = QCheckBox("Filtra PO")
        self.chk_po.setStyleSheet("font-weight: bold; color: #495057;")
        self.chk_po.stateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.chk_po)

        filter_layout.addSpacing(20)

        # AREA Filter
        filter_layout.addWidget(QLabel("Area:"))
        self.combo_area = QComboBox()
        self.combo_area.setMinimumWidth(150)
        self.combo_area.addItem("Tutte")
        self.combo_area.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.combo_area)

        filter_layout.addSpacing(15)

        # STATO PdL Filter
        filter_layout.addWidget(QLabel("Stato PdL:"))
        self.combo_stato = QComboBox()
        self.combo_stato.setMinimumWidth(150)
        self.combo_stato.addItem("Tutti")
        self.combo_stato.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.combo_stato)

        # Reset Button
        self.btn_reset = QPushButton("Reset Filtri")
        self.btn_reset.setStyleSheet("""
            QPushButton {
                background-color: #6c757d; color: white; border: none;
                border-radius: 4px; padding: 4px 8px;
            }
            QPushButton:hover { background-color: #5a6268; }
        """)
        self.btn_reset.clicked.connect(self._reset_filters)
        filter_layout.addWidget(self.btn_reset)

        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # --- Table ---
        self.table = ExcelTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.setWordWrap(True)

        # Change selection behavior to Cells
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        # Connect double click to select row
        self.table.cellDoubleClicked.connect(self._on_double_click)

        # Style (Light/Black)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #e9ecef;
                font-size: 13px;
                border: 1px solid #dee2e6;
                selection-background-color: #e7f1ff;
                selection-color: #0d6efd;
            }
            QTableWidget::item { color: black; }
            QTableWidget::item:selected { background-color: #e7f1ff; color: #0d6efd; }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: black;
                padding: 4px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)

        self.table.auto_copy_headers = True
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Basic Sizing & Visibility
        # Hide PS (0) and PO (14)
        self.table.setColumnHidden(0, True)
        self.table.setColumnHidden(14, True)

        # Adjust widths
        # PS(0), AREA(1), PdL(2), IMP(3), DESC(4), LUN..VEN(5-9), STATO P(10), STATO A(11), DATA(12), PERS(13), PO(14), AVVISO(15)
        self.table.setColumnWidth(1, 80) # Area
        self.table.setColumnWidth(2, 80) # PdL
        self.table.setColumnWidth(3, 60) # Imp
        self.table.setColumnWidth(4, 350) # Descrizione (Wide)
        # Days
        for i in range(5, 10):
            self.table.setColumnWidth(i, 50)

        self.table.setColumnWidth(10, 120) # Stato PdL
        self.table.setColumnWidth(11, 120) # Stato Att
        self.table.setColumnWidth(12, 100) # Data
        self.table.setColumnWidth(13, 150) # Pers
        self.table.setColumnWidth(15, 250) # Avviso (Wide)

        # Context Menu
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)

        layout.addWidget(self.table)

    def refresh_data(self):
        """Metodo pubblico per ricaricare i dati."""
        self._load_data()

    def _load_data(self):
        """Carica i dati dal database."""
        data = ContabilitaManager.get_attivita_programmate_data()

        self.table.setSortingEnabled(False)
        self.table.blockSignals(True)
        self.table.setRowCount(0)

        try:
            self.table.setRowCount(len(data))

            for row_idx, row_data in enumerate(data):
                for col_idx in range(len(self.COLUMNS)):
                    val = row_data[col_idx]
                    val_str = str(val).strip() if val is not None else ""
                    if val_str.lower() == "nan": val_str = ""

                    item = QTableWidgetItem(val_str)
                    self.table.setItem(row_idx, col_idx, item)

            self.table.resizeRowsToContents()
            self._populate_filters()

        finally:
            self.table.blockSignals(False)
            self.table.setSortingEnabled(True)

    def _populate_filters(self):
        """Popola i combobox con i valori unici."""
        areas = set()
        stati = set()

        # Scan table directly (safer than re-querying DB if filtered)
        # AREA is col 1, STATO PdL is col 10
        for r in range(self.table.rowCount()):
            item_area = self.table.item(r, 1)
            if item_area and item_area.text():
                areas.add(item_area.text())

            item_stato = self.table.item(r, 10)
            if item_stato and item_stato.text():
                stati.add(item_stato.text())

        # Update Area Combo
        curr_area = self.combo_area.currentText()
        self.combo_area.blockSignals(True)
        self.combo_area.clear()
        self.combo_area.addItem("Tutte")
        self.combo_area.addItems(sorted(list(areas)))
        if curr_area in areas: self.combo_area.setCurrentText(curr_area)
        self.combo_area.blockSignals(False)

        # Update Stato Combo
        curr_stato = self.combo_stato.currentText()
        self.combo_stato.blockSignals(True)
        self.combo_stato.clear()
        self.combo_stato.addItem("Tutti")
        self.combo_stato.addItems(sorted(list(stati)))
        if curr_stato in stati: self.combo_stato.setCurrentText(curr_stato)
        self.combo_stato.blockSignals(False)

    def apply_filters(self):
        """Applica i filtri alla tabella."""
        filter_ps = self.chk_ps.isChecked()
        filter_po = self.chk_po.isChecked()
        filter_area = self.combo_area.currentText()
        filter_stato = self.combo_stato.currentText()

        # Indices: PS=0, AREA=1, STATO PdL=10, PO=14
        for r in range(self.table.rowCount()):
            hide = False

            # PS Filter (Show only if PS is NOT empty)
            if filter_ps:
                item = self.table.item(r, 0)
                if not item or not item.text().strip():
                    hide = True

            # PO Filter (Show only if PO is NOT empty)
            if not hide and filter_po:
                item = self.table.item(r, 14)
                if not item or not item.text().strip():
                    hide = True

            # Area Filter
            if not hide and filter_area != "Tutte":
                item = self.table.item(r, 1)
                if not item or item.text() != filter_area:
                    hide = True

            # Stato Filter
            if not hide and filter_stato != "Tutti":
                item = self.table.item(r, 10)
                if not item or item.text() != filter_stato:
                    hide = True

            self.table.setRowHidden(r, hide)

    def _reset_filters(self):
        self.chk_ps.setChecked(False)
        self.chk_po.setChecked(False)
        self.combo_area.setCurrentIndex(0)
        self.combo_stato.setCurrentIndex(0)
        self.apply_filters()

    def _on_double_click(self, row, col):
        """Doppio click seleziona l'intera riga."""
        self.table.selectRow(row)

    def filter_data(self, text):
        """Filtra la tabella (Search Bar globale)."""
        # Reset specific filters temporarily or apply strictly?
        # Usually search bar adds to existing filters.
        # But for simplicity, let's say Search Bar overrides or works with AND.
        # Let's apply standard text search AND logic.

        search_terms = text.lower().split()
        cols = self.table.columnCount()

        for r in range(self.table.rowCount()):
            # First check specific filters by calling logic manually or trusting state?
            # Re-evaluating filters for every row is expensive if we do full loop.
            # Efficient way: Check if hidden by filters first?
            # Actually, `apply_filters` resets visibility.
            # Let's modify logic: Search bar is "extra".

            # 1. Check strict filters
            filter_ps = self.chk_ps.isChecked()
            filter_po = self.chk_po.isChecked()
            filter_area = self.combo_area.currentText()
            filter_stato = self.combo_stato.currentText()

            hide = False
            if filter_ps:
                item = self.table.item(r, 0)
                if not item or not item.text().strip(): hide = True
            if not hide and filter_po:
                item = self.table.item(r, 14)
                if not item or not item.text().strip(): hide = True
            if not hide and filter_area != "Tutte":
                item = self.table.item(r, 1)
                if not item or item.text() != filter_area: hide = True
            if not hide and filter_stato != "Tutti":
                item = self.table.item(r, 10)
                if not item or item.text() != filter_stato: hide = True

            # 2. Check Search Text
            if not hide and text:
                row_visible = False
                for c in range(cols):
                    item = self.table.item(r, c)
                    if item and item.text():
                        if text.lower() in item.text().lower():
                            row_visible = True
                            break
                if not row_visible:
                    # Check combined terms
                    row_text = " ".join([self.table.item(r, c).text().lower() for c in range(cols) if self.table.item(r, c)])
                    if not all(term in row_text for term in search_terms):
                        hide = True

            self.table.setRowHidden(r, hide)

    def _show_context_menu(self, pos):
        """Menu contestuale."""
        menu = QMenu(self)
        lyra_action = QAction("✨ Analizza Riga con Lyra", self)
        lyra_action.triggered.connect(lambda: self.table._analyze_row_at(pos))
        menu.addAction(lyra_action)
        menu.exec(self.table.viewport().mapToGlobal(pos))
