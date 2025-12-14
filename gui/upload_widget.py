from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout)
from PySide6.QtCore import Qt, Signal

class UploadWidget(QWidget):
    # Signal to start the login process (empty list task)
    start_upload_signal = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        info_lbl = QLabel("Funzionalità Carico TS:\n\n"
                          "1. Il Bot aprirà il browser e farà il login automatico\n"
                          "2. Navigherà a Gestione Timesheet\n"
                          "3. Per ogni riga nel Database (stato='da_processare'):\n"
                          "   - Inserirà il Numero OdA\n"
                          "   - Cliccherà su 'Estrai OdA'\n"
                          "   - Se trovato: cliccherà sull'icona link\n"
                          "   - Se non trovato: aggiornerà lo stato a 'errore'\n\n"
                          "Lo stato delle righe sarà aggiornato in tempo reale nella tab Database.")
        info_lbl.setAlignment(Qt.AlignLeft)
        info_lbl.setWordWrap(True)
        layout.addWidget(info_lbl)

        layout.addStretch()

        self.start_btn = QPushButton("Avvia Carica TS")
        self.start_btn.setFixedHeight(40)
        self.start_btn.setStyleSheet("font-weight: bold; background-color: #2196F3; color: white;")
        self.start_btn.clicked.connect(self.on_start_clicked)

        layout.addWidget(self.start_btn)
        layout.addStretch()

        self.setLayout(layout)

    def on_start_clicked(self):
        self.start_upload_signal.emit()
