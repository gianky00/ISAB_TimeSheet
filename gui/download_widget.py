from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QScrollArea, QFrame,
                               QMessageBox, QDateEdit)
from PySide6.QtCore import Qt, Signal, QDate

class DownloadRow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.oda_input = QLineEdit()
        self.oda_input.setPlaceholderText("Numero OdA")

        self.pos_input = QLineEdit()
        self.pos_input.setPlaceholderText("Posizione OdA")

        layout.addWidget(self.oda_input)
        layout.addWidget(self.pos_input)

        self.setLayout(layout)

    def get_data(self):
        return self.oda_input.text().strip(), self.pos_input.text().strip()

class DownloadWidget(QWidget):
    # Signal to start the bot: list of (oda, pos), data_da string
    start_download_signal = Signal(list, str)

    def __init__(self):
        super().__init__()
        self.rows = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Date Input
        date_layout = QHBoxLayout()
        date_lbl = QLabel("Data Inizio Timesheet:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        # Default to 01.01.2025 as per previous hardcoded value, or current year start
        self.date_edit.setDate(QDate(2025, 1, 1))

        date_layout.addWidget(date_lbl)
        date_layout.addWidget(self.date_edit)
        date_layout.addStretch()
        main_layout.addLayout(date_layout)

        # Instruction Label
        lbl = QLabel("Inserisci fino a 20 righe di Numero OdA e Posizione OdA")
        main_layout.addWidget(lbl)

        # Scroll Area for rows
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.scroll_content)

        main_layout.addWidget(self.scroll)

        # Buttons Control
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("+ Aggiungi Riga")
        add_btn.clicked.connect(self.add_row)

        remove_btn = QPushButton("- Rimuovi Riga")
        remove_btn.clicked.connect(self.remove_row)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        main_layout.addLayout(btn_layout)

        # Start Button
        self.start_btn = QPushButton("Avvia Scarico TS")
        self.start_btn.clicked.connect(self.on_start_clicked)
        self.start_btn.setFixedHeight(40)
        self.start_btn.setStyleSheet("font-weight: bold; background-color: #4CAF50; color: white;")
        main_layout.addWidget(self.start_btn)

        self.setLayout(main_layout)

        # Add initial row
        self.add_row()

    def add_row(self):
        if len(self.rows) >= 20:
            QMessageBox.warning(self, "Limite Raggiunto", "Massimo 20 righe consentite.")
            return

        row = DownloadRow()
        self.scroll_layout.addWidget(row)
        self.rows.append(row)

    def remove_row(self):
        if not self.rows:
            return

        row = self.rows.pop()
        self.scroll_layout.removeWidget(row)
        row.deleteLater()

    def on_start_clicked(self):
        data_to_process = []
        for row in self.rows:
            oda, pos = row.get_data()
            if oda: # Only add if OdA is present
                data_to_process.append((oda, pos))

        if not data_to_process:
            QMessageBox.warning(self, "Attenzione", "Inserire almeno un Numero OdA.")
            return

        data_da = self.date_edit.date().toString("dd.MM.yyyy")

        # Emit signal to Main Window/Controller
        self.start_download_signal.emit(data_to_process, data_da)
