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

        info_lbl = QLabel("Funzionalità Carico TS:\n"
                          "Premi il pulsante sottostante per avviare il Login.\n"
                          "Il Bot si fermerà dopo l'accesso per permettere operazioni manuali.")
        info_lbl.setAlignment(Qt.AlignCenter)
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
