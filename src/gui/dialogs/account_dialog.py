from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)

from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon


class AccountDialog(QDialog):
    """Dialog per aggiungere/modificare un account."""

    def __init__(self, parent=None, username="", password=""):
        super().__init__(parent)
        self.setWindowTitle("Account ISAB")
        self.setFixedWidth(350)
        self.setStyleSheet("font-size: 15px;")

        layout = QFormLayout(self)

        self.username_edit = QLineEdit(username)
        self.username_edit.setMinimumHeight(35)
        layout.addRow("Username:", self.username_edit)

        self.password_edit = QLineEdit(password)
        self.password_edit.setMinimumHeight(35)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        # Password layout with toggle
        pass_layout = QHBoxLayout()
        pass_layout.setContentsMargins(0, 0, 0, 0)
        pass_layout.setSpacing(5)

        pass_layout.addWidget(self.password_edit)

        self.toggle_pass_btn = QPushButton()
        self.toggle_pass_btn.setIcon(get_colored_icon(get_asset_path(Icons.EYE), "#000000"))
        self.toggle_pass_btn.setIconSize(QSize(20, 20))
        self.toggle_pass_btn.setToolTip("Mostra/Nascondi password")
        self.toggle_pass_btn.setFixedSize(35, 35)
        self.toggle_pass_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_pass_btn.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border: 1px solid black;
                border-radius: 4px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
            }
        """
        )
        self.toggle_pass_btn.clicked.connect(self._toggle_password_visibility)
        pass_layout.addWidget(self.toggle_pass_btn)

        layout.addRow("Password:", pass_layout)

        btns = QHBoxLayout()
        ok_btn = QPushButton("Salva")
        ok_btn.setMinimumHeight(35)
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Annulla")
        cancel_btn.setMinimumHeight(35)
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(ok_btn)
        btns.addWidget(cancel_btn)

        layout.addRow(btns)

    def _toggle_password_visibility(self):
        if self.password_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_pass_btn.setIcon(get_colored_icon(get_asset_path(Icons.LOCK), "#000000"))
            self.toggle_pass_btn.setToolTip("Nascondi password")
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_pass_btn.setIcon(get_colored_icon(get_asset_path(Icons.EYE), "#000000"))
            self.toggle_pass_btn.setToolTip("Mostra password")

    def get_data(self):
        return self.username_edit.text(), self.password_edit.text()
