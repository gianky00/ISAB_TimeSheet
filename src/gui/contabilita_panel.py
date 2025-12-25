"""
Bot TS - Contabilita Panel
Pannello per la visualizzazione della Contabilità Strumentale.
"""
import os
import re
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QMessageBox, QMenu, QTableWidget,
    QHeaderView, QTableWidgetItem, QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QAbstractItemView,
    QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QAction, QFont, QColor
import time
import json
import tempfile
import subprocess

from src.core.contabilita_manager import ContabilitaManager
from src.core import config_manager
from src.gui.widgets import ExcelTableWidget, StatusIndicator


class ContabilitaWorker(QThread):
    """Worker per l'importazione in background."""
    finished_signal = pyqtSignal(bool, str, int, int)
    progress_signal = pyqtSignal(str)

    def __init__(self, file_path: str, giornaliere_path: str = "", attivita_path: str = "", certificati_path: str = ""):
        super().__init__()
        self.file_path = file_path
        self.giornaliere_path = giornaliere_path
        self.attivita_path = attivita_path
        self.certificati_path = certificati_path
        self.start_time = 0

    def run(self):
        # Inizializza DB se necessario
        ContabilitaManager.init_db()

        self.progress_signal.emit("⏳ Analisi carico di lavoro...")

        # Scan workload for Global ETA
        sheets, files = ContabilitaManager.scan_workload(self.file_path, self.giornaliere_path)

        # Attività Programmate counts as 1 task if configured
        attivita_task = 1 if self.attivita_path and os.path.exists(self.attivita_path) else 0

        # Certificati Campione counts as 1 task if configured
        certificati_task = 1 if self.certificati_path and os.path.exists(self.certificati_path) else 0

        total_ops = sheets + files + attivita_task + certificati_task
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

        # 4. Import Certificati Campione (se configurato)
        msg_certificati = ""
        if success and self.certificati_path:
            cert_cb = lambda c, t: global_progress(c, sheets + files + attivita_task, "Certificati Campione")
            cert_success, cert_msg, cert_added, cert_removed = ContabilitaManager.import_certificati_campione(self.certificati_path)
            cert_cb(1, 1)
            msg_certificati = f" | Certificati: {cert_msg}" if cert_success else f" | Err Certificati: {cert_msg}"
            total_added += cert_added
            total_removed += cert_removed

        self.finished_signal.emit(success, msg + msg_giornaliere + msg_attivita + msg_certificati, total_added, total_removed)


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

        # --- TAB 4: Certificati Campione ---
        self.certificati_widget = CertificatiCampioneTab()
        self.main_tabs.addTab(self.certificati_widget, "📜 Certificati Campione")

        # --- TAB 5: KPI ---
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

        # Aggiorna Certificati Campione
        if hasattr(self, 'certificati_widget'):
            self.certificati_widget.refresh_data()

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
        elif current_main_widget == getattr(self, 'certificati_widget', None):
            target_widget = self.certificati_widget

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
        elif current_main_widget == getattr(self, 'certificati_widget', None):
            target_widget = self.certificati_widget

        if target_widget and hasattr(target_widget, 'filter_data'):
            target_widget.filter_data(text)

    def start_import_process(self):
        """Avvia il processo di importazione (chiamato dall'esterno o init)."""
        config = config_manager.load_config()
        path = config.get("contabilita_file_path", "")
        giornaliere_path = config.get("giornaliere_path", "")
        attivita_path = config.get("attivita_programmate_path", "")
        certificati_path = config.get("certificati_campione_path", "")

        if not path or not os.path.exists(path):
            self.status_label.setText("⚠️ File contabilità non configurato o non trovato.")
            return

        self.status_label.setText("🔄 Aggiornamento in corso...")
        self.refresh_btn.setDisabled(True) # Disable button during update

        self.worker = ContabilitaWorker(path, giornaliere_path, attivita_path, certificati_path)
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
        "DATA\nPREV.", "MESE", "N°\nPREV.", "TOTALE\nPREV.", "ATTIVITA'",
        "TCL", "ODC", "STATO\nATTIVITA'", "TIPOLOGIA", "ORE\nSP", "RESA", "ANNOTAZIONI"
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

        # Force Read-Only
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

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
        "DATA", "PERSONALE", "TCL", "DESCRIZIONE\nATTIVITA'", "N°\nPREV.", "ODC",
        "PDL", "INIZIO", "FINE", "ORE"
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

        # Force Read-Only
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

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
        'PS', 'AREA', 'PdL', 'IMP.', "DESCRIZIONE\nATTIVITA'", 'LUN', 'MAR', 'MER',
        'GIO', 'VEN', "STATO\nPdL", "STATO\nATTIVITA'", "DATA\nCONTROLLO",
        "PERSONALE\nIMPIEGATO", 'PO', 'AVVISO'
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

        # Force Read-Only
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

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

            # Index for styles column (last one)
            style_col_idx = len(self.COLUMNS) # Since COLUMNS has 16 items (0-15), style is at 16?
            # In DB query: SELECT ..., styles FROM ...
            # So if COLUMNS is length 16, row_data length is 17

            for row_idx, row_data in enumerate(data):
                # Check for styles
                row_styles = {}
                if len(row_data) > len(self.COLUMNS):
                    style_json = row_data[len(self.COLUMNS)]
                    if style_json:
                        try: row_styles = json.loads(style_json)
                        except: pass

                for col_idx in range(len(self.COLUMNS)):
                    val = row_data[col_idx]
                    val_str = str(val).strip() if val is not None else ""
                    if val_str.lower() == "nan": val_str = ""

                    # Format Data Controllo (Index 12)
                    if col_idx == 12 and val_str:
                         try:
                             if ' ' in val_str: val_str = val_str.split(' ')[0]
                             dt = datetime.strptime(val_str, "%Y-%m-%d")
                             val_str = dt.strftime("%d/%m/%Y")
                         except ValueError:
                             pass

                    item = QTableWidgetItem(val_str)

                    # Apply Styles
                    # Mapping col_idx to DB Key?
                    # COLUMNS = ['PS', 'AREA', 'PdL', ...]
                    # We need to map index back to the key used in styles json
                    # ATTIVITA_PROGRAMMATE_MAPPING keys are messy, but values are clean db_cols
                    # The get_data query returns columns in order of ATTIVITA_PROGRAMMATE_COLS
                    # which is list(ATTIVITA_PROGRAMMATE_MAPPING.values())
                    # So index matches the list of values

                    db_keys = list(ContabilitaManager.ATTIVITA_PROGRAMMATE_MAPPING.values())
                    if col_idx < len(db_keys):
                        key = db_keys[col_idx]
                        if key in row_styles:
                            style = row_styles[key]
                            if 'fg' in style:
                                item.setForeground(QColor(style['fg']))
                            if 'bg' in style:
                                item.setBackground(QColor(style['bg']))

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


class CertificatiCampioneTab(QWidget):
    """Tab per Certificati Campione (Tree View)."""

    HEADERS = [
        "Modello /\nTipo", "Costruttore", "Matricola", "Range\nStrumento", "Errore\nmax %",
        "Certificato\nTaratura", "Scadenza\nCertificato", "Emissione\nCertificato", "ID-COEMI", "Stato\nCertificato"
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.addStretch()

        self.btn_analyze = QPushButton("📊 Analizza")
        self.btn_analyze.setStyleSheet("""
            QPushButton {
                background-color: #6610f2; color: white; border: none;
                border-radius: 4px; padding: 6px 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #520dc2; }
        """)
        self.btn_analyze.clicked.connect(self._run_analysis)
        toolbar.addWidget(self.btn_analyze)

        layout.addLayout(toolbar)

        # Tree Widget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(self.HEADERS)
        self.tree.setWordWrap(True)
        self.tree.setAlternatingRowColors(True)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        # FORCE READ ONLY
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Styling
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                color: black;
                font-size: 13px;
                border: 1px solid #dee2e6;
            }
            QTreeWidget::item {
                color: black;
                padding: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #e7f1ff;
                color: #0d6efd;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: black;
                padding: 4px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)

        header = self.tree.header()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Dimensions
        self.tree.setColumnWidth(0, 200) # Modello
        self.tree.setColumnWidth(1, 120) # Costruttore
        self.tree.setColumnWidth(2, 120) # Matricola
        self.tree.setColumnWidth(3, 120) # Range
        self.tree.setColumnWidth(4, 100) # Errore
        self.tree.setColumnWidth(5, 140) # Certificato
        self.tree.setColumnWidth(6, 120) # Scadenza
        self.tree.setColumnWidth(7, 120) # Emissione
        self.tree.setColumnWidth(8, 100) # ID

        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)

        layout.addWidget(self.tree)

    def refresh_data(self):
        self._load_data()

    def _load_data(self):
        data = ContabilitaManager.get_certificati_campione_data()
        self.tree.clear()
        self.tree.setSortingEnabled(False)

        # Groups: Key -> List of rows
        groups = {}

        # Column Indices (based on HEADERS order which matches DB)
        # 0: Modello, 1: Costruttore, 2: Matricola, 3: Range
        # 4: Errore, 5: Certificato, 6: Scadenza, 7: Emissione, 8: ID, 9: Stato

        for row_data in data:
            # Key: (Modello, Costruttore, Matricola, Range)
            k0 = str(row_data[0]).strip() if row_data[0] else ""
            k1 = str(row_data[1]).strip() if row_data[1] else ""
            k2 = str(row_data[2]).strip() if row_data[2] else ""
            k3 = str(row_data[3]).strip() if row_data[3] else ""

            key = (k0, k1, k2, k3)

            if key not in groups:
                groups[key] = []
            groups[key].append(row_data)

        for key, rows in groups.items():
            # Sort rows by Emissione (Index 7) Descending
            def parse_date(r):
                val = r[7]
                if not val: return datetime.min
                s = str(val).strip()
                # Try common formats
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
                    try: return datetime.strptime(s, fmt)
                    except: continue
                return datetime.min

            rows.sort(key=parse_date, reverse=True)

            # Latest is rows[0]
            latest = rows[0]

            # Create Top Item
            top_item = self._create_item(latest)

            # Add Children (History)
            if len(rows) > 1:
                for i in range(1, len(rows)):
                     child = self._create_item(rows[i])
                     top_item.addChild(child)

            self.tree.addTopLevelItem(top_item)

        self.tree.setSortingEnabled(True)

    def _create_item(self, row_data):
        strings = []
        for i, val in enumerate(row_data):
            # Format Errore max % (Index 4)
            if i == 4:
                strings.append(self._format_percentage(val))
            else:
                s = str(val).strip() if val is not None else ""
                if s.lower() == 'nan': s = ""
                strings.append(s)

        item = QTreeWidgetItem(strings)
        return item

    def _format_percentage(self, val):
        """Formats 0.0005 -> 0,05%, 0.01 -> 1%."""
        if val is None or str(val).strip() == "": return ""
        try:
            # Handle comma decimal input if present
            s_val = str(val).replace(",", ".")
            f = float(s_val)
            pct = f * 100

            # Format avoiding scientific notation
            # Use 'f' but strip zeros? Or 'g'?
            # 'g' is good but switches to sci notation for large/small numbers.
            # 15.5 -> 15.5. 0.05 -> 0.05.
            s = "{0:g}".format(pct)
            return s.replace(".", ",") + "%"
        except:
            return str(val)

    def filter_data(self, text):
        search_terms = text.lower().split()
        root = self.tree.invisibleRootItem()
        child_count = root.childCount()

        for i in range(child_count):
            item = root.child(i)
            # Check Item
            match = self._item_matches(item, search_terms)

            # Check children
            child_match = False
            for j in range(item.childCount()):
                sub = item.child(j)
                if self._item_matches(sub, search_terms):
                    child_match = True
                    sub.setHidden(False)
                else:
                    sub.setHidden(True)

            # Logic: Show if item matches OR any child matches
            if match or child_match:
                item.setHidden(False)
                if child_match and not match:
                    item.setExpanded(True)
            else:
                item.setHidden(True)

    def _item_matches(self, item, search_terms):
        if not search_terms: return True
        # Join all column text
        row_text = " ".join([item.text(c).lower() for c in range(self.tree.columnCount())])
        return all(term in row_text for term in search_terms)

    def _show_context_menu(self, pos):
        item = self.tree.itemAt(pos)
        if not item: return

        menu = QMenu(self)
        lyra = QAction("✨ Analizza Riga con Lyra", self)
        lyra.triggered.connect(lambda: self._analyze_item(item))
        menu.addAction(lyra)
        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def _analyze_item(self, item):
        row_data = []
        for c in range(self.tree.columnCount()):
            header = self.tree.headerItem().text(c).replace('\n', ' ')
            row_data.append(f"**{header}**: {item.text(c)}")

        context = " | ".join(row_data)

        win = self.window()
        if hasattr(win, "analyze_with_lyra"):
            win.analyze_with_lyra(context)

    def _run_analysis(self):
        """Esegue lo script PowerShell di analisi."""
        config = config_manager.load_config()
        path = config.get("certificati_campione_path", "")

        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Attenzione", "File Certificati Campione non configurato o non trovato.\nVerifica nelle impostazioni.")
            return

        # Prepare PowerShell Script
        # We inject the configured path into the script
        ps_script = r"""
# --- Parametri Iniziali ---
$Global:ExcelFilePath = "__FILE_PATH_PLACEHOLDER__"
$Global:SheetName = "strumenti campione ISAB SUD"
$startRow = 9

# --- Carica gli assembly necessari ---
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# --- Definizione API di Windows per PrintWindow (per screenshot) ---
Add-Type -ReferencedAssemblies System.Windows.Forms, System.Drawing -TypeDefinition @"
    using System;
    using System.Runtime.InteropServices;
    using System.Drawing;
    public class User32 {
        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool PrintWindow(IntPtr hwnd, IntPtr hdcBlt, uint nFlags);
    }
"@

# --- Funzione per creare e mostrare la finestra di riepilogo personalizzata ---
function Show-CustomSummaryBox {
    param (
        [string]$Title,
        [System.Collections.ArrayList]$Scaduti,
        [System.Collections.ArrayList]$Prossimi3Giorni,
        [datetime]$Oggi,
        [string]$ExcelPathForVBA
    )

    $form = New-Object System.Windows.Forms.Form
    $form.Text = $Title
    $form.StartPosition = [System.Windows.Forms.FormStartPosition]::CenterScreen
    $form.Width = 1052
    $form.Height = 600
    $form.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::Sizable
    $form.MaximizeBox = $true
    $form.MinimizeBox = $true
    $form.Padding = New-Object System.Windows.Forms.Padding(10)

    $richTextBox = New-Object System.Windows.Forms.RichTextBox
    $richTextBox.Dock = [System.Windows.Forms.DockStyle]::Fill
    $richTextBox.BorderStyle = [System.Windows.Forms.BorderStyle]::FixedSingle
    $richTextBox.ReadOnly = $true
    $richTextBox.Font = New-Object System.Drawing.Font("Consolas", 10)
    $richTextBox.ScrollBars = [System.Windows.Forms.RichTextBoxScrollBars]::Both
    $richTextBox.WordWrap = $false

    $appendToRichTextBox = {
        param(
            [string]$Text,
            [System.Drawing.Color]$Color = ([System.Drawing.Color]::FromName("Black")),
            [bool]$Bold = $false,
            [bool]$NewLine = $true
        )
        $richTextBox.SelectionStart = $richTextBox.TextLength
        $richTextBox.SelectionLength = 0
        $richTextBox.SelectionColor = $Color
        $currentFont = $richTextBox.SelectionFont
        if ($Bold) {
            $richTextBox.SelectionFont = New-Object System.Drawing.Font($currentFont, [System.Drawing.FontStyle]::Bold)
        } else {
            $richTextBox.SelectionFont = New-Object System.Drawing.Font($currentFont, [System.Drawing.FontStyle]::Regular)
        }
        $textToAppend = if ($NewLine) { "$Text`n" } else { $Text }
        $richTextBox.AppendText($textToAppend)
        $richTextBox.SelectionColor = $richTextBox.ForeColor
        $richTextBox.SelectionFont = $currentFont
    }

    $panelBottom = New-Object System.Windows.Forms.Panel
    $panelBottom.Height = 75
    $panelBottom.Dock = [System.Windows.Forms.DockStyle]::Bottom
    $panelBottom.Padding = New-Object System.Windows.Forms.Padding(10, 5, 10, 5)

    $labelFilePath = New-Object System.Windows.Forms.Label
    $labelFilePath.Text = "File analizzato: $ExcelPathForVBA"
    $labelFilePath.AutoSize = $true
    $labelFilePath.Location = New-Object System.Drawing.Point(0, 3)
    $labelFilePath.Anchor = [System.Windows.Forms.AnchorStyles]::Top -bor [System.Windows.Forms.AnchorStyles]::Left
    $panelBottom.Controls.Add($labelFilePath)

    $labelRedattoDa = New-Object System.Windows.Forms.Label
    $labelRedattoDa.Text = "Redatto da: Allegretti Giancarlo"
    $labelRedattoDa.AutoSize = $true
    $labelRedattoDa.Anchor = [System.Windows.Forms.AnchorStyles]::Top -bor [System.Windows.Forms.AnchorStyles]::Left
    $yPosSecondLabel = $labelFilePath.Location.Y + $labelFilePath.PreferredSize.Height + 3
    $labelRedattoDa.Location = New-Object System.Drawing.Point(0, $yPosSecondLabel)
    $panelBottom.Controls.Add($labelRedattoDa)

    $okButton = New-Object System.Windows.Forms.Button
    $okButton.Text = "Chiudi"
    $okButton.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    $okButton.Height = 30
    $okButton.Width = 100
    $okButton.Anchor = [System.Windows.Forms.AnchorStyles]::Bottom -bor [System.Windows.Forms.AnchorStyles]::Right

    $captureSendButton = New-Object System.Windows.Forms.Button
    $captureSendButton.Text = "Cattura e Invia Email"
    $captureSendButton.Height = 30
    $captureSendButton.Width = 180
    $captureSendButton.Anchor = [System.Windows.Forms.AnchorStyles]::Bottom -bor [System.Windows.Forms.AnchorStyles]::Right

    $okButton.Location = New-Object System.Drawing.Point(
        ([int]$panelBottom.ClientSize.Width - [int]$okButton.Width),
        ([int]$panelBottom.ClientSize.Height - [int]$okButton.Height)
    )
    $captureSendButton.Location = New-Object System.Drawing.Point(
        ([int]$okButton.Location.X - [int]$captureSendButton.Width - 10),
        ([int]$panelBottom.ClientSize.Height - [int]$captureSendButton.Height)
    )
    $okButton.Add_Click({ $form.Close() })
    $panelBottom.Controls.Add($captureSendButton)
    $panelBottom.Controls.Add($okButton)

    $form.PerformLayout()
    $availableWidthForLabels = ([int]$captureSendButton.Location.X - [int]$panelBottom.Padding.Left - 15)
    if ($labelFilePath.PreferredSize.Width > $availableWidthForLabels) {
        $labelFilePath.AutoSize = $false
        $labelFilePath.Width = $availableWidthForLabels
        $toolTipForPath = New-Object System.Windows.Forms.ToolTip
        $toolTipForPath.SetToolTip($labelFilePath, $ExcelPathForVBA)
    }
    if ($labelRedattoDa.PreferredSize.Width > $availableWidthForLabels) {
         $labelRedattoDa.AutoSize = $false
         $labelRedattoDa.Width = $availableWidthForLabels
    }

    $form.Controls.Add($richTextBox)
    $form.Controls.Add($panelBottom)
    $form.CancelButton = $okButton

    # --- Popolamento RichTextBox (Logica Testo Migliorata v2) ---
    $numeroScaduti = if ($Scaduti) { $Scaduti.Count } else { 0 }
    $numeroProssimi3Giorni = if ($Prossimi3Giorni) { $Prossimi3Giorni.Count } else { 0 }
    $null = $appendToRichTextBox.Invoke("RIEPILOGO SCADENZE STRUMENTI", [System.Drawing.Color]::Black, $true, $false)
    $null = $appendToRichTextBox.Invoke(" (Data analisi: $($Oggi.ToString('dd/MM/yyyy')))`n", [System.Drawing.Color]::Gray, $false, $true)
    $null = $appendToRichTextBox.Invoke("")
    $null = $appendToRichTextBox.Invoke("Quantità Totale Strumenti ", [System.Drawing.Color]::Black, $true, $false)
    $null = $appendToRichTextBox.Invoke("SCADUTI", ([System.Drawing.Color]::FromName("Red")), $true, $false)
    $null = $appendToRichTextBox.Invoke(": $numeroScaduti", [System.Drawing.Color]::Black, $true, $true)
    $null = $appendToRichTextBox.Invoke("Quantità Strumenti ", [System.Drawing.Color]::Black, $true, $false)
    $null = $appendToRichTextBox.Invoke("IN SCADENZA", ([System.Drawing.Color]::FromName("DarkOrange")), $true, $false)
    $null = $appendToRichTextBox.Invoke(" (oggi e prossimi 3 giorni): $numeroProssimi3Giorni", [System.Drawing.Color]::Black, $true, $true)
    $null = $appendToRichTextBox.Invoke("----------------------------------------------------------------------------------------------------------------------------------")
    if ($numeroScaduti -eq 0 -and $numeroProssimi3Giorni -eq 0) {
        $null = $appendToRichTextBox.Invoke("`nNessuno strumento risulta attualmente scaduto o in scadenza nei prossimi 3 giorni.", ([System.Drawing.Color]::FromName("DarkGreen")), $true)
    } else {
        if ($numeroScaduti -gt 0) {
            $null = $appendToRichTextBox.Invoke("`n--- STRUMENTI SCADUTI (Quantità: $numeroScaduti) ---", ([System.Drawing.Color]::FromName("Red")), $true)
            foreach ($item in $Scaduti) {
                $line = "ID: $($item.IDCOEMI.PadRight(10)) | Strumento: $($item.Strumento.PadRight(30)) | Costr: $($item.Costruttore.PadRight(15)) | Matricola: $($item.Matricola.PadRight(15)) | Scad: "
                $null = $appendToRichTextBox.Invoke($line, [System.Drawing.Color]::Black, $false, $false)
                $null = $appendToRichTextBox.Invoke($item.DataScadenza.ToString('dd/MM/yyyy'), ([System.Drawing.Color]::FromName("Red")), $true, $false)
                $null = $appendToRichTextBox.Invoke(" (Riga: $($item.RigaExcel))", [System.Drawing.Color]::Gray, $false, $true)
            }
        } else {
            $null = $appendToRichTextBox.Invoke("`nNessuno strumento risulta attualmente scaduto.", [System.Drawing.Color]::DarkGreen, $false, $true)
        }
        if ($numeroProssimi3Giorni -gt 0) {
            $null = $appendToRichTextBox.Invoke("`n--- STRUMENTI IN SCADENZA (OGGI E PROSSIMI 3 GIORNI) (Quantità: $numeroProssimi3Giorni) ---", ([System.Drawing.Color]::FromName("DarkOrange")), $true)
            foreach ($item in $Prossimi3Giorni) {
                $line = "ID: $($item.IDCOEMI.PadRight(10)) | Strumento: $($item.Strumento.PadRight(30)) | Costr: $($item.Costruttore.PadRight(15)) | Matricola: $($item.Matricola.PadRight(15)) | Scad: "
                $null = $appendToRichTextBox.Invoke($line, [System.Drawing.Color]::Black, $false, $false)
                $null = $appendToRichTextBox.Invoke($item.DataScadenza.ToString('dd/MM/yyyy'), ([System.Drawing.Color]::FromName("DarkOrange")), $true, $false)
                $null = $appendToRichTextBox.Invoke(" (Riga: $($item.RigaExcel))", [System.Drawing.Color]::Gray, $false, $true)
            }
        }
    }

    $captureSendButton.Add_Click({
        $screenshotPath = $null
        try {
            $form.Refresh()
            Start-Sleep -Milliseconds 250
            $bitmapForCapture = New-Object System.Drawing.Bitmap($form.Width, $form.Height)
            $gfxFromImage = [System.Drawing.Graphics]::FromImage($bitmapForCapture)
            $hdcBitmap = $gfxFromImage.GetHdc()
            $captureSuccess = [User32]::PrintWindow($form.Handle, $hdcBitmap, 0x2) # PW_RENDERFULLCONTENT
            $gfxFromImage.ReleaseHdc($hdcBitmap)
            $gfxFromImage.Dispose()
            if (-not $captureSuccess) { Throw "PrintWindow API call failed." }
            $screenshotFileName = "summary_screenshot_ps_capture.png"
            $screenshotPath = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), $screenshotFileName)
            if (Test-Path $screenshotPath) { Remove-Item $screenshotPath -Force -ErrorAction SilentlyContinue }
            $bitmapForCapture.Save($screenshotPath, [System.Drawing.Imaging.ImageFormat]::Png)
            $bitmapForCapture.Dispose()
        } catch {
            [System.Windows.Forms.MessageBox]::Show("Errore cattura screenshot: $($_.Exception.Message)", "Errore Screenshot", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
            $screenshotPath = $null
        }
        if ($screenshotPath -and (Test-Path $screenshotPath)) {
            $excelApp = $null
            $workbookToRunMacroIn = $null
            try {
                try { $excelApp = [System.Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application") } catch {}
                if ($excelApp -eq $null) { $excelApp = New-Object -ComObject Excel.Application }
                $foundWorkbook = $null
                foreach($wb in $excelApp.Workbooks){ if($wb.FullName -eq $ExcelPathForVBA){ $foundWorkbook = $wb; break } }
                if($foundWorkbook -eq $null){ $workbookToRunMacroIn = $excelApp.Workbooks.Open($ExcelPathForVBA) } else { $workbookToRunMacroIn = $foundWorkbook }
                if ($workbookToRunMacroIn) {
                    $macroName = "InviaEmailConScreenshotDaPS"
                    $excelApp.Run("'$($workbookToRunMacroIn.Name)'!$macroName", $screenshotPath)
                } else {
                    [System.Windows.Forms.MessageBox]::Show("Impossibile aprire workbook Excel: $ExcelPathForVBA", "Errore Workbook", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
                }
            } catch {
                 [System.Windows.Forms.MessageBox]::Show("Errore avvio macro VBA: $($_.Exception.Message)", "Errore VBA", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
            } finally {
                if ($excelApp -ne $null) { $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excelApp); $excelApp = $null }
                [GC]::Collect()
            }
        } else {
            [System.Windows.Forms.MessageBox]::Show("Screenshot non catturato. Impossibile inviare email.", "Info Screenshot", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
        }
        $form.Close()
    })

    $form.TopMost = $true
    $null = $form.ShowDialog()
    $form.Dispose()
}

# --- Logica Principale dello Script ---
$excelAppReader = $null
$workbookReader = $null
$wsReader = $null
try {
    $excelAppReader = New-Object -ComObject Excel.Application
    $excelAppReader.Visible = $false
    $excelAppReader.DisplayAlerts = $false
    if (-not (Test-Path $Global:ExcelFilePath)) {
        [System.Windows.Forms.MessageBox]::Show("Errore: File Excel non trovato: `n$($Global:ExcelFilePath)", "Errore File", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
        exit # Esce dallo script se il file non è trovato
    }
    $workbookReader = $excelAppReader.Workbooks.Open($Global:ExcelFilePath)
    try {
        $wsReader = $workbookReader.Sheets.Item($Global:SheetName)
    } catch {
        [System.Windows.Forms.MessageBox]::Show("Errore: Foglio '$($Global:SheetName)' non trovato.", "Errore Foglio", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
        # Pulizia parziale prima di exit
        if ($workbookReader -ne $null) { $workbookReader.Close($false); $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($workbookReader); $workbookReader = $null }
        if ($excelAppReader -ne $null) { $excelAppReader.Quit(); $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excelAppReader); $excelAppReader = $null }
        exit
    }
    if ($wsReader.AutoFilterMode) { $wsReader.AutoFilterMode = $false }
    $lastRow = $wsReader.Cells($wsReader.Rows.Count, "X").End(-4162).Row
    if ($lastRow -lt $startRow) {
        [System.Windows.Forms.MessageBox]::Show("Nessun dato da elaborare.", "Nessun Dato", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
        # Anche qui, pulizia prima di terminare il blocco try se non ci sono dati
        # Altrimenti, Show-CustomSummaryBox non verrà chiamato e il finally non pulirà questi oggetti
    } else {
        $scadenzeList = New-Object System.Collections.ArrayList
        $oggi = (Get-Date).Date
        for ($i = $startRow; $i -le $lastRow; $i++) {
            $promemoriaValue = $wsReader.Cells($i, "X").Value2
            $giorniScadenzaValue = $wsReader.Cells($i, "W").Value2
            if ($promemoriaValue -ne $null -and $promemoriaValue.ToString().Trim().ToUpper() -eq "SI") {
                $giorniDouble = 0
                $isNumeric = [System.Double]::TryParse($giorniScadenzaValue, [ref]$giorniDouble)
                if ($giorniScadenzaValue -ne $null -and $isNumeric) {
                    $dataScadenzaCalcolata = $oggi.AddDays($giorniDouble)
                    $scadenzaItem = [PSCustomObject]@{
                        Strumento    = if ($wsReader.Cells($i, "G").Value2 -ne $null) { $wsReader.Cells($i, "G").Value2.ToString() } else { "N/D" }
                        Costruttore  = if ($wsReader.Cells($i, "I").Value2 -ne $null) { $wsReader.Cells($i, "I").Value2.ToString() } else { "N/D" }
                        Matricola    = if ($wsReader.Cells($i, "K").Value2 -ne $null) { $wsReader.Cells($i, "K").Value2.ToString() } else { "N/D" }
                        IDCOEMI      = if ($wsReader.Cells($i, "V").Value2 -ne $null) { $wsReader.Cells($i, "V").Value2.ToString() } else { "N/D" }
                        DataScadenza = $dataScadenzaCalcolata
                        RigaExcel    = $i
                    }
                    $null = $scadenzeList.Add($scadenzaItem)
                } else { Write-Warning "Riga $($i): Valore non numerico colonna W." }
            }
        }

        # NON chiudere $excelAppReader e $workbookReader qui se verranno usati in Show-CustomSummaryBox
        # o se la pulizia è solo nel finally.
        # LA PULIZIA ORA E' SOLO NEL BLOCCO FINALLY ESTERNO

        if ($scadenzeList.Count -eq 0) {
            [System.Windows.Forms.MessageBox]::Show("Nessuno strumento con promemoria 'SI'.", "Info", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
        } else {
            $scaduti = $scadenzeList | Where-Object {$_.DataScadenza -lt $oggi} | Sort-Object DataScadenza
            $dataInizioProssimi = $oggi
            $dataFineProssimi = $oggi.AddDays(3)
            $prossimi3Giorni = $scadenzeList | Where-Object {$_.DataScadenza -ge $dataInizioProssimi -and $_.DataScadenza -le $dataFineProssimi} | Sort-Object DataScadenza

            # Chiudi l'istanza di Excel usata per la lettura DATI QUI, prima di mostrare il form,
            # per evitare conflitti se Show-CustomSummaryBox tenta di usare la stessa istanza o file.
            if ($wsReader -ne $null) { $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($wsReader); $wsReader = $null }
            if ($workbookReader -ne $null) { $workbookReader.Close($false); $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($workbookReader); $workbookReader = $null }
            if ($excelAppReader -ne $null) { $excelAppReader.Quit(); $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excelAppReader); $excelAppReader = $null }
            Remove-Variable excelAppReader, workbookReader, wsReader -ErrorAction SilentlyContinue
            [GC]::Collect(); [GC]::WaitForPendingFinalizers()

            Show-CustomSummaryBox -Title "Avviso Scadenze Strumenti" -Scaduti $scaduti -Prossimi3Giorni $prossimi3Giorni -Oggi $oggi -ExcelPathForVBA $Global:ExcelFilePath
        }
    }
} catch {
    $errorMessage = "Errore script: `n" + $_.Exception.Message
    if ($_.Exception.StackTrace) { $errorMessage += "`n`nStackTrace: `n" + $_.Exception.StackTrace }
    [System.Windows.Forms.MessageBox]::Show($errorMessage, "Errore Script PowerShell", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
} finally {
    # Pulizia finale degli oggetti COM di lettura, nel caso non sia stata fatta prima (es. errore precoce)
    if ($wsReader -ne $null) {
        $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($wsReader)
        $wsReader = $null # Evita tentativi multipli di rilascio
    }
    if ($workbookReader -ne $null) {
        try {
            if (($workbookReader.Saved -eq $false) -and ($workbookReader.ReadOnly -eq $false)){
                 $workbookReader.Close($false)
            } else {
                 $workbookReader.Close()
            }
        } catch { Write-Warning "Avviso nel blocco finally: Impossibile chiudere workbookReader. Potrebbe essere già chiuso. Dettagli: $($_.Exception.Message)"}
        $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($workbookReader)
        $workbookReader = $null # Evita tentativi multipli di rilascio
    }
    if ($excelAppReader -ne $null) {
        try {
            $excelAppReader.Quit()
        } catch { Write-Warning "Avviso nel blocco finally: Impossibile fare Quit su excelAppReader. Potrebbe essere già chiuso. Dettagli: $($_.Exception.Message)"}
        $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excelAppReader)
        $excelAppReader = $null # Evita tentativi multipli di rilascio
    }

    Remove-Variable excelAppReader, workbookReader, wsReader -ErrorAction SilentlyContinue

    [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}
"""

        # Replace placeholder
        ps_script = ps_script.replace("__FILE_PATH_PLACEHOLDER__", path.replace("\\", "\\\\"))

        try:
            # Create temp file with .ps1 extension
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False, encoding='utf-8') as tmp:
                tmp.write(ps_script)
                tmp_path = tmp.name

            # Execute with PowerShell
            # -ExecutionPolicy Bypass to allow running the script
            # Use subprocess.Popen to run detached or check output?
            # Since it opens WinForms, it might block. We probably want it non-blocking or simple call.
            subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-File", tmp_path], shell=True)

            # Note: We cannot easily delete the temp file immediately if Popen is async.
            # It will linger in temp, which is acceptable or we use a cleanup mechanism.

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile avviare l'analisi:\n{e}")
