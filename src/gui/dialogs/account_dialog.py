from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon


class AccountDialog(QDialog):
    """Dialog per aggiungere/modificare un account."""

    def __init__(self, parent: QWidget | None = None, username: str = "", password: str = "") -> None:
        super().__init__(parent)
        self.setWindowTitle("Account")
        self.setFixedWidth(350)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        # Main Layout (Vertical) instead of Form for better control
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        form = QFormLayout()
        form.setSpacing(10)

        self.username_edit = QLineEdit(username)
        self.username_edit.setMinimumHeight(35)
        form.addRow("Username:", self.username_edit)

        self.password_edit = QLineEdit(password)
        self.password_edit.setMinimumHeight(35)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        # Password layout with toggle
        pass_layout = QHBoxLayout()
        pass_layout.setContentsMargins(0, 0, 0, 0)
        pass_layout.setSpacing(5)

        pass_layout.addWidget(self.password_edit)

        self.toggle_pass_btn = QPushButton()
        self.toggle_pass_btn.setIcon(get_colored_icon(get_asset_path(Icons.EYE), "#555555"))
        self.toggle_pass_btn.setIconSize(QSize(20, 20))
        self.toggle_pass_btn.setToolTip("Mostra/Nascondi password")
        self.toggle_pass_btn.setFixedSize(35, 35)
        self.toggle_pass_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_pass_btn.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #adb5bd;
            }
        """
        )
        self.toggle_pass_btn.clicked.connect(self._toggle_password_visibility)
        pass_layout.addWidget(self.toggle_pass_btn)

        form.addRow("Password:", pass_layout)
        main_layout.addLayout(form)

        # Buttons
        btns = QHBoxLayout()
        btns.setSpacing(10)
        btns.addStretch()

        cancel_btn = ModernButton("Annulla", variant=ModernButton.Variant.GHOST)
        cancel_btn.clicked.connect(self.reject)

        ok_btn = ModernButton("Salva", variant=ModernButton.Variant.PRIMARY)
        ok_btn.clicked.connect(self.accept)

        btns.addWidget(cancel_btn)
        btns.addWidget(ok_btn)

        main_layout.addLayout(btns)

    def _toggle_password_visibility(self) -> None:
        if self.password_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_pass_btn.setIcon(get_colored_icon(get_asset_path(Icons.LOCK), "#555555"))
            self.toggle_pass_btn.setToolTip("Nascondi password")
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_pass_btn.setIcon(get_colored_icon(get_asset_path(Icons.EYE), "#555555"))
            self.toggle_pass_btn.setToolTip("Mostra password")

    def get_data(self) -> tuple[str, str]:
        return self.username_edit.text(), self.password_edit.text()
