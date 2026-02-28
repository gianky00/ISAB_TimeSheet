from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.audit_manager import AuditManager
from src.core.employees import employee_manager
from src.core.sync_tracker import SyncTracker
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import SearchInput, StandardInput, StandardTable
from src.gui.widgets.modern_button import ModernButton


class EmployeeEditorDialog(QDialog):
    """Dialog per aggiunta/modifica dipendente."""

    def __init__(self, parent=None, employee_data=None):
        super().__init__(parent)
        self.setWindowTitle("Scheda Dipendente")
        self.setMinimumWidth(400)
        self.data = employee_data or {}
        self.mode = "edit" if employee_data else "add"

        main_layout = QVBoxLayout(self)
        self.main_layout = main_layout  # User custom member

        form = QFormLayout()
        self.inputs = {}

        fields = [
            ("Cognome", "cognome"),
            ("Nome", "nome"),
            ("Data Nascita (GG/MM/AAAA)", "data_nascita"),
            ("Codice Fiscale", "codice_fiscale"),
            ("Badge", "badge"),
            ("Data Assunzione (GG/MM/AAAA)", "data_assunzione"),
        ]

        for label, key in fields:
            le = StandardInput()
            if self.data.get(key):
                le.setText(str(self.data.get(key)))
            self.inputs[key] = le
            form.addRow(label, le)

        main_layout.addLayout(form)

        # Bottoni Custom con stile ModernButton
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        self.btn_cancel = ModernButton("Annulla", variant=ModernButton.Variant.GHOST)
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancel)

        self.btn_save = ModernButton("Salva", variant=ModernButton.Variant.SUCCESS)
        self.btn_save.clicked.connect(self.accept)
        btn_layout.addWidget(self.btn_save)

        main_layout.addLayout(btn_layout)

    def get_data(self):
        """Estrae i dati inseriti nei campi di input e li normalizza in maiuscolo."""
        return {k: v.text().strip().upper() for k, v in self.inputs.items()}


class DipendentiManagerPanel(QWidget):
    """
    Pannello di gestione CRUD Dipendenti.
    """

    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DipendentiManagerPanel")

        # Widget members (Strict Typing - Option D)
        self.lbl_count: QLabel
        self.search_bar: QLineEdit
        self.lbl_sync_status: QLabel
        self.btn_sync: ModernButton
        self.btn_add: ModernButton
        self.table: QTableWidget

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self._setup_header()
        self._setup_toolbar()
        self._setup_table()

        # Caricamento dati differito per non bloccare la UI all'avvio
        QTimer.singleShot(100, self.refresh_data)

    def _setup_header(self):
        header_layout = QHBoxLayout()

        title = QLabel("Gestione Dipendenti")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLORS['text_dark']};")

        subtitle = QLabel("Visualizza e modifica l'anagrafica del personale.")
        subtitle.setStyleSheet(f"font-size: 14px; color: {COLORS['text_muted']};")

        text_layout = QVBoxLayout()
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        header_layout.addLayout(text_layout)
        header_layout.addStretch()

        # Stats rapide (Badge)
        self.lbl_count = QLabel("0 Dipendenti")
        self.lbl_count.setStyleSheet(
            f"""
            background-color: {COLORS["bg_hover"]}; color: {COLORS["text_dark"]};
            padding: 5px 15px; border-radius: 15px; font-weight: bold;
        """
        )
        header_layout.addWidget(self.lbl_count)

        self.main_layout.addLayout(header_layout)

    def _setup_toolbar(self):
        self.toolbar_card = QFrame()
        self.toolbar_card.setObjectName("filterBar")
        from src.gui.styles import LABEL_MUTED, LINEEDIT_STYLE

        self.toolbar_card.setStyleSheet(f"""
            QFrame#filterBar {{
                background-color: {COLORS["bg_white"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 12px;
            }}
        """)
        toolbar_layout = QHBoxLayout(self.toolbar_card)
        toolbar_layout.setContentsMargins(15, 10, 15, 10)
        toolbar_layout.setSpacing(15)

        # Sezione Ricerca
        search_v = QVBoxLayout()
        search_v.setSpacing(4)
        lbl_search = QLabel("CERCA DIPENDENTE")
        lbl_search.setStyleSheet(LABEL_MUTED)
        self.search_bar = SearchInput()
        self.search_bar.setPlaceholderText("Nome, Badge o CF...")
        self.search_bar.setFixedWidth(300)
        self.search_bar.setStyleSheet(LINEEDIT_STYLE)
        self.search_bar.textChanged.connect(self._filter_table)
        search_v.addWidget(lbl_search)
        search_v.addWidget(self.search_bar)
        toolbar_layout.addLayout(search_v)

        toolbar_layout.addStretch()

        # Info & Actions
        info_v = QVBoxLayout()
        info_v.setSpacing(4)
        info_v.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Sync Status
        self.lbl_sync_status = QLabel("")
        self.lbl_sync_status.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        info_v.addWidget(self.lbl_sync_status)

        actions_h = QHBoxLayout()
        actions_h.setSpacing(8)

        self.btn_sync = ModernButton(
            "SYNC CSV",
            variant=ModernButton.Variant.SECONDARY,
            size=ModernButton.Size.SMALL,
        )
        self.btn_sync.clicked.connect(self._sync_from_csv)

        self.btn_add = ModernButton(
            "NUOVO DIPENDENTE",
            variant=ModernButton.Variant.SUCCESS,
            size=ModernButton.Size.SMALL,
        )
        self.btn_add.clicked.connect(self._add_employee)

        actions_h.addWidget(self.btn_sync)
        actions_h.addWidget(self.btn_add)
        info_v.addLayout(actions_h)

        toolbar_layout.addLayout(info_v)
        self.main_layout.addWidget(self.toolbar_card)

    def _setup_table(self):
        self.table = StandardTable()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Cognome", "Nome", "Badge", "Codice Fiscale", "Assunzione"]
        )

        # Stile Tabella
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        v_header = self.table.verticalHeader()
        if v_header is None:
            raise RuntimeError("Table vertical header is None")
        v_header.setVisible(False)
        h_header = self.table.horizontalHeader()
        if h_header is None:
            raise RuntimeError("Table horizontal header is None")
        h_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        h_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID stretto
        h_header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Badge stretto

        # Use global styles from light.qss
        # self.table.setStyleSheet(...)

        self.table.doubleClicked.connect(self._edit_selected)

        self.main_layout.addWidget(self.table)

    def refresh_data(self):
        """Ricarica i dati dal DB."""
        try:
            self.lbl_sync_status.setText(f"Ultimo Sync: {SyncTracker.get_formatted_status('dipendenti')}")
            employees = employee_manager.get_all_employees()
            self.table.setRowCount(0)

            for row in employees:
                idx = self.table.rowCount()
                self.table.insertRow(idx)

                # Mapping colonne: ID, Cognome, Nome, Badge, CF, Assunzione
                items = [
                    QTableWidgetItem(str(row["id_risorsa"])),
                    QTableWidgetItem(row["cognome"]),
                    QTableWidgetItem(row["nome"]),
                    QTableWidgetItem(str(row["badge"] or "")),
                    QTableWidgetItem(row["codice_fiscale"] or ""),
                    QTableWidgetItem(row["data_assunzione"] or ""),
                ]

                for col_idx, item in enumerate(items):
                    self.table.setItem(idx, col_idx, item)

                # Colorazione se inattivo (opzionale, se avessimo il campo stato)
                # if not row['monitoraggio_attivo']:

            self.lbl_count.setText(f"{len(employees)} Dipendenti")
            self._filter_table(self.search_bar.text())  # Riapplica filtro se presente

        except Exception as e:
            ConfirmationDialog.show_error(self, "Errore", f"Impossibile caricare i dati: {e}")

    def _filter_table(self, text):
        """Filtra la tabella in locale con supporto multi-termine (AND logico)."""
        search_terms = text.lower().split()
        if not search_terms:
            for i in range(self.table.rowCount()):
                self.table.setRowHidden(i, False)
            return

        for i in range(self.table.rowCount()):
            # Costruiamo una stringa unica con tutto il contenuto della riga
            row_vals = []
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                if item:
                    row_vals.append(item.text().lower())
            row_content = " ".join(row_vals)

            # Verifichiamo che TUTTI i termini cercati siano presenti nella riga
            match = all(term in row_content for term in search_terms)
            self.table.setRowHidden(i, not match)

    def _sync_from_csv(self):
        """Permette di selezionare un file CSV e avvia l'importazione."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona Anagrafica Dipendenti",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )

        if not file_path:
            return

        try:
            count = employee_manager.import_from_csv(file_path)
            ConfirmationDialog.show_info(self, "Sync Completato", f"Importati/Aggiornati {count} dipendenti.")
            self.refresh_data()
            self.data_changed.emit()
            AuditManager.instance().log_action(
                "Sync CSV", "dipendenti", "Manuale", {"file": file_path, "count": count}
            )
        except Exception as e:
            ConfirmationDialog.show_warning(self, "Errore Sync", f"Errore durante l'importazione:\n{e}")

    def _add_employee(self):
        dialog = EmployeeEditorDialog(self)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if employee_manager.add_employee(data):
                AuditManager.instance().log_action(
                    action="ADD_EMPLOYEE",
                    category="dipendenti",
                    entity=data.get("badge", "-"),
                    status="SUCCESS",
                    params=str(data),
                )
                self.refresh_data()
                self.data_changed.emit()
            else:
                ConfirmationDialog.show_warning(
                    self,
                    "Errore",
                    "Errore durante l'inserimento nel DB (forse ID duplicato?)",
                )

    def _edit_selected(self):
        selection_model = self.table.selectionModel()
        if selection_model is None:
            raise RuntimeError("Table selection model is None")
        rows = selection_model.selectedRows()
        if not rows:
            return

        row_idx = rows[0].row()
        id_item = self.table.item(row_idx, 0)
        if id_item is None:
            raise RuntimeError(f"Table item at row {row_idx}, column 0 is None")
        id_risorsa = id_item.text()

        # Recuperiamo dati completi
        def get_item_text(r, c):
            it = self.table.item(r, c)
            return it.text() if it else ""

        current_data = {
            "id_risorsa": id_risorsa,
            "cognome": get_item_text(row_idx, 1),
            "nome": get_item_text(row_idx, 2),
            "badge": get_item_text(row_idx, 3),
            "codice_fiscale": get_item_text(row_idx, 4),
            "data_assunzione": get_item_text(row_idx, 5),
        }

        dlg = EmployeeEditorDialog(self, current_data)
        if dlg.exec():
            new_data = dlg.get_data()
            if employee_manager.update_employee(int(id_risorsa), new_data):
                self.refresh_data()
                self.data_changed.emit()
                AuditManager.instance().log_action("Modifica Dipendente", "dipendenti", id_risorsa)
            else:
                ConfirmationDialog.show_warning(self, "Errore", "Impossibile aggiornare i dati.")
