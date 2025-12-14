from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                               QHeaderView, QMessageBox, QDateEdit, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, QDate

class DownloadWidget(QWidget):
    # Signal to start the bot: list of (oda, pos), data_da string
    start_download_signal = Signal(list, str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # --- Date Input Section ---
        date_layout = QHBoxLayout()
        date_lbl = QLabel("Data Inizio Timesheet:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        # Default to 01.01.2025 as per request, or can be dynamic
        self.date_edit.setDate(QDate(2025, 1, 1))

        date_layout.addWidget(date_lbl)
        date_layout.addWidget(self.date_edit)
        date_layout.addStretch()
        main_layout.addLayout(date_layout)

        # --- Table Section ---
        lbl = QLabel("Lista OdA da scaricare:")
        main_layout.addWidget(lbl)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Numero OdA", "Posizione OdA"])

        # Stretch columns to fill space
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        main_layout.addWidget(self.table)

        # --- Controls (Add/Remove) ---
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("+ Aggiungi Riga")
        add_btn.clicked.connect(self.add_row)

        remove_btn = QPushButton("- Rimuovi Riga")
        remove_btn.clicked.connect(self.remove_row)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        main_layout.addLayout(btn_layout)

        # --- Start Button ---
        self.start_btn = QPushButton("Avvia Scarico TS")
        self.start_btn.clicked.connect(self.on_start_clicked)
        self.start_btn.setFixedHeight(40)
        self.start_btn.setStyleSheet("font-weight: bold; background-color: #4CAF50; color: white;")
        main_layout.addWidget(self.start_btn)

        self.setLayout(main_layout)

        # Add a default starting row
        self.add_row()

    def add_row(self):
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        # Optional: Initialize with empty strings or specific widgets if needed,
        # but default QTableWidgetItem editing is sufficient.

    def remove_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
        else:
            # If no row selected, remove the last one?
            # Or show warning? User asked for "Remove selected",
            # let's try removing last if none selected for convenience,
            # or just require selection.
            # Behavior: Remove last if count > 0
            count = self.table.rowCount()
            if count > 0:
                self.table.removeRow(count - 1)

    def on_start_clicked(self):
        data_to_process = []
        rows = self.table.rowCount()

        for r in range(rows):
            item_oda = self.table.item(r, 0)
            item_pos = self.table.item(r, 1)

            oda = item_oda.text().strip() if item_oda else ""
            pos = item_pos.text().strip() if item_pos else ""

            if oda: # Only add if OdA is present
                data_to_process.append((oda, pos))

        if not data_to_process:
            QMessageBox.warning(self, "Attenzione", "Inserire almeno un Numero OdA.")
            return

        data_da = self.date_edit.date().toString("dd.MM.yyyy")

        # Emit signal to Main Window/Controller
        self.start_download_signal.emit(data_to_process, data_da)
