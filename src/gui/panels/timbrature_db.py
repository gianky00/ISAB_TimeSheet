"""
SyncroJob - Timbrature Database Panel
Pannello per la visualizzazione del Database Timbrature Isab con architettura Master-Detail.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional, Tuple

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage
from src.core import config_manager
from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.gui.formatters import FastTableModel, format_date_it
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon


class TimbratureDBPanel(QWidget):
    """Pannello per la visualizzazione del Database Timbrature Isab con architettura Master-Detail."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_path = config_manager.CONFIG_DIR / "data" / "timbrature_Isab.db"
        self.storage = TimbratureStorage(self.db_path)

        # Load configurable lists
        self.lists = self.storage.get_lists()
        self.reparti = self.lists.get("reparti", [])
        self.cantieri = self.lists.get("cantieri", [])

        # Colonne della Tabella (Vista Master)
        self.master_headers = [
            "Data",
            "Cognome",
            "Nome",
            "Ingresso",
            "Uscita",
            "Reparto",
            "Cantiere",
        ]

        # Mapping completo per il Dettaglio (Tutte le 18 colonne rilevate)
        self.full_headers = [
            "Data",
            "Ingresso",
            "Uscita",
            "Nome",
            "Cognome",
            "Codice Fiscale",
            "ID Dipendente",
            "Fornitore",
            "Numero Badge",
            "Reparto",
            "Cantiere",
            "Presenza TS",
            "Sito",
            "Codice RILPRES",
            "Codice Qualifica",
            "Specializzazione",
            "Società Ospitante",
            "Data Inserimento",
        ]

        self.model = FastTableModel([], self.master_headers)
        # Configure Date Formatter for Col 0 (Data)
        self.model.set_column_formatter(0, format_date_it)

        self._raw_full_data = []  # Buffer per i dati completi

        self._setup_ui()
        # Pre-caricamento immediato e profondo
        QTimer.singleShot(50, self.refresh_data)

    def _setup_ui(self):
        """Configura l'interfaccia utente."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setProperty("class", "Level2Tabs")  # Clean Style

        # --- UNIFIED TOOLBAR (Corner Widget) ---
        self.toolbar_container = QWidget()
        toolbar_layout = QHBoxLayout(self.toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setFixedWidth(200)
        self.search_input.textChanged.connect(lambda: self.refresh_data())

        # Reparto Filter
        self.reparto_filter = QComboBox()
        self.reparto_filter.addItem("Tutti i reparti", "Tutti")
        for rep in self.reparti:
            self.reparto_filter.addItem(rep, rep)
        self.reparto_filter.currentIndexChanged.connect(lambda: self.refresh_data())
        self.reparto_filter.setMinimumWidth(130)

        # Cantiere Filter
        self.cantiere_filter = QComboBox()
        self.cantiere_filter.addItem("Tutti i cantieri", "Tutti")
        for cant in self.cantieri:
            self.cantiere_filter.addItem(cant, cant)
        self.cantiere_filter.currentIndexChanged.connect(lambda: self.refresh_data())
        self.cantiere_filter.setMinimumWidth(130)

        # Import Button
        import_btn = QPushButton("Importa")
        import_btn.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), "#FFFFFF"))
        import_btn.setFixedSize(90, 32)
        import_btn.clicked.connect(self._import_excel_manually)

        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(self.reparto_filter)
        toolbar_layout.addWidget(self.cantiere_filter)
        toolbar_layout.addWidget(import_btn)

        self.tabs.setCornerWidget(self.toolbar_container, Qt.Corner.TopRightCorner)

        # --- TAB 1: Database (Master-Detail) ---
        self.tab_database = QWidget()
        self._setup_database_tab(self.tab_database)
        self.tabs.addTab(
            self.tab_database,
            get_colored_icon(get_asset_path(Icons.DATABASE), "#546E7A"),
            "Database",
        )

        # --- TAB 2: Impostazioni (Dipendenti) ---
        self.tab_settings = QWidget()
        self._setup_settings_tab(self.tab_settings)
        self.tabs.addTab(
            self.tab_settings,
            get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), "#546E7A"),
            "Impostazioni",
        )

        # Connect tab change
        self.tabs.currentChanged.connect(self._on_tab_changed)

        self.main_layout.addWidget(self.tabs)

    def _setup_database_tab(self, parent_widget):
        from PyQt6.QtWidgets import QFormLayout, QScrollArea, QSplitter

        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(0, 5, 0, 0)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- TABELLA (MASTER) ---
        self.db_table = QTableView()
        self.db_table.setModel(self.model)
        self.db_table.verticalHeader().setVisible(False)
        self.db_table.setAlternatingRowColors(True)
        self.db_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.db_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.db_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.db_table.setSortingEnabled(True)

        header = self.db_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)

        self.db_table.selectionModel().selectionChanged.connect(
            self._on_selection_changed
        )
        self.splitter.addWidget(self.db_table)

        # --- PANNELLO DETTAGLIO (DETAIL) ---
        detail_container = QWidget()
        detail_layout = QVBoxLayout(detail_container)
        detail_layout.setContentsMargins(10, 0, 5, 0)

        detail_title = QLabel("Dettaglio Timbratura")
        detail_title.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: #2196F3; margin-bottom: 5px;"
        )
        detail_layout.addWidget(detail_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.form_layout = QFormLayout(scroll_content)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.form_layout.setSpacing(10)

        self.detail_labels = {}
        for h in self.full_headers:
            val_label = QLabel("-")
            val_label.setWordWrap(True)
            val_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            self.detail_labels[h] = val_label
            self.form_layout.addRow(f"<b>{h}:</b>", val_label)

        scroll.setWidget(scroll_content)
        detail_layout.addWidget(scroll)

        self.splitter.addWidget(detail_container)
        self.splitter.setStretchFactor(0, 3)  # Ridotto stretch tabella
        self.splitter.setStretchFactor(
            1, 2
        )  # Aumentato stretch dettaglio per leggibilità

        layout.addWidget(self.splitter)

    def _on_selection_changed(self, selected, _deselected):
        """Aggiorna il pannello dettaglio quando si seleziona una riga."""
        indexes = self.db_table.selectionModel().selectedRows()
        if not indexes:
            return

        # Use the UserRole to get the original row data/index intact after sorting
        # The model returns the METADATA object for UserRole
        row_data = indexes[0].data(Qt.ItemDataRole.UserRole)

        if row_data:
            # We stored the FULL RAW ROW tuple as metadata
            data = row_data

            # Indices source:
            # 0:data, 1:ingresso, 2:uscita, 3:nome, 4:cognome, 5:presenza_ts, 6:sito,
            # 7:cf, 8:id_dip, 9:fornitore, 10:cod_rilpres, 11:num_badge, 12:cod_qual,
            # 13:specializ, 14:soc_osp, 15:data_ins, 16:rep, 17:cant

            mapping = {
                "Data": 0,
                "Ingresso": 1,
                "Uscita": 2,
                "Nome": 3,
                "Cognome": 4,
                "Codice Fiscale": 7,
                "ID Dipendente": 8,
                "Fornitore": 9,
                "Numero Badge": 11,
                "Reparto": 16,
                "Cantiere": 17,
                "Presenza TS": 5,
                "Sito": 6,
                "Codice RILPRES": 10,
                "Codice Qualifica": 12,
                "Specializzazione": 13,
                "Società Ospitante": 14,
                "Data Inserimento": 15,
            }

            for h in self.full_headers:
                idx = mapping.get(h)
                val = (
                    str(data[idx]) if idx is not None and data[idx] is not None else ""
                )

                if val.lower() in ["nan", "none"]:
                    val = ""

                # Formattazione speciale Data
                if h == "Data" and val:
                    try:
                        dt = datetime.strptime(val, "%Y-%m-%d")
                        val = dt.strftime("%d/%m/%Y")
                    except Exception:
                        pass
                        try:
                            date_part = val.split(" ")[0]
                            dt = datetime.strptime(date_part, "%Y-%m-%d")
                            val = dt.strftime("%d/%m/%Y")
                        except Exception:
                            pass

                # Formattazione speciale Data Inserimento
                if h == "Data Inserimento" and val:
                    try:
                        # Estraiamo solo la parte data se presente l'ora
                        date_part = val.split(" ")[0]
                        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                            try:
                                dt = datetime.strptime(date_part, fmt)
                                val = dt.strftime("%d/%m/%Y")
                                break
                            except ValueError:
                                continue
                    except Exception:
                        pass

                self.detail_labels[h].setText(val)

    def refresh_data(self):
        """Carica i dati dal DB e aggiorna il modello virtuale."""
        text = self.search_input.text()
        reparto = self.reparto_filter.currentData()
        cantiere = self.cantiere_filter.currentData()

        # Recuperiamo i dati completi
        rows = self.storage.get_timbrature_with_reparto(
            limit=2000,
            filter_text=text,
            filter_reparto=reparto,
            filter_cantiere=cantiere,
        )
        self._raw_full_data = rows

        # Formattazione per la vista Master
        # Headers: Data, Cognome, Nome, Ingresso, Uscita, Reparto, Cantiere
        # Source indices: 0, 4, 3, 1, 2, 16, 17
        master_rows = []
        for row in rows:
            # Mantieni la data in formato ISO (YYYY-MM-DD) per l'ordinamento corretto
            # La visualizzazione sarà gestita dal formatter (format_date_it)
            iso_date = str(row[0]).split(" ")[0] if row[0] else ""

            m_row = [
                iso_date,  # Raw ISO Date
                row[4] or "",  # Cognome
                row[3] or "",  # Nome
                row[1] or "",  # Ingresso
                row[2] or "",  # Uscita
                row[16] or "",  # Reparto
                row[17] or "",  # Cantiere
            ]
            master_rows.append(m_row)

        # Pass master_rows as Data, and raw 'rows' as Metadata (UserRole)
        # This links the Visual Row to the Full Source Row securely
        self.model.update_data(master_rows, new_metadata=rows)
        # Ottimizza colonne dopo il caricamento
        QTimer.singleShot(0, lambda: self.db_table.resizeColumnsToContents())

    def _setup_settings_tab(self, parent_widget):
        layout = QVBoxLayout(parent_widget)

        # Header Controls
        header_layout = QHBoxLayout()

        info = QLabel("Gestione Dipendenti")
        info.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(info)

        header_layout.addStretch()

        # Open Settings Button
        open_settings_btn = ModernButton(
            "Gestisci Liste",
            variant=ModernButton.Variant.SECONDARY,
            size=ModernButton.Size.SMALL,
        )
        open_settings_btn.setToolTip("Gestisci reparti e cantieri nelle Impostazioni")
        open_settings_btn.clicked.connect(self._open_settings)
        header_layout.addWidget(open_settings_btn)

        layout.addLayout(header_layout)

        sub = QLabel(
            "Assegna Reparto e Cantiere ai dipendenti. Modifiche salvate automaticamente."
        )
        sub.setStyleSheet("color: #6c757d; margin-bottom: 5px;")
        layout.addWidget(sub)

        # Filters for Settings
        filter_layout = QHBoxLayout()
        self.filter_empty_cb = QCheckBox("Mostra solo dati mancanti (Vuoti)")

        # Load saved state
        config = config_manager.load_config()
        self.filter_empty_cb.setChecked(
            config.get("timbrature_filter_empty_only", False)
        )

        self.filter_empty_cb.stateChanged.connect(self._on_filter_empty_changed)
        filter_layout.addWidget(self.filter_empty_cb)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Table
        self.settings_table = QTableWidget()
        self.settings_table.verticalHeader().setVisible(False)
        self.settings_table.setColumnCount(4)
        self.settings_table.setHorizontalHeaderLabels(
            ["Nome", "Cognome", "Reparto", "Cantiere"]
        )

        header = self.settings_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.settings_table)

    def _on_filter_empty_changed(self, state):
        """Save preference and reload settings table."""
        config_manager.set_config_value(
            "timbrature_filter_empty_only", self.filter_empty_cb.isChecked()
        )
        self._load_settings_data()

    def _on_tab_changed(self, index):
        # Toggle toolbar visibility based on tab
        if index == 0:  # Database
            if hasattr(self, "toolbar_container"):
                self.toolbar_container.show()
            self.refresh_data()
        else:  # Settings
            if hasattr(self, "toolbar_container"):
                self.toolbar_container.hide()
            self._load_settings_data()

    def _open_settings(self):
        """Naviga verso il pannello impostazioni della finestra principale."""
        main_window = self.window()
        if hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def _manage_list(self, list_key, title):
        """Dialog generico per gestire liste di stringhe."""
        current_list = self.lists.get(list_key, [])

        d = QDialog(self)
        d.setWindowTitle(title)
        d.setMinimumWidth(300)
        layout = QVBoxLayout(d)

        list_widget = QListWidget()
        list_widget.addItems(current_list)
        layout.addWidget(list_widget)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Aggiungi")
        del_btn = QPushButton("Rimuovi")
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        layout.addLayout(btn_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(d.accept)
        layout.addWidget(button_box)

        def add_item():
            text, ok = QInputDialog.getText(d, "Aggiungi", "Nome:")
            if ok and text:
                text = text.upper()
                if text not in current_list:
                    current_list.append(text)
                    list_widget.addItem(text)
                    self.storage.save_lists(self.lists)
                    self._update_combo_boxes()

        def del_item():
            row = list_widget.currentRow()
            if row >= 0:
                item = list_widget.takeItem(row)
                val = item.text()
                if val in current_list:
                    current_list.remove(val)
                    self.storage.save_lists(self.lists)
                    self._update_combo_boxes()

        add_btn.clicked.connect(add_item)
        del_btn.clicked.connect(del_item)

        d.exec()

    def _update_combo_boxes(self):
        """Aggiorna i filtri e le combo nella tabella."""
        # Refresh local cache
        self.reparti = self.lists.get("reparti", [])
        self.cantieri = self.lists.get("cantieri", [])

        # Update Main Filters
        self.reparto_filter.blockSignals(True)
        self.reparto_filter.clear()
        self.reparto_filter.addItem("Tutti i reparti", "Tutti")
        for rep in self.reparti:
            self.reparto_filter.addItem(rep, rep)
        self.reparto_filter.blockSignals(False)

        self.cantiere_filter.blockSignals(True)
        self.cantiere_filter.clear()
        self.cantiere_filter.addItem("Tutti i cantieri", "Tutti")
        for cant in self.cantieri:
            self.cantiere_filter.addItem(cant, cant)
        self.cantiere_filter.blockSignals(False)

        # Refresh Settings Table Combos (Reload data)
        self._load_settings_data()

    def _load_settings_data(self):
        """Carica i dipendenti unici nella tabella impostazioni."""
        employees = self.storage.get_employees()
        show_empty_only = self.filter_empty_cb.isChecked()

        self.settings_table.blockSignals(True)
        self.settings_table.setRowCount(0)

        # Filter list first
        filtered_employees = []
        for emp in employees:
            if show_empty_only:
                # Se entrambi sono pieni, salta
                if emp["reparto"] and emp["cantiere"]:
                    continue
            filtered_employees.append(emp)

        for i, emp in enumerate(filtered_employees):
            self.settings_table.insertRow(i)

            # Nome
            item_nome = QTableWidgetItem(emp["nome"])
            item_nome.setFlags(item_nome.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.settings_table.setItem(i, 0, item_nome)

            # Cognome
            item_cognome = QTableWidgetItem(emp["cognome"])
            item_cognome.setFlags(item_cognome.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.settings_table.setItem(i, 1, item_cognome)

            combo_rep = QComboBox()
            combo_rep.addItems([""] + self.reparti)
            combo_rep.setCurrentText(emp["reparto"])
            combo_rep.setStyleSheet(
                "QComboBox { border: none; background: transparent; }"
            )

            combo_cant = QComboBox()
            combo_cant.addItems([""] + self.cantieri)
            combo_cant.setCurrentText(emp["cantiere"])
            combo_cant.setStyleSheet(
                "QComboBox { border: none; background: transparent; }"
            )

            # Connect signals with closures
            nome = emp["nome"]
            cognome = emp["cognome"]

            # Update Reparto
            combo_rep.currentTextChanged.connect(
                lambda text, n=nome, c=cognome: self.storage.update_employee_details(
                    n, c, reparto=text
                )
            )

            # Update Cantiere
            combo_cant.currentTextChanged.connect(
                lambda text, n=nome, c=cognome: self.storage.update_employee_details(
                    n, c, cantiere=text
                )
            )

            self.settings_table.setCellWidget(i, 2, combo_rep)
            self.settings_table.setCellWidget(i, 3, combo_cant)

        self.settings_table.blockSignals(False)

    def _import_excel_manually(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona File Excel Timbrature",
            str(Path.home() / "Downloads"),
            "Excel Files (*.xlsx *.xls)",
        )

        if not file_path:
            return

        try:

            def gui_log(msg):
                print(msg)

            success = self.storage.import_excel(file_path, gui_log)

            if success:
                AuditManager.instance().log_action(
                    "Importazione Manuale Timbrature",
                    category="database",
                    params={"file": Path(file_path).name},
                )
                self.refresh_data()
                ToastManager.instance().show(
                    "Dati importati correttamente nel database.", "success"
                )
                self._load_settings_data()
            else:
                ToastManager.instance().show("Impossibile importare il file.", "error")

        except Exception as e:
            ToastManager.instance().show(f"Errore durante l'importazione: {e}", "error")
