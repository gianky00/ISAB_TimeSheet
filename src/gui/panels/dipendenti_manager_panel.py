from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.audit_manager import AuditManager
from src.core.employees import employee_manager
from src.gui.widgets.modern_button import ModernButton


class EmployeeEditorDialog(QDialog):
    """Dialog per aggiunta/modifica dipendente."""

    def __init__(self, parent=None, employee_data=None):
        super().__init__(parent)
        self.setWindowTitle("Scheda Dipendente")
        self.setMinimumWidth(400)
        self.data = employee_data or {}
        self.mode = "edit" if employee_data else "add"

        self.layout = QVBoxLayout(self)

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
            le = QLineEdit()
            if self.data.get(key):
                le.setText(str(self.data.get(key)))
            self.inputs[key] = le
            form.addRow(label, le)

        self.layout.addLayout(form)

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

        self.layout.addLayout(btn_layout)

    def get_data(self):
        return {k: v.text().strip().upper() for k, v in self.inputs.items()}


class DipendentiManagerPanel(QWidget):
    """
    Pannello di gestione CRUD Dipendenti.
    """

    data_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DipendentiManagerPanel")

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
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")

        subtitle = QLabel("Visualizza e modifica l'anagrafica del personale.")
        subtitle.setStyleSheet("font-size: 14px; color: #666;")

        text_layout = QVBoxLayout()
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        header_layout.addLayout(text_layout)
        header_layout.addStretch()

        # Stats rapide (Badge)
        self.lbl_count = QLabel("0 Dipendenti")
        self.lbl_count.setStyleSheet(
            """
            background-color: #e9ecef; color: #495057;
            padding: 5px 15px; border-radius: 15px; font-weight: bold;
        """
        )
        header_layout.addWidget(self.lbl_count)

        self.main_layout.addLayout(header_layout)

    def _setup_toolbar(self):
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        # Ricerca
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cerca per nome, badge o CF...")
        self.search_bar.setFixedWidth(300)
        self.search_bar.setStyleSheet(
            """
            QLineEdit { padding: 8px; border: 1px solid #ced4da; border-radius: 4px; }
            QLineEdit:focus { border: 1px solid #0d6efd; }
        """
        )
        self.search_bar.textChanged.connect(self._filter_table)
        toolbar.addWidget(self.search_bar)

        toolbar.addStretch()

        # Bottoni
        self.btn_refresh = ModernButton("Aggiorna", variant=ModernButton.Variant.GHOST)
        self.btn_refresh.clicked.connect(self.refresh_data)
        toolbar.addWidget(self.btn_refresh)

        self.btn_sync = ModernButton("Sync da CSV", variant=ModernButton.Variant.SECONDARY)
        self.btn_sync.clicked.connect(self._sync_from_csv)
        toolbar.addWidget(self.btn_sync)

        self.btn_add = ModernButton("Nuovo Dipendente", variant=ModernButton.Variant.PRIMARY)
        self.btn_add.clicked.connect(self._add_employee)
        toolbar.addWidget(self.btn_add)

        self.main_layout.addLayout(toolbar)

    def _setup_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Cognome", "Nome", "Badge", "Codice Fiscale", "Assunzione"]
        )

        # Stile Tabella
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )  # ID stretto
        self.table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )  # Badge stretto

        self.table.setStyleSheet(
            """
            QTableWidget { border: 1px solid #dee2e6; border-radius: 4px; background: white; }
            QHeaderView::section { background-color: #f8f9fa; padding: 8px; border: none; font-weight: bold; }
            QTableWidget::item { padding: 5px; }
            QTableWidget::item:selected { background-color: #e7f1ff; color: #000; }
        """
        )

        self.table.doubleClicked.connect(self._edit_selected)

        self.main_layout.addWidget(self.table)

    def refresh_data(self):
        """Ricarica i dati dal DB."""
        try:
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
                #    for i in range(6): self.table.item(idx, i).setForeground(QBrush(QColor("gray")))

            self.lbl_count.setText(f"{len(employees)} Dipendenti")
            self._filter_table(self.search_bar.text())  # Riapplica filtro se presente

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile caricare i dati: {e}")

    def _filter_table(self, text):
        """Filtra la tabella in locale con supporto multi-termine (AND logico)."""
        search_terms = text.lower().split()
        if not search_terms:
            for i in range(self.table.rowCount()):
                self.table.setRowHidden(i, False)
            return

        for i in range(self.table.rowCount()):
            # Costruiamo una stringa unica con tutto il contenuto della riga
            row_content = " ".join(
                self.table.item(i, j).text().lower()
                for j in range(self.table.columnCount())
                if self.table.item(i, j)
            )

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
            QMessageBox.information(self, "Sync Completato", f"Importati/Aggiornati {count} dipendenti.")
            self.refresh_data()
            self.data_changed.emit()
            AuditManager.instance().log_action(
                "Sync CSV", "dipendenti", "Manuale", {"file": file_path, "count": count}
            )
        except Exception as e:
            QMessageBox.warning(self, "Errore Sync", f"Errore durante l'importazione:\n{e}")

    def _add_employee(self):
        dlg = EmployeeEditorDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            if employee_manager.add_employee(data):
                self.refresh_data()
                self.data_changed.emit()
                AuditManager.instance().log_action(
                    "Aggiunta Dipendente",
                    "dipendenti",
                    f"{data['cognome']} {data['nome']}",
                )
            else:
                QMessageBox.warning(
                    self,
                    "Errore",
                    "Errore durante l'inserimento nel DB (forse ID duplicato?)",
                )

    def _edit_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return

        row_idx = rows[0].row()
        id_risorsa = self.table.item(row_idx, 0).text()

        # Recuperiamo dati completi
        # Qui facciamo un trucco: prendiamo i dati dalla tabella per velocità,
        # ma l'ideale sarebbe rileggere dal DB se ci sono campi nascosti.
        current_data = {
            "id_risorsa": id_risorsa,
            "cognome": self.table.item(row_idx, 1).text(),
            "nome": self.table.item(row_idx, 2).text(),
            "badge": self.table.item(row_idx, 3).text(),
            "codice_fiscale": self.table.item(row_idx, 4).text(),
            "data_assunzione": self.table.item(row_idx, 5).text(),
        }

        dlg = EmployeeEditorDialog(self, current_data)
        if dlg.exec():
            new_data = dlg.get_data()
            if employee_manager.update_employee(id_risorsa, new_data):
                self.refresh_data()
                self.data_changed.emit()
                AuditManager.instance().log_action("Modifica Dipendente", "dipendenti", id_risorsa)
            else:
                QMessageBox.warning(self, "Errore", "Impossibile aggiornare i dati.")
