from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class ConfirmationDialog(QDialog):
    """Dialog di conferma personalizzato."""

    def __init__(self, parent=None, title="Conferma", message="Sei sicuro?"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(350)
        self.setStyleSheet("font-size: 15px; background-color: white;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Messaggio
        self.msg_label = QLabel(message)
        self.msg_label.setWordWrap(True)
        self.msg_label.setStyleSheet("color: #212529; font-weight: 500;")
        layout.addWidget(self.msg_label)

        # Pulsanti
        btns = QHBoxLayout()
        btns.setSpacing(10)

        self.ok_btn = QPushButton("Elimina")
        self.ok_btn.setMinimumHeight(40)
        self.ok_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """
        )
        self.ok_btn.clicked.connect(self.accept)

        self.cancel_btn = QPushButton("Annulla")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f8f9fa;
                color: #212529;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """
        )
        self.cancel_btn.clicked.connect(self.reject)

        btns.addWidget(self.ok_btn)
        btns.addWidget(self.cancel_btn)

        layout.addLayout(btns)
